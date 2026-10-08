import socket

HOST = "0.0.0.0"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(1)

print(f"Server listening on {HOST}:{PORT}")

while True:
	connection, address = server.accept()
	print(f"Connection from {address}")
	data = connection.recv(4096)
	print(f"Received: {data}")
	connection.close()
