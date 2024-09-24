import os
import socket
import sys
import threading
import ssl
import time
from file_reading import normal_open, mmap_open
import string_search
from configparser import ConfigParser

# Configuration
config = ConfigParser()
config.read('config.ini')

ssl_enabled = config.getboolean('DEFAULT', 'SSL')
REREAD_ON_QUERY = config.getboolean('DEFAULT', 'REREAD_ON_QUERY')
port = int(config.get('DEFAULT', 'port'))
linuxpath = config.get('DEFAULT', 'linuxpath')


# Define the buffer size for receiving data
BUFFER_SIZE = int(config.get('DEFAULT', 'BUFFER_SIZE'))
# Minimum allowable length for search strings
min_allowable_search = int(config.get('DEFAULT',
                           'min_allowable_search'))

# open file
file_content = normal_open(linuxpath)
file_content = sorted([i.strip() for i in file_content])


def receive_data(conn):
    """Receive and decode data from the client connection."""
    try:
        data = conn.recv(BUFFER_SIZE).decode('utf-8').strip()
        if not data:  # Stop if there is no more data
            return None
        return data
    except ConnectionError:
        print("Connection error occurred while receiving data.")
        return None
    except UnicodeDecodeError:
        print("Decoding error: Received data cannot be decoded as UTF-8.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def handle_client(conn, addr, search_string):
    """Process a client's search request and send back the result."""

    search_term = b'\n' + search_string.encode('utf-8') + b'\n'
    try:
        if REREAD_ON_QUERY:
            # search_string=search_string.encode('utf-8')
            # This method searches in bytes
            start_time = time.time()
            file = mmap_open(linuxpath)
            result = string_search.search_chunk_with_find(file, search_term)
            response = "STRING EXISTS\n" if result != -1\
                else "STRING NOT FOUND\n"

            # response = parallel_search_reread_true(linuxpath, search_string)
            end_time = time.time()
        else:
            start_time = time.time()
            response = string_search.bisect_search(search_string, file_content)
            end_time = time.time()
        execution_time = (end_time - start_time) * 1000

    except Exception as e:
        response = f'There was an error! {e}'
        execution_time = 0  # Set to zero in case of error

    # Log the query and performance
    log_message = (
        f"DEBUG: [{time.strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Query: '{search_string}', Client: {addr}, "
        f"Execution time: {execution_time} ms\n"
        )

    # Send the response and log back to the client
    conn.sendall((response + log_message).encode())
    conn.close()


def small_length_string(conn, addr, search_string):
    """Handle search requests with strings that are too short."""
    if len(search_string) < min_allowable_search:
        start_time = time.time()
        response = "STRING NOT FOUND\n"
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        log_message = (
            f"DEBUG: [{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Query: '{search_string}', Client: {addr}, "
            f"Execution time: {execution_time} ms\n"
            )
        # Send the response and log back to the client
        conn.sendall((response + log_message).encode())
        conn.close()


def creating_socket():
    """Create a server socket with optional SSL support."""
    try:
        ip = socket.gethostbyname('localhost')
    except socket.gaierror as err:
        print(f"There was a problem resolving the host: {err}")
        sys.exit(1)  # Exit with a non-zero status to indicate failure

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if ssl_enabled:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=config.get('DEFAULT', 'cert'),
                                    keyfile=config.get('DEFAULT', 'key'))
            server_socket = context.wrap_socket(server_socket,
                                                server_side=True)
            print('Server is listening with SSL on...')
        else:
            print('Server is connected without SSL!')

        return server_socket, ip

    except (ssl.SSLError, socket.error) as e:
        print(f"Failed to create server socket: {e}")
        sys.exit(1)  # Exit with a non-zero status to indicate failure


def main():
    """Start the server and handle incoming client connections."""
    server_socket, ip = creating_socket()
    server_socket.bind((ip, port))
    server_socket.listen()

    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr} has been established.")

            search_string = receive_data(conn)
            if not search_string:
                continue

            if len(search_string) < min_allowable_search:
                small_length_string(conn, addr, search_string)
            else:
                # Start a new thread to handle the client connection
                client_thread = threading.Thread(
                    target=handle_client, args=(conn, addr, search_string))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
