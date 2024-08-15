from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from splendor_bot.game import new_game
from splendor_bot.types import Card


app = FastAPI()
templates = Jinja2Templates(directory="templates")


def card_html(request: Request, card: Card) -> HTMLResponse:
    game_state = new_game(n_players=2)
    card = game_state.revealed_cards_by_level[0][0]
    return templates.TemplateResponse(
        request=request,
        name="card.html",
        context={
            "card": card,
        }
    )


@app.get("/", response_class=HTMLResponse)
def game(request: Request):
    game_state = new_game(n_players=2)
    card = game_state.revealed_cards_by_level[0][0]
    return card_html(request, card)
