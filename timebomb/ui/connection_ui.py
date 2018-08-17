from PySide.QtGui import *
from timebomb.defs import ui_defs
from timebomb.ui import join_game_ui
from timebomb.ui import create_account_ui
from timebomb.ui import forgot_password_ui


class ConnectionUi(QWidget):
    def __init__(self):
        super(ConnectionUi, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.resize(250, 150)
        self.setWindowTitle("Connection")

        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        # PLAYER UI
        self.group_player_infos = QGroupBox("Player's Infos")
        self.layout_main.addWidget(self.group_player_infos)

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
        self.layout_main.addWidget(self.widget_connect)
        self.layout_connect = QHBoxLayout()
        self.widget_connect.setLayout(self.layout_connect)

        self.widget_add_items = QWidget()
        self.layout_connect.addWidget(self.widget_add_items)
        self.layout_add_items = QVBoxLayout()
        self.widget_add_items.setLayout(self.layout_add_items)

        self.font_underline = QFont()
        self.font_underline.setUnderline(True)

        self.button_create_account = QPushButton("Create Account?")
        self.layout_add_items.addWidget(self.button_create_account)
        self.button_create_account.setFlat(True)
        self.button_create_account.setFont(self.font_underline)

        self.button_pass_forgot = QPushButton("Password forgot?")
        self.layout_add_items.addWidget(self.button_pass_forgot)
        self.button_pass_forgot.setFlat(True)
        self.button_pass_forgot.setFont(self.font_underline)

        self.button_connect = QPushButton("CONNECT")
        self.layout_connect.addWidget(self.button_connect)

        self.button_create_account.clicked.connect(self._create_account)
        self.button_pass_forgot.clicked.connect(self._pass_forgot)
        self.button_connect.clicked.connect(self._connection_ui)

        self.show()

    def _create_account(self):
        self.create_account_ui = create_account_ui.CreateAccountUi()

    def _pass_forgot(self):
        self.forgot_password_ui = forgot_password_ui.ForgotPasswordUi()

    def _valid_password(self, player_login, player_password):
        bdd = ui_defs.read_bdd()

        if bdd[player_login]["password"] == player_password:
            return True

    def _connection_ui(self):
        self.player_login = self.line_edit_login.text()

        if ui_defs.player_exist(self.player_login):
            input_password = ui_defs.encode_password(self.line_edit_password.text())

            if self._valid_password(self.player_login, input_password):
                self.join_game_ui = join_game_ui.JoinGameUi(self.player_login)
                self.close()

            else:
                ui_defs.message_box('Wrong Password', 'This is not a good password.')

        else:
            ui_defs.message_box('Wrong Login', 'This login doesn\'t exist yet.')
