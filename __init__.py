import random


GAME_FINISHED = "GAME_FINISHED"
TEAM_SHERLOCK = "TEAM_SHERLOCK"
TEAM_MORIARTY = "TEAM_MORIARTY"
CARD_BOMB = "CARD_BOMB"
CARD_NEUTRAL = "CARD_NEUTRAL"
CARD_DEFUSE = "CARD_DEFUSE"
PLAYER_COUNT_TO_SHERLOCK_REPARTITION = {4: 3, 5: 3, 6: 4, 7: 5, 8: 5}


class Player(object):
    def __init__(self, name):
        self.name = name
        self.cards = list()
        self.team = None


def init_deck(player_count):
    cards = list()

    defuse_count = player_count
    neutral_count = (player_count * 4) - 1

    cards += [CARD_BOMB]
    cards += [CARD_DEFUSE] * defuse_count
    cards += [CARD_NEUTRAL] * neutral_count

    random.shuffle(cards)

    return cards


def ask_for_player_name():
    name = raw_input("Entrez un nom de joueur :")
    new_player = Player(name)
    return new_player


def ask_for_player(player, players):
    player_names = list()
    for index, player_ in enumerate(players):
        player_names.append("{index} : {name}".format(index=index, name=player_.name))

    question = "{player}, choisissez un joueur parmi\n{players}\n:".format(
        player=player.name,
        players='\n'.join(player_names)
    )

    number = raw_input(question)

    try:
        number = int(number)
    except ValueError:
        print('Numero inccorrect !')
        return ask_for_player(player, players)

    if number not in range(len(players)):
        print('Numero inccorrect !')
        return ask_for_player(player, players)

    return players[number]


def ask_for_card(player, player_chosen):
    question = "{player}, choisissez une carte 0 - {max_card} parmi celles de {player_chosen}".format(
        player=player.name,
        max_card=len(player_chosen.cards) - 1,
        player_chosen=player_chosen.name
    )

    number = raw_input(question)

    try:
        number = int(number)
    except ValueError:
        print('Numero inccorrect !')
        return ask_for_card(player, player_chosen)

    if number not in range(len(player.cards)):
        print('Numero inccorrect !')
        return ask_for_card(player, player_chosen)

    return player.cards[number]


class Game(object):

    def __init__(self, player_count=4):
        self.player_count = min(max(4, player_count), 8)
        self.sherlock_count = PLAYER_COUNT_TO_SHERLOCK_REPARTITION[self.player_count]
        self.moriarty_count = self.player_count - self.sherlock_count
        self.deck = init_deck(self.player_count)
        self.deal_index = 0
        self.players = list()
        self.current_player_index = 0
        self.defuse_found_count = 0

    def _all_players_initialized(self):
        return len(self.players) == self.player_count

    def _sherlock_count(self):
        return len([player for player in self.players if player.team == TEAM_SHERLOCK])

    def _moriarty_count(self):
        return len([player for player in self.players if player.team == TEAM_MORIARTY])

    def _select_player_team(self):
        if self._sherlock_count() == self.sherlock_count:
            return TEAM_MORIARTY

        if self._moriarty_count() == self.moriarty_count:
            return TEAM_SHERLOCK

        return random.choice([TEAM_SHERLOCK, TEAM_MORIARTY])

    def _player_to_deal(self):
        for player in self.players:
            if not player.cards:
                return player

    def _all_players_dealt(self):
        return self._player_to_deal() is None

    def _deal_cards(self, player):
        for index_ in range(5):
            player.cards.append(self.deck[self.deal_index])
            self.deal_index += 1

    def _round_number(self):
        player_card_count = max([len(player.cards) for player in self.players])
        return 5 - player_card_count

    def _selectable_players(self, current_player):
        selectable_players = list()
        expected_card_count = 5 - self._round_number()

        for player_ in self.players:
            if player_ == current_player: continue
            if len(player_.cards) != expected_card_count: continue
            selectable_players.append(player_)

        return selectable_players

    def step(self):
        #
        # Init Players
        if not self._all_players_initialized():
            new_player = ask_for_player_name()
            new_player.team = self._select_player_team()
            self.players.append(new_player)
            # return
        print "ok"
        #
        # Deal Cards
        if not self._all_players_dealt():
            player_to_deal = self._player_to_deal()
            self._deal_cards(player_to_deal)
            return

        #
        # Rounds
        print("=" * 50)
        print("Tour numero {}".format(self._round_number()))

        player = self.players[self.current_player_index]
        players = self._selectable_players(player)
        player_chosen = ask_for_player(player, players)
        card_chosen = ask_for_card(player, player_chosen)
        player_chosen.cards.remove(card_chosen)

        self.current_player_index += 1
        if self.current_player_index >= self.player_count:
            self.current_player_index = 0

        if card_chosen == CARD_BOMB:
            print("La bombe explose !!")
            return GAME_FINISHED

        if card_chosen == CARD_NEUTRAL:
            print("Carte Neutre")
            return

        if card_chosen == CARD_DEFUSE:
            self.defuse_found_count += 1
            lasting_count = self.player_count - self.defuse_found_count

            if lasting_count == 0:
                print("La bombe est desamorcee !")
                return GAME_FINISHED
            else:
                print("Carte Defuse, plus que {} a trouver !".format(lasting_count))
                return


if __name__ == '__main__':
    game = Game()

    while True:
        status = game.step()
        if status == GAME_FINISHED:
            break

    print("La partie est finie !")
