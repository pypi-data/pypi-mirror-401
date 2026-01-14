import asyncio
import json
import logging
import time
from queue import Queue, Empty
from threading import Thread, Event, Lock
from typing import Dict, Optional
import pkg_resources

import paho.mqtt.client as mqtt

from .mqtt_trigger_service import MQTTTriggerService
from ..models.alert import Alert
from ..models.device import ModbusClient, ModbusConnection
from ..models.measurement import Measurement, ModBusMeasurement


class MQTTService:
    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str,
            topics: Dict[str, Dict[str, str]],
            modbus_clients: Optional[Dict[str, ModbusClient]] = None,
            modbus_connections: Optional[Dict[str, ModbusConnection]] = None,
            keepalive: int = 60,
            reconnect_min_delay: int = 1,
            reconnect_max_delay: int = 120
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.topics = topics
        self.keepalive = keepalive
        self.reconnect_min_delay = reconnect_min_delay
        self.reconnect_max_delay = reconnect_max_delay

        # Connection state tracking
        self.is_connected_flag = False
        self.connection_lock = Lock()
        self.reconnect_count = 0
        self.last_disconnect_time = None
        self.manual_disconnect = False

        # Message handling
        self.message_queue = Queue()
        self.stop_event = Event()
        self.loop = None  # Store reference to event loop
        self.health_check_task = None

        # Initialize MQTT client with unique client ID
        import socket
        client_id = f"rtu_{socket.gethostname()}_{username}"
        self.client = mqtt.Client(client_id=client_id, clean_session=False)

        # Only enable TLS if using secure port (8883)
        if self.port == 8883:
            try:
                # Load CA certificate from package resources
                cert_path = pkg_resources.resource_filename('dataskipper_boat', 'emqxsl-ca.crt')
                self.client.tls_set(ca_certs=cert_path)
                logging.info("TLS enabled for MQTT (port 8883)")
            except Exception as e:
                logging.warning(f"Failed to set TLS certificate: {e}")
                logging.info("Proceeding without TLS certificate validation")
        else:
            logging.info(f"Using plain MQTT (port {self.port}, no TLS)")

        self.client.username_pw_set(username, password)

        # Set up trigger service if Modbus clients are provided
        self.trigger_service = None
        if modbus_clients and modbus_connections:
            self.trigger_service = MQTTTriggerService(
                modbus_clients=modbus_clients,
                modbus_connections=modbus_connections
            )

        # Set up MQTT callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self.on_message

        # Configure automatic reconnection
        self.client.reconnect_delay_set(min_delay=reconnect_min_delay, max_delay=reconnect_max_delay)

        # Initial connection attempt
        self._connect()

    def _connect(self):
        """Initial connection attempt with error handling."""
        try:
            logging.info(f"Attempting to connect to MQTT broker at {self.host}:{self.port}...")
            self.client.connect(self.host, self.port, keepalive=self.keepalive)
            self.client.loop_start()
            logging.info("MQTT loop started")
        except Exception as e:
            logging.error(f'Failed to connect with MQTT server: {e}')
            logging.info("Will retry connection automatically...")

    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connection is established"""
        with self.connection_lock:
            if rc == 0:
                self.is_connected_flag = True
                self.reconnect_count = 0
                logging.info(f"✓ Successfully connected to MQTT broker (rc={rc})")

                # Resubscribe to all topics on reconnection
                if self.trigger_service:
                    self.subscribe_to_trigger_topics()

                # Log reconnection success if this was a reconnect
                if self.last_disconnect_time:
                    downtime = time.time() - self.last_disconnect_time
                    logging.info(f"Connection restored after {downtime:.1f} seconds of downtime")
                    self.last_disconnect_time = None
            else:
                self.is_connected_flag = False
                error_messages = {
                    1: "Connection refused - incorrect protocol version",
                    2: "Connection refused - invalid client identifier",
                    3: "Connection refused - server unavailable",
                    4: "Connection refused - bad username or password",
                    5: "Connection refused - not authorized"
                }
                error_msg = error_messages.get(rc, f"Unknown error code: {rc}")
                logging.error(f"✗ Failed to connect to MQTT broker: {error_msg}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback when connection is lost"""
        with self.connection_lock:
            self.is_connected_flag = False

            # Don't log/reconnect if this was a manual disconnect
            if self.manual_disconnect:
                logging.info("Disconnected from MQTT broker (manual)")
                return

            self.last_disconnect_time = time.time()
            self.reconnect_count += 1

            if rc == 0:
                logging.warning("⚠ Disconnected from MQTT broker gracefully")
            else:
                logging.error(f"✗ Unexpectedly disconnected from MQTT broker (rc={rc})")

            logging.info(f"Automatic reconnection attempt #{self.reconnect_count} will begin shortly...")

            # The paho client will automatically attempt to reconnect
            # due to loop_start() and reconnect_delay_set() configuration

    def on_message(self, client, userdata, message):
        """Synchronous callback that queues messages for processing"""
        if not self.trigger_service:
            return
            
        try:
            logging.debug(f"Received MQTT message on topic: {message.topic}")
            self.message_queue.put((message.topic, message.payload))
            logging.debug("Successfully queued message for processing")
        except Exception as e:
            logging.error(f"Error queueing MQTT message: {e}")

    async def start_processing(self, loop):
        """Start message processing - called from main async context"""
        self.loop = loop
        self.stop_event.clear()

        # Start message processing in a separate thread
        self.process_thread = Thread(target=self._process_messages)
        self.process_thread.daemon = True
        self.process_thread.start()
        logging.info("Message processing thread started")

        # Start health monitoring task
        self.health_check_task = asyncio.create_task(self._health_monitor())
        logging.info("MQTT health monitoring started")

    async def _health_monitor(self):
        """Periodically check connection health and attempt recovery if needed."""
        check_interval = 30  # Check every 30 seconds

        while not self.stop_event.is_set():
            try:
                await asyncio.sleep(check_interval)

                # Check if we're supposed to be connected but aren't
                with self.connection_lock:
                    is_connected = self.is_connected_flag

                if not is_connected and not self.manual_disconnect:
                    logging.warning("Health check: MQTT connection lost, attempting recovery...")
                    try:
                        # Try to reconnect manually if automatic reconnection isn't working
                        if not self.client.is_connected():
                            self.client.reconnect()
                            logging.info("Manual reconnection attempt initiated")
                    except Exception as e:
                        logging.error(f"Health check reconnection failed: {e}")
                else:
                    # Connection is healthy
                    logging.debug("Health check: MQTT connection is healthy")

            except asyncio.CancelledError:
                logging.info("Health monitor task cancelled")
                break
            except Exception as e:
                logging.error(f"Error in MQTT health monitor: {e}")
                # Don't break, keep monitoring

    def _process_messages(self):
        """Process messages in a separate thread"""
        while not self.stop_event.is_set():
            try:
                # Get message with timeout to allow checking stop_event
                try:
                    topic, payload = self.message_queue.get(timeout=0.1)
                except Empty:
                    continue

                logging.debug(f"Processing message from topic: {topic}")
                
                # Create future for async processing
                future = asyncio.run_coroutine_threadsafe(
                    self.trigger_service.handle_mqtt_message(
                        topic=topic,
                        message=payload.decode()
                    ),
                    self.loop
                )

                try:
                    # Wait for result with timeout
                    result = future.result(timeout=10)
                    
                    if result:
                        logging.debug(f"Message processing result: {result}")
                        # Send response if configured
                        if (
                            result.get("success") 
                            and "write_results" in result 
                            and all(result["write_results"].values())
                        ):
                            actions = result.get("on_true_actions")
                        else:
                            actions = result.get("on_false_actions")
                            
                        if actions:
                            # Handle both dictionary and ActionSet object cases
                            if isinstance(actions, dict):
                                response_topic = actions.get("response_topic")
                                response_message = actions.get("response_message")
                            else:
                                response_topic = actions.response_topic
                                response_message = actions.response_message
                            
                            if response_topic and response_message:
                                response = {
                                    "success": result.get("success", False),
                                    "message": response_message,
                                    "details": {
                                        "condition_values": result.get("condition_values", {}),
                                        "write_results": result.get("write_results", {})
                                    }
                                }
                                self.client.publish(
                                    response_topic,
                                    json.dumps(response)
                                )
                                logging.debug(f"Published response to: {response_topic}")
                            
                except Exception as e:
                    logging.error(f"Error processing MQTT message: {e}", exc_info=True)
                finally:
                    self.message_queue.task_done()
                    
            except Exception as e:
                logging.error(f"Error in message processing thread: {e}", exc_info=True)
                # Brief sleep on error to prevent tight loop
                self.stop_event.wait(1.0)

    def subscribe_to_trigger_topics(self):
        """Subscribe to all topics configured in triggers."""
        if not self.trigger_service:
            return
            
        topics = set()
        for client in self.trigger_service.modbus_clients.values():
            if not client.mqtt_triggers:
                continue
            for trigger in client.mqtt_triggers:
                if isinstance(trigger, dict):
                    topics.add(trigger.get('topic'))
                else:
                    topics.add(trigger.topic)
        
        for topic in topics:
            if topic:  # Only subscribe if topic is not None
                try:
                    self.client.subscribe(topic)
                    logging.info(f"Subscribed to trigger topic: {topic}")
                except Exception as e:
                    logging.error(f"Failed to subscribe to topic {topic}: {e}")

    def publish_measurement(self, measurement: [Measurement | ModBusMeasurement], topic: str) -> bool:
        """Publish measurement with connection check and retry logic."""
        if not topic:
            topic = self.topics[measurement.device_type]["measurements"]

        # Check connection status
        with self.connection_lock:
            if not self.is_connected_flag:
                logging.warning(f"Cannot publish measurement: MQTT not connected (reconnection in progress)")
                return False

        try:
            result = self.client.publish(
                topic,
                json.dumps(measurement.to_dict()),
                qos=1  # At least once delivery
            )

            # Check if publish was successful
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.debug(f"Successfully published measurement to {topic}")
                return True
            elif result.rc == mqtt.MQTT_ERR_NO_CONN:
                logging.error("Failed to publish measurement: No connection")
                # Trigger reconnection attempt
                self._attempt_reconnect()
                return False
            else:
                logging.error(f"Failed to publish measurement: Error code {result.rc}")
                return False

        except Exception as e:
            logging.error(f'Failed to publish measurement to MQTT server: {e}')
            return False

    def publish_alert(self, alert: Alert) -> bool:
        """Publish alert with connection check and retry logic."""
        topic = self.topics[alert.device_type]["alerts"]

        # Check connection status
        with self.connection_lock:
            if not self.is_connected_flag:
                logging.warning(f"Cannot publish alert: MQTT not connected (reconnection in progress)")
                return False

        try:
            result = self.client.publish(
                topic,
                json.dumps(alert.to_dict()),
                qos=1  # At least once delivery
            )

            # Check if publish was successful
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logging.debug(f"Successfully published alert to {topic}")
                return True
            elif result.rc == mqtt.MQTT_ERR_NO_CONN:
                logging.error("Failed to publish alert: No connection")
                # Trigger reconnection attempt
                self._attempt_reconnect()
                return False
            else:
                logging.error(f"Failed to publish alert: Error code {result.rc}")
                return False

        except Exception as e:
            logging.error(f'Failed to publish alert to MQTT server: {e}')
            return False

    def _attempt_reconnect(self):
        """Attempt to manually trigger reconnection if not already in progress."""
        try:
            if not self.client.is_connected() and not self.manual_disconnect:
                logging.info("Triggering manual reconnection attempt...")
                self.client.reconnect()
        except Exception as e:
            logging.error(f"Manual reconnection attempt failed: {e}")

    def disconnect(self):
        """Disconnect from MQTT broker and cleanup."""
        logging.info("Shutting down MQTT service...")

        # Set manual disconnect flag to prevent reconnection attempts
        with self.connection_lock:
            self.manual_disconnect = True

        # Stop event processing
        self.stop_event.set()

        # Cancel health monitoring task if it exists
        if self.health_check_task and not self.health_check_task.done():
            self.health_check_task.cancel()
            logging.info("Health monitoring task cancelled")

        # Wait for message processing thread to finish
        if hasattr(self, 'process_thread') and self.process_thread.is_alive():
            self.process_thread.join(timeout=5.0)
            if self.process_thread.is_alive():
                logging.warning("Message processing thread did not stop gracefully")

        # Disconnect MQTT client
        if self.client:
            try:
                self.client.loop_stop()
                self.client.disconnect()
                logging.info("MQTT client disconnected successfully")
            except Exception as e:
                logging.error(f"Error disconnecting MQTT client: {e}")

    def is_connected(self) -> bool:
        """Check if MQTT is currently connected."""
        with self.connection_lock:
            return self.is_connected_flag

    def get_connection_stats(self) -> dict:
        """Get connection statistics for monitoring."""
        with self.connection_lock:
            return {
                "connected": self.is_connected_flag,
                "reconnect_count": self.reconnect_count,
                "last_disconnect_time": self.last_disconnect_time,
                "manual_disconnect": self.manual_disconnect
            }