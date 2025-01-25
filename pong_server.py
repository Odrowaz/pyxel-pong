import socket
import struct
from pong_networking_commons import PacketType

DEBUG_MODE = True
HOST = 'localhost'
PORT = 12345

clients = {} #client addresses and clientID
next_client_id = 0

def start_server():
    global clients, next_client_id
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST,PORT))
    if DEBUG_MODE:
        print("Server listening on {0}:{1}".format(HOST,PORT))
    
    is_server_running = True

    while is_server_running:
        try:
            data, client_address = server_socket.recvfrom(1024)
            if DEBUG_MODE:
                print("Received {0} bytes of data.".format(len(data)))
            if client_address not in clients:
                client_id = next_client_id
                next_client_id += 1
                clients[client_address] = client_id
                if DEBUG_MODE:
                    print("Assigned ID {0} at client {1}".format(client_id, client_address))
                server_socket.sendto(struct.pack(">BB",PacketType.REQUEST_ID,client_id),client_address) # packet with packettype + clientid 
                ###do the same later in the RequestID management
                # every time I receive a RequestID message:
                # - reply to the requesting client with his ID (struct.pack(">BB",PacketType.REQUEST_ID,client_id))
                # - send a SPAWN message to all the other clients with the ID (struct.pack(">BB",PacketType.SPAWN,client_id))
                # - send a SPAWN message to the requesting id client for each client already in the client list (that is not the requesting one) with its own client id             
            else:
                if len(data) == 1:
                    packet_type, = struct.unpack(">B",data)
                    if packet_type == PacketType.REQUEST_ID:
                        if DEBUG_MODE:
                            print("Resending client ID {0} to client {1}".format(clients[client_address],client_address))
                        server_socket.sendto(struct.pack(">BB", PacketType.REQUEST_ID, clients[client_address]),client_address)
                        #as in the previous Id management
                elif len(data) == 10:
                    packet_type, client_id, x_pos, y_pos = struct.unpack(">BBII",data)
                    if DEBUG_MODE:
                        print("received packet with type {0} from clientID {1} wit pos x:{2} y:{3}".format(packet_type,client_id,x_pos,y_pos))
                    for client in clients:
                        if client != client_address:
                            server_socket.sendto(data, client)
        except Exception as e:
            print("Server error: {0}".format(e))

if __name__ == "__main__":
    print("Server main starting...")
    start_server()