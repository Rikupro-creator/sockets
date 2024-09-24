import pytest
import socket
import ssl
from unittest.mock import patch, MagicMock
import server
import string_search
from server import (
    receive_data, handle_client, small_length_string,
    creating_socket, REREAD_ON_QUERY, min_allowable_search)


# Fixture to create a mock socket object
@pytest.fixture
def mock_socket():
    return MagicMock(spec=socket.socket)


# Fixture to create a mock SSL context object
@pytest.fixture
def mock_ssl_context():
    return MagicMock(spec=ssl.SSLContext)


# Test case for successful data reception from the client
def test_receive_data_success(mock_socket):
    mock_socket.recv.return_value = b'test data'
    assert receive_data(mock_socket) == 'test data'


# Test case when the received data is empty
def test_receive_data_empty(mock_socket):
    mock_socket.recv.return_value = b''
    assert receive_data(mock_socket) is None


# Test case for handling a connection error during data reception
def test_receive_data_connection_error(mock_socket):
    mock_socket.recv.side_effect = ConnectionError()
    assert receive_data(mock_socket) is None


# Test case for handling a Unicode decoding error during data reception
def test_receive_data_unicode_error(mock_socket):
    mock_socket.recv.return_value = b'\xff\xfe'  # Invalid UTF-8
    assert receive_data(mock_socket) is None


# Parametrized test case for handling client requests
@pytest.mark.parametrize("reread_on_query", [True, False])
def test_handle_client(mock_socket, reread_on_query):
    # Patch REREAD_ON_QUERY to test both true and false scenarios
    with patch('server.REREAD_ON_QUERY', reread_on_query):
        # Patch the search functions based on REREAD_ON_QUERY value
        with patch('server.mmap_open', return_value=b"file_content"):
            with patch('string_search.search_chunk_with_find',
                       return_value=-1) as mock_search_true:
                with patch('string_search.bisect_search',
                           return_value="STRING NOT FOUND\n")\
                            as mock_search_false:

                    # Call handle_client with mock data
                    handle_client(mock_socket, ('127.0.0.1', 12345),
                                  'test_string')

                    # Assert the correct search function was called
                    if reread_on_query:
                        mock_search_true.assert_called_once()
                    else:
                        mock_search_false.assert_called_once()

                    # Assert that sendall and close methods were called once
                    mock_socket.sendall.assert_called_once()
                    mock_socket.close.assert_called_once()


# Test case for handling strings shorter than the minimum allowable length
def test_small_length_string(mock_socket):
    small_length_string(mock_socket, ('127.0.0.1', 12345), 'small')
    # Assert that sendall and close methods were called once
    mock_socket.sendall.assert_called_once()
    mock_socket.close.assert_called_once()
    # Assert that the response contains "STRING NOT FOUND\n"
    assert b"STRING NOT FOUND\n" in mock_socket.sendall.call_args[0][0]


# Test case for creating a socket without SSL
@patch('socket.gethostbyname')
def test_creating_socket_without_ssl(mock_gethostbyname, mock_socket):
    mock_gethostbyname.return_value = '127.0.0.1'
    # Patch ssl_enabled to False and the socket creation to return mock_socket
    with patch('server.ssl_enabled', False):
        with patch('socket.socket', return_value=mock_socket):
            server_socket, ip = creating_socket()
            # Assert that the correct IP address is returned
            assert ip == '127.0.0.1'
            # Assert that the returned socket is the mock_socket
            assert server_socket == mock_socket


# Test case for handling host resolution errors
def test_creating_socket_host_resolution_error():
    # Patch gethostbyname to raise a socket.gaierror
    with patch('socket.gethostbyname', side_effect=socket.gaierror):
        with pytest.raises(SystemExit):
            creating_socket()


# Test case for handling SSL errors during socket creation
def test_creating_socket_ssl_error():
    # Patch gethostbyname to return a valid IP address
    # And socket creation to raise ssl.SSLError
    with patch('socket.gethostbyname', return_value='127.0.0.1'):
        with patch('socket.socket', side_effect=ssl.SSLError):
            with pytest.raises(SystemExit):
                creating_socket()
