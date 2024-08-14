from splendor_bot.game import new_game, move_to_next_player


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
