from dataclasses import dataclass
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from uuid import uuid4, UUID

from splendor_bot.game import new_game, Player
from splendor_bot.types import GameState

from server.routers.diagnose import print_diagnose
from server.routers.splendor.game_html import game_board_html
from server.routers.splendor.pubsub import PubSub


router = APIRouter(prefix="/splendor")
templates = Jinja2Templates(directory="templates")
pubsub = PubSub()


@dataclass
class Connection:
    websocket: WebSocket
    in_waiting_room: bool
    game_uuid: UUID


@dataclass
class Game:
    in_waiting_room: bool
    game_state: GameState | None
    connection_uuids: list[UUID]


connections: dict[UUID, Connection] = {}
games: dict[UUID, Game] = {}


@print_diagnose
@router.get("/new-waiting-room", response_class=RedirectResponse)
async def create_new_waiting_room(request: Request):
    game_uuid = uuid4()
    game = Game(in_waiting_room=True, game_state=None, connection_uuids=[])
    games[game_uuid] = game
    return RedirectResponse(f"/splendor/waiting-room/{game_uuid}")



@router.websocket("/waiting-room/{game_uuid}")
async def create_new_player_and_join_waiting_room(websocket: WebSocket, game_uuid: str):
    await websocket.accept()
    connection = Connection(websocket=websocket, in_waiting_room=True, game_uuid=game_uuid)
    connection_uuid = uuid4()
    connections[connection_uuid] = connection
    print("New connection", connection_uuid)
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
        connections.pop(connection_uuid)
        print("Connection closed", connection_uuid)
        print(connections)
    return templates.TemplateResponse(
        request=request,
        name="waiting_room.html",
        context={
            "game_uuid": game_uuid,
        },
    )


@router.websocket("/game/{game_uuid}", response_class=HTMLResponse)
async def display_game(websocket: WebSocket, game_uuid: str):
    return create_new_game(request, n_players=4)










@router.websocket("/ws-test-connection/{connection_id}")
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


def create_new_game(request: Request, n_players: int) -> HTMLResponse:
    """
    Create new game, and return the game HTML.
    """
    game_uuid = "test_game_id"
    game_state = new_game(
        players=[Player(f"Player {i}") for i in range(n_players)],
    )
    game_html = game_board_html(request, game_state)
    # TODO: add div to HTML with the game_uuid
    add_game_id_html = lambda game_html, game_uuid: game_html
    game_html = add_game_id_html(game_html, game_uuid)
    return game_html


def add_new_player_to_new_game(request: Request, game_uuid: str) -> HTMLResponse:
    """
    Add a new player to an existing game specified by game_uuid, and return the game HTML.
    """


def add_new_player_to_existing_game(request: Request, game_uuid: str) -> HTMLResponse:
    n_players = 4
    game_state = new_game(
        players=[Player(f"Player {i}") for i in range(n_players)],
    )


@router.get("/ws-test/{connection_id}", response_class=HTMLResponse)
def websocket_test(request: Request, connection_id: str):
    game_uuid = "test_game_id"
    return add_new_player_to_existing_game(request, game_uuid)
    return templates.TemplateResponse(
        request=request,
        name="ws_test.html",
        context={
            "connection_id": connection_id, },
    )
