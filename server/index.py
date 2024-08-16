from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from splendor_bot.game import new_game
from splendor_bot.types import Card, Noble


app = FastAPI()
app.mount(
    "/css",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "css"),
    name="css",
)
templates = Jinja2Templates(directory="templates")


def card(request: Request, card: Card):
    return templates.TemplateResponse(
        request=request,
        name="card.html",
        context={
            "card": card,
        }
    ).body


def noble(request: Request, noble: Noble):
    return templates.TemplateResponse(
        request=request,
        name="noble.html",
        context={
            "noble": noble,
        }
    )


@app.get("/", response_class=HTMLResponse)
def game(request: Request):
    game_state = new_game(n_players=2)
    return templates.TemplateResponse(
        request=request,
        name="card.html",
        context={
            "card": game_state.revealed_cards_by_level[0][0],
        }
        # context={
            # "card_html": card(request, game_state.revealed_cards_by_level[0][0]),
            # "noble_html": noble(request, game_state.nobles[0]),
        # }
    )
