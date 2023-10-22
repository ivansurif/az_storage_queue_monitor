from azure.storage.queue import QueueClient, QueueServiceClient
from azure.core.exceptions import ResourceNotFoundError


class QueueWriter:
    def __init__(self, connection_string, queue_name):
        self.queue_client = QueueClient.from_connection_string(connection_string, queue_name)
        self.queue_name = queue_name
        # self.ensure_queue_exists()

    def ensure_queue_exists(self):
        print(self.queue_name)
        try:
            res = self.queue_client.receive_messages(max_messages = 1)
            for message in res:
                print(message.content)
            return True
        except ResourceNotFoundError as e:
            if e.error_code == 'QueueNotFound':
                print(f'The specified queue "{self.queue_name}" was not found.')
            else:
                print(f'Another resource-related error occurred: {e}')
            return False
        except Exception as e:
            print(f'UNCAUGHT EXCEPTION: {e.reason} \nERROR CODE: {e.error_code}')
            return False
    


        try:
            self.queue_client.create_queue()
        except ResourceExistsError:
            pass  # Queue already exists, so we can safely pass
        except Exception as e:
            print(f"An unexpected error occurred during queue creation: {e}")

    def write_message(self, message_content):
        try:
            message = self.queue_client.send_message(message_content)
            return message.id
        except Exception as e:
            print(f"An unexpected error occurred while sending message: {e}")
            return None
