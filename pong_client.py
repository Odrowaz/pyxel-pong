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
        self.ball = None
        self.points = [0, 0]
        self.my_counter = 0
        self.other_player_counter = 0
        self.delay = 0

    def create_packet(self, packet_type, data = ()):
        if packet_type == PacketType.POSITION:
            packet = struct.pack(">BBQIIfffff", packet_type, self.client_id, self.my_counter, *data)
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
                        packet_type, client_id, encoded_player_name = struct.unpack(f">BB{len(data) - 2}s", data)
                        self.clients[client_id] = {}
                        self.clients[client_id][1] = encoded_player_name.decode()
                        print(f'Player {self.clients[client_id][1]} connected')
                        pass
                    elif packet_type == PacketType.POSITION:
                        packet_type, client_id, counter, x_pos, y_pos, ball_x, ball_y, ball_speed, ball_x_speed, ball_y_speed = struct.unpack(">BBQIIfffff",data)     
                        if counter > self.other_player_counter:
                            self.other_player_counter = counter
                            self.clients[client_id][0] = (x_pos, y_pos)
                        if client_id == 0:
                            self.ball.x = ball_x 
                            self.ball.y = ball_y
                            self.ball.base_speed = ball_speed
                            self.ball.x_speed = ball_x_speed
                            self.ball.y_speed = ball_y_speed

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
            if self.delay == 0:
                self.send_position_data()
                self.delay = 1
            else:
                self.delay -= 1
        else:
            data = self.create_packet(PacketType.REQUEST_ID)
            self.send_packet(data)

    def send_position_data(self):
        ball_data = (self.ball.x, self.ball.y, self.ball.base_speed, self.ball.x_speed, self.ball.y_speed)
        packet = self.create_packet(PacketType.POSITION, (*self.pos, *ball_data))
        self.send_packet(packet)

    def send_points_data(self):
        packet = self.create_packet(PacketType.POINT)
        self.send_packet(packet)