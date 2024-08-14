import random

from splendor_bot.base_deck import decks_by_level, nobles
from splendor_bot.types import Gems, GameState, Player


def new_game(n_players: int) -> GameState:
    # changes for number of players
    assert 2 <= n_players <= 4, "Only 2-4 players are supported."
    n_gems = (
        4 if n_players == 2 else
        5 if n_players == 3 else
        7
    )
    gem_pool = Gems(n_gems, n_gems, n_gems, n_gems, n_gems, 5)
    revealed_nobles = random.sample(nobles, n_players+1)
    first_player_n = random.randint(0, n_players-1)
    # deal cards
    decks_by_level_after_deal = [
        random.sample(deck, len(deck))
        for deck in decks_by_level
    ]
    revealed_cards_by_level = [
        [decks_by_level_after_deal[level].pop() for _ in range(4)]
        for level in range(3)
    ]
    # set up game
    return GameState(
        players=[Player() for _ in range(n_players)],
        decks_by_level=decks_by_level_after_deal,
        revealed_cards_by_level=revealed_cards_by_level,
        nobles=revealed_nobles,
        gem_pool=gem_pool,
        first_player_n=first_player_n,
        current_player_n=first_player_n,
        turn=1,
    )


"""
def reveal_card(game: GameState, level: int) -> GameState:
    return GameState(
        card = game.decks_by_level[level].pop()
        game.revealed_cards_by_level[level].append(card)
    )


def take_gems(self, gems: Gems) -> None:
    assert len(gems) <= 3, "Can only take up to 3 gems."
    assert gems <= self.gem_pool, "Not enough gems in the pool."
    assert sum(gems[i] > self.players[self.current_player_n].gems[i] for i in range(6)) <= 1, "Can only take 2 gems of the same color."
    # take the gems
    self.gem_pool -= gems
    self.players[self.current_player_n].gems += gems
"""
