from pytest import raises

from splendor_bot.game import new_test_game, take_gems, move_to_next_player, end_turn
from splendor_bot.types import Gems


def test_move_to_next_player():
    game_state = new_test_game(n_players=2)
    first_player = game_state.first_player_n
    assert game_state.current_player_n == first_player
    assert game_state.round == 1

    game_state = move_to_next_player(game_state)
    assert game_state.current_player_n == (0 if first_player == 1 else 1)
    assert game_state.round == 1

    game_state = move_to_next_player(game_state)
    assert game_state.current_player_n == first_player
    assert game_state.round == 2


def test_end_turn():
    game_state = new_test_game(n_players=2)
    player_n = game_state.current_player_n
    for _ in range(3):
        game_state = take_gems(game_state, player_n, Gems(1, 1, 1, 0, 0, 0))
    # unnecessary gem return
    with raises(Exception):
        end_turn(game_state, Gems(1, 0, 0, 0, 0, 0))

    game_state = take_gems(game_state, player_n, Gems(1, 1, 1, 0, 0, 0))
    # wrong number of gems returned
    with raises(Exception):
        end_turn(game_state, Gems(1, 0, 0, 0, 0, 0))

    # correct gem return
    game_state = end_turn(game_state, Gems(1, 1, 0, 0, 0, 0))
    assert game_state.players[player_n].gems == Gems(3, 3, 4, 0, 0, 0)
    assert game_state.gem_pool == Gems(1, 1, 0, 4, 4, 5)
    assert game_state.current_player_n == (0 if player_n == 1 else 1)
    game_state.check_consistency()


def test_end_game():
    # trigger last round
    game_state = new_test_game(n_players=3)
    first_player = game_state.players[game_state.current_player_n]
    first_player.points = 15
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert game_state.current_player_n == (game_state.first_player_n + 1) % 3
    assert game_state.last_round
    assert game_state.winners == []

    # last round continues
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert game_state.current_player_n == (game_state.first_player_n + 2) % 3
    assert game_state.winners == []

    # game ends after last round with first player as winner
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert game_state.current_player_n == (game_state.first_player_n + 2) % 3
    assert game_state.winners == [first_player]

    # further continuation does nothing
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert game_state.current_player_n == (game_state.first_player_n + 2) % 3
    assert game_state.winners == [first_player]


def test_score_winner():
    # normal winner
    game_state = new_test_game(n_players=2)
    first_player = game_state.players[game_state.current_player_n]
    first_player.points = 15
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert game_state.winners == [first_player]

    # tiebreaker winner
    game_state = new_test_game(n_players=2)
    first_player = game_state.players[game_state.current_player_n]
    first_player.points = 15
    first_player.purchased_cards = [
        game_state.decks_by_level[0][0],
        game_state.decks_by_level[0][1],
    ]
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert game_state.winners == []
    second_player = game_state.players[(game_state.current_player_n) % 2]
    second_player.points = 15
    second_player.purchased_cards = [
        game_state.decks_by_level[1][0],
    ]
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert game_state.winners == [second_player]

    # tie
    game_state = new_test_game(n_players=2)
    first_player = game_state.players[game_state.current_player_n]
    first_player.points = 15
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    second_player = game_state.players[(game_state.current_player_n) % 2]
    second_player.points = 15
    game_state = end_turn(game_state, Gems(0, 0, 0, 0, 0, 0))
    assert len(game_state.winners) == 2
    assert first_player in game_state.winners
    assert second_player in game_state.winners
