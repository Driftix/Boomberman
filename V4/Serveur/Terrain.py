import asyncio
import random
from bs4 import BeautifulSoup
import json
from Props.Bonus_add_bomb import Bonus_add_bomb
from Props.Bonus_extension import Bonus_extension
from Props.Air import Air
from Props.Brick import Brick
from Props.Wall import Wall
from Props.Bomb import Bomb
from Player import Player

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
            "event" : "updateTerrain",
            "terrain" : str(self.convert2DToTerrain())
        }
        return json.dumps(initTerrain)

    #Attention il envoie deux instructions à chaque fois c'est bizarre
    def canPlayerMove(self,x,y):
        '''En fait ici on va récupérer les infos de la map (bs4 => 2D)
        dans un tableau 2D pour pouvoir, via nos coordonnées, regarder si il y a une brique / mur / air etc'''
        #Si jamais essaye de sortir du tableau
        try : 
            if isinstance(self.terrain2D[x][y],(Wall,Brick,Bomb)):
                return False
            else:                    
                return True
        except IndexError:
            return False
    def addPlayer(self,player):
        playerCount = 0
        if(isinstance(self.terrain2D[0][0], Player)):
            print("instance joueur")
        for row in self.terrain2D:
            for cell in row :
                if isinstance(cell,Player):
                    playerCount += 1
        if playerCount == 0:
            player.position[0] = 0
            player.position[1] = 0
        elif playerCount == 1:
            player.position[0] = 0
            player.position[1] = len(self.terrain2D)-1
        elif playerCount == 2:
            player.position[0] = len(self.terrain2D)-1
            player.position[1] = 0
        elif playerCount == 3:
            player.position[0] = len(self.terrain2D)-1
            player.position[1] = len(self.terrain2D)-1
        self.terrain2D[player.position[0]][player.position[1]] = player
    
    def updatePlayer(self,player,x,y):
        #On remet de l'air sur l'ancienne position
        if(not isinstance(self.terrain2D[player.position[0]][player.position[1]],Bomb)):
            self.terrain2D[player.position[0]][player.position[1]] = Air()
        if(isinstance(self.terrain2D[x][y], Bonus_extension)):
            player.bomb.radius += 1
        elif(isinstance(self.terrain2D[x][y], Bonus_add_bomb)):
            player.bomb.quantity +=1
        #On déplace le joueur sur la carte
        self.terrain2D[x][y] = player
        #maj position joueur
        player.position[0] = x
        player.position[1] = y
        print("terrain: {}".format("update"))

    def placeBomb(self,x,y,bomb):
        self.terrain2D[x][y] = bomb

    def destroyTerrainBomb(self,x,y,bomb):
        self.terrain2D[x][y] = Air()
        return self.explodeTerrain(x,y,bomb)
  

    def explodeTerrain(self,x,y, bomb):
        radius = bomb.radius
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

    def destroyY(self,radius,x,y,step):
        destroyed = []
        for ty in range(y, y+radius,step): 
            try:
                #Pour la dispertion total
                if isinstance(self.terrain2D[x][ty],(Air,Bomb)): #Pour pouvoir rajouter plus de destructibles
                    self.terrain2D[x][ty] = Air()
                    destroyed.append((x, ty))
                     #Pour l'explosion d'une seule brique
                elif isinstance(self.terrain2D[x][ty],Brick):
                    #Rajouter un random pour mettre un bonus
                    choices = [Air(), Bonus_extension(),Bonus_add_bomb()]
                    weights = [0.88,0.06,0.06]
                    self.terrain2D[x][ty] = random.choices(choices,weights=weights)[0]
                    #self.terrain2D[x][ty] =  Air()
                    destroyed.append((x,ty))
                    break
                elif isinstance(self.terrain2D[x][ty], Player):
                    self.terrain2D[x][ty].isAlive = False
                    self.terrain2D[x][ty] = Air()
                    break
                #Pour l'arret d'une explosion
                elif isinstance(self.terrain2D[x][ty],Wall):
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
                if isinstance(self.terrain2D[tx][y],(Air,Bomb)) : #Pour pouvoir rajouter plus de destructibles
                    self.terrain2D[tx][y] = Air()
                    destroyed.append((tx, y))
                elif isinstance(self.terrain2D[tx][y], Brick):
                    #Rajouter un random pour mettre un bonus
                    choices = [Air(), Bonus_extension(), Bonus_add_bomb()]
                    weights = [0.88,0.06,0.06]
                    self.terrain2D[tx][y] = random.choices(choices,weights=weights)[0]
                    #self.terrain2D[tx][y] = Air()
                    destroyed.append((tx, y))
                    break
                elif isinstance(self.terrain2D[tx][y],Player):
                    self.terrain2D[tx][y].isAlive = False
                    self.terrain2D[tx][y] = Air()
                    destroyed.append((tx, y))
                    break
                elif isinstance(self.terrain2D[tx][y],Wall):
                    break
            except IndexError:
                break
        return destroyed

  
