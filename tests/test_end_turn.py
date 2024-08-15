from pytest import raises

from splendor_bot.game import new_game, take_gems, move_to_next_player, end_turn
from splendor_bot.types import Gems


def test_move_to_next_player():
    game_state = new_game(n_players=2)
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
    game_state = new_game(n_players=2)
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
