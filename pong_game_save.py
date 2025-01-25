import json

save_file = None

class GameSave():
    def __init__(self, path):
        global save_file
        self.player_data = {}
        self.path = path
        save_file = self
        pass

    def load(self):
        try:
            with open(self.path, 'r') as save_handle:
                self.player_data = json.load(save_handle)
        except Exception as e:
            if e.errno == 2:
                print("no save file found, starting a new game")
            else:
                print("an error has occurred reading gam e file: {0}".format(e))
                exit()
            
    def save(self, players):
        try:
            for player in players:
                self.player_data[f"player{player.controller}"] = {
                   "score": player.score,
                   "name": player.name
                }
            with open(self.path, 'w') as save_handle:
                json.dump(self.player_data, save_handle, indent=4)
        except Exception as e:
            print("an error has occurred: {0}".format(e))