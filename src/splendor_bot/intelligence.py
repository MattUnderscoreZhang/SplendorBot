from torch import nn, Tensor

from splendor_bot.types import Player


class NeuralNet(nn.Module):
    def __init__(self):
        # action selection
        self.fc1 = nn.Linear(1, 1)
        # action parameter selection

    def select_action(self, state: Tensor) -> Tensor:
        return self.forward(state)

    def forward(self, x: Tensor) -> Tensor:


class BotPlayer(Player):
    def __init__(self):
    def take_action(self, game_state: "GameState") -> "GameState":
        pass


"""
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
"""
