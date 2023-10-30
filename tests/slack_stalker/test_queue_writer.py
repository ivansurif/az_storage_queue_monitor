import pytest
from unittest.mock import Mock, patch
from azure.core.exceptions import ResourceNotFoundError

from slack_stalker.queue_writer import QueueWriter


# Use the patch decorator to mock the QueueClient.from_connection_string
@patch("azure.storage.queue.QueueClient.from_connection_string")
@pytest.mark.unit
class TestCheckIfQueueExists:

    def test_check_if_queue_exists_queue_exists(self, mock_from_connection_string):
        # Mock the queue_client.receive_messages method to return a list with a message
        mock_client = Mock()
        mock_client.receive_messages.return_value = [Mock(content="test message")]
        mock_from_connection_string.return_value = mock_client

        writer = QueueWriter("dummy_connection_string", "dummy_queue")
        assert writer.check_if_queue_exists() == True


    def test_check_if_queue_exists_queue_not_found(self, mock_from_connection_string):
        # Mock the queue_client.receive_messages method to raise a ResourceNotFoundError with 'QueueNotFound' error code
        mock_client = Mock()
        mock_client.receive_messages.side_effect = ResourceNotFoundError("Queue not found")
        mock_client.receive_messages.side_effect.error_code = "QueueNotFound"
        mock_from_connection_string.return_value = mock_client

        writer = QueueWriter("dummy_connection_string", "dummy_queue")
        assert writer.check_if_queue_exists() == (False, 'QueueNotFound')


    def test_check_if_queue_exists_resource_not_found(self, mock_from_connection_string):
        # Mock the queue_client.receive_messages method to raise a ResourceNotFoundError with a different error code
        mock_client = Mock()
        mock_client.receive_messages.side_effect = ResourceNotFoundError("Resource not found")
        mock_client.receive_messages.side_effect.error_code = "ResourceNotFoundOther"
        mock_from_connection_string.return_value = mock_client

        writer = QueueWriter("dummy_connection_string", "dummy_queue")
        assert writer.check_if_queue_exists() == (False, 'ResourceNotFoundError')


    def test_check_if_queue_exists_general_exception(self, mock_from_connection_string):
        # Mock the queue_client.receive_messages method to raise a general exception
        mock_client = Mock()
        mock_client.receive_messages.side_effect = Exception("Some exception")
        mock_from_connection_string.return_value = mock_client

        writer = QueueWriter("dummy_connection_string", "dummy_queue")
        result = writer.check_if_queue_exists()
        assert result[0] == False
        assert isinstance(result[1], Exception)
