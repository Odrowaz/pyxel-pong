import pyxel
from pong_game_save import save_file
   
def manage_score(players, ball):
    if ball.x + ball.radius > pyxel.width:
        players[0].add_score()
        ball.reset()
        save_file.save(players)
    elif ball.x - ball.radius < 0:
        players[1].add_score()
        ball.reset()
        save_file.save(players)