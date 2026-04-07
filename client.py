"""
CMPT 371 A3: File-Transfer System
Architecture: Fixed-Length Header Protocol over TCP via CLI
Reference: ChatGPT used to help generate print statements (status/errors)
"""

import socket
import os
import sys
from tqdm import tqdm

HOST = '127.0.0.1' 
PORT = 65000 # use 65000 to avoid potential port collision  
HEADER_SIZE = 64 # must be the same as server

def send_file(client_socket, file_path, file_name):
        # get file name (removes the folder path)
        actual_filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        header_string = f"{actual_filename}|{file_size}"
           
        # convert into into bytes
        header_bytes = header_string.encode('utf-8')
        
        # pad bytes with null characters -> exactly 64 bytes
        # ChatGPT used for syntax for this line
        padded_header = header_bytes.ljust(HEADER_SIZE, b'\0')

        # send 64byte header first
        client_socket.sendall(padded_header)

        # send file
        # 'rb' -> read binary mode
        with open(file_path, 'rb') as file:
            # ChatGPT used for this line -> formatting the progress bar
            progress = tqdm(total = file_size, unit = 'B', unit_scale = True, unit_divisor = 1024, desc = f"Sending {actual_filename}")

            # send the file in chunks -> 1024 bytes at a time
            while True:
                data = file.read(1024)
                
                # if data' is empty -> end of the file
                if not data:
                    break
                
                # ensures every byte in chunk is sent
                client_socket.sendall(data)
                
                progress.update(len(data))

            progress.close()
        print(f"Transfer complete!")

def start_client():
    # if no file name argument
    if len(sys.argv) < 2:
        print("Error: You must provide a filename to send.")
        print("Usage: python client.py <filename>")
        print("Example: python client.py test_file.txt")
        return
        
    # take user input for file name
    file_name = sys.argv[1]
    file_path = os.path.join("client_data", file_name)

    # make sure the file actually exists before trying to send it
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        print("Please create the file and folder first before running the client.")
        return

    # create socket -> AF_INET for IPv4, SOCK_STREAM for TCP -> must match the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"Connecting to server at {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print("Connected successfully!")

        send_file(client_socket, file_path, file_name)

if __name__ == "__main__":
    start_client()