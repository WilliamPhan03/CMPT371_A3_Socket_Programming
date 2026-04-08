"""
CMPT 371 A3: File-Transfer System
Architecture: TCP Sockets with Single-Threaded Blocking Session Management
Reference: ChatGPT used to help generate print statements (status/errors)
"""

import socket
import os
from tqdm import tqdm

HOST = '127.0.0.1' 
PORT = 65000 # use 65000 to avoid potential port collision  
HEADER_SIZE = 64 # must be the same as client

if not os.path.exists("server_data"):
    os.makedirs("server_data")

def receive_file(client_connection):
    # first 64 bytes is the filename
    header = client_connection.recv(HEADER_SIZE)
    
    if not header:
        print("Error: No header received.")
        return
    
    # ChatGPT used for syntax for this line
    header_string = header.rstrip(b'\0').decode('utf-8')

    filename, file_size_str = header_string.split('|')

    # convert to int for progress bar
    file_size = int(file_size_str)
    
    file_path = os.path.join("server_data", filename)
    
    # receive file
    # 'wb' -> write binary
    with open(file_path, 'wb') as file:
        # ChatGPT used for this line -> formatting the progress bar
        progress = tqdm(total = file_size, unit = 'B', unit_scale = True, unit_divisor = 1024, desc = f"Receiving {filename}")
        
        # receive the file in small chunks -> 1024 bytes at a time
        while True:
            data = client_connection.recv(1024)
            
            # if data' is empty -> client has finished sending file
            if not data:
                break
            
            # write chunk into our file
            file.write(data)
            progress.update(len(data))

        progress.close()
                
    print(f"Transfer complete! File saved to: {file_path}")
    return True


def start_server():
    # create socket -> AF_INET for IPv4, SOCK_STREAM for TCP -> must match the client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        
        # bind socket
        server_socket.bind((HOST, PORT))
        
        # listen for client connections
        server_socket.listen()

        # prevents accept blocking for shutdown 
        server_socket.settimeout(1.0)

        print(f"Server started successfully. Listening on {HOST}:{PORT}...")
        print("Waiting for a client to connect...")

        # while loop -> allow multiple files to be sent over one connection -> manual shutdown
        while True:
            try:
                client_connection, client_address = server_socket.accept()

                # ensures the connection is closed after finishing
                with client_connection:
                    print(f"Success! Client connected from: {client_address}")
                    
                    receive_file(client_connection)
            
            # allows keyboard interrupt (cross-compatible)
            except socket.timeout:
                continue

if __name__ == "__main__":
    try:
        start_server()
    # ChatGPT used for syntax for for this line
    except KeyboardInterrupt:
        print("\nServer shut down.")