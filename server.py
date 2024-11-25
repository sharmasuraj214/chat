import socket
import threading

HOST = '127.0.0.1'  
PORT = 5000         


chat_rooms = {}


def handle_client(client_socket, client_address):
    client_socket.send("Welcome to the Chat Server!\nEnter a room name to join or create:".encode())
    room = client_socket.recv(1024).decode().strip()
    
    if room not in chat_rooms:
        chat_rooms[room] = []
    chat_rooms[room].append(client_socket)

    client_socket.send(f"Joined room: {room}. Start chatting!".encode())

    try:
        while True:
            msg = client_socket.recv(1024).decode()
            if msg.lower() == 'exit':  # Exit the room
                chat_rooms[room].remove(client_socket)
                client_socket.send("You have left the chat room.".encode())
                break

            
            for client in chat_rooms[room]:
                if client != client_socket:
                    client.send(f"[{room}] {client_address}: {msg}".encode())
    except:
        chat_rooms[room].remove(client_socket)
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    main()
