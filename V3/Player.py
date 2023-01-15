import json
from Bomb import Bomb

class Player:
    def __init__(self,identifier):
        print("Initialisation du Joueur: {}...".format(identifier))
        self.identifier = identifier
        self.positionX = 0
        self.positionY = 0
        self.bomb = Bomb(3)
        self.bombQuantity = 2
        
    def getDataPlayer(self, playable):
        initPlayer = {
            "event" : "initPlayer",
            "identifier" : self.identifier,
            "x" : self.positionX,
            "y" :self.positionY,
            "playable" : playable
        }
        return json.dumps(initPlayer)
    
    def updatePosition(self,connectedClients):
        #Modifier pour que en fonction du nb de client on soit mis dans les coins
        '''for client in connectedClients:
            if str(connectedClients[client].getIdentifier()) != self.identifier:
                self.positionX += 5
                self.positionY += 5'''
        player = len(connectedClients) # 1 / 2 / 3 / 4
        if player == 1:
            self.positionX = 0
            self.positionY = 0
        elif player == 2:
            self.positionX = 0
            self.positionY = 29
        elif player == 3:
            self.positionX = 29
            self.positionY = 0
        elif player == 4:
            self.positionX = 29
            self.positionY = 29

    def movePlayer(self,x,y):
        self.positionX = x
        self.positionY = y

    def movePlayerData(self,x,y):
        move = {
            "event" : "confirmMove",
            "identifier" : self.identifier,
            "x" : x,
            "y" : y,
        }
        return json.dumps(move)

    def getIdentifier(self):
        return self.identifier
    def getBomb(self):
        return self.bomb
    def getBombQuantity(self):
        return self.bombQuantity
    def decreaseBombQuantity(self):
        self.bombQuantity -=1
