import pyxel
from pong_game_save import save_file
   
def manage_score(players, ball, network):
    if ball.x + ball.radius > pyxel.width:
        players[0].add_score()
        __save_and_reset(ball, players, network)
    elif ball.x - ball.radius < 0:
        players[1].add_score()
        __save_and_reset(ball, players, network)

def __save_and_reset(ball, players, network):
    ball.reset()
    if not network:
        save_file.save(players)