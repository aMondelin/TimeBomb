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
        self.create_account_ui = CreateAccountUi()

    def _pass_forgot(self):
        self.forgot_password_ui = ForgotPasswordUi()

    def _valid_password(self, player_login, player_password):
        bdd = read_bdd()

        if bdd[player_login]["password"] == player_password:
            return True

    def _connection_ui(self):
        self.player_login = self.line_edit_login.text()

        if player_exist(self.player_login):
            input_password = encode_password(self.line_edit_password.text())

            if self._valid_password(self.player_login, input_password):
                self.join_game_ui = JoinGameUi(self.player_login)
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
        player_dict[u"password"] = unicode(encode_password(player_password))

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
            if not player_exist(player_login):
                if self._same_password():
                    if self._valid_email(player_email):
                        bdd = read_bdd()
                        new_player = self._create_dict_player(player_password, player_email)
                        bdd[player_login] = new_player
                        write_bdd(bdd)

                        message_box('OK', 'Your account is now active.')

                        self.join_game_ui = JoinGameUi(player_login)
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

        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.widget_player_login = QWidget()
        self.layout_main.addWidget(self.widget_player_login)
        self.layout_player_login = QHBoxLayout()
        self.widget_player_login.setLayout(self.layout_player_login)

        self.label_player_login = QLabel("Player's login: ")
        self.layout_player_login.addWidget(self.label_player_login)
        self.line_edit_player_login = QLineEdit()
        self.layout_player_login.addWidget(self.line_edit_player_login)

        self.button_send = QPushButton("SEND NEW PASSWORD")
        self.button_send.setMaximumWidth(125)
        self.layout_main.addWidget(self.button_send)

        self.button_send.clicked.connect(self._send_new_password)

        self.show()

    def _assign_password_to_player(self, player, password):
        bdd = read_bdd()
        bdd[player]["password"] = encode_password(password)
        write_bdd(bdd)

    def _send_new_password(self):
        player_login = self.line_edit_player_login.text()
        try:
            from_adress = "time.bomb.antho@gmail.com"
            to_adress = players_infos(player_login)["email"]

            email_to_send = MIMEMultipart()
            email_to_send['From'] = from_adress
            email_to_send['To'] = to_adress
            email_to_send['Subject'] = 'New Time Bomb Password'

            new_password = generate_random_password()
            self._assign_password_to_player(player_login, new_password)
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


class SettingsProfileUi(QWidget):
    def __init__(self, player_login):
        super(SettingsProfileUi, self).__init__()
        self.player_login = player_login
        self._init_ui()

    def _init_ui(self):
        self.resize(300, 100)
        self.setWindowTitle('Settings')

        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.widget_rename = QWidget()
        self.layout_main.addWidget(self.widget_rename)
        self.layout_rename = QHBoxLayout()
        self.widget_rename.setLayout(self.layout_rename)
        self.label_rename = QLabel('Login: ')
        self.layout_rename.addWidget(self.label_rename)
        self.line_edit_rename = QLineEdit()
        self.line_edit_rename.setPlaceholderText(self.player_login)
        self.layout_rename.addWidget(self.line_edit_rename)

        self.widget_current_password = QWidget()
        self.layout_main.addWidget(self.widget_current_password)
        self.layout_current_password = QHBoxLayout()
        self.widget_current_password.setLayout(self.layout_current_password)
        self.label_current_password = QLabel('Current Password: ')
        self.layout_current_password.addWidget(self.label_current_password)
        self.line_edit_current_password = QLineEdit()
        self.line_edit_current_password.setEchoMode(self.line_edit_current_password.Password)
        self.layout_current_password.addWidget(self.line_edit_current_password)

        self.widget_new_password = QWidget()
        self.layout_main.addWidget(self.widget_new_password)
        self.layout_new_password = QHBoxLayout()
        self.widget_new_password.setLayout(self.layout_new_password)
        self.label_new_password = QLabel('New Password: ')
        self.layout_new_password.addWidget(self.label_new_password)
        self.line_edit_new_password = QLineEdit()
        self.line_edit_new_password.setEchoMode(self.line_edit_new_password.Password)
        self.layout_new_password.addWidget(self.line_edit_new_password)

        self.widget_confirm_password = QWidget()
        self.layout_main.addWidget(self.widget_confirm_password)
        self.layout_confirm_password = QHBoxLayout()
        self.widget_confirm_password.setLayout(self.layout_confirm_password)
        self.label_confirm_password = QLabel('Confirm Password: ')
        self.layout_confirm_password.addWidget(self.label_confirm_password)
        self.line_edit_confirm_password = QLineEdit()
        self.line_edit_confirm_password.setEchoMode(self.line_edit_confirm_password.Password)
        self.layout_confirm_password.addWidget(self.line_edit_confirm_password)

        self.button_update = QPushButton('UPDATE')
        self.layout_main.addWidget(self.button_update)

        self.button_update.clicked.connect(self._update_profile)

        self.show()

        self.line_edit_rename.clearFocus()

    def _update_profile(self):
        new_login = self.line_edit_rename.text()
        current_password = self.line_edit_current_password.text()
        new_password = self.line_edit_new_password.text()
        confirm_password = self.line_edit_confirm_password.text()

        bdd = read_bdd()
        player_infos = bdd[self.player_login]

        if new_login != "":
            if not player_exist(new_login):
                del bdd[self.player_login]

                bdd[new_login] = player_infos
            else:
                message_box('', 'This login already exist.')

        if new_password != "":
            if encode_password(current_password) == player_infos["password"]:
                if new_password == confirm_password:
                    update_password = encode_password(new_password)

                    player_infos["password"] = update_password
                else:
                    message_box('', 'Both password are not the same.')
            else:
                message_box('', 'You have to complete your current password.')

        write_bdd(bdd)

        message_box('OK', 'Update Complete!')
        self.close()


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
        self.settings_profile_ui = SettingsProfileUi(self.player_login)

    def _create_game_ui(self):
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
        self.game_ui = GameUi(game_name)


class GameUi(QWidget):
    def __init__(self, game_name):
        super(GameUi, self).__init__()
        self.game_name = game_name
        self._init_ui()

    def _init_ui(self):
        self.resize(300, 150)
        self.setWindowTitle(self.game_name)

        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.group_self_infos = QGroupBox()
        self.layout_main.addWidget(self.group_self_infos)
        self.layout_self_infos = QHBoxLayout()
        self.group_self_infos.setLayout(self.layout_self_infos)

        self.label_self_team = QLabel('Your team: [......]')
        self.layout_self_infos.addWidget(self.label_self_team)

        self.label_self_deck = QLabel('Your deck: [......]')
        self.layout_self_infos.addWidget(self.label_self_deck)

        self.group_game_infos = QGroupBox()
        self.layout_main.addWidget(self.group_game_infos)
        self.layout_game_infos = QHBoxLayout()
        self.group_game_infos.setLayout(self.layout_game_infos)

        self.label_round_left = QLabel('Round left: [.]')
        self.layout_game_infos.addWidget(self.label_round_left)

        self.label_wire_count = QLabel('Wire found: [.]')
        self.layout_game_infos.addWidget(self.label_wire_count)

        self.label_current_player = QLabel('Current Player: [......]')
        self.layout_game_infos.addWidget(self.label_current_player)

        self.widget_tchat_ui = QWidget()
        self.layout_main.addWidget(self.widget_tchat_ui)
        self.layout_tchat_ui = QVBoxLayout()
        self.widget_tchat_ui.setLayout(self.layout_tchat_ui)

        self.line_edit_recv_messages = QLineEdit()
        self.line_edit_recv_messages.setReadOnly(True)
        self.layout_tchat_ui.addWidget(self.line_edit_recv_messages)

        self.line_edit_send_answers = QLineEdit()
        self.line_edit_send_answers.setEnabled(False)
        self.layout_tchat_ui.addWidget(self.line_edit_send_answers)

        self.show()


def generate_ui():
    app = QApplication(sys.argv)
    main_ui = ConnectionUi()
    sys.exit(app.exec_())


if __name__ == "__main__":
    generate_ui()
