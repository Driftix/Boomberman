import asyncio
import websockets
import json
import secrets
from Player import Player
from boomberman import *

players = []


async def handler(websocket):
    try :
        #Ici les messages qu'on recoit
        async for message in websocket:
            print(f"Received message: {message}")
            message = json.loads(message)
            match message["type"]:
                case 'join':
                    break
                case 'connect':
                    players.append(Player(websocket.id, 5,3,0,0))

                    event = {
                        "type": "init",
                        "coo_x": 0,
                        "coo_y":0,
                        "id":websocket.id
                    }
                    await websocket.send(json.dumps(event))

                    print("Joueur créé")
                    break
                #Fonctionne pas encore
                case 'disconnect':
                    print("Suppression du joueur")
                    for p in players:
                        if(p.uid == websocket.id):
                            players.remove(p)
                            print("disconnected")
                    print("players : {}".format(players))
    #Rajouter des except si jamais on en a besoin
    finally :
        print("End")
        


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())