from splendor_bot import game


# this is a manual gameplay test, where the player controls both sides via a CLI


def take_gems(game_state: game.GameState) -> game.GameState:
    gems = game.Gems(
        *[int(input(f"{gem}: ")) for gem in ["white", "blue", "green", "red", "black"]] + [0]
    )
    return game.take_gems(game_state, game_state.current_player_n, gems)


def reserve_card_from_deck(game_state: game.GameState) -> game.GameState:
    level = int(input("Level: "))
    return game.reserve_card_from_deck(game_state, game_state.current_player_n, level)


def reserve_card_from_board(game_state: game.GameState) -> game.GameState:
    level = int(input("Level: "))
    card_n = int(input("Card number: "))
    return game.reserve_card_from_board(game_state, game_state.current_player_n, level, card_n)


def purchase_card_from_board(game_state: game.GameState) -> game.GameState:
    level = int(input("Level: "))
    card_n = int(input("Card number: "))
    return game.purchase_card_from_board(game_state, game_state.current_player_n, level, card_n)


def purchase_reserved_card(game_state: game.GameState) -> game.GameState:
    card_n = int(input("Card number: "))
    return game.purchase_reserved_card(game_state, game_state.current_player_n, card_n)


def end_turn(game_state: game.GameState) -> game.GameState:
    current_player = game_state.players[game_state.current_player_n]
    gems_to_return = (
        game.Gems(0, 0, 0, 0, 0, 0)
        if len(current_player.gems) < 10
        else game.Gems(
            *[int(input(f"{gem}: ")) for gem in ["white", "blue", "green", "red", "black"]] + [0]
        )
    )
    return game.end_turn(game_state, gems_to_return)


actions = [
    take_gems,
    reserve_card_from_deck,
    reserve_card_from_board,
    purchase_card_from_board,
    purchase_reserved_card,
]


if __name__ == "__main__":
    game_state = game.new_game(n_players=2)
    action_list = ('\n').join([f'{i}: {action.__name__}' for i, action in enumerate(actions)])
    while not game_state.winners:
        action_n = int(input(f"{action_list}\nSelect an action: "))
        try:
            game_state = actions[action_n](game_state)
            game_state = end_turn(game_state)
        except Exception as e:
            print("ERROR:", e)
        print()
