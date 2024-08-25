from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path

from splendor_bot.game import new_game
from splendor_bot.pubsub import PubSub
from splendor_bot.types import Card, Noble, Gems, Player, GameState


app = FastAPI()
# https://stackoverflow.com/questions/73917396/why-doesnt-uvicorn-pick-up-changes-to-css-files
app.mount(
    "/css",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "css"),
    name="css",
)
templates = Jinja2Templates(directory="templates")


def gem_card_html(request: Request, card: Card) -> str:
    return templates.TemplateResponse(
        request=request,
        name="gem_card.html",
        context={
            "card": card,
        }
    ).body.decode('utf-8')


def noble_card_html(request: Request, noble: Noble) -> str:
    return templates.TemplateResponse(
        request=request,
        name="noble_card.html",
        context={
            "noble": noble,
        }
    ).body.decode('utf-8')


def card_back_html(request: Request, level: int) -> str:
    return templates.TemplateResponse(
        request=request,
        name="card_back.html",
        context={
            "level": level,
        }
    ).body.decode('utf-8')


def gem_pool_html(request: Request, gems: Gems) -> str:
    return templates.TemplateResponse(
        request=request,
        name="gem_pool.html",
        context={
            "gems": gems,
        }
    ).body.decode('utf-8')


def player_html(
    request: Request,
    player: Player,
    is_first_player: bool,
    is_current_player: bool,
    is_winner: bool,
    is_last_round: bool,
) -> str:
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
    ).body.decode('utf-8')


def game_board(request: Request, game_state: GameState) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="game_board.html",
        context={
            "players_html": [
                player_html(
                    request,
                    player,
                    i == game_state.first_player_n,
                    i == game_state.current_player_n,
                    player in game_state.winners,
                    game_state.last_round,
                )
                for i, player in enumerate(game_state.players)
            ],
            "decks_html": [
                card_back_html(request, i+1 if len(game_state.decks_by_level[i]) > 0 else -1)
                for i in range(3)
            ],
            "gem_cards_html": [
                [
                    gem_card_html(request, game_state.revealed_cards_by_level[i][j])
                    for j in range(len(game_state.revealed_cards_by_level[i]))
                ]
                for i in range(len(game_state.revealed_cards_by_level))
            ],
            "nobles_html": [
                noble_card_html(request, noble)
                for noble in game_state.nobles
            ],
            "gem_pool_html": gem_pool_html(request, game_state.gem_pool),
        }
    )


@app.get("/", response_class=HTMLResponse)
def game(request: Request):
    n_players = 4
    game_state = new_game(
        players=[Player(f"Player {i}") for i in range(n_players)],
    )
    return game_board(request, game_state)


pubsub = PubSub()
connections: dict[str, WebSocket] = {}


@app.get("/ws_test/{connection_id}", response_class=HTMLResponse)
def websocket_test(request: Request, connection_id: str):
    return templates.TemplateResponse(
        request=request,
        name="ws_test.html",
        context={
            "connection_id": connection_id,
        },
    )


@app.websocket("/ws_test_connection/{connection_id}")
async def websocket_test_connection(websocket: WebSocket, connection_id: str):
    await websocket.accept()
    connections[connection_id] = websocket
    print("New connection", connection_id)
    print(connections)
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            message = json_data["message"]
            if message.isnumeric():
                message = int(message)
                print("Received number", message)
                await websocket.send_text(f'<div id="id_number">{message}</div>')
            else:
                print("Received string", message)
                await websocket.send_text(f'<div id="id_text">{message}</div>')
    except WebSocketDisconnect:
        connections.pop(connection_id)
        print("Connection closed", connection_id)
        print(connections)
