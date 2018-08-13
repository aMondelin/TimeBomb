import os
import sys
import json
import random
import hashlib
import smtplib
import re

from PySide.QtGui import *
from email import MIMEMultipart
from email import MIMEText


def read_bdd():
    bdd_player_path = os.getcwd()
    bdd_player_path = os.path.join(bdd_player_path, "bdd_players.json")
    with open(bdd_player_path, 'r') as f_json:
        bdd_file = json.load(f_json)

    return bdd_file


def write_bdd(new_bdd):
    bdd_player_path = os.getcwd()
    bdd_player_path = os.path.join(bdd_player_path, "bdd_players.json")

    with open(bdd_player_path, 'w') as write_file:
        json.dump(new_bdd, write_file, indent=4)


def player_exist(player_login):
    bdd = read_bdd()

    if player_login in bdd:
        return True


def encode_password(password):
    input_password = hashlib.sha1(str(password))
    input_password = input_password.hexdigest()

    return input_password


def generate_random_password():
    return random.randint(10000000, 99999999)


def players_infos(player):
    bdd = read_bdd()
    return bdd[player]


def message_box(message_title, message_text):
    message_box = QMessageBox()
    message_box.setWindowTitle(message_title)
    message_box.setText(message_text)

    message_box.exec_()


class ConnectionUi(QWidget):
    def __init__(self):
        super(ConnectionUi, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.resize(250, 150)
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

        self.button_create_account.clicked.connect(self.create_account)
        self.button_pass_forgot.clicked.connect(self.pass_forgot)
        self.button_connect.clicked.connect(self.connection_ui)

        self.show()

    def create_account(self):
        self.create_account_ui = CreateAccountUi()

    def pass_forgot(self):
        self.forgot_password_ui = ForgotPasswordUi()

    def valid_password(self, player_login, player_password):
        bdd = read_bdd()

        if bdd[player_login]["password"] == player_password:
            return True

    def connection_ui(self):
        player_login = self.line_edit_login.text()

        if player_exist(player_login):
            input_password = encode_password(self.line_edit_password.text())

            if self.valid_password(player_login, input_password):
                self.join_game_ui = JoinGameUi()
                self.close()

            else:
                message_box('Wrong Password', 'This is not a good password.')

        else:
            message_box('Wrong Login', 'This login doesn\'t exist yet.')


class CreateAccountUi(QWidget):
    def __init__(self):
        super(CreateAccountUi, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.resize(275, 275)
        self.setWindowTitle("Create Account")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.group_account_infos = QGroupBox("Account's Infos")
        self.main_layout.addWidget(self.group_account_infos)
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
        self.main_layout.addWidget(self.button_create)

        self.button_create.clicked.connect(self.create_player)

        self.show()

    def same_password(self):
        if self.line_edit_password.text() == self.line_edit_password_confirm.text():
            return True

    def create_dict_player(self, player_password, player_email):
        player_dict = dict()
        player_dict[u"email"] = unicode(player_email)
        player_dict[u"password"] = unicode(encode_password(player_password))

        return player_dict

    def valid_email(self, email):
        verify_expression = re.compile(r"^[\w\S\._-]+@[\w\S\.-]+\.([a-zA-Z]{2,3})$")

        if not re.search(verify_expression, email) is None:
            return True

    def create_player(self):
        player_login = self.line_edit_login.text()
        player_password = self.line_edit_password.text()
        player_email = self.line_edit_email.text()

        if player_login != '' and player_password != '' and player_email != '':
            if not player_exist(player_login):
                if self.same_password():
                    if self.valid_email(player_email):
                        bdd = read_bdd()
                        new_player = self.create_dict_player(player_password, player_email)
                        bdd[player_login] = new_player
                        write_bdd(bdd)

                        message_box('OK', 'Your account is now active.')

                        self.join_game_ui = JoinGameUi()
                        self.close()
                    else:
                        message_box('Unvalid email', 'Please enter a valid email.')
                else:
                    message_box('Wrong Password', 'You have to input same passwords.')
            else:
                message_box('Wrong Login', 'This login already exist yet.')
        else:
            message_box('', 'You have to complete all informations.')


class ForgotPasswordUi(QWidget):
    def __init__(self):
        super(ForgotPasswordUi, self).__init__()
        self._init_ui()

    def _init_ui(self):
        self.resize(250, 50)
        self.setWindowTitle("Password forgot?")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.widget_player_login = QWidget()
        self.main_layout.addWidget(self.widget_player_login)
        self.layout_player_login = QHBoxLayout()
        self.widget_player_login.setLayout(self.layout_player_login)

        self.label_player_login = QLabel("Player's login: ")
        self.layout_player_login.addWidget(self.label_player_login)
        self.line_edit_player_login = QLineEdit()
        self.layout_player_login.addWidget(self.line_edit_player_login)

        self.button_send = QPushButton("SEND NEW PASSWORD")
        self.button_send.setMaximumWidth(125)
        self.main_layout.addWidget(self.button_send)

        self.button_send.clicked.connect(self.send_new_password)

        self.show()

    def assign_password_to_player(self, player, password):
        bdd = read_bdd()
        bdd[player]["password"] = encode_password(password)
        write_bdd(bdd)

    def send_new_password(self):
        player_login = self.line_edit_player_login.text()
        try:
            from_adress = "time.bomb.antho@gmail.com"
            to_adress = players_infos(player_login)["email"]

            email_to_send = MIMEMultipart()
            email_to_send['From'] = from_adress
            email_to_send['To'] = to_adress
            email_to_send['Subject'] = 'New Time Bomb Password'

            new_password = generate_random_password()
            self.assign_password_to_player(player_login, new_password)
            email_body = (
                'Your new time bomb password : ' + str(new_password) +
                "\n\nYou'll could change it in your preferences.\n\nSee you soon in game!"
            )
            email_to_send.attach(MIMEText(email_body, 'plain'))

            gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
            gmail_server.starttls()
            gmail_server.login(from_adress, "TimeBomb78+")
            gmail_server.sendmail(from_adress, to_adress, str(email_to_send))
            gmail_server.quit()

            message_box('OK', 'A new password has been send.')

            self.close()

        except KeyError:
            message_box('Wrong Login', 'This login doesn\'t exist.')


class JoinGameUi(QWidget):
    def __init__(self):
        super(JoinGameUi, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(300, 250)
        self.setWindowTitle("Server's Room")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.button_create_game = QPushButton("Create New Game")
        self.main_layout.addWidget(self.button_create_game)

        self.list_servers = QListWidget()
        self.main_layout.addWidget(self.list_servers)

        self.button_create_game.clicked.connect(self.create_game_ui)

        self.show()

    def create_game_ui(self):
        self.create_game_ui = CreateGameUi()


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
        self.layout_game_info = QVBoxLayout()
        self.group_game_info.setLayout(self.layout_game_info)

        self.group_game_name = QWidget()
        self.layout_game_name = QHBoxLayout()
        self.group_game_name.setLayout(self.layout_game_name)
        self.label_game_name = QLabel("Game's Name: ")
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


def generate_ui():
    app = QApplication(sys.argv)
    main_ui = ConnectionUi()
    sys.exit(app.exec_())


if __name__ == "__main__":
    generate_ui()
