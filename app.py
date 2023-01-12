import asyncio
import websockets
import json
import secrets
from boomberman import *

ROOM = {}

#Gestion d'erreur
async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def start(websocket):
    game = boomberman()
    connected = {websocket}

    room_key = secrets.token_urlsafe(20)
    ROOM[room_key] = game, connected

    try:
        event = {
            "type":"init",
            "join":room_key
        }
        await websocket.send(json.dumps(event))

    finally:
        del ROOM[room_key] 


async def handler(websocket):
    # Lire & traiter les événements "init" depuis le navigateur
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    if "join" in event:
        print(message)
    else: 
        print("injh")
        print(message)
   

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())