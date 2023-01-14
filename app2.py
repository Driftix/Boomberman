import asyncio
import websockets
import json
import secrets
from boomberman import *

Room = []
JOIN = {}
#async def move(websocket, player,x,y) :



async def handler(websocket):
    # Lire & traiter les événements "init" depuis le navigateur
    event = json.loads(await websocket.recv())
    playerExist = False
    if event["event"] == "Connect":         
        if not Room :
            Room.append(event["identifier"])
        else :
            for playerID in Room :
                if event["identifier"] == playerID:
                    playerExist = True
            if not playerExist :
                Room.append(event["identifier"])
    elif event["event"] == "Move" :
        print(json.dumps(event))
        print(websocket.id)
        await websocket.send(json.dumps(event))

    print("Event Triggered") 

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())