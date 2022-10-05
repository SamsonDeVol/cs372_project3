# Samson DeVol webserver for cs372 project 2
# 9-26-2022

import socket, sys

# parse inputs
port_number = int(sys.argv[1])

# ask OS for a socket
s = socket.socket()

# bind to port and listen
s.bind(('', port_number))
s.listen()

# outer loop for creating connections
while 1:
  new_conn = s.accept()
  print(new_conn)
  new_socket = new_conn[0]

  # inner loop for recieving
  while 1:
    if "\r\n\r\n" in new_socket.recv(4096).decode():
      break

  new_socket.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!\r\n".encode())
  new_socket.close()
