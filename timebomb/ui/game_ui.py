from PySide.QtGui import *


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
