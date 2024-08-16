from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from splendor_bot.game import new_game
from splendor_bot.types import Card, Noble, Gems, Player


app = FastAPI()
# https://stackoverflow.com/questions/73917396/why-doesnt-uvicorn-pick-up-changes-to-css-files
app.mount(
    "/css",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "css"),
    name="css",
)
templates = Jinja2Templates(directory="templates")


def gem_card(request: Request, card: Card):
    return templates.TemplateResponse(
        request=request,
        name="gem_card.html",
        context={
            "card": card,
        }
    )


def noble_card(request: Request, noble: Noble):
    return templates.TemplateResponse(
        request=request,
        name="noble_card.html",
        context={
            "noble": noble,
        }
    )


def card_back(request: Request, level: int):
    return templates.TemplateResponse(
        request=request,
        name="card_back.html",
        context={
            "level": level,
        }
    )


def gem_pool(request: Request, gems: Gems):
    return templates.TemplateResponse(
        request=request,
        name="gem_pool.html",
        context={
            "gems": gems,
        }
    )


def player(
    request: Request,
    player: Player,
    is_first_player: bool,
    is_current_player: bool,
    is_winner: bool,
    is_last_round: bool,
):
    return templates.TemplateResponse(
        request=request,
        name="player.html",
        context={
            "player": player,
            "is_first_player": is_first_player,
            "is_current_player": is_current_player,
            "is_winner": is_winner,
            "is_last_round": is_last_round,
        }
    )


@app.get("/", response_class=HTMLResponse)
def game(request: Request):
    game_state = new_game(n_players=2)
    # return gem_card(request, game_state.revealed_cards_by_level[0][0])
    # return noble_card(request, game_state.nobles[0])
    # return card_back(request, 3)
    # return gem_pool(request, game_state.gem_pool)
    return player(request, game_state.players[0], False, True, False, True)
