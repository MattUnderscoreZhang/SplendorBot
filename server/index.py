from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from splendor_bot.game import new_game
from splendor_bot.types import Card, Noble


app = FastAPI()
templates = Jinja2Templates(directory="templates")


def card_html(request: Request, card: Card) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="card.html",
        context={
            "card": card,
        }
    )


def noble_html(request: Request, noble: Noble) -> HTMLResponse:
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
    # card = game_state.revealed_cards_by_level[0][0]
    # return card_html(request, card)
    noble = game_state.nobles[0]
    return noble_html(request, noble)
