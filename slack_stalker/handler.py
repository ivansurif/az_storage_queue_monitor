import os, uuid
from dotenv import load_dotenv


from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage
from azure.core.exceptions import ResourceNotFoundError

from queue_writer import QueueWriter


def handle(data, client, secrets):
    load_dotenv()  # take environment variables from .env.
    try:
        # Retrieve the connection string for use with the application. The storage
        # connection string is stored in an environment variable on the machine
        # running the application called AZURE_STORAGE_CONNECTION_STRING.
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        queue_name = data['queue_name']
        # Instantiate a QueueClient which will be used to create and manipulate the queue
        queue_client = QueueClient.from_connection_string(connect_str, queue_name)
        writer = QueueWriter(connect_str, queue_name)
        if writer.ensure_queue_exists():
            print(f'Queue "{queue_name}" exists')
        else:
            print(f'ABORTING: Provided Queue name "{queue_name}" doesn\'t exist or error when reading from queue')
        
    except:
        pass
