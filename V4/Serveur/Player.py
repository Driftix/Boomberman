from Props.Bomb import Bomb


class Player:
    def __init__(self,websocket):
        self.websocket = websocket
        self.className = "player"
        self.position = [0,0]
        self.bomb = Bomb(3,3,5)
        self.isAlive = True
