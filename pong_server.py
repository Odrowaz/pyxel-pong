import socket
import struct
from pong_networking_commons import PacketType

DEBUG_MODE = True
HOST = 'localhost'
PORT = 12345

clients = {}  # Stores client addresses as keys and (client_id, player_name) as values
next_client_id = 0

def start_server():
    global clients, next_client_id
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    if DEBUG_MODE:
        print("Server listening on {0}:{1}".format(HOST, PORT))

    is_server_running = True

    while is_server_running:
            data, client_address = server_socket.recvfrom(1024)
            if not data:
                if DEBUG_MODE:
                    print(f"No data received from {client_address}. Skipping.")
                continue

            # Handle new client connection
            if client_address not in clients:
                if len(clients) == 2:  # Only allow 2 players
                    if DEBUG_MODE:
                        print(f"Connection refused: Maximum players reached. Client {client_address} rejected.")
                    continue

                # Assign a new client ID
                client_id = next_client_id
                next_client_id += 1
                clients[client_address] = (client_id, None)  # Initialize without a player name
                if DEBUG_MODE:
                    print(f"Assigned ID {client_id} to client {client_address}")

            # Unpack the packet type
            packet_type, = struct.unpack(">B", data[:1])
            if DEBUG_MODE:
                print(f"Received {len(data)} bytes of data from {client_address}. Packet type: {packet_type}")

            # Handle REQUEST_ID packet
            if packet_type == PacketType.REQUEST_ID:
                _, encoded_player_name = struct.unpack(f">B{len(data) - 1}s", data)
                clients[client_address] = (clients[client_address][0], encoded_player_name)  # Update with player name
                if DEBUG_MODE:
                    print(f"Client {client_address} requested ID. Assigned ID: {clients[client_address][0]}, Name: {encoded_player_name.decode()}")

                # Send the client their assigned ID
                server_socket.sendto(struct.pack(">BB", PacketType.REQUEST_ID, clients[client_address][0]), client_address)

                # Notify other clients about the new player
                for client in clients:
                    if client != client_address:
                        new_player_spawn_packet = struct.pack(f">BB{len(encoded_player_name)}s", PacketType.SPAWN, clients[client_address][0], encoded_player_name)
                        old_player = clients[client]
                        old_player_spawn_packet = struct.pack(f">BB{len(old_player[1])}s", PacketType.SPAWN, old_player[0], old_player[1])
                        server_socket.sendto(new_player_spawn_packet, client)
                        server_socket.sendto(old_player_spawn_packet, client_address)


            # Handle POSITION packet
            elif packet_type == PacketType.POSITION:
                _, client_id, _, x_pos, y_pos, ball_x, ball_y = struct.unpack(">BBQIIff", data)
                if DEBUG_MODE:
                    print(f"Received position update from client ID {client_id}: x={x_pos}, y={y_pos}")

                # Broadcast the position update to all other clients
                for client in clients:
                    if client != client_address:
                        server_socket.sendto(data, client)

            # Handle client disconnection (not explicitly implemented in UDP)
            # You may need a heartbeat mechanism to detect disconnections


if __name__ == "__main__":
    print("Server starting...")
    start_server()