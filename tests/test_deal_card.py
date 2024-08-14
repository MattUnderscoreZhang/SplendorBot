from splendor_bot.game import new_game, deal_card


def test_deal_card():
    game_state = new_game(n_players=2)
    assert [len(cards) for cards in game_state.revealed_cards_by_level] == [4, 4, 4]
    assert [len(cards) for cards in game_state.decks_by_level] == [36, 26, 16]

    game_state = deal_card(game_state, level=1)
    assert [len(cards) for cards in game_state.revealed_cards_by_level] == [5, 4, 4]
    assert [len(cards) for cards in game_state.decks_by_level] == [35, 26, 16]

    game_state = deal_card(game_state, level=2)
    assert [len(cards) for cards in game_state.revealed_cards_by_level] == [5, 5, 4]
    assert [len(cards) for cards in game_state.decks_by_level] == [35, 25, 16]

    game_state = deal_card(game_state, level=3)
    assert [len(cards) for cards in game_state.revealed_cards_by_level] == [5, 5, 5]
    assert [len(cards) for cards in game_state.decks_by_level] == [35, 25, 15]
