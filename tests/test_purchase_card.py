from pytest import raises

from splendor_bot.game import (
    new_game,
    take_gems,
    purchase_card,
    purchase_card_from_board,
    reserve_card_from_board,
    purchase_reserved_card,
)
from splendor_bot.types import Card, Gems


def test_purchase_card():
    game_state = new_game(n_players=2)
    # not enough gems
    with raises(Exception):
        purchase_card(
            game_state,
            player_n=0,
            card=Card(
                level=1,
                points=1,
                generation=Gems(1, 0, 0, 0, 0, 0),
                cost=Gems(1, 0, 0, 0, 0, 0),
            ),
        )

    # purchase first card
    game_state = take_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 0, 0, 0))
    game_state = purchase_card(
        game_state,
        player_n=0,
        card=Card(
            level=1,
            points=1,
            generation=Gems(1, 0, 0, 0, 0, 0),
            cost=Gems(1, 0, 0, 0, 0, 0),
        ),
    )
    assert game_state.players[0].gems == Gems(0, 1, 1, 0, 0, 0)
    assert len(game_state.players[0].purchased_cards) == 1
    assert game_state.players[0].points == 1
    assert game_state.players[0].generation == Gems(1, 0, 0, 0, 0, 0)

    # purchase second card using gem generation
    game_state = take_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 0, 0, 0))
    assert game_state.players[0].gems == Gems(1, 2, 2, 0, 0, 0)
    game_state = purchase_card(
        game_state,
        player_n=0,
        card=Card(
            level=2,
            points=2,
            generation=Gems(0, 0, 0, 2, 0, 0),
            cost=Gems(2, 2, 2, 0, 0, 0),
        ),
    )
    assert game_state.players[0].gems == Gems(0, 0, 0, 0, 0, 0)
    assert len(game_state.players[0].purchased_cards) == 2
    assert game_state.players[0].points == 3
    assert game_state.players[0].generation == Gems(1, 0, 0, 2, 0, 0)

    # purchase with gold
    game_state = take_gems(game_state, player_n=0, gems=Gems(0, 0, 0, 0, 0, 1))
    game_state = purchase_card(
        game_state,
        player_n=0,
        card=Card(
            level=1,
            points=1,
            generation=Gems(0, 0, 0, 0, 1, 0),
            cost=Gems(1, 0, 0, 3, 0, 0),
        ),
    )
    assert game_state.players[0].gems == Gems(0, 0, 0, 0, 0, 0)
    assert len(game_state.players[0].purchased_cards) == 3
    assert game_state.players[0].points == 4
    assert game_state.players[0].generation == Gems(1, 0, 0, 2, 1, 0)


def test_purchase_card_from_board():
    game_state = new_game(n_players=2)
    # not enough gems
    with raises(Exception):
        purchase_card_from_board(game_state, player_n=0, level=1, card_n=0)
    # invalid card
    with raises(Exception):
        purchase_card_from_board(game_state, player_n=0, level=4, card_n=0)
    # invalid card
    with raises(Exception):
        purchase_card_from_board(game_state, player_n=0, level=1, card_n=4)

    game_state.players[0].gems = Gems(4, 4, 4, 4, 4, 0)
    card = game_state.revealed_cards_by_level[0][0]
    game_state = purchase_card_from_board(game_state, player_n=0, level=1, card_n=0)
    assert len(game_state.players[0].purchased_cards) == 1
    assert game_state.players[0].points == card.points
    assert game_state.players[0].gems == Gems(4, 4, 4, 4, 4, 0) - card.cost
    assert game_state.players[0].generation == card.generation


def test_purchase_reserved_card():
    game_state = new_game(n_players=2)
    game_state = reserve_card_from_board(game_state, player_n=0, level=1, card_n=0)
    # invalid card
    with raises(Exception):
        purchase_reserved_card(game_state, player_n=0, card_n=1)

    game_state.players[0].gems = Gems(4, 4, 4, 4, 4, 0)
    card = game_state.players[0].reserved_cards[0]
    game_state = purchase_reserved_card(game_state, player_n=0, card_n=0)
    assert len(game_state.players[0].reserved_cards) == 0
    assert len(game_state.players[0].purchased_cards) == 1
    assert game_state.players[0].points == card.points
    assert game_state.players[0].gems == Gems(4, 4, 4, 4, 4, 0) - card.cost
    assert game_state.players[0].generation == card.generation
