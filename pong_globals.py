import pyxel
from pong_game_save import save_file
   
def manage_score(players, ball, network, client):
    if network:
        players[0].score = client.points[0]
        players[1].score = client.points[1]
    if not network or client.client_id == 0:
        if ball.x + ball.radius > pyxel.width:
            if network:
                client.points[0] += 1
                client.send_points_data()
            else:
                players[0].add_score()
            __save_and_reset(ball, players, network)
        elif ball.x - ball.radius < 0:
            if network:
                client.points[1] += 1
                client.send_points_data()
            else:
                players[1].add_score()
            __save_and_reset(ball, players, network)

def __save_and_reset(ball, players, network):
    ball.reset()
    if not network:
        save_file.save(players)