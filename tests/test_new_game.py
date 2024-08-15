from pytest import raises

from splendor_bot.game import new_game


def test_n_players():
    for n_players in [1, 5]:
        with raises(Exception):
            new_game(n_players=n_players)


def test_game_consistency():
    for n_players in [2, 3, 4]:
        game_state = new_game(n_players=n_players)
        game_state.check_consistency()


def test_cards_dealt():
    for n_players in [2, 3, 4]:
        game_state = new_game(n_players=n_players)
        assert [len(cards) for cards in game_state.revealed_cards_by_level] == [4, 4, 4]
