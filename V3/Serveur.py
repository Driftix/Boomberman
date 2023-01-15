import asyncio
from EventController import EventController
import websockets
from Terrain import Terrain
from Player import Player

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
                #On envoie en premier le terrain au client
                terrainData = terrain.getDataTerrain()
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
                        guest = Player(str(client.id))
                        guestData = guest.getDataPlayer(False)
                        await websocket.send(guestData)
            elif eventController.getClient_event() == "move":
                x = eventController.getClient_Data()["x"]
                y = eventController.getClient_Data()["y"]
                #Utilisation coord demandées+ coords actuelle client
                if terrain.canPlayerMove(x,y) :
                    #Si le joueur a le droit de bouger, on envoie à tous les client un mouvement
                    #avec l'identifier du websocket qui a fait la demande
                    movePlayerData = connected_clients[websocket].movePlayerData(x,y)
                    #pas oublier de mettre à jour la position côté serveur
                    connected_clients[websocket].movePlayer(x,y)

                    for client in connected_clients :
                        #on envoie à tout le monde la nouvelle position
                        await client.send(movePlayerData)
            elif eventController.getClient_event() == "placeBomb":
                x = eventController.getClient_Data()["x"]
                y = eventController.getClient_Data()["y"]
                #on fait passer le player pour récupérer les stats de ses bombes
                terrain.placeBomb(connected_clients[websocket])

    except websockets.exceptions.ConnectionClosed:
        # Enlever la connexion de la liste des clients connectés
        connected_clients.pop(websocket)


start_server = websockets.serve(handle_connection, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

