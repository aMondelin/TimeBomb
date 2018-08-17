import smtplib
from PySide.QtGui import *
from email import MIMEMultipart
from email import MIMEText
from timebomb.defs import ui_defs


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
        bdd = ui_defs.read_bdd()
        bdd[player]["password"] = ui_defs.encode_password(password)
        ui_defs.write_bdd(bdd)

    def _send_new_password(self):
        player_login = self.line_edit_player_login.text()
        try:
            from_adress = "time.bomb.antho@gmail.com"
            to_adress = ui_defs.players_infos(player_login)["email"]

            email_to_send = MIMEMultipart()
            email_to_send['From'] = from_adress
            email_to_send['To'] = to_adress
            email_to_send['Subject'] = 'New Time Bomb Password'

            new_password = ui_defs.generate_random_password()
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

            ui_defs.message_box('OK', 'A new password has been send.')

            self.close()

        except KeyError:
            ui_defs.message_box('Wrong Login', 'This login doesn\'t exist.')
