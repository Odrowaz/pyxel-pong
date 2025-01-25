import pyxel
import pong_players
from pong_ball import PongBall
from pong_globals import manage_score
from pong_managers import UpdateManager, DrawManager, PhysicsManager

class App():
    def __init__(self, game_width, game_height):        
        pyxel.init(game_width, game_height)
        
        self.update_manager = UpdateManager()
        self.draw_manager = DrawManager()
        self.physics_manager = PhysicsManager()
        
        self.player1 = pong_players.Player1(10, 35, 9)
        self.player2 = pong_players.Player2(160, 35, 2)
        
        self.ball = PongBall(7)
        
        self.update_manager.register(self.player1, self.player2, self.ball)
        self.draw_manager.register(self.player1, self.player2, self.ball)
        self.physics_manager.register(self.player1, self.player2, self.ball)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.update_manager.tick()
        self.physics_manager.tick()
        manage_score((self.player1, self.player2), self.ball)
    
    def draw(self):
        self.draw_manager.tick()