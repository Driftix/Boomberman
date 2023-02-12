import random
from bs4 import BeautifulSoup
import json
from Props.Air import Air
from Props.Brick import Brick
from Props.Wall import Wall
from Props.Bomb import Bomb

class Terrain :
    def __init__(self,width, height):
        self.width = width
        self.height = height
        print("Instantiation du terrain...")
        self.terrain = self.generateTerrain(width,height)
        print("Terrain Créé...")
        print("Instantiation du terrain 2D...")
        self.terrain2D = self.convertTerrainTo2D()
        print("Terrain 2D Créé...")

    def generateTerrain(self,width, height):
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
                choices = [Wall(), Brick(), Air()]
                weights = [0.12, 0.28, 0.6]
                td["class"] = random.choices(choices,weights=weights)[0]
            tbody.append(tr)
        return table

    def convertTerrainTo2D(self):
        cells = self.terrain.findAll("td")
        terrain2D = [[0 for x in range(self.width)] for y in range(self.height)] 
        for cell in cells:
            terrainX = int(cell['id'].split(',')[0])
            terrainY = int(cell['id'].split(',')[1])
            terrain2D[terrainX][terrainY] = cell['class']
        return terrain2D
    
    def convert2DToTerrain(self):
        soup = BeautifulSoup("", "html.parser")
        table = soup.new_tag("table")
        table["id"] = "table"
        table["border"] = "1"
        table["cellpadding"] = "5"
        table["cellspacing"] = "0"
        tbody = soup.new_tag("tbody")
        table.append(tbody)
        for i in range(len(self.terrain2D)):
            tr = soup.new_tag("tr")
            for j in range(len(self.terrain2D[i])):
                td = soup.new_tag("td")
                td["id"] = f"{i},{j}"
                td["class"] = self.terrain2D[i][j].className
                tr.append(td)
            tbody.append(tr)
        return table
    #Pour envoyer la donnée au client on reconvertis la map en Html
    def getDataClientTerrain(self):
        initTerrain = {
            "event" : "initTerrain",
            "terrain" : str(self.convert2DToTerrain())
        }
        return json.dumps(initTerrain)

    #Attention il envoie deux instructions à chaque fois c'est bizarre
    def canPlayerMove(self,player,x,y,old_x,old_y):
        '''En fait ici on va récupérer les infos de la map (bs4 => 2D)
        dans un tableau 2D pour pouvoir, via nos coordonnées, regarder si il y a une brique / mur / air etc'''
        #Si jamais essaye de sortir du tableau
        try : 
            if isinstance(self.terrain2D[x][y],(Wall,Brick,Bomb,player.__class__)):
                return False
            else:
                return True
        except IndexError:
            return False

   
    def placeBomb(self,pos,bomb):
        #on modifie la classe en bombe
        self.terrain2D[pos["x"]][pos["y"]] = bomb
    
    def getDataBombTerrain(self,pos,bomb):
        return json.dumps({
            "event" : "bombPlaced",
            "x" : pos["x"],
            "y": pos["y"],
            "radius" : bomb.getRadius(),
        })
    
    def explodeData(self,pos,bomb):

        destroyed = self.explodeTerrain(pos,bomb)
        #Après avoir détruit le terrain on récupère le tableau pour l'envoyer au client
        #Pour qu'il mette à jour sa vue
        return json.dumps({
            "event" : "explode",
            "radius" : bomb.getRadius(),
            "terrain" : self.terrain2D,
            "destroyed" : destroyed
        })
    
    def explodeTerrain(self,pos,bomb):
        x = pos["x"]
        y = pos["y"]
        radius = bomb.getRadius()
        destroyed_blocs = []
        #on part de la bombe puis on augmente

        for destroyed in self.destroyY(radius+1,x,y,1):
             destroyed_blocs.append(destroyed)
        for destroyed in self.destroyY(-radius-1,x,y,-1):
            destroyed_blocs.append(destroyed)
        for destroyed in self.destroyX(radius+1,x,y,1):
             destroyed_blocs.append(destroyed)
        for destroyed in self.destroyX(-radius-1,x,y,-1):
             destroyed_blocs.append(destroyed)
        return destroyed_blocs
    

    def getUpdateTerrainData(self):
        return json.dumps({
            "event" : "updateTerrain",
            "terrain" : self.terrain2D
        })


    #Pour aller vers le haut radius positif => step 1
    #Pour aller vers le bas radius négatif => step -1
    def destroyY(self,radius,x,y,step):
        destroyed = []
        for ty in range(y, y+radius,step): 
            try:
                #Pour la dispertion total
                if self.terrain2D[x][ty] in ["air","bomb"] : #Pour pouvoir rajouter plus de destructibles
                    self.terrain2D[x][ty] = "air"
                    destroyed.append((x, ty))
                #Pour l'arret d'une explosion
                elif self.terrain2D[x][ty] in ["wall"]:
                    break
                #Pour l'explosion d'une seule brique
                elif self.terrain2D[x][ty] in ["brick"]:
                    self.terrain2D[x][ty] = "air"
                    destroyed.append((x,ty))
                    break
            except IndexError:
                break
        return destroyed
    
    #Pour aller vers le haut radius positif => step 1
    #Pour aller vers le bas radius négatif => step -1
    def destroyX(self,radius,x,y,step):
        destroyed = []
        for tx in range(x, x+radius,step): 
            try:
                if self.terrain2D[tx][y] in ["air","bomb"] : #Pour pouvoir rajouter plus de destructibles
                    self.terrain2D[tx][y] = "air"
                    destroyed.append((tx, y))
                elif self.terrain2D[tx][y] in ["wall"]:
                    break
                elif self.terrain2D[tx][y] in ["brick"]:
                    self.terrain2D[tx][y] = "air"
                    destroyed.append((tx, y))
                    break
            except IndexError:
                break
        return destroyed





  
