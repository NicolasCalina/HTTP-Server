# HTTP Server Implementation

This is a simple HTTP server implemented on top of the TCP protocol. Currently, it supports only the `GET` request, with additional request types planned for future implementation.

## Features
- Built on top of the TCP protocol
- Handles basic `GET` requests
- Serves static files from the server's directory
- Returns appropriate status codes (`200 OK`, `404 Not Found`, `501 Not Implemented`)

## Prerequisites
Ensure you have Python installed on your system. This implementation is compatible with Python 3.

## How to Run the Server

1. Clone this repository or copy the script to your local machine.
2. Open a terminal and navigate to the directory where the script is located.
3. Run the server using the following command:
   
   ```bash
   python server.py
   ```

By default, the server runs on `127.0.0.1:6969`.



