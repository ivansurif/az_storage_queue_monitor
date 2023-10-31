import os, uuid
from dotenv import load_dotenv


from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage
from azure.core.exceptions import ResourceNotFoundError

from queue_writer import QueueWriter


def handle(data, client, secrets):
    load_dotenv()  # take environment variables from .env.
    # Retrieve the connection string for use with the application. The storage
    # connection string is stored in an environment variable on the machine
    # running the application called AZURE_STORAGE_CONNECTION_STRING.
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    queue_name = data['queue_name']
    # Instantiate a QueueClient which will be used to create and manipulate the queue
    queue_client = QueueClient.from_connection_string(connect_str, queue_name)
    writer = QueueWriter(connect_str, queue_name)
    queue_query_result = writer.check_if_queue_exists()
    if queue_query_result[0]:
        print(f'Queue "{queue_name}" exists')
        # ADD PROCESSING LOGIC HERE
    elif queue_query_result[1] == 'QueueNotFound':
        print(f'Provided Queue name "{queue_name}" doesn\'t exist')
        return
    elif queue_query_result[1] == 'ResourceNotFoundError':
        print(f'Resource Not Found error with error code != "QueueNotFound"')
        return
    else:
        print(f'ABORTING: error when reading from queue. Generic Exception!')
        print(queue_query_result[1].status_code)
        print(queue_query_result[1].error_code)
        print(queue_query_result[1].reason)
        return
