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
        if(cellClass == "brick" or cellClass == "wall"):
            return False
        else:
            return True
        '''for cell in cells:
            terrainX = int(cell['id'].split(',')[0])
            terrainY = int(cell['id'].split(',')[1])
            if(terrainX == x and terrainY == y):
                #print("x:{} / y:{} / cellule:{}".format(x,y,cell['class']))
                if(cell['class'] == "brick" or cell['class'] == "wall"):
                    return False
                else :
                    return True
                #terrain2D[x][y] = cell['class']'''

    def convertTerrainTo2D(self):
        cells = self.terrain.findAll("td")
        terrain2D = [[0 for x in range(self.width)] for y in range(self.height)] 
        for cell in cells:
            terrainX = int(cell['id'].split(',')[0])
            terrainY = int(cell['id'].split(',')[1])
            terrain2D[terrainX][terrainY] = cell['class']
        return terrain2D
    
    def placeBomb(player):
        #mettre un timer
        #Quand le timer sera arrivé au bout il faudra envoyer la nouvelle carte au client
        print("bombPlaced")

  