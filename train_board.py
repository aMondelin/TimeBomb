import hashlib

mdp = hashlib.sha1(b'Antho')
mdp = mdp.hexdigest()

print mdp