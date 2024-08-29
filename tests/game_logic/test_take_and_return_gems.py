from pytest import raises

from splendor_bot.game_logic.game import new_test_game, take_gems, return_gems
from splendor_bot.game_logic.types import Gems


def test_bad_takes():
    game_state = new_test_game(n_players=2)
    # negative gems
    with raises(Exception):
        take_gems(game_state, player_n=0, gems=Gems(-1, 0, 0, 0, 0, 0))
    # colored + gold
    with raises(Exception):
        take_gems(game_state, player_n=0, gems=Gems(1, 1, 0, 0, 0, 1))
    # too many colors
    with raises(Exception):
        take_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 1, 1, 0))
    # too many of one color
    with raises(Exception):
        take_gems(game_state, player_n=0, gems=Gems(0, 3, 0, 0, 0, 0))
    # invalid distribution
    with raises(Exception):
        take_gems(game_state, player_n=0, gems=Gems(1, 2, 0, 0, 0, 0))


def test_not_enough_gems_to_return():
    game_state = new_test_game(n_players=2)
    with raises(Exception):
        return_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 1, 1, 0))


def test_take_gold():
    game_state = new_test_game(n_players=2)
    game_state = take_gems(game_state, player_n=0, gems=Gems(0, 0, 0, 0, 0, 1))
    assert game_state.players[0].gems == Gems(0, 0, 0, 0, 0, 1)


def test_take_three_gems_different_color():
    game_state = new_test_game(n_players=2)
    game_state = take_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 0, 0, 0))
    assert game_state.players[0].gems == Gems(1, 1, 1, 0, 0, 0)


def test_take_two_gems_same_color():
    game_state = new_test_game(n_players=2)
    game_state = take_gems(game_state, player_n=0, gems=Gems(0, 0, 2, 0, 0, 0))
    assert game_state.players[0].gems == Gems(0, 0, 2, 0, 0, 0)


def test_return_gems():
    game_state = new_test_game(n_players=2)
    game_state = take_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 0, 0, 0))
    game_state = return_gems(game_state, player_n=0, gems=Gems(1, 0, 0, 0, 0, 0))
    game_state = return_gems(game_state, player_n=0, gems=Gems(0, 1, 0, 0, 0, 0))
    game_state = return_gems(game_state, player_n=0, gems=Gems(0, 0, 1, 0, 0, 0))
    assert game_state.players[0].gems == Gems(0, 0, 0, 0, 0, 0)
    assert game_state.gem_pool == Gems(4, 4, 4, 4, 4, 5)
    game_state.check_consistency()


def test_take_fewer_gems_different_colors():
    game_state = new_test_game(n_players=2)
    for _ in range(4):
        game_state = take_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 0, 0, 0))
    assert game_state.players[0].gems == Gems(4, 4, 4, 0, 0, 0)
    assert game_state.gem_pool == Gems(0, 0, 0, 4, 4, 5)
    with raises(Exception):
        take_gems(game_state, player_n=0, gems=Gems(0, 0, 0, 0, 1, 0))
    game_state = take_gems(game_state, player_n=0, gems=Gems(0, 0, 0, 1, 1, 0))
    assert game_state.players[0].gems == Gems(4, 4, 4, 1, 1, 0)
    assert game_state.gem_pool == Gems(0, 0, 0, 3, 3, 5)


def test_take_one_gem():
    game_state = new_test_game(n_players=2)
    for _ in range(4):
        game_state = take_gems(game_state, player_n=0, gems=Gems(1, 1, 1, 0, 0, 0))
    game_state = return_gems(game_state, player_n=0, gems=Gems(0, 0, 4, 0, 0, 0))
    for _ in range(4):
        game_state = take_gems(game_state, player_n=0, gems=Gems(0, 0, 1, 1, 1, 0))
    game_state = return_gems(game_state, player_n=0, gems=Gems(0, 0, 1, 0, 0, 0))
    assert game_state.players[0].gems == Gems(4, 4, 3, 4, 4, 0)
    assert game_state.gem_pool == Gems(0, 0, 1, 0, 0, 5)
    game_state = take_gems(game_state, player_n=0, gems=Gems(0, 0, 1, 0, 0, 0))
