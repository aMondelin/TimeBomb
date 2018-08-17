from PySide.QtGui import *
from timebomb.defs import ui_defs


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

        bdd = ui_defs.read_bdd()
        player_infos = bdd[self.player_login]

        if new_login != "":
            if not ui_defs.player_exist(new_login):
                del bdd[self.player_login]

                bdd[new_login] = player_infos
            else:
                ui_defs.message_box('', 'This login already exist.')

        if new_password != "":
            if ui_defs.encode_password(current_password) == player_infos["password"]:
                if new_password == confirm_password:
                    update_password = ui_defs.encode_password(new_password)

                    player_infos["password"] = update_password
                else:
                    ui_defs.message_box('', 'Both password are not the same.')
            else:
                ui_defs.message_box('', 'You have to complete your current password.')

                ui_defs.write_bdd(bdd)

                ui_defs.message_box('OK', 'Update Complete!')
