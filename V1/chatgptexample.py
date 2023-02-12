import asyncio
import websockets

connected_clients = set()

async def handle_connection(websocket, path):
    # Ajouter la connexion à la liste des clients connectés
    connected_clients.add(websocket)
    try:
        # Attendre l'événement "connection"
        event = await websocket.recv()
        print(f"Reçu : {event}")
        # Envoyer un message de bienvenue
        await websocket.send("Welcome!")
        # Attendre les événements "keydown"
        while True:
            event = await websocket.recv()
            if event.startswith("keydown:"):
                print(f"Touche appuyée : {event.split(':')[1]}")
                # Envoyer un message de diffusion à tous les clients connectés
                for client in connected_clients:
                    if client != websocket: :
                        await client.send(event)
    except websockets.exceptions.ConnectionClosed:
        # Enlever la connexion de la liste des clients connectés
        connected_clients.remove(websocket)

start_server = websockets.serve(handle_connection, "localhost", 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
