from pytest import raises

from splendor_bot.game import new_test_game, reserve_card_from_board, reserve_card_from_deck
from splendor_bot.types import Gems


def test_reserve_card_from_board():
    game_state = new_test_game(n_players=2)
    # invalid card
    with raises(Exception):
        reserve_card_from_board(game_state, player_n=0, level=3, card_n=0)
    # invalid card
    with raises(Exception):
        reserve_card_from_board(game_state, player_n=0, level=0, card_n=4)

    card = game_state.revealed_cards_by_level[0][0]
    game_state = reserve_card_from_board(game_state, player_n=0, level=0, card_n=0)
    assert len(game_state.players[0].reserved_cards) == 1
    assert game_state.players[0].reserved_cards[0] == card
    assert game_state.players[0].points == 0
    assert game_state.players[0].gems == Gems(0, 0, 0, 0, 0, 1)
    assert game_state.players[0].generation == Gems(0, 0, 0, 0, 0, 0)

    game_state = reserve_card_from_board(game_state, player_n=0, level=0, card_n=0)
    game_state = reserve_card_from_board(game_state, player_n=0, level=0, card_n=0)
    # can't reserve more than 3 cards
    with raises(Exception):
        reserve_card_from_board(game_state, player_n=0, level=0, card_n=0)


def test_reserve_card_from_deck():
    game_state = new_test_game(n_players=2)
    # invalid card
    with raises(Exception):
        reserve_card_from_deck(game_state, player_n=0, level=3)

    card = game_state.decks_by_level[0][-1]
    game_state = reserve_card_from_deck(game_state, player_n=0, level=0)
    assert len(game_state.players[0].reserved_cards) == 1
    assert game_state.players[0].reserved_cards[0] == card
    assert game_state.players[0].points == 0
    assert game_state.players[0].gems == Gems(0, 0, 0, 0, 0, 1)
    assert game_state.players[0].generation == Gems(0, 0, 0, 0, 0, 0)

    game_state = reserve_card_from_deck(game_state, player_n=0, level=0)
    game_state = reserve_card_from_deck(game_state, player_n=0, level=0)
    # can't reserve more than 3 cards
    with raises(Exception):
        reserve_card_from_deck(game_state, player_n=0, level=0)
