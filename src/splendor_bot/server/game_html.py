from jinja2 import Environment, FileSystemLoader

from splendor_bot.game_logic.types import Card, Noble, Gems, Player, GameState


env = Environment(loader=FileSystemLoader("assets/templates"))


def gem_card_html(card: Card) -> str:
    return env.get_template("gem_card.html").render(
        {
            "card": card,
        }
    )


def noble_card_html(noble: Noble) -> str:
    return env.get_template("noble_card.html").render(
        {
            "noble": noble,
        }
    )


def card_back_html(level: int) -> str:
    return env.get_template("card_back.html").render(
        {
            "level": level,
        }
    )


def gem_pool_html(gems: Gems) -> str:
    return env.get_template("gem_pool.html").render(
        {
            "gems": gems,
        }
    )


def player_html(
    player: Player,
    is_first_player: bool,
    is_current_player: bool,
    is_winner: bool,
    is_last_round: bool,
) -> str:
    return env.get_template("player.html").render(
        {
            "player": player,
            "is_first_player": is_first_player,
            "is_current_player": is_current_player,
            "is_winner": is_winner,
            "is_last_round": is_last_round,
        }
    )


def game_board_html(game_state: GameState) -> str:
    return env.get_template("game_board.html").render(
        {
            "players_html": [
                player_html(
                    player,
                    i == game_state.first_player_n,
                    i == game_state.current_player_n,
                    player in game_state.winners,
                    game_state.last_round,
                )
                for i, player in enumerate(game_state.players)
            ],
            "decks_html": [
                card_back_html(i+1 if len(game_state.decks_by_level[i]) > 0 else -1)
                for i in range(3)
            ],
            "gem_cards_html": [
                [
                    gem_card_html(game_state.revealed_cards_by_level[i][j])
                    for j in range(len(game_state.revealed_cards_by_level[i]))
                ]
                for i in range(len(game_state.revealed_cards_by_level))
            ],
            "nobles_html": [
                noble_card_html(noble)
                for noble in game_state.nobles
            ],
            "gem_pool_html": gem_pool_html(game_state.gem_pool),
        }
    )
