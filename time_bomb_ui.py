import os, sys, json
from PySide.QtGui import *


def read_bdd():
    bdd_player_path = os.getcwd()
    bdd_player_path = os.path.join(bdd_player_path, "bdd_players.json")
    with open(bdd_player_path, 'r') as f_json:
        bdd_file = json.load(f_json)

    return bdd_file


class connectionUi(QWidget):
    def __init__(self):
        super(connectionUi, self).__init__()

        self._init_ui()

    def _init_ui(self):
        self.resize(225, 150)
        self.setWindowTitle("Connection")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # PLAYER UI
        self.group_player_infos = QGroupBox("Player's Infos")
        self.main_layout.addWidget(self.group_player_infos)

        self.layout_player_infos = QVBoxLayout()
        self.group_player_infos.setLayout(self.layout_player_infos)

        # Login UI
        self.widget_login = QWidget()
        self.layout_player_infos.addWidget(self.widget_login)

        self.layout_login = QHBoxLayout()
        self.widget_login.setLayout(self.layout_login)

        self.label_login = QLabel("Login: ")
        self.layout_login.addWidget(self.label_login)

        self.line_edit_login = QLineEdit()
        self.layout_login.addWidget(self.line_edit_login)

        # PASSWORD UI
        self.widget_password = QWidget()
        self.layout_player_infos.addWidget(self.widget_password)

        self.layout_password = QHBoxLayout()
        self.widget_password.setLayout(self.layout_password)

        self.label_password = QLabel("Password: ")
        self.layout_password.addWidget(self.label_password)

        self.line_edit_password = QLineEdit()
        self.line_edit_password.setEchoMode(self.line_edit_password.Password)
        self.layout_password.addWidget(self.line_edit_password)

        # CONNECTION UI
        self.widget_connect = QWidget()
        self.main_layout.addWidget(self.widget_connect)

        self.layout_connect = QHBoxLayout()
        self.widget_connect.setLayout(self.layout_connect)

        self.label_pass_forgot = QLabel("Password forgot?")
        self.layout_connect.addWidget(self.label_pass_forgot)

        self.button_connect = QPushButton("CONNECT")
        self.layout_connect.addWidget(self.button_connect)

        self.button_connect.clicked.connect(self.join_game_ui)


        self.show()

    def join_game_ui(self):
        bdd = read_bdd()
        print bdd["Antho"]
        self.join_game_ui = joinGameUi()
        self.close()


class joinGameUi(QWidget):
    def __init__(self):
        super(joinGameUi, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.resize(300, 250)
        self.setWindowTitle("Server's Room")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.create_game = QPushButton("Create New Game")
        self.main_layout.addWidget(self.create_game)

        self.servers_list = QListWidget()
        self.main_layout.addWidget(self.servers_list)


        self.create_game.clicked.connect(self.create_game_ui)

        self.show()

    def create_game_ui(self):
        self.create_game_ui = createGameUi()


class createGameUi(QWidget):
    def __init__(self):
        super(createGameUi, self).__init__()

        self._init_ui()

    def _init_ui(self):
        self.resize(290, 280)
        self.setWindowTitle("Create Game")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.group_game_info = QGroupBox("Game's Infos")
        self.layout_game_info = QVBoxLayout()
        self.group_game_info.setLayout(self.layout_game_info)

        self.group_game_name = QWidget()
        self.layout_game_name = QHBoxLayout()
        self.group_game_name.setLayout(self.layout_game_name)
        self.label_game_name =  QLabel("Game's Name: ")
        self.line_edit_game_name = QLineEdit()

        self.group_nb_players = QWidget()
        self.layout_nb_players = QHBoxLayout()
        self.group_nb_players.setLayout(self.layout_nb_players)
        self.label_nb_players = QLabel("Nb Players: ")
        self.label_nb_players.setMaximumWidth(70)
        self.spin_box_nb_players = QSpinBox()
        self.spin_box_nb_players.setMaximumWidth(35)
        self.spin_box_nb_players.setRange(4, 8)
        self.spin_box_nb_players.setValue(4)
        self.spacer_nb_player = QSpacerItem(130, 20)

        self.group_settings = QGroupBox("Settings")
        self.layout_settings = QVBoxLayout()
        self.group_settings.setLayout(self.layout_settings)

        self.group_settings_team = QWidget()
        self.layout_settings_team = QHBoxLayout()
        self.group_settings_team.setLayout(self.layout_settings_team)
        self.spacer1_settings_team = QSpacerItem(20, 40)
        self.label_settings_team = QLabel("Teams: ")
        self.label_settings_team.setMaximumWidth(40)
        self.radio_settings_team_auto = QRadioButton("Auto")
        self.radio_settings_team_auto.setMaximumWidth(70)
        self.radio_settings_team_auto.toggle()
        self.radio_settings_team_manually = QRadioButton("Manually")
        self.radio_settings_team_manually.setMaximumWidth(70)
        self.spacer2_settings_team = QSpacerItem(20, 40)

        self.group_settings_manually = QWidget()
        self.layout_settings_manually = QHBoxLayout()
        self.group_settings_manually.setLayout(self.layout_settings_manually)
        self.spacer1_settings_manually = QSpacerItem(20, 40)
        self.label_settings_manually_sherlock = QLabel("Sherlock: ")
        self.label_settings_manually_sherlock.setMaximumWidth(50)
        self.spin_box_settings_manually_sherlock = QSpinBox()
        self.spin_box_settings_manually_sherlock.setMaximumWidth(35)
        self.spin_box_settings_manually_sherlock.setRange(1, 7)
        self.spin_box_settings_manually_sherlock.setValue(3)
        self.label_settings_manually_moriarty = QLabel("Moriarty: ")
        self.label_settings_manually_moriarty.setMaximumWidth(50)
        self.spin_box_settings_manually_moriarty = QSpinBox()
        self.spin_box_settings_manually_moriarty.setMaximumWidth(35)
        self.spin_box_settings_manually_moriarty.setRange(1, 7)
        self.spin_box_settings_manually_moriarty.setValue(1)
        self.spacer2_settings_manually = QSpacerItem(20, 40)

        self.button_create_game = QPushButton("CREATE GAME")
        self.button_create_game.setMaximumWidth(150)

        # Game Main Connections
        self.main_layout.addWidget(self.group_game_info)
        self.main_layout.addWidget(self.button_create_game)

        # Game's Infos Connections
        self.layout_game_info.addWidget(self.group_game_name)
        self.layout_game_info.addWidget(self.group_nb_players)
        self.layout_game_info.addWidget(self.group_settings)

        # Layout Game Name Connections
        self.layout_game_name.addWidget(self.label_game_name)
        self.layout_game_name.addWidget(self.line_edit_game_name)

        # Layout Nb Players Connections
        self.layout_nb_players.addWidget(self.label_nb_players)
        self.layout_nb_players.addWidget(self.spin_box_nb_players)
        self.layout_nb_players.addItem(self.spacer_nb_player)

        # Layout Settings Connections
        self.layout_settings.addWidget(self.group_settings_team)
        self.layout_settings.addWidget(self.group_settings_manually)

        self.layout_settings_team.addItem(self.spacer1_settings_team)
        self.layout_settings_team.addWidget(self.label_settings_team)
        self.layout_settings_team.addWidget(self.radio_settings_team_auto)
        self.layout_settings_team.addWidget(self.radio_settings_team_manually)
        self.layout_settings_team.addItem(self.spacer2_settings_team)

        self.layout_settings_manually.addItem(self.spacer1_settings_manually)
        self.layout_settings_manually.addWidget(self.label_settings_manually_sherlock)
        self.layout_settings_manually.addWidget(self.spin_box_settings_manually_sherlock)
        self.layout_settings_manually.addWidget(self.label_settings_manually_moriarty)
        self.layout_settings_manually.addWidget(self.spin_box_settings_manually_moriarty)
        self.layout_settings_manually.addItem(self.spacer2_settings_manually)

        self.show()


def generateUi():
    app = QApplication(sys.argv)
    main_ui = connectionUi()
    sys.exit(app.exec_())


if __name__ == "__main__":
    generateUi()
