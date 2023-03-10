import asyncio
import json
from EventController import EventController
import websockets
from Terrain import Terrain
from Player import Player
import threading
import time

connected_clients = {}

terrain = Terrain(10,10)
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
                #On envoie en premier le terrain non modifié au client
                terrainData = terrain.getDataTerrain()
                await websocket.send(terrainData)
                #On met à jour la carte
                terrainDataUpdate = terrain.getUpdateTerrainData()
                await websocket.send(terrainDataUpdate)
                #Ensuite crée son player
                player = Player(str(websocket.id))
                #On ajoute la connexion avec clé valeur => websock player
                connected_clients[websocket] = player
                #On veut pas que notre joueur soit au dessus d'un autre joueur
                player.updatePosition(connected_clients,terrain)
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
                if terrain.canPlayerMove(x,y,old_x,old_y) :
                    #Si le joueur a le droit de bouger, on envoie à tous les client un mouvement
                    #avec l'identifier du websocket qui a fait la demande
                    movePlayerData = connected_clients[websocket].movePlayerData(x,y)
                    #pas oublier de mettre à jour la position côté serveur
                    connected_clients[websocket].movePlayer(x,y)

                    for client in connected_clients :
                        #on envoie à tout le monde la nouvelle position
                        await client.send(movePlayerData)
            elif eventController.getClient_event() == "placeBomb":
                #le timer sera mis côté client mais la gestion des dégats sera géré côté serveur
                #en gros on pourra tricher avec la console en changeant le timer mais pas d'autre idée
                x = eventController.getClient_Data()["x"]
                y = eventController.getClient_Data()["y"]
                #Pour le moment on place juste la bomb côté serveur
                terrain.placeBomb(x,y)
                #puis on envoie un event pour avoir la bombe partout (avec ses caractéristiques)
                bombTerrainData = terrain.getDataBombTerrain(x,y,connected_clients[websocket])
                #On oublie pas de retirer une bombe à notre joueur
                connected_clients[websocket].decreaseBombQuantity()
                for client in connected_clients:
                    await client.send(bombTerrainData)
                #Après avoir placé la bombe il faut lancer un timer en tâche de fond
                asyncio.create_task(countdown(2,bombTerrainData))


    except websockets.exceptions.ConnectionClosed:
        # Enlever la connexion de la liste des clients connectés
        connected_clients.pop(websocket)

async def countdown(n,bomb):
    while n > 0:
        #print(n)
        n -= 1
        await asyncio.sleep(1)
    for client in connected_clients:
        #on récupère la bombe et on renvoie l'event avec "explode"
        bombData = terrain.explodeData(bomb)
        #print(bombData)
        await client.send(bombData)

start_server = websockets.serve(handle_connection, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

