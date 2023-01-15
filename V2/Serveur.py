import asyncio
import websockets
import json
from bs4 import BeautifulSoup


connected_clients = set()

import random

def create_html_table(width, height):
    soup = BeautifulSoup("", "html.parser")

    table = soup.new_tag("table")
    table["id"] = "table"
    table["border"] = "1"
    table["cellpadding"] = "5"
    table["cellspacing"] = "0"

    tbody = soup.new_tag("tbody")
    table.append(tbody)

    for i in range(width):
        tr = soup.new_tag("tr")
        for j in range(height):
            td = soup.new_tag("td")
            td["id"] = f"{i},{j}"
            tr.append(td)
            choices = ["wall", "brick", "air"]
            weights = [0.12, 0.58, 0.3]
            td["class"] = random.choices(choices,weights=weights)[0]

            '''if random.choices(choices,weights=weights)[0]: 
                td["class"] = "random-class"'''


            # probabilités associées à chaque classe
           
            # choisir aléatoirement une classe
        tbody.append(tr)
    return str(table)


terrain = create_html_table(30,30)

async def handle_connection(websocket, path):
    # On ajoute la connexion à la liste des clients connectés
    connected_clients.add(websocket)
    try:
        # Loop en attente d'event client
        #await websocket.send(json.dumps(create_html_table(50,50)))
        while True:
            event = await websocket.recv()
            client_data = json.loads(event)
            client_event = client_data["event"]
            #Il faut envoyer une info à tous les clients pour créer un joueur
            if client_event == "connect":
                #Faut check combien il y a de joueur
                #Au début on peut identifier avec id websocket
                #On envoie l'info de création d'un joueur à tout le monde
                initPlayer = {
                    "event" : "initPlayer",
                    "identifier" : str(websocket.id),
                    "x" : 0,
                    "y" :0,
                }
                #On pourra le réutiliser pour faire des maps plus cool
                initTerrain = {
                    "event" : "initTerrain",
                    "terrain" : terrain
                }
                await websocket.send(json.dumps(initTerrain))
                await websocket.send(json.dumps(initPlayer))
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
                            "x" : client_data["x"],
                            "y" : client_data["y"],
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
        "x" : 0,
        "y" : 0
    }

start_server = websockets.serve(handle_connection, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

