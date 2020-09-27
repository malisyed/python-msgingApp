import threading
import socket

host = "127.0.0.1"
port = 11000 #Should be greater than 10000 to avoid connecting to reserved port 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []
#check if name already exists

def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			name = names[index]
			broadcast(f"{name} left the chat".encode('ascii'))
			names.remove(name)
			break


def receieve():
	while True:
		client, address = server.accept()
		
		client.send("NAME".encode('ascii'))
		name = client.recv(1024).decode('ascii')
		names.append(name)
		clients.append(client)
		
		print(f"New connection: {str(address)} with Name: {name}")
		client.send("Connection established, you have joined the chat!".encode('ascii'))
		broadcast(f"{name} joined the chatroom!".encode('ascii'))
		
		
		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

print("Server started")
receieve()