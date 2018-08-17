from PySide.QtGui import *
from timebomb.ui import game_ui


class CreateGameUi(QWidget):
    def __init__(self):
        super(CreateGameUi, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.resize(290, 280)
        self.setWindowTitle("Create Game")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.group_game_info = QGroupBox("Game's Infos")
        self.main_layout.addWidget(self.group_game_info)
        self.layout_game_info = QVBoxLayout()
        self.group_game_info.setLayout(self.layout_game_info)

        self.group_game_name = QWidget()
        self.layout_game_info.addWidget(self.group_game_name)
        self.layout_game_name = QHBoxLayout()
        self.group_game_name.setLayout(self.layout_game_name)

        self.label_game_name = QLabel("Game's Name: ")
        self.layout_game_name.addWidget(self.label_game_name)

        self.line_edit_game_name = QLineEdit()
        self.layout_game_name.addWidget(self.line_edit_game_name)

        self.group_nb_players = QWidget()
        self.layout_game_info.addWidget(self.group_nb_players)
        self.layout_nb_players = QHBoxLayout()
        self.group_nb_players.setLayout(self.layout_nb_players)

        self.label_nb_players = QLabel("Nb Players: ")
        self.label_nb_players.setMaximumWidth(70)
        self.layout_nb_players.addWidget(self.label_nb_players)

        self.spin_box_nb_players = QSpinBox()
        self.spin_box_nb_players.setMaximumWidth(35)
        self.spin_box_nb_players.setRange(4, 8)
        self.spin_box_nb_players.setValue(4)
        self.layout_nb_players.addWidget(self.spin_box_nb_players)

        self.spacer_nb_player = QSpacerItem(130, 20)
        self.layout_nb_players.addItem(self.spacer_nb_player)

        self.group_settings = QGroupBox("Settings")
        self.layout_game_info.addWidget(self.group_settings)
        self.layout_settings = QVBoxLayout()
        self.group_settings.setLayout(self.layout_settings)

        self.group_settings_team = QWidget()
        self.layout_settings.addWidget(self.group_settings_team)
        self.layout_settings_team = QHBoxLayout()
        self.group_settings_team.setLayout(self.layout_settings_team)

        self.spacer1_settings_team = QSpacerItem(20, 40)
        self.layout_settings_team.addItem(self.spacer1_settings_team)

        self.label_settings_team = QLabel("Teams: ")
        self.label_settings_team.setMaximumWidth(40)
        self.layout_settings_team.addWidget(self.label_settings_team)

        self.radio_settings_team_auto = QRadioButton("Auto")
        self.radio_settings_team_auto.setMaximumWidth(70)
        self.radio_settings_team_auto.toggle()
        self.layout_settings_team.addWidget(self.radio_settings_team_auto)
        self.radio_settings_team_auto.clicked.connect(self._enable_manually_team)

        self.radio_settings_team_manually = QRadioButton("Manually")
        self.radio_settings_team_manually.setMaximumWidth(70)
        self.layout_settings_team.addWidget(self.radio_settings_team_manually)
        self.radio_settings_team_manually.clicked.connect(self._enable_manually_team)

        self.spacer2_settings_team = QSpacerItem(20, 40)
        self.layout_settings_team.addItem(self.spacer2_settings_team)

        self.group_settings_manually = QWidget()
        self.layout_settings.addWidget(self.group_settings_manually)
        self.group_settings_manually.setEnabled(False)
        self.layout_settings_manually = QHBoxLayout()
        self.group_settings_manually.setLayout(self.layout_settings_manually)

        self.spacer1_settings_manually = QSpacerItem(20, 40)
        self.layout_settings_manually.addItem(self.spacer1_settings_manually)

        self.label_settings_manually_sherlock = QLabel("Sherlock: ")
        self.label_settings_manually_sherlock.setMaximumWidth(50)
        self.layout_settings_manually.addWidget(self.label_settings_manually_sherlock)

        self.spin_box_settings_manually_sherlock = QSpinBox()
        self.spin_box_settings_manually_sherlock.setMaximumWidth(35)
        self.spin_box_settings_manually_sherlock.setRange(1, 7)
        self.spin_box_settings_manually_sherlock.setValue(3)
        self.layout_settings_manually.addWidget(self.spin_box_settings_manually_sherlock)

        self.label_settings_manually_moriarty = QLabel("Moriarty: ")
        self.label_settings_manually_moriarty.setMaximumWidth(50)
        self.layout_settings_manually.addWidget(self.label_settings_manually_moriarty)

        self.spin_box_settings_manually_moriarty = QSpinBox()
        self.spin_box_settings_manually_moriarty.setMaximumWidth(35)
        self.spin_box_settings_manually_moriarty.setRange(1, 7)
        self.spin_box_settings_manually_moriarty.setValue(1)
        self.layout_settings_manually.addWidget(self.spin_box_settings_manually_moriarty)

        self.spacer2_settings_manually = QSpacerItem(20, 40)
        self.layout_settings_manually.addItem(self.spacer2_settings_manually)

        self.button_create_game = QPushButton("CREATE GAME")
        self.button_create_game.setMaximumWidth(150)
        self.button_create_game.clicked.connect(self._game_ui)
        self.main_layout.addWidget(self.button_create_game)

        self.show()

    def _enable_manually_team(self):
        if self.radio_settings_team_manually.isChecked():
            self.group_settings_manually.setEnabled(True)

        else:
            self.group_settings_manually.setEnabled(False)

    def _game_ui(self):
        game_name = self.line_edit_game_name.text()
        self.game_ui = game_ui.GameUi(game_name)
