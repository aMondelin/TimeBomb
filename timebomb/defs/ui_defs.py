import os
import json
import random
import hashlib
from PySide.QtGui import *


def bdd_path():
    current_path = os.getcwd()
    bdd_player_path = os.path.join(os.path.dirname(current_path), "bdd_players.json")

    return bdd_player_path


def read_bdd():
    bdd_player_path = bdd_path()

    with open(bdd_player_path, 'r') as f_json:
        bdd_file = json.load(f_json)

    return bdd_file


def write_bdd(new_bdd):
    bdd_player_path = bdd_path()

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
