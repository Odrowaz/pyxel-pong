import pyxel
from pong_game_save import save_file

class PlayerBase:
    def __init__(self, x, y, color, network):
        self.width = 10
        self.score = 0
        self.height = 50
        self.x = x
        self.y = y
        self.color = color
        if not network:
            if (value := save_file.player_data.get(f"player{self.controller}", {}).get("score")) is not None:
                    self.set_score(int(value))
            self.name = save_file.player_data.get(f"player{self.controller}", {}).get("name", f"Player {self.controller}")
        pass
    
    def collide(self, other):
        # dal player non mi interessa gestire la collisione
        pass
    
    def get_score(self):
        return self.score
    
    def set_score(self, score):
        self.score = score
    
    def add_score(self):
        self.score += 1
    
    def update(self):
        if self.y + self.height > pyxel.height:
            self.y = pyxel.height - self.height
        if self.y < 0:
            self.y = 0
        pass
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)
        pass
    
    def draw_score_text(self,x,y):
        pyxel.text(x, y, f"{self.name}: {self.score}", 6)
    
    
class Player1(PlayerBase):
    def __init__(self, x, y, color, network, client=None):
        self.controller = "1"
        super().__init__(x, y, color, network)
        self.client = client
        if network:
            self.name = client.name
        
    def update(self):
        if pyxel.btn(pyxel.KEY_W):
            self.y -= 6
        elif pyxel.btn(pyxel.KEY_S):
            self.y += 6
        super().update()
        self.client.pos = (self.x, self.y)
        
    def draw(self):
        super().draw()
        self.draw_score_text(10 if self.x == 10 else 120 ,10)

class Player2(PlayerBase):
    def __init__(self, x, y, color, network):
        self.controller = "2"
        super().__init__(x, y, color, network)
        
    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 6
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.y += 6
        super().update()
        
    def draw(self):
        super().draw()
        self.draw_score_text(120,10)

class PlayerNet(PlayerBase):
    def __init__(self, x, y, color, player_id, client, name):
        self.controller = "Net"
        self.player_id = player_id
        self.client = client
        self.name = name
        super().__init__(x, y, color, True)
        
    def update(self):
        self.x = self.client.clients[self.player_id][0][0]
        self.y = self.client.clients[self.player_id][0][1]
        pass
        
    def draw(self):
        super().draw()
        self.draw_score_text(10 if self.x == 10 else 120,10)