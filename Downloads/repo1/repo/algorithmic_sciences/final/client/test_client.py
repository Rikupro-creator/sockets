import pytest
from unittest.mock import patch, MagicMock
import socket
import ssl
import client  # Change 'your_script' to the actual script name


# Test the create_socket function with SSL enabled
@patch('ssl.SSLContext.load_verify_locations')
@patch('ssl.SSLContext.wrap_socket')
@patch('socket.socket')
def test_create_socket_with_ssl(mock_socket,
                                mock_wrap_socket, mock_load_verify_locations):
    # Ensure ssl_enabled is True
    with patch('client.ssl_enabled', True):  # Change 'your_script' to 'client'
        mock_client_socket = MagicMock()
        mock_socket.return_value = mock_client_socket

        # Call the function
        result_socket = client.create_socket()

        # Ensure SSL/TLS context and socket wrapping are done
        mock_wrap_socket.assert_called_once_with(
            mock_client_socket, server_hostname=client.server_ip)
        mock_load_verify_locations.assert_called_once_with('server.crt')
        assert result_socket == mock_wrap_socket.return_value


# Test the create_socket function without SSL
@patch('socket.socket')
def test_create_socket_without_ssl(mock_socket):
    # Ensure ssl_enabled is False
    with patch('client.ssl_enabled', False):
        mock_client_socket = MagicMock()
        mock_socket.return_value = mock_client_socket

        # Call the function
        result_socket = client.create_socket()

        # SSL wrapping should not occur, just return the raw socket
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        assert result_socket == mock_client_socket


# Test main function with mocked socket connection and interaction
@patch('builtins.input', return_value='test_search')
@patch('client.create_socket')  # Correct module reference here
def test_main(mock_create_socket, mock_input):
    # Mock client socket
    mock_client_socket = MagicMock()
    mock_create_socket.return_value = mock_client_socket

    # Call main function
    client.main()  # Use the correct module reference

    # Verify the socket connection, send, receive, and close
    mock_client_socket.connect.assert_called_once_with(
        (client.server_ip, client.server_port))
    mock_client_socket.sendall.assert_called_once_with(b'test_search')
    mock_client_socket.recv.assert_called_once()
    mock_client_socket.close.assert_called_once()


# Test main with socket error (simulating connection failure)
@patch('builtins.input', return_value='test_search')
@patch('client.create_socket')  # Correct module reference here
def test_main_socket_error(mock_create_socket, mock_input):
    # Mock client socket and simulate connection failure
    mock_client_socket = MagicMock()
    mock_client_socket.connect.side_effect = socket.error('Connection failed')
    mock_create_socket.return_value = mock_client_socket

    # Call main function
    client.main()  # Use the correct module reference

    # Verify the connection failed and close was called
    mock_client_socket.connect.assert_called_once_with(
        (client.server_ip, client.server_port))
    mock_client_socket.close.assert_called_once()


# Test main with SSL error (simulating SSL handshake failure)
@patch('builtins.input', return_value='test_search')
@patch('client.create_socket')  # Correct module reference here
def test_main_ssl_error(mock_create_socket, mock_input):
    # Mock client socket and simulate SSL error
    mock_client_socket = MagicMock()
    mock_client_socket.connect.side_effect = ssl.SSLError('SSL Error occurred')
    mock_create_socket.return_value = mock_client_socket

    # Call main function
    client.main()  # Use the correct module reference

    # Verify SSL error was caught and close was called
    mock_client_socket.connect.assert_called_once_with(
        (client.server_ip, client.server_port))
    mock_client_socket.close.assert_called_once()
