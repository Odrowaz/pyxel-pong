from PySide6.QtWidgets import *
from PySide6.QtCore import *
import pong_game_save
import os
import json

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.setWindowTitle("Pong")
        
        mainLayout = QVBoxLayout()
        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        
        self.setCentralWidget(mainWidget)
        
        text = QLabel()
        text.setText("Pong Domenico Landriscina")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.slots = (QPushButton("Save Slot 1"), QPushButton("Save Slot 2"), QPushButton("Save Slot 3"))
        
        slot1 = self.slots[0]
        slot1.setCheckable(True)
        slot1.clicked.connect(self.on_slot_selected(0))
        
        slot2 = self.slots[1]
        slot2.setCheckable(True)
        slot2.clicked.connect(self.on_slot_selected(1))
        
        slot3 = self.slots[2]
        slot3.setCheckable(True)
        slot3.clicked.connect(self.on_slot_selected(2))
        
        
        player1_label = QLabel("Player 1: ")
        player1_score_label = QLabel("Score: ")
        
        self.player1_score = QLineEdit()
        self.player1_score.setEnabled(False)
        
        self.player1_edit = QLineEdit()
        self.player1_edit.setEnabled(False)
        self.player1_edit.setMaxLength(10)
        self.player1_edit.textChanged.connect(self.enable_disable_buttons)

        player1_section_layout = QHBoxLayout()
        player1_section_layout.addWidget(player1_label)
        player1_section_layout.addWidget(self.player1_edit)
        player1_section_layout.addWidget(player1_score_label)
        player1_section_layout.addWidget(self.player1_score)
        
        player1_section = QWidget()
        player1_section.setLayout(player1_section_layout)
        
        player2_label = QLabel("Player 2: ")
        player2_score_label = QLabel("Score: ")
        
        self.player2_score = QLineEdit()
        self.player2_score.setEnabled(False)
        
        self.player2_edit = QLineEdit()
        self.player2_edit.setEnabled(False)
        self.player2_edit.setMaxLength(10)
        self.player2_edit.textChanged.connect(self.enable_disable_buttons)
        
        player2_section_layout = QHBoxLayout()
        player2_section_layout.addWidget(player2_label)
        player2_section_layout.addWidget(self.player2_edit)
        player2_section_layout.addWidget(player2_score_label)
        player2_section_layout.addWidget(self.player2_score)
        
        player2_section = QWidget()
        player2_section.setLayout(player2_section_layout)
        
        self.new_game = QPushButton("New Game")
        self.new_game.setEnabled(False)
        self.new_game.clicked.connect(self.on_new_game_clicked)
        
        self.load_game = QPushButton("Load Game")
        self.load_game.setEnabled(False)
        self.load_game.clicked.connect(self.on_load_game_clicked)
        
        mainLayout.addWidget(text)
        mainLayout.addWidget(slot1)
        mainLayout.addWidget(slot2)
        mainLayout.addWidget(slot3)
        mainLayout.addWidget(QHLine())
        mainLayout.addWidget(player1_section)
        mainLayout.addWidget(player2_section)
        mainLayout.addWidget(QHLine())
        mainLayout.addWidget(self.new_game)
        mainLayout.addWidget(self.load_game)
        
        
    def check_if_name_is_valid(self, name):
        return len(name) > 0 and len(name) <= 10
    
    def enable_disable_buttons(self):
        self.new_game.setEnabled(self.check_if_name_is_valid(self.player1_edit.text()) and self.check_if_name_is_valid(self.player2_edit.text()))
        if os.path.isfile(f"save{self.selected_slot}.json"):
            self.load_game.setEnabled(self.check_if_name_is_valid(self.player1_edit.text()) and self.check_if_name_is_valid(self.player2_edit.text()))
        else:
            self.load_game.setEnabled(False)    
            
    def on_slot_selected(self, slot):
        def select_slot(checked):
            if checked:
                self.selected_slot = slot
                self.enable_disable_buttons()
                self.read_player_data()
                    
                indexes = list(range(len(self.slots)))
                indexes.remove(slot)
                for i in indexes:
                    self.slots[i].setChecked(False)
            else:
                self.new_game.setEnabled(False)
                self.load_game.setEnabled(False)
                self.player1_edit.setText("")
                self.player1_edit.setEnabled(False)
                self.player2_edit.setText("")
                self.player2_edit.setEnabled(False)
        return select_slot
    
    def read_player_data(self):
        try:
            with open(f"save{self.selected_slot}.json", "r") as handle:
                data = json.load(handle)
        except:
            data = {}
        self.player1_edit.setText(data.get("player1", {}).get("name", "Player 1"))
        self.player1_score.setText(str(data.get("player1", {}).get("score", "0")))
        self.player1_edit.setEnabled(True)
        self.player2_edit.setText(data.get("player2", {}).get("name", "Player 2"))
        self.player2_score.setText(str(data.get("player2", {}).get("score", "0")))
        self.player2_edit.setEnabled(True)
        
    def save_player_data(self, load_game):
        data = {
            "player1": {},
            "player2": {}
        }
        try:
            if not os.path.isfile(f"save{self.selected_slot}.json"):
                open(f"save{self.selected_slot}.json", "w").close()                
            with open(f"save{self.selected_slot}.json", "r+") as handle:
                    if load_game:
                        save_content = json.load(handle)
                        data = save_content
                    handle.truncate(0)
                    handle.seek(0)
                    data["player1"]["name"] = self.player1_edit.text()
                    data["player2"]["name"] = self.player2_edit.text()
                    json.dump(data, handle, indent=4)
        except Exception as e:
            print(e)
            exit(-1)
        
    
    def on_new_game_clicked(self):
            self.start_game(False)
        
    def on_load_game_clicked(self):
            self.start_game(True)
    
    def start_game(self, load):
            self.save_player_data(load)
            pong_game_save.GameSave(f"save{self.selected_slot}.json").load()
            self.close()
            # Init Save File Before importing pong
            from pong_game import App
            App(180,160, False)
            
app = QApplication()

window = MainWindow()
window.show()

app.exec()