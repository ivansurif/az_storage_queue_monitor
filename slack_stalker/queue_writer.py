from azure.storage.queue import QueueClient, QueueServiceClient
from azure.core.exceptions import ResourceNotFoundError
import base64, json

class QueueWriter:
    def __init__(self, connection_string, queue_name):
        self.queue_client = QueueClient.from_connection_string(connection_string, queue_name)
        self.queue_name = queue_name
        # self.ensure_queue_exists()

    def check_if_queue_exists(self):
        try:
            res = self.queue_client.receive_messages(max_messages = 1)
            for message in res:
                decoded_string = base64.b64decode(message.content).decode('utf-8')
                # For better formatting, load as JSON and dump with indent
                decoded_json = json.loads(decoded_string)
                pretty_json = json.dumps(decoded_json, indent=4)
                print(pretty_json)

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
