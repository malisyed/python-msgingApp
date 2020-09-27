import socket
import threading

name = input("Enter a name for the chatroom: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 11000))

def receive():
	while True:
		try:
			message = client.recv(1024).decode('ascii')
			if message == "NAME":
				client.send(name.encode('ascii'))
			else:
				print(message)
		except:
			print("Error occurred,disconnecting from server")
			client.close()
			break

def send():
	while True:
		message = f'{name}: {input("")}'
		client.send(message.encode('ascii'))
		

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()