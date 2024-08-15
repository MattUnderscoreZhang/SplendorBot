from copy import deepcopy
import random

from splendor_bot.base_deck import decks_by_level, nobles
from splendor_bot.types import Gems, GameState, Player, Card


def new_game(n_players: int) -> GameState:
    # changes for number of players
    assert 2 <= n_players <= 4, "Only 2-4 players are supported."
    n_gems = (
        4 if n_players == 2 else
        5 if n_players == 3 else
        7
    )
    gem_pool = Gems(n_gems, n_gems, n_gems, n_gems, n_gems, 5)
    revealed_nobles = random.sample(nobles, n_players+1)
    first_player_n = random.randint(0, n_players-1)
    # deal cards
    decks_by_level_after_deal = [
        random.sample(deck, len(deck))
        for deck in decks_by_level
    ]
    revealed_cards_by_level = [
        [decks_by_level_after_deal[level].pop() for _ in range(4)]
        for level in range(3)
    ]
    # set up game
    return GameState(
        players=[Player() for _ in range(n_players)],
        decks_by_level=decks_by_level_after_deal,
        revealed_cards_by_level=revealed_cards_by_level,
        nobles=revealed_nobles,
        gem_pool=gem_pool,
        first_player_n=first_player_n,
        current_player_n=first_player_n,
        round=1,
        last_round=False,
        winner=None,
    )


def deal_card(game_state: GameState, level: int) -> GameState:
    game_state = deepcopy(game_state)
    # TODO: take no action if deck is empty
    card = game_state.decks_by_level[level-1].pop()
    game_state.revealed_cards_by_level[level-1].append(card)
    return game_state


def move_to_next_player(game_state: GameState) -> GameState:
    game_state = deepcopy(game_state)
    game_state.current_player_n = (game_state.current_player_n + 1) % len(game_state.players)
    if game_state.current_player_n == game_state.first_player_n:
        game_state.round += 1
    return game_state


def return_gems(game_state: GameState, player_n: int, gems: Gems) -> GameState:
    game_state = deepcopy(game_state)
    player = game_state.players[player_n]
    assert gems <= player.gems, \
        f"Not enough gems. Tried to return {gems}, but player has {player.gems}."
    player.gems -= gems
    game_state.gem_pool += gems
    return game_state


def win_nobles(game_state: GameState, player_n: int) -> GameState:
    game_state = deepcopy(game_state)
    player = game_state.players[player_n]
    for noble in reversed(game_state.nobles):
        if player.generation >= noble.requirements:
            player.nobles.append(noble)
            game_state.nobles.remove(noble)
            player.points += noble.points
    return game_state


def end_turn(game_state: GameState, gems_to_return: Gems) -> GameState:
    game_state = deepcopy(game_state)
    if len(game_state.players[game_state.current_player_n].gems) > 10:
        game_state = return_gems(game_state, game_state.current_player_n, gems_to_return)
        assert len(game_state.players[game_state.current_player_n].gems) == 10, \
            "Returned the wrong number of gems."
    else:
        assert len(gems_to_return) == 0, "Unnecessary gem return."
    game_state = win_nobles(game_state, game_state.current_player_n)
    # TODO: check last round
    # TODO: check end game
    # TODO: if game over, score winner, else move to next player
    game_state = move_to_next_player(game_state)
    return game_state


def take_gems(game_state: GameState, player_n: int, gems: Gems) -> GameState:
    game_state = deepcopy(game_state)
    # validate that gems are takable
    assert gems > Gems(0, 0, 0, 0, 0, 0), "Must take at least one gem."
    assert gems <= game_state.gem_pool, f"Not enough gems. Tried to take {gems}, but gem pool is {game_state.gem_pool}."
    # can only take one yellow by itself (when reserving a card)
    if gems.yellow != 0:
        assert gems == Gems(0, 0, 0, 0, 0, 1), f"Can only take one yellow by itself. Tried to take {gems}."
    # rules for normal gem taking
    else:
        # counting non-yellow colors
        n_colors_in_pool = sum([val > 0 and key != "yellow" for key, val in game_state.gem_pool.__dict__.items()])
        taking_n_colors = sum(val > 0 and key != "yellow" for key, val in gems.__dict__.items())
        # if taking one color
        if taking_n_colors == 1:
            gem_color = [key for key, val in gems.__dict__.items() if val > 0][0]
            # (disputed rule) can take just 1 gem if there's less than 4 of that color
            if len(gems) == 1:
                assert n_colors_in_pool == 1 and game_state.gem_pool.__dict__[gem_color] < 4, \
                    f"Invalid selection. Tried to take {gems}, when gem pool is {game_state.gem_pool}."
            # can only take 2 gems of a color if there are 4 or more of that color
            else:
                assert len(gems) == 2, f"Can only take 2 gems of one color. Tried to take {gems}."
                assert game_state.gem_pool.__dict__[gem_color] >= 4, \
                    f"Invalid selection. Tried to take {gems} from {game_state.gem_pool}."
        # if taking different colors
        else:
            # (disputed rule) can take less than 3 gems if there aren't at least 3 colors
            assert len(gems) == taking_n_colors == min(n_colors_in_pool, 3), \
                f"Must take (up to) 3 gems of different colors. Tried to take {gems}."
    # take gems
    game_state.players[player_n].gems += gems
    game_state.gem_pool -= gems
    return game_state


def purchase_card(game_state: GameState, player_n: int, card: Card) -> GameState:
    game_state = deepcopy(game_state)
    player = game_state.players[player_n]
    # TODO: allow use of yellow gems
    assert card.cost <= player.gems, \
        f"Not enough gems. Tried to pay {card.cost}, but player has {player.gems}."
    player.gems -= card.cost
    player.generation += card.generation
    player.purchased_cards.append(card)
    player.points += card.points
    return game_state


def purchase_card_from_board(game_state: GameState, player_n: int, level: int, card_n: int) -> GameState:
    game_state = deepcopy(game_state)
    assert 1 <= level <= 3, f"Invalid level {level}."
    assert 0 <= card_n < len(game_state.revealed_cards_by_level[level-1]), f"Invalid card number {card_n}."
    card = game_state.revealed_cards_by_level[level-1].pop(card_n)
    game_state = purchase_card(game_state, player_n, card)
    game_state = deal_card(game_state, level)
    return game_state


def reserve_card(game_state: GameState, player_n: int, level: int, card_n: int) -> GameState:
    game_state = deepcopy(game_state)
    assert 1 <= level <= 3, f"Invalid level {level}."
    assert 0 <= card_n < len(game_state.revealed_cards_by_level[level-1]), f"Invalid card number {card_n}."
    assert len(game_state.players[player_n].reserved_cards) < 3, "Can't reserve more than 3 cards."
    card = game_state.revealed_cards_by_level[level-1].pop(card_n)
    game_state.players[player_n].reserved_cards.append(card)
    game_state = deal_card(game_state, level)
    # if there's no yellow gems left, don't do anything
    if game_state.gem_pool.yellow > 0:
        game_state = take_gems(game_state, player_n, Gems(0, 0, 0, 0, 0, 1))
    return game_state


def purchase_reserved_card(game_state: GameState, player_n: int, card_n: int) -> GameState:
    game_state = deepcopy(game_state)
    player = game_state.players[player_n]
    assert 0 <= card_n < len(player.reserved_cards), f"Invalid card number {card_n}."
    card = player.reserved_cards.pop(card_n)
    game_state = purchase_card(game_state, player_n, card)
    return game_state
