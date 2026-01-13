import json
import logging
import ssl
import sys
import time
from queue import Queue
from threading import Thread

import pika

from .utils import RBMQ_aggregation_status, RBMQ_run_status


class Consumer:
    def __init__(self, config: dict, msg_queue: Queue, run_status_callback):
        self.msg_queue = msg_queue
        self.run_status_callback = run_status_callback
        rabbitmq_config = {
            "leaf_name": "",
            "leaf_id": "",
            "queue_password": "",
            "host": "rabbitmq.branchkey.com",
            "port": 5671,
            "ssl": True,
            "branch_id": "",
            "tree_id": "",
            "heartbeat_time_s": 30,
            "conn_retries": 3,
            "conn_retry_delay_s": 3,
            "max_reconnect_attempts": 10,
            "reconnect_backoff_factor": 2.0,
            "reconnect_max_delay": 60,
        }

        for key in config:
            rabbitmq_config[key] = config[key]

        self.queue_name = rabbitmq_config["leaf_id"]

        self.rabbitmq_config = rabbitmq_config

        # Reconnection settings
        self.max_reconnect_attempts = rabbitmq_config["max_reconnect_attempts"]
        self.reconnect_backoff_factor = rabbitmq_config["reconnect_backoff_factor"]
        self.reconnect_max_delay = rabbitmq_config["reconnect_max_delay"]
        self.current_reconnect_attempt = 0
        self._should_stop = False  # Flag to track intentional shutdowns

        self.conn = self.__get_connection_with_retry()
        self.channel = self.conn.channel()
        self.exchange = self.rabbitmq_config["branch_id"]

    def __get_connection(self):
        try:
            creds = pika.PlainCredentials(
                self.rabbitmq_config["leaf_id"], self.rabbitmq_config["queue_password"]
            )

            # Configure SSL if enabled
            ssl_options = None
            if self.rabbitmq_config.get("ssl", False):
                ssl_context = ssl.create_default_context()
                ssl_options = pika.SSLOptions(ssl_context)

            conn = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.rabbitmq_config["host"],
                    port=self.rabbitmq_config["port"],
                    virtual_host=self.rabbitmq_config["tree_id"],
                    credentials=creds,
                    ssl_options=ssl_options,
                    heartbeat=int(self.rabbitmq_config["heartbeat_time_s"]),
                    connection_attempts=int(self.rabbitmq_config["conn_retries"]),
                    retry_delay=int(self.rabbitmq_config["conn_retry_delay_s"]),
                    client_properties={
                        "connection_name": "leaf-" + self.rabbitmq_config["leaf_id"]
                    },
                )
            )

        except Exception as e:
            error_msg = f"[Consumer] Error while connecting to rabbitmq: {e}"
            logging.error(error_msg)
            raise Exception(error_msg)

        return conn

    def __get_connection_with_retry(self):
        """Get RabbitMQ connection with exponential backoff retry

        Attempts to establish a connection with exponential backoff between retries.
        Backoff delay is calculated as: min(backoff_factor ^ attempt, max_delay)

        Returns:
            pika.BlockingConnection: Established RabbitMQ connection

        Raises:
            Exception: If connection fails after max_reconnect_attempts
        """
        attempt = 0

        while attempt < self.max_reconnect_attempts:
            try:
                return self.__get_connection()
            except Exception as e:
                attempt += 1
                if attempt >= self.max_reconnect_attempts:
                    logging.error(
                        f"[Consumer] Failed to connect after {attempt} attempts: {e}"
                    )
                    raise

                # Calculate backoff delay with exponential increase
                delay = min(
                    self.reconnect_backoff_factor ** attempt,
                    self.reconnect_max_delay
                )

                logging.warning(
                    f"[Consumer] Connection attempt {attempt} failed. "
                    f"Retrying in {delay:.1f}s... Error: {e}"
                )
                time.sleep(delay)

    def _check_connection_health(self) -> bool:
        """Check if connection and channel are healthy

        Returns:
            bool: True if both connection and channel are open and healthy
        """
        try:
            return (
                self.conn is not None
                and self.conn.is_open
                and self.channel is not None
                and self.channel.is_open
            )
        except Exception:
            return False

    def _handle_reconnection(self):
        """Handle reconnection after connection loss

        Attempts to re-establish connection and channel with exponential backoff.
        Resets reconnection counter on success.
        """
        logging.info("[Consumer] Attempting to reconnect...")
        try:
            # Close existing connections if they exist
            try:
                if hasattr(self, 'channel') and self.channel:
                    self.channel.close()
            except Exception:
                pass

            try:
                if hasattr(self, 'conn') and self.conn:
                    self.conn.close()
            except Exception:
                pass

            # Re-establish connection and channel
            self.conn = self.__get_connection_with_retry()
            self.channel = self.conn.channel()
            logging.info("[Consumer] Reconnection successful")
            self.current_reconnect_attempt = 0

        except Exception as e:
            logging.error(f"[Consumer] Reconnection failed: {e}")
            raise

    def __callback(self, ch, method, properties, body):
        try:
            msg = body.decode()
            logging.debug("[Consumer] Message received: " + str(msg))
        except Exception("Error with msg from RabbitMQ") as e:
            logging.error(f"[Consumer] Failed with msg from RabbitMQ {str(msg)}")
            raise e
        try:
            msg = json.loads(msg)
        except Exception as e:
            logging.error(f"[Consumer] Failed decode message to JSON {str(e)}")
            raise e
        if "message_type" not in msg:
            raise Exception("message_type not in msg from RBMQ")
        logging.debug(f"[Consumer] Message type ready {type(msg['message_type'])}")

        if msg["message_type"] == RBMQ_aggregation_status:
            logging.debug(
                "[Consumer] Putting agg_id to Queue: "
                + str(msg["body"]["aggregation_id"])
            )
            if self.msg_queue.full():
                logging.debug(
                    "[Consumer] Removing old agg_id from Queue: "
                    + str(self.msg_queue.get(block=True))
                )
            self.msg_queue.put(msg["body"]["aggregation_id"], block=False)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        elif msg["message_type"] == RBMQ_run_status:
            logging.debug(
                "[Consumer] setting run_status: " + str(msg["body"]["run_status"])
            )
            self.run_status_callback(msg["body"]["run_status"])
            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            logging.error("Failed to match message type")

    def start(self):
        """Start consuming with automatic reconnection on failure

        Continuously attempts to consume messages from RabbitMQ.
        If connection is lost, automatically attempts to reconnect
        with exponential backoff.
        """
        while not self._should_stop:
            try:
                self.channel.basic_consume(
                    queue=self.queue_name, on_message_callback=self.__callback
                )
                logging.info("[Consumer] Starting rabbitmq consumer")
                self.current_reconnect_attempt = 0  # Reset on successful connection
                self.channel.start_consuming()

                # If start_consuming() returns normally (e.g., stop_consuming called), exit loop
                if self._should_stop:
                    break

            except pika.exceptions.AMQPConnectionError as e:
                if self._should_stop:
                    break
                logging.error(f"[Consumer] Connection lost: {e}")
                try:
                    self._handle_reconnection()
                except Exception as reconnect_error:
                    logging.error(f"[Consumer] Failed to reconnect: {reconnect_error}")
                    self.stop(reconnect_error)
                    break

            except Exception as e:
                logging.error(f"[Consumer] Unexpected error: {e}")
                self.stop(e)
                break

    def stop(self, err=None):
        """Stop the consumer and close connections"""
        self._should_stop = True  # Signal to stop the reconnection loop
        if err:
            logging.info("[Consumer] Stopping rabbitmq consumer due to error: " + str(err))
        else:
            logging.info("[Consumer] Stopping rabbitmq consumer")
        try:
            if hasattr(self, 'channel') and self.channel and self.channel.is_open:
                self.channel.close()
        except Exception as e:
            logging.debug(f"[Consumer] Error closing channel (expected during shutdown): {e}")
        try:
            if hasattr(self, 'conn') and self.conn and self.conn.is_open:
                self.conn.close()
        except Exception as e:
            logging.debug(f"[Consumer] Error closing connection (expected during shutdown): {e}")
        return

    def request_stop(self):
        """Request the consumer to stop from another thread (thread-safe)"""
        self._should_stop = True  # Signal to stop the reconnection loop
        try:
            if hasattr(self, 'conn') and self.conn and self.conn.is_open:
                # Use pika's thread-safe callback mechanism to stop consuming
                self.conn.add_callback_threadsafe(self._stop_consuming_callback)
        except Exception as e:
            logging.warning(f"[Consumer] Error requesting stop: {e}")

    def _stop_consuming_callback(self):
        """Internal callback to stop consuming (runs in consumer thread)"""
        try:
            if hasattr(self, 'channel') and self.channel and self.channel.is_open:
                self.channel.stop_consuming()
        except Exception as e:
            logging.debug(f"[Consumer] Error in stop callback: {e}")

    def spawn_consumer_thread(self):
        print("Starting Consumer")
        t = ConsumerThread(target=self.start, callback=self.stop, daemon=True)
        t.consumer = self  # Store Consumer reference for thread-safe shutdown
        t.start()
        return t


class ConsumerThread(Thread):
    def __init__(self, callback=None, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.callback = callback
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == "call":
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == "line":
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
