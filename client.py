import socket
import threading

HOST = '127.0.0.1'
PORT = 5000


def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(msg)
        except:
            print("Disconnected from server.")
            break


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

  
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

   
    while True:
        msg = input()
        client_socket.send(msg.encode())
        if msg.lower() == 'exit':  
            break

    client_socket.close()

if __name__ == "__main__":
    main()
