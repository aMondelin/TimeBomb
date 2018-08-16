import random

PLAYER_COUNT = 0

# ROUND COUNTS
ROUND_COUNT = 0
PLAYER_MOVES = 0

# TYPES/CARDS VALUES
PLAYER_BAD = 0
PLAYER_GOOD = 1
CARD_NEUTRAL = 0
CARD_GOOD = 1
CARD_BOMB = 2

# GAME INFOS
DEFAULT_TEAMS = {4: [3, 1], 5: [3, 2], 6: [4, 2], 7: [5, 3], 8: [5, 3]}
GOOD_PLAYERS = []
CURRENT_PLAYERS = {}
DECK_CARDS = [CARD_BOMB]

# ask_player_count = input("Combien de joueurs? (4 a 8 joueurs):")
#
# if ask_player_count < 4 or ask_player_count > 8:
#     wrong_count = True
#
#     while wrong_count:
#         ask_player_count = input("Le nombre de joueurs est incorrect. Reessayez (4 a 8 joueurs):")
#
#         if 3 < ask_player_count < 9 :
#             wrong_count = False

# PLAYER COUNT
def define_player_count():
    global PLAYER_COUNT

    wrong_count = True

    while wrong_count:
        ask_player_count = input("Combien de joueurs? (4 a 8 joueurs):")

        if ask_player_count < 4 or ask_player_count > 8:
            print "Le nombre de joueurs est incorrect."
        if 3 < ask_player_count < 9 :
            wrong_count = False

        PLAYER_COUNT = ask_player_count


# PREPARE SIDES ARRAY
def players_side():
    global  GOOD_PLAYERS

    good_players_count = DEFAULT_TEAMS.get(PLAYER_COUNT)[0]
    GOOD_PLAYERS = random.sample(range(PLAYER_COUNT), good_players_count)


# UPDATE DECK_CARDS
def append_cards(nb_cards, card_value):
    global DECK_CARDS

    for card in range(0,nb_cards):
        DECK_CARDS.append(card_value)


# INIT DECK CARDS
def init_deck(nb_players):
    nb_good_card = nb_players
    nb_neutral_card = (nb_players*4) - 1

    append_cards(nb_good_card, CARD_GOOD)
    append_cards(nb_neutral_card, CARD_NEUTRAL)


# CARD DISTRIBUTION
def card_distribution():
    for card in range(0, 5):
        for player in range(0, len(CURRENT_PLAYERS)):
            random_number = random.randint(0, len(DECK_CARDS)-1)
            random_card = DECK_CARDS[random_number]
            del DECK_CARDS[random_number]

            player_infos = CURRENT_PLAYERS.get(player)
            player_infos[1].append(random_card)

            CURRENT_PLAYERS[player] = player_infos


# ASSIGN PLAYER' SIDE AND CARDS
def create_players():
    for player in range(0, PLAYER_COUNT):
        player_side = PLAYER_BAD
        if player in GOOD_PLAYERS:
            player_side = PLAYER_GOOD
        CURRENT_PLAYERS[player] = [player_side, []]

define_player_count()
players_side()
init_deck(PLAYER_COUNT)
create_players()
card_distribution()

print CURRENT_PLAYERS


def players_hand(player):
    player_item = CURRENT_PLAYERS.get(player)
    player_cards = player_item[1]

    print ("Player {} have {} cards.".format(player, len(player_cards)))


party_core = "active"

while party_core == "active":
    # 1ST PLAYER
    first_player = random.randint(0, PLAYER_COUNT)
    print ("Player {} is the first player.".format(first_player))

    # Main rounds (4 max)
    for big_round in range(0, 4):
        # Rounds per players (player's count)
        for small_round in range(0, PLAYER_COUNT):
            # Hands' Players' Infos
            for player in range(0, PLAYER_COUNT):
                players_hand(player)

            player_choice = input("Select player's name:")

            party_core = "inactive"

if party_core == "bomb_exploded":
    print ("The bomb exploded, Sherlock's team lose the game.")
elif party_core == "time_spent":
    print ("Time spent. The bomb exploded, Sherlock's team lose the game.")
elif party_core == "active":
    print ("Sherlock's team defused the bomb, Moriarty's team lose the game.")

# retry_answer = input("Retry? y/n:")
