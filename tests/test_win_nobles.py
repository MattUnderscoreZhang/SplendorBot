from splendor_bot.base_deck import nobles
from splendor_bot.game import new_test_game, win_nobles
from splendor_bot.types import Gems


def test_win_nobles():
    # alter game state to have all nobles and give player lots of gem generation
    game_state = new_test_game(n_players=2)
    game_state.nobles = nobles
    game_state.players[0].generation = Gems(0, 0, 4, 4, 4, 0)

    # check that player wins three nobles and gets points for them
    game_state = win_nobles(game_state, player_n=0)
    assert len(game_state.nobles)  == 7
    assert len(game_state.players[0].nobles) == 3
    assert game_state.players[0].points == 9
    for noble in game_state.players[0].nobles:
        assert list(noble.requirements.__dict__.values()) in [
            [0, 0, 4, 4, 0, 0],
            [0, 0, 0, 4, 4, 0],
            [0, 0, 3, 3, 3, 0],
        ]
