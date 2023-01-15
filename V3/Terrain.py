import random
from bs4 import BeautifulSoup
import json

class Terrain :
    def __init__(self,width, height):
        self.width = width
        self.height = height
        print("Instantiation du terrain...")
        self.terrain = self.createTerrain(width,height)
        print("Terrain Créé...")
        self.terrain2D = self.convertTerrainTo2D()
        print("Terrain 2D en memoire")

    def createTerrain(self,width, height):
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
                weights = [0.12, 0.28, 0.6]
                td["class"] = random.choices(choices,weights=weights)[0]
            tbody.append(tr)
        return table

    def getStrTerrain(self):
        return str(self.terrain)

    def getDataTerrain(self):
        initTerrain = {
            "event" : "initTerrain",
            "terrain" : self.getStrTerrain()
        }
        return json.dumps(initTerrain)

    #Attention il envoie deux instructions à chaque fois c'est bizarre
    def canPlayerMove(self,x,y):
        '''En fait ici on va récupérer les infos de la map (bs4 => 2D)
        dans un tableau 2D pour pouvoir, via nos coordonnées, regarder si il y a une brique / mur / air etc'''
        cells = self.terrain.findAll("td")
        cellClass = self.terrain2D[x][y]
        if(cellClass == "brick" or cellClass == "wall" or cellClass == "bomb"):
            return False
        else:
            return True

    def convertTerrainTo2D(self):
        cells = self.terrain.findAll("td")
        terrain2D = [[0 for x in range(self.width)] for y in range(self.height)] 
        for cell in cells:
            terrainX = int(cell['id'].split(',')[0])
            terrainY = int(cell['id'].split(',')[1])
            terrain2D[terrainX][terrainY] = cell['class']
        return terrain2D
    
    def placeBomb(self,x,y):
        #on modifie la classe en bombe
        self.terrain2D[x][y] = "bomb"
    
    def getDataBombTerrain(self,x,y,player):
        return json.dumps({
            "event" : "bombPlaced",
            "x" : x,
            "y": y,
            "radius" : player.getBomb().getRadius(),
        })
    def explodeData(self,bomb):
        bomb = json.loads(bomb)
        #il faudra détruire le terrain par la même occasion
        destroyed = self.explodeTerrain(bomb)
        #Après avoir détruit le terrain on récupère le tableau pour l'envoyer au client
        #Pour qu'il mette à jour sa vue
        return json.dumps({
            "event" : "explode",
            "x" : bomb["x"],
            "y" : bomb["y"],
            "radius" : bomb["radius"],
            "terrain" : self.terrain2D,
            "destroyed" : destroyed
        })
    def explodeTerrain(self,bomb):
        x = bomb["x"]
        y = bomb["y"]
        radius = bomb["radius"]
        destroyed_blocs = []
        #on part de la bombe puis on augmente 
        for destroyed in self.destroyOrdonnee(radius,x,y):
            destroyed_blocs.append(destroyed)
        for destroyed in self.destroyAbscisse(radius,x,y):
            destroyed_blocs.append(destroyed)
        return destroyed_blocs

    #un peu fait le sauvage mais tant pis
    def destroyOrdonnee(self,radius,x,y):
        destroyed = []
        for tx in range(x-radius, x+radius+1):
            if self.terrain2D[tx][y] in ["brick","air","bomb"] : #Pour pouvoir rajouter plus de destructibles
                self.terrain2D[tx][y] = "air"
                destroyed.append((tx, y))
        return destroyed

    def destroyAbscisse(self,radius,x,y):
        destroyed = []
        for ty in range(y-radius, y+radius+1): 
            if self.terrain2D[x][ty] in ["brick","air","bomb"] : #Pour pouvoir rajouter plus de destructibles
                self.terrain2D[x][ty] = "air"
                destroyed.append((x, ty))
        return destroyed
    def getUpdateTerrainData(self):
        return json.dumps({
            "event" : "updateTerrain",
            "terrain" : self.terrain2D
        })




  