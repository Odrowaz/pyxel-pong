import socket
import struct
from pong_networking_commons import PacketType

DEBUG_MODE = True
HOST = 'localhost'
PORT = 12345

clients = {} #client addresses (clientID, name)
next_client_id = 0

def start_server():
    global clients, next_client_id
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST,PORT))
    if DEBUG_MODE:
        print("Server listening on {0}:{1}".format(HOST,PORT))
    
    is_server_running = True

    while is_server_running:
            data, client_address = server_socket.recvfrom(1024)
            if client_address not in clients:
                if len(clients) == 2:
                    continue
        
                client_id = next_client_id
                next_client_id += 1

                if len(clients) > 0:
                    for client in clients:
                        spawn_packet = struct.pack(f">BB{len(clients[client][1])}s", PacketType.SPAWN, clients[client][0], encoded_player_name)
                        server_socket.sendto(spawn_packet, client_address)

                clients[client_address] = (client_id,)
                if DEBUG_MODE:
                    print("Assigned ID {0} at client {1}".format(client_id, client_address))

            if not data:
                print(f"Player {clients[client_address][0]} disconnected!")
                clients.pop(client_address)

            packet_type, = struct.unpack(">B",data[:1])
            if DEBUG_MODE:
                print("Received {0} bytes of data.".format(len(data)))

            if packet_type == PacketType.REQUEST_ID:
                packet_type, encoded_player_name = struct.unpack(f">B{len(data) - 1}s", data)
                clients[client_address] = (clients[client_address][0], encoded_player_name)
                if DEBUG_MODE:
                    print("Resending client ID {0} to client {1}".format(clients[client_address][0],client_address))
                server_socket.sendto(struct.pack(">BB", PacketType.REQUEST_ID, clients[client_address][0]) ,client_address)
                spawn_packet = struct.pack(f">BB{len(encoded_player_name)}s", PacketType.SPAWN, clients[client_address][0], encoded_player_name)
                for client in clients:
                    if client != client_address:
                        server_socket.sendto(spawn_packet, client)
                #as in the previous Id management
            elif packet_type == PacketType.POSITION:
                packet_type, client_id, x_pos, y_pos = struct.unpack(">BBII",data)
                if DEBUG_MODE:
                    print("received packet with type {0} from clientID {1} wit pos x:{2} y:{3}".format(packet_type,client_id,x_pos,y_pos))
                for client in clients:
                    if client != client_address:
                        server_socket.sendto(data, client)


if __name__ == "__main__":
    print("Server main starting...")
    start_server()