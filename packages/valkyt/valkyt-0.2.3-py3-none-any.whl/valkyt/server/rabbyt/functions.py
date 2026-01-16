import json
import pika

from loguru import logger
from .connection import RabbitMQConnection

class Rabbyt(RabbitMQConnection):

    def send(self, data: dict):
        body = json.dumps(data)

        try:
            self.connect()
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=body
            )
            logger.success(f"Message sent to RabbitMQ [ {data} ]")

        except Exception as err:
            logger.error(f"RabbitMQ send failed: {err}")
            self.close()
            raise

    def send_v2(self, data: dict):
        """short-lived"""
        
        body = json.dumps(data)

        try:
            connection = pika.BlockingConnection(self.parameters)
            channel = connection.channel()

            channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=body
            )
            logger.success(f"Message sent to RabbitMQ [ {data} ]")

            connection.close()

        except Exception as err:
            logger.error(f"RabbitMQ send failed: {err}")
            raise
