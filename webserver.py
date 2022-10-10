# Samson DeVol webserver for cs372 project 2
# 9-26-2022

import os
import socket, sys

content_type_map = {'.txt': 'text/plain', '.html': 'text/html'}
# set up socket to listen on port, exit if port not specified
try: 
  port_number = int(sys.argv[1])
  s = socket.socket()
  s.bind(('', port_number))
  s.listen()
except: 
  print("need port number input like: $webserver.py PORT")
  sys.exit(1)

# outer loop for creating connections
while 1:
  new_conn = s.accept()
  print(new_conn)
  new_socket = new_conn[0]
  message = b''

  # inner loop for recieving
  while 1:
    message += new_socket.recv(4096)
    if b'\r\n\r\n' in message:
      break

  message = message.decode()

  # parse first line
  first = message.split("\r\n")[0]

  # parse request, path, protocol and filename from recieved 
  request_method, path_rec, protocol_rec= first.split(" ")

  # parse file name and content extenstion
  file_name_rec = os.path.split(path_rec)[-1] 
  content_extension = os.path.splitext(file_name_rec)[-1]

  # read from specified file name, 404 if not found
  try:
    with open(file_name_rec) as fp:
      data = fp.read()   # Read entire file
      data = data.encode("ISO-8859-1")
      content_length = len(data)
      new_socket.sendall("HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(content_type_map[content_extension], content_length, data.decode()).encode())
  except:
    new_socket.sendall("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found\r\n".encode())
  new_socket.close()

