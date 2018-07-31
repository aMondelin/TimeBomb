import random
import socket
import select


GAME_SERVER = 0
GAME_FINISHED = "GAME_FINISHED"
TEAM_SHERLOCK = "TEAM_SHERLOCK"
TEAM_MORIARTY = "TEAM_MORIARTY"
CARD_BOMB = "CARD_BOMB"
CARD_NEUTRAL = "CARD_NEUTRAL"
CARD_DEFUSE = "CARD_DEFUSE"
DEFAULT_TEAMS = {4: [3, 1], 5: [3, 2], 6: [4, 2], 7: [5, 3], 8: [5, 3]}


class Player(object):
    def __init__(self, name):
        self.name = name
        self.cards = list()
        self.team = None


def init_deck(player_count):
    deck_cards = list()

    defuse_count = player_count
    neutral_count = (player_count * 4) - 1

    deck_cards += [CARD_BOMB]
    deck_cards += [CARD_DEFUSE] * defuse_count
    deck_cards += [CARD_NEUTRAL] * neutral_count

    random.shuffle(deck_cards)

    return deck_cards


def init_player_sides(player_count):
    player_sides = list()

    good_count = DEFAULT_TEAMS.get(player_count)[0]
    bad_count = DEFAULT_TEAMS.get(player_count)[1]

    player_sides += [TEAM_SHERLOCK] * good_count
    player_sides += [TEAM_MORIARTY] * bad_count

    random.shuffle(player_sides)

    return player_sides


def ask_player_count():
    ask_player_count = 0

    wrong_count = True
    while wrong_count:
        ask_player_count = input("Combien de joueurs? (4 a 8 joueurs):")

        if ask_player_count < 4 or ask_player_count > 8:
            print "Le nombre de joueurs est incorrect."
        if 3 < ask_player_count < 9 :
            wrong_count = False

    return ask_player_count


def ask_player_name():
    player_name = raw_input("Enter player's name:")
    new_player = Player(player_name)
    return new_player


def ask_for_player(player, players):
    player_names = list()
    for index, current_player in enumerate(players):
        player_names.append("{index} : {name}".format(index= index, name=current_player.name))

    question = "{player}, choisissez un joueur parmi\n{player_list}\n:".format(
        player = player.name,
        player_list = "\n".join(player_names)
    )

    player.send(question)
    number = player.recv(1024)
    number = number.decode()

    try:
        number = int(number)
    except ValueError:
        print("Mauvais numero!")
        return ask_for_player(player, players)

    if number not in range(len(players)):
        print("Mauvais numero!")
        return ask_for_player(player, players)

    return players[number]


def print_all_players(players):
    for player in players:
        print "    {current_player} a {nb_cards} dont {deck_card}\n".format(
            current_player = player.name,
            nb_cards = len(player.cards),
            deck_card = player.cards
        )


def ask_for_card(current_player, player_chosen):
    question = "{current_player}, choisissez une carte 0 a {max_cards} parmi celles de {player_chosen}\n:".format(
        current_player = current_player.name,
        max_cards = len(player_chosen.cards) - 1,
        player_chosen = player_chosen.name
    )

    number = raw_input(question)

    try:
        number = int(number)
    except ValueError:
        print("Mauvais numero!")
        return ask_for_card(current_player, player_chosen)

    if number not in range(len(player_chosen.cards)):
        print("Mauvais numero!")
        return ask_for_card(current_player, player_chosen)

    return player_chosen.cards[number]


class Game(object):

    def __init__(self):
        self.player_count = ask_player_count()
        self.players = list()
        self.player_sides = init_player_sides(self.player_count)
        self.deck = init_deck(self.player_count)
        self.round_index = 0
        self.defuse_found_count = 0
        self.current_player_index = random.randint(0, self.player_count)

    def _launch_server(self):
        global GAME_SERVER

        game_ip = ''
        game_port = 5060

        GAME_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        GAME_SERVER.bind((game_ip, game_port))
        GAME_SERVER.listen(5)

    def _all_players_initialized(self):
        return len(self.players) == self.player_count

    def _player_side(self):
        random_int = random.randint(0, len(self.player_sides) - 1)
        player_side = self.player_sides[random_int]
        del self.player_sides[random_int]

        return player_side

    def _card_to_give(self):
        random_int = random.randint(0, len(self.deck) - 1)
        card_to_deal = self.deck[random_int]
        del self.deck[random_int]

        return card_to_deal

    def _check_round(self):
        return self.round_index%self.player_count

    def _cards_in_deck(self):
        return len(self.deck)

    def _number_cards_to_deal(self):
        return self._cards_in_deck()/self.player_count

    def _get_back_deck_cards(self):
        for player in self.players:
            self.deck += player.cards

    def _reset_player_cards(self):
        for player in self.players:
            # del player.cards[:]
            player.cards[:] = []

    def _deal_cards(self):
        if not self._cards_in_deck():
            self._get_back_deck_cards()

        self._reset_player_cards()

        number_cards = self._number_cards_to_deal()
        for player in self.players:
            for card in range(number_cards):
                player.cards.append(self._card_to_give())

    def _selectable_players(self, current_player):
        selectable_players = list()

        for player in self.players:
            if player == current_player: continue
            if not len(player.cards): continue
            selectable_players.append(player)

        return selectable_players

    def step(self):
        # Init Players
        if not self._all_players_initialized():
            new_player = ask_player_name()
            new_player.team = self._player_side()
            self.players.append(new_player)
            return

        # Deal Cards
        check_round_number = self._check_round()
        if self.round_index == 0 or check_round_number == 0:
            self._deal_cards()

        print_all_players(self.players)

        current_player = self.players[self.current_player_index]
        other_players = self._selectable_players(current_player)
        player_chosen = ask_for_player(current_player, other_players)
        card_chosen = ask_for_card(current_player, player_chosen)
        player_chosen.cards.remove(card_chosen)

        self.current_player_index = self.players.index(player_chosen)
        self.round_index += 1

        # if self.round_index == 5:
        #     return GAME_FINISHED

        if self.round_index == self.player_count * 4:
            print "Vous n'avez pas pu desamorcer la bombe a temps. L'equipe de Moriarty gagne la partie!\n"
            return GAME_FINISHED

        if card_chosen == CARD_NEUTRAL:
            print "Vous avez retourne une carte neutre.\n"
            return

        if card_chosen == CARD_DEFUSE:
            self.defuse_found_count += 1
            defuse_to_found = self.player_count - self.defuse_found_count

            if defuse_to_found == 0:
                print "La bombe a ete desamorcee. L'equipe de Sherlock gagne la partie!\n"
                return GAME_FINISHED
            else:
                print "Vous avez retourne une carte defuse. Il ne vous en reste plus que {}\n".format(defuse_to_found)
                return

        if card_chosen == CARD_BOMB:
            print "Vous avez retourne la bombe. L'equipe de Moriarty gagne la partie!\n"
            return GAME_FINISHED


if __name__ == '__main__':
    game = Game()

    game._launch_server()

    players_online = []
    server_launched = True
    while server_launched:
        asked_connections, wlist, xlist = select.select([GAME_SERVER], [], [], 0.05)

        for connection in asked_connections:
            new_player, player_infos = connection.accept()
            players_online.append(new_player)
            new_player.send(b"Vous etes connecte au serveur. Bonne partie!")

        # --
        player_to_read = []
        try:
            player_to_read, wlist, xlist = select.select(players_online, [], [], 0.05)
        except select.error:
            pass
        else:
            for player in player_to_read:
                received_msg = player.recv(1024)
                received_msg = received_msg.decode()
                print players_online
                print(received_msg)
                player.send(b"5/5")

                if received_msg == "fin":
                    server_launched = False

        if len(players_online) == game.player_count:
            game_state = game.step()
            if game_state == GAME_FINISHED:
                break sur

    print("The game is done!")

    question = "Wanna retry? y/n"
    answer = raw_input(question)

    for new_player in players_online:
        new_player.close()
    GAME_SERVER.close()
