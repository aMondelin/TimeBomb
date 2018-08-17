from PySide.QtGui import *

from timebomb.ui import create_game_ui
from timebomb.ui import settings_profile_ui


class JoinGameUi(QWidget):
    def __init__(self, player_login):
        super(JoinGameUi, self).__init__()
        self.player_login = player_login
        self._init_ui()

    def _init_ui(self):
        self.resize(300, 250)
        self.setWindowTitle("Server's Room")

        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.menu_main = QMenuBar()
        self.layout_main.setMenuBar(self.menu_main)

        self.menu_file = self.menu_main.addMenu('File')
        self.menu_file.addAction('Exit', self._exit_profile)

        self.menu_profile = self.menu_main.addMenu('Profile')
        self.menu_profile.addAction('Stats', self._stat_profile)
        self.menu_profile.addAction('Settings', self._settings_profile)

        self.button_create_game = QPushButton("Create New Game")
        self.layout_main.addWidget(self.button_create_game)

        self.list_servers = QListWidget()
        self.layout_main.addWidget(self.list_servers)

        self.button_create_game.clicked.connect(self._create_game_ui)

        self.show()

    def _exit_profile(self):
        self.close()

    def _stat_profile(self):
        print "STATS PROFILE"

    def _settings_profile(self):
        self.settings_profile_ui = settings_profile_ui.SettingsProfileUi(self.player_login)

    def _create_game_ui(self):
        self.create_game_ui = create_game_ui.CreateGameUi()
