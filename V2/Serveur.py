import asyncio
import websockets
import json

connected_clients = set()

async def handle_connection(websocket, path):
    # On ajoute la connexion à la liste des clients connectés
    connected_clients.add(websocket)
    try:
        '''# Attendre l'événement "connection"
        event = await websocket.recv()
        print(f"Reçu : {event}")
        # Envoyer un message de bienvenue
        await websocket.send("Welcome!")'''
        # Loop en attente d'event client
        while True:
            event = await websocket.recv()
            client_data = json.loads(event)
            client_event = client_data["event"]
            #Il faut envoyer une info à tous les clients pour créer un joueur
            if client_event == "connect":
                #Faut check combien il y a de joueur
                #Au début on peut identifier avec id websocket
                #On envoie l'info de création d'un joueur à tout le monde
                init = {
                    "event" : "initPlayer",
                    "identifier" : str(websocket.id),
                }
                await websocket.send(json.dumps(init))
            elif client_event == "iKnowMyName":
                #On crée le nouveau joueur chez tout le monde sauf lui
                websocketToConnectedPlayers = createPlayer(websocket)
                for client in connected_clients : 
                    if client != websocket:
                        await client.send(json.dumps(websocketToConnectedPlayers))
                        connectedPlayersToWebSocket = createPlayer(client)
                        await websocket.send(json.dumps(connectedPlayersToWebSocket))

                    #print(connectedPlayersToWebSocket)
            elif client_event  == "move":
                for client in connected_clients :
                    if client != websocket : 
                        move = {
                            "event" : "move",
                            "key" : client_data["key"],
                            "identifier" : client_data["identifier"]
                        }
                        await client.send(json.dumps(move))
            else :
                print("else")

    except websockets.exceptions.ConnectionClosed:
        # Enlever la connexion de la liste des clients connectés
        connected_clients.remove(websocket)

def createPlayer(socket):
    return {
        "event" : "newPlayer",
        "identifier" : str(socket.id),
    }

start_server = websockets.serve(handle_connection, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
