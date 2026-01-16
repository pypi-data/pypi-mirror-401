import pika
import json
from loguru import logger

class RabbitMQConnection:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: str,
        virtual_host: str,
        queue: str,
        routing_key: str,
        exchange: str
    ):
        self.queue = queue
        self.routing_key = routing_key
        self.exchange = exchange

        self.credential = pika.PlainCredentials(
            username=username,
            password=password
        )

        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=self.credential,
            heartbeat=30,
            blocked_connection_timeout=300
        )

        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def connect(self):
        if (
            not hasattr(self, "connection")
            or self.connection is None
            or self.connection.is_closed
        ):
            logger.warning("Reconnecting RabbitMQ...")
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()

    def close(self):
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except Exception:
            pass
