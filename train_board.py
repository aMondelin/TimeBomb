import os
import hashlib

mdp = hashlib.sha1(b'Antho')
mdp = mdp.hexdigest()

print mdp

print os.path.abspath("train_board.py")