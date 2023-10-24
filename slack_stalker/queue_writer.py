from azure.storage.queue import QueueClient, QueueServiceClient
from azure.core.exceptions import ResourceNotFoundError


class QueueWriter:
    def __init__(self, connection_string, queue_name):
        self.queue_client = QueueClient.from_connection_string(connection_string, queue_name)
        self.queue_name = queue_name
        # self.ensure_queue_exists()

    def check_if_queue_exists(self):
        try:
            res = self.queue_client.receive_messages(max_messages = 1)
            for message in res:
                print(message.content)
            return True
        except ResourceNotFoundError as e:
            if e.error_code == 'QueueNotFound':
                return False, 'QueueNotFound'
            else:
                return False, 'ResourceNotFoundError'
        except Exception as e:
            return False, e
    
    def create_queue(self):
        res = self.queue_client.create_queue()

    def write_message(self, message_content):
        try:
            message = self.queue_client.send_message(message_content)
            return message.id
        except Exception as e:
            print(f"An unexpected error occurred while sending message: {e}")
            return None
