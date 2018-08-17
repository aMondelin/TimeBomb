import re
from PySide.QtGui import *
from timebomb.defs import ui_defs
from timebomb.ui import join_game_ui


class CreateAccountUi(QWidget):
    def __init__(self):
        super(CreateAccountUi, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.resize(275, 275)
        self.setWindowTitle("Create Account")

        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.group_account_infos = QGroupBox("Account's Infos")
        self.layout_main.addWidget(self.group_account_infos)
        self.layout_account_infos = QVBoxLayout()
        self.group_account_infos.setLayout(self.layout_account_infos)

        self.widget_login = QWidget()
        self.layout_account_infos.addWidget(self.widget_login)
        self.layout_login = QHBoxLayout()
        self.widget_login.setLayout(self.layout_login)
        self.label_login = QLabel("Name: ")
        self.layout_login.addWidget(self.label_login)
        self.line_edit_login = QLineEdit()
        self.layout_login.addWidget(self.line_edit_login)

        self.widget_password = QWidget()
        self.layout_account_infos.addWidget(self.widget_password)
        self.layout_password = QHBoxLayout()
        self.widget_password.setLayout(self.layout_password)
        self.label_password = QLabel("Password: ")
        self.layout_password.addWidget(self.label_password)
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setEchoMode(self.line_edit_password.Password)
        self.layout_password.addWidget(self.line_edit_password)

        self.widget_password_confirm = QWidget()
        self.layout_account_infos.addWidget(self.widget_password_confirm)
        self.layout_password_confirm = QHBoxLayout()
        self.widget_password_confirm.setLayout(self.layout_password_confirm)
        self.label_password_confirm = QLabel("Confirm password: ")
        self.layout_password_confirm.addWidget(self.label_password_confirm)
        self.line_edit_password_confirm = QLineEdit()
        self.line_edit_password_confirm.setEchoMode(self.line_edit_password_confirm.Password)
        self.layout_password_confirm.addWidget(self.line_edit_password_confirm)

        self.widget_email = QWidget()
        self.layout_account_infos.addWidget(self.widget_email)
        self.layout_email = QHBoxLayout()
        self.widget_email.setLayout(self.layout_email)
        self.label_email = QLabel("Email: ")
        self.layout_email.addWidget(self.label_email)
        self.line_edit_email = QLineEdit()
        self.layout_email.addWidget(self.line_edit_email)

        self.button_create = QPushButton("CREATE ACCOUNT")
        self.layout_main.addWidget(self.button_create)

        self.button_create.clicked.connect(self._create_player)

        self.show()

    def _same_password(self):
        if self.line_edit_password.text() == self.line_edit_password_confirm.text():
            return True

    def _create_dict_player(self, player_password, player_email):
        player_dict = dict()
        player_dict[u"email"] = unicode(player_email)
        player_dict[u"password"] = unicode(ui_defs.encode_password(player_password))

        return player_dict

    def _valid_email(self, email):
        verify_expression = re.compile(r"^[\w\S\._-]+@[\w\S\.-]+\.([a-zA-Z]{2,3})$")

        if not re.search(verify_expression, email) is None:
            return True

    def _create_player(self):
        player_login = self.line_edit_login.text()
        player_password = self.line_edit_password.text()
        player_email = self.line_edit_email.text()

        if player_login != '' and player_password != '' and player_email != '':
            if not ui_defs.player_exist(player_login):
                if self._same_password():
                    if self._valid_email(player_email):
                        bdd = ui_defs.read_bdd()
                        new_player = self._create_dict_player(player_password, player_email)
                        bdd[player_login] = new_player
                        ui_defs.write_bdd(bdd)

                        ui_defs.message_box('OK', 'Your account is now active.')

                        self.join_game_ui = join_game_ui.JoinGameUi(player_login)
                        self.close()
                    else:
                        ui_defs.message_box('Unvalid email', 'Please enter a valid email.')
                else:
                    ui_defs.message_box('Wrong Password', 'You have to input same passwords.')
            else:
                ui_defs.message_box('Wrong Login', 'This login already exist yet.')
        else:
            ui_defs.message_box('', 'You have to complete all informations.')
