import pyxel
import pong_players
from pong_ball import PongBall
from pong_globals import manage_score
from pong_managers import UpdateManager, DrawManager, PhysicsManager
import pong_client
import sys

class App():
    def __init__(self, game_width, game_height, network, player_name = ''):        
        pyxel.init(game_width, game_height)
        
        self.update_manager = UpdateManager()
        self.draw_manager = DrawManager()
        self.physics_manager = PhysicsManager()
        self.game_started = False
        self.connected = False
        self.player1 = None
        self.player2 = None
        
        if not network:
            self.player1 = pong_players.Player2(10, 35, 9)
            self.player2 = pong_players.Player1(160, 35, 2)
            self.ball = PongBall(7)
            self.update_manager.register(self.player1, self.player2, self.ball)
            self.draw_manager.register(self.player1,self.player2, self.ball)
            self.physics_manager.register(self.player1, self.player2, self.ball)
            self.game_started = True
        else:
            self.client = pong_client.PongClient(player_name)

        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.update_manager.tick()
        self.physics_manager.tick()
        self.client.run_client()
        if self.game_started:
            manage_score((self.player1, self.player2), self.ball)
        elif self.client.client_id != '' and not self.connected:
            pos = self.client.pos
            self.player1 = pong_players.Player1(pos[0], pos[1], 9, True, self.client)
            self.draw_manager.register(self.player1)
            self.update_manager.register(self.player1)
            self.physics_manager.register(self.player1)
            self.connected = True
            
        elif len(self.client.clients) > 0:
            player_id = list(self.client.clients.keys())[0]
            player_data = self.client.clients[player_id]
            if len(player_data) == 2:
                pos = player_data[0]
                player_name = player_data[1]
                print(pos)
                self.player2 = pong_players.PlayerNet(pos[0], pos[1], 2, player_id, self.client, player_name)
                self.draw_manager.register(self.player2)
                self.update_manager.register(self.player2)
                self.physics_manager.register(self.player2)

        if self.player1 != None and self.player2 != None and not self.game_started:
            self.ball = self.ball = PongBall(7)
            self.physics_manager.register(self.ball)
            self.draw_manager.register(self.ball)
            self.update_manager.register(self.ball)
            self.game_started = True

        
        
    
    def draw(self):
        self.draw_manager.tick()


if __name__ == '__main__':
    App(180,160, True, sys.argv[1])