import asyncio
import json
from EventController import EventController
import websockets
from Terrain import Terrain
import secrets

from Player import Player

connexions = {} 
eventController = EventController()

#Mettre asyncio ici => une methode qui remplace x y bomb
#Update pour terrain tous les joueurs
#Une autre x y Air => Au même moment destruction des alentours :D
#Puis update du terrain pour tous les joueurs de nouveau

async def placeBomb(n,x,y,bomb,terrain,clients):
    terrain.placeBomb(x,y,bomb)
    for client in clients:
        await client.websocket.send(terrain.getDataClientTerrain())
    while n > 0:
        n -= 1
        await asyncio.sleep(1)
    destroyed_blocs = terrain.destroyTerrainBomb(x,y,bomb)
    #Optimiser
    for client in clients:
        await client.websocket.send(terrain.getDataClientTerrain())
    for client in clients :
        await client.websocket.send(json.dumps({"event":"animate","destroyed":destroyed_blocs}))

async def decreaseBomb(player):
    player.bomb.quantity -= 1
    await player.websocket.send(json.dumps({"event":"updateBomb","qty":player.bomb.quantity}))
    time = player.bomb.loadTime
    while time > 0:
        time -= 1
        await asyncio.sleep(1)
    player.bomb.quantity += 1
    await player.websocket.send(json.dumps({"event":"updateBomb","qty":player.bomb.quantity}))

async def handle_connection(websocket, path):
    # On ajoute la connexion à la liste des clients connectés
    try:
        # Loop en attente d'event client
        while True:
            #Récupération de l'event et ajout des données à l'event controller
            event = await websocket.recv()
            eventController.addEventData(event)
            #Si le player start
            if eventController.getClient_event() == "start":
                #On crée une partie avec une url, qui sera direct rejoins
                join_key = secrets.token_urlsafe(12)
                #On initialise la connexion (sans mettre le joueur dedans mais en mettant le terrain)
                connexions[join_key] = {
                    "clients" : [],
                    "shared_field" : Terrain(30,30)
                }
                await websocket.send(json.dumps({
                    "event":"start",
                    "key":join_key
                }))

            elif eventController.getClient_event() == "join":
                join_key = eventController.getClient_Data()["key"]
              
                #Il faut ajouter notre joueur au jeu
                newPlayer = Player(websocket)
                connexions[join_key]["shared_field"].addPlayer(newPlayer)
                connexions[join_key]["clients"].append(newPlayer)
                #On envoie toujours le terrain HTML aux clients
                #Il faut l'envoyer à tout le monde pour faire la maj de la carte
                for client in connexions[join_key]["clients"]:
                    await client.websocket.send(connexions[join_key]["shared_field"].getDataClientTerrain())

            elif eventController.getClient_event() == "move":
                movement = eventController.getClient_Data()["direction"]
                join_key = eventController.getClient_Data()["key"]
                for player in connexions[join_key]["clients"]:
                    #On recherche le joueur pour avoir sa position sur le terrain
                    if player.websocket == websocket and player.isAlive:
                        if movement == "up":
                            if connexions[join_key]["shared_field"].canPlayerMove(player.position[0]-1, player.position[1]):
                                connexions[join_key]["shared_field"].updatePlayer(player,player.position[0]-1,player.position[1])
                        if movement == "down":
                            if connexions[join_key]["shared_field"].canPlayerMove(player.position[0]+1, player.position[1]):
                                connexions[join_key]["shared_field"].updatePlayer(player,player.position[0]+1,player.position[1])
                        if movement == "right":
                            if connexions[join_key]["shared_field"].canPlayerMove(player.position[0], player.position[1]+1):
                                connexions[join_key]["shared_field"].updatePlayer(player,player.position[0],player.position[1]+1)
                        if movement == "left":
                            if connexions[join_key]["shared_field"].canPlayerMove(player.position[0], player.position[1]-1):
                                connexions[join_key]["shared_field"].updatePlayer(player,player.position[0],player.position[1]-1)
                        #On update la carte
                        for client in connexions[join_key]["clients"]:
                            await client.websocket.send(connexions[join_key]["shared_field"].getDataClientTerrain())
                        break
            elif eventController.getClient_event() == "placeBomb":
                #Récup du joueur qui à placé la bombe
                for player in connexions[join_key]["clients"] :
                    if player.websocket == websocket and player.isAlive and player.bomb.quantity > 0:
                        asyncio.create_task(placeBomb(2,player.position[0],player.position[1],player.bomb,connexions[join_key]["shared_field"], connexions[join_key]["clients"]))
                        asyncio.create_task(decreaseBomb(player))
    except websockets.exceptions.ConnectionClosed:
        #Enlever la connexion de la liste des clients connectés
        #connected_clients.pop(websocket)
        print("connexion closed")

            
start_server = websockets.serve(handle_connection, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

