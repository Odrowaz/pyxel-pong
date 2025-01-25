import struct
import socket
import select
from pong_networking_commons import PacketType

class PongClient():
    def __init__(self, name):
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server_address = ('localhost',12345)
        self.client_id = ""        
        self.name = name
        self.client_socket.setblocking(False)
        self.socket_list = [self.client_socket]
        self.is_client_running = True
        self.clients = {} #ClientID, [(pos), name]
        self.player_pos = (0, 0)
        self.ball_pos = (0, 0)
        self.points = [0, 0]
        self.my_counter = 0
        self.other_player_counter = 0

    def create_packet(self, packet_type, data = ()):
        if packet_type == PacketType.POSITION:
            print(data)
            packet = struct.pack(">BBQIIff", packet_type, self.client_id, self.my_counter, *data)
            self.my_counter += 1
        elif packet_type == PacketType.REQUEST_ID:
            packet = struct.pack(f">B{len(self.name)}s", packet_type, self.name.encode())
        elif packet_type == PacketType.POINT:
            packet = struct.pack(f">BBBB", packet_type, self.client_id, *self.points)
        return packet
    
    def send_packet(self, packet):
        self.client_socket.sendto(packet, self.server_address)

    def receive_data(self, read_sockets):
        for read_socket in read_sockets:
            if read_socket == self.client_socket:
                try:
                    data, _ = self.client_socket.recvfrom(1024)
                    packet_type, = struct.unpack(">B",data[:1])
                    if packet_type == PacketType.REQUEST_ID and self.client_id == '':
                        packet_type, received_client_id = struct.unpack(">BB",data)
                        self.client_id = received_client_id
                        print(f'My ID is {received_client_id}')
                        self.pos = (10, 35) if self.client_id == 0 else (160, 35)
                    elif packet_type == PacketType.SPAWN:
                        print('Spawning')
                        packet_type, client_id, encoded_player_name = struct.unpack(f">BB{len(data) - 2}s", data)
                        self.clients[client_id] = {}
                        self.clients[client_id][1] = encoded_player_name.decode()
                        pass
                    elif packet_type == PacketType.POSITION:
                        packet_type, client_id, counter, x_pos, y_pos, ball_x, ball_y = struct.unpack(">BBQIIff",data)     
                        if counter > self.other_player_counter:
                            self.other_player_counter = counter
                            self.clients[client_id][0] = (x_pos, y_pos)
                        if client_id == 0:
                            self.ball_pos = (ball_x, ball_y)
                    elif packet_type == PacketType.POINT:
                        packet_type, client_id, player_1_points, player_2_points = struct.unpack(">BBBB",data)     
                        if client_id == 0:
                            self.points = (player_1_points, player_2_points)
                except Exception as e:
                    print("Error: ", e)
                    pass

    def run_client(self):        
        self.read_sockets, _ , _ = select.select(self.socket_list,[],[],0)
        self.receive_data(self.read_sockets)
        if self.client_id != '':
            self.send_position_data()
        else:
            data = self.create_packet(PacketType.REQUEST_ID)
            self.send_packet(data)

    def send_position_data(self):
        packet = self.create_packet(PacketType.POSITION, (*self.pos, *self.ball_pos))
        self.send_packet(packet)

    def send_points_data(self):
        packet = self.create_packet(PacketType.POINT, (*self.pos, *self.ball_pos))
        self.send_packet(packet)


if __name__ == "__main__":
    print("Main client started")
    client = PongClient()
    client.run_client()
