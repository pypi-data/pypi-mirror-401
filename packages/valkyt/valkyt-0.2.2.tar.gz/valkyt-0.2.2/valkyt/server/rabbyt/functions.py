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
