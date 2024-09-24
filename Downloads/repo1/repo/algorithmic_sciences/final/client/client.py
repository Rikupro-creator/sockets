import socket
import ssl
import sys

# Configuration
ssl_enabled = False
server_ip = 'localhost'
server_port = 6281
BUFFER_SIZE = 1024


def create_socket():
    """
    Create a client socket and wrap it with SSL/TLS if enabled.

    Returns:
        socket: A socket object, wrapped with SSL/TLS if
        ssl_enabled is True.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if ssl_enabled:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('server.crt')
        client_socket = context.wrap_socket(
            client_socket, server_hostname=server_ip)
        print('Connected with SSL/TLS.')
    else:
        print('Connected without SSL/TLS.')

    return client_socket


def main():
    """
    Main function to create a socket, connect to the server,
    send a search string,and print the server's response.
    """
    client_socket = create_socket()
    print('Connection created')
    try:
        client_socket.connect((server_ip, server_port))

        # Prompt the user for a search string
        search_string = input('What do you want to search? ')

        # Send the search string to the server
        client_socket.sendall(search_string.encode())

        # Receive and print the response from the server
        response = client_socket.recv(BUFFER_SIZE).decode()
        print("Server response:\n", response)

    except (socket.error, ssl.SSLError) as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
