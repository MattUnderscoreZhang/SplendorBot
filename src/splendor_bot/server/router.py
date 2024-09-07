from dataclasses import dataclass, field
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
import json
import random
from starlette.websockets import WebSocketDisconnect
import string
from uuid import uuid4, UUID

from splendor_bot.game_logic.game import new_game, Player
from splendor_bot.game_logic.types import GameState

from splendor_bot.server.game_html import game_board_html
from splendor_bot.server.pubsub import PubSub


splendor_prefix = "/splendor"
router = APIRouter(prefix=splendor_prefix)
env = Environment(loader=FileSystemLoader("assets/templates"))


################################
# ACTIVE GAMES AND CONNECTIONS #
################################


@dataclass
class PlayerConnection:
    websocket: WebSocket
    player_name: str
    connection_uuid: UUID
    disconnected_from_game: bool = False


@dataclass
class ActiveGame:
    game_state: GameState | None = field(default=None)
    n_players: int = 4
    player_connections: list[PlayerConnection] = field(default_factory=list)
    pubsub: PubSub = field(default_factory=PubSub)


active_games: dict[str, ActiveGame] = {}


async def _add_player_to_waiting_room(game_id: str, player_connection: PlayerConnection):
    game = active_games[game_id]
    game.player_connections.append(player_connection)
    # subscribe to game updates
    game.pubsub.subscribe(
        "update_game",
        lambda: player_connection.websocket.send_text(
            env.get_template("waiting_room.html").render(
                {
                    "game_id": game_id,
                    "player_names": [
                        player_connection.player_name
                        for player_connection
                        in game.player_connections
                    ],
                    "player_n": sum([
                        player_n
                        for player_n, player in enumerate(game.player_connections)
                        if player.connection_uuid == player_connection.connection_uuid
                    ]),
                    "n_players": game.n_players,
                },
            )
            if game.game_state is None
            else game_board_html(game.game_state)
        ),
        player_connection.connection_uuid,
    )
    # push game update
    await game.pubsub.publish("update_game")


async def _remove_player_from_waiting_room(game_id: str, player_connection: PlayerConnection):
    if game_id not in active_games:
        return
    game = active_games[game_id]
    game.player_connections.remove(player_connection)
    game.pubsub.unsubscribe("update_game", player_connection.connection_uuid)
    await game.pubsub.publish("update_game")
    if len(game.player_connections) == 0:
        del active_games[game_id]


async def _disconnect_player_from_game(game_id: str, player_connection: PlayerConnection):
    if game_id not in active_games:
        return
    game = active_games[game_id]
    player_connection.disconnected_from_game = True
    await game.pubsub.publish("update_game")
    if (
        sum([(not player.disconnected_from_game) for player in game.player_connections]) == 0
        or sum([(player.disconnected_from_game) for player in game.player_connections]) >= 2
    ):
        del active_games[game_id]
        # TODO: kick remaining players back to waiting room


async def _reconnect_player_to_game(game_id: str, player_connection: PlayerConnection):
    ...


##############################
# ROUTER ENDPOINTS AND LOGIC #
##############################


@router.get("/", response_class=HTMLResponse)
async def create_new_game(request: Request):
    # this game HTML opens a websocket connection to the waiting room
    return env.get_template("new_game.html").render(
        {"splendor_prefix": splendor_prefix}
    )


@router.websocket("/")
async def waiting_room_websocket(websocket: WebSocket):
    await websocket.accept()
    player_connection = PlayerConnection(
        websocket=websocket,
        player_name="Human Player",
        connection_uuid=uuid4(),
    )
    game_id = ""
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            if game_id == "":
                # no game joined yet
                game_id = await _join_game_and_get_id(game_id, player_connection, json_data)
            else:
                game = active_games[game_id]
                if game.game_state is None:
                    # still in waiting room
                    await _update_waiting_room(game, player_connection, json_data)
                else:
                    # game has started
                    await _update_game(game, player_connection, json_data)
    except WebSocketDisconnect:
        if game_id == "":
            return
        game = active_games[game_id]
        if game.game_state is None:
            await _remove_player_from_waiting_room(game_id, player_connection)
        else:
            await _disconnect_player_from_game(game_id, player_connection)


async def _join_game_and_get_id(
    game_id: str,
    player_connection: PlayerConnection,
    json_data: dict,
) -> str:
    if "join_waiting_room" not in json_data.keys():
        return ""
    # create new game
    if json_data["join_waiting_room"] == "new_game":
        game_id = "".join(random.choices(string.ascii_uppercase, k=4))
        active_games[game_id] = ActiveGame()
    # check what game to join, and give warning if game does not exist
    elif json_data["join_waiting_room"] == "existing_game":
        game_id = json_data["game_id"].upper()
        if game_id == "":
            return ""
        elif game_id not in active_games:
            await player_connection.websocket.send_text(f'<div id="warning">Game with ID {game_id} does not exist</div>')
            return ""
    # add player to game
    await _add_player_to_waiting_room(game_id, player_connection)
    return game_id


async def _update_waiting_room(
    game: ActiveGame,
    player_connection: PlayerConnection,
    json_data: dict,
) -> None:
    # update player name
    if "update_player_name" in json_data.keys():
        player_connection.player_name = json_data["update_player_name"]
        await game.pubsub.publish("update_game")
    # change settings
    if "n_players" in json_data.keys():
        game.n_players = int(json_data["n_players"])
        await game.pubsub.publish("update_game")
    # start game
    if "start_game" in json_data.keys():
        n_bots = game.n_players - len(game.player_connections)
        players = [
            Player(
                name=player_connection.player_name,
                is_bot=False,
            )
            for player_connection
            in game.player_connections
        ] + [
            Player(
                name=f"Bot {i}",
                is_bot=True,
            )
            for i in range(n_bots)
        ]
        random.shuffle(players)
        game.game_state = new_game(players)
        await game.pubsub.publish("update_game")


async def _update_game(
    game: ActiveGame,
    player_connection: PlayerConnection,
    json_data: dict,
) -> None:
    await game.pubsub.publish("update_game")
