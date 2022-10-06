# Samson DeVol webserver for cs372 project 2
# 9-26-2022

import os
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
  message = ""

  # inner loop for recieving
  while 1:
    message += new_socket.recv(4096).decode()
    if "\r\n\r\n" in message:
      break

  # parse first line
  first = message.split("\r\n")[0]

  # parse request, path, and filename from recieved 
  request_method = first.split(" ")[0]
  path_rec = first.split(" ")[1]
  file_name_rec = os.path.split(path_rec)[-1]

  # parse protocol and content extenstion 
  protocol_rec = first.split(" ")[2]
  content_extension = os.path.splitext(file_name_rec)[-1]

  # set content type for response
  # TODO: use a map
  if content_extension == '.txt':
    content_type = "text/plain"
  elif content_extension == '.html':
    content_type = "text/html"

  # read from specified file name, 404 if not found
  try:
    with open(file_name_rec) as fp:
      data = fp.read()   # Read entire file
      data = data.encode("ISO-8859-1")
      content_length = len(data)
      new_socket.sendall("HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}\r\n".format(content_type, content_length, data.decode()).encode())
  except:
    new_socket.sendall("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found\r\n".encode())
  new_socket.close()

