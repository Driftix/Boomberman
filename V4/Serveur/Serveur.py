import asyncio
import json
from EventController import EventController
import websockets
from Terrain import Terrain
from Props.Player import Player
import threading
import time

connected_clients = {}

terrain = Terrain(30,30)
eventController = EventController()

async def handle_connection(websocket, path):
    # On ajoute la connexion à la liste des clients connectés
    try:
        # Loop en attente d'event client
        while True:
            #Récupération de l'event et ajout des données à l'event controller
            event = await websocket.recv()
            eventController.addEventData(event)
            #On check l'event et on traite
            if eventController.getClient_event() == "connect":
                #On envoie direct le terrain en cours au client
                terrainData = terrain.getDataClientTerrain()
                await websocket.send(terrainData)
                #Ensuite crée son player
                player = Player(str(websocket.id))
                #On ajoute la connexion avec clé valeur => websock player
                connected_clients[websocket] = player
                #On veut pas que notre joueur soit au dessus d'un autre joueur
                player.updatePosition(connected_clients)
                #On créé une data pour joueur principale et autre joueur
                playablePlayerData = player.getDataPlayer(True)
                unplayablePlayerData = player.getDataPlayer(False)
                #Il faut l'envoyer à tous les clients déjà connectés
                for client in connected_clients:
                    if client.id == websocket.id:
                        #Si le client c'est lui on l'envoie jouable
                        await client.send(playablePlayerData)
                    else: 
                         #sinon on envoie un non playable
                        await client.send(unplayablePlayerData)                 
                    #on envoie le même joueur non jouable aux autres déjà connectés
                    if(client.id != websocket.id):
                        guest = connected_clients[client]
                        guestData = guest.getDataPlayer(False)
                        await websocket.send(guestData)
            elif eventController.getClient_event() == "move":
                x = eventController.getClient_Data()["x"]
                y = eventController.getClient_Data()["y"]
                old_x = eventController.getClient_Data()["old_x"]
                old_y = eventController.getClient_Data()["old_y"]
                #Utilisation coord demandées+ coords actuelle client
                if terrain.canPlayerMove(connected_clients[websocket],x,y,old_x,old_y) :
                    #Si le joueur a le droit de bouger, on envoie à tous les client un mouvement
                    #avec l'identifier du websocket qui a fait la demande
                    movePlayerData = connected_clients[websocket].movePlayerData(x,y)
                    #pas oublier de mettre à jour la position côté serveur
                    connected_clients[websocket].movePlayer(x,y)

                    for client in connected_clients :
                        #on envoie à tout le monde la nouvelle position
                        await client.send(movePlayerData)
            elif eventController.getClient_event() == "placeBomb":
                #Initialisation des coordonnées de la bombe
                pos = {
                    "x" : eventController.getClient_Data()["x"],
                    "y" : eventController.getClient_Data()["y"]
                }
                playerBomb = connected_clients[websocket].getBomb()
                
                
                #On place la bombe sur le terrain
                terrain.placeBomb(pos,playerBomb)
                #puis on envoie un event pour avoir la bombe partout (avec ses caractéristiques)
                bombTerrainData = terrain.getDataBombTerrain(pos,playerBomb)
                #On oublie pas de retirer une bombe à notre joueur
                connected_clients[websocket].decreaseBombQuantity()

                for client in connected_clients:
                    await client.send(bombTerrainData)
                #Après avoir placé la bombe il faut lancer un timer en tâche de fond
                asyncio.create_task(countdown(2,pos,playerBomb))


    except websockets.exceptions.ConnectionClosed:
        # Enlever la connexion de la liste des clients connectés
        connected_clients.pop(websocket)

async def countdown(n,pos,bomb):
    while n > 0:
        #print(n)
        n -= 1
        await asyncio.sleep(1)
    for client in connected_clients:
        #on récupère la bombe et on renvoie l'event avec "explode"
        bombData = terrain.explodeData(pos,bomb)
        await client.send(bombData)

start_server = websockets.serve(handle_connection, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

