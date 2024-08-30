from dataclasses import dataclass
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from uuid import uuid4, UUID

from splendor_bot.game_logic.game import new_game, Player
from splendor_bot.game_logic.types import GameState

from splendor_bot.server.game_html import game_board_html
from splendor_bot.server.pubsub import PubSub


splendor_prefix = "/splendor"
router = APIRouter(prefix=splendor_prefix)
templates = Jinja2Templates(directory="assets/templates")
pubsub = PubSub()


@dataclass
class PlayerConnection:
    websocket: WebSocket
    game_uuid: UUID
    name: str


@dataclass
class ActiveGame:
    game_state: GameState | None
    player_connections: list[PlayerConnection]


active_games: dict[UUID, ActiveGame] = {}


@router.get("/new-game", response_class=RedirectResponse)
async def create_new_game(request: Request):
    game_uuid = uuid4()
    return RedirectResponse(f"{splendor_prefix}/game/{game_uuid}")


@router.get("/game/{game_uuid}", response_class=HTMLResponse)
async def display_game_or_waiting_room(request: Request, game_uuid: UUID):
    if game_uuid not in active_games:
        game = ActiveGame(game_state=None, player_connections=[])
        active_games[game_uuid] = game
        # TODO: give alert that game did not exist on redirect
        return RedirectResponse(f"{splendor_prefix}/new-game")
    if active_games[game_uuid].game_state is None:
        return templates.TemplateResponse(
            request=request,
            name="waiting_room.html",
            context={
                "splendor_prefix": splendor_prefix,
                "game_uuid": game_uuid,
                "player_names": [player_connection.name for player_connection in active_games[game_uuid].player_connections],
            },
        )
    else:
        return game_board_html(request, game_state=active_games[game_uuid].game_state)  # type: ignore


@router.websocket("/game/{game_uuid}")
async def game_websocket(websocket: WebSocket, game_uuid: UUID):
    await websocket.accept()
    # create new player connection
    player_connection = PlayerConnection(websocket=websocket, game_uuid=game_uuid, name="Player Name")
    game_player_connections = active_games[game_uuid].player_connections
    game_player_connections.append(player_connection)
    # subscribe to player list updates
    callback_uuid = pubsub.subscribe(
        f"update_players_list_{game_uuid}",
        lambda game_player_connections: player_connection.websocket.send_text(
            f'''<div id="players_in_waiting_room">{{{{ {
                [player_connection.name for player_connection in game_player_connections]
            } }}}}</div>'''
        ),
    )
    # publish new player
    await pubsub.publish(f"update_players_list_{game_uuid}", game_player_connections)
    # handle websocket messages
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            # in waiting room
            if active_games[game_uuid].game_state is None:
                # update player name
                if "player_name" in json_data:
                    player_connection.name = json_data["player_name"]
                    print(player_connection.name)
                    await pubsub.publish(f"update_players_list_{game_uuid}", game_player_connections)
                # start game
                if "start_game" in json_data:
                    """
                    TODO
                    """
                    n_players = len(game_player_connections)
                    active_games[game_uuid].game_state = new_game(
                        players=[Player(f"Player {i}") for i in range(n_players)],
                    )
            # in game
            else:
                ...
    except WebSocketDisconnect:
        game_player_connections.remove(player_connection)
        pubsub.unsubscribe(f"update_players_list_{game_uuid}", callback_uuid)
        await pubsub.publish(f"update_players_list_{game_uuid}", game_player_connections)
