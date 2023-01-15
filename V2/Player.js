import { Bomb } from "./Bomb.js";

class Player{
    constructor(posX, posY, identifier){
        this.position = [posX,posY];
        this.identifier = identifier;
        this.playerElement = document.createElement("div");
        this.playerElement = this.addStyle(this.playerElement);
        this.playerElement.id = identifier;
        this.playerBomb = new Bomb();
    }
    addStyle(element){
        element.style.width = "10px";
        element.style.height = "10px";
        element.style.background = "red";
        element.style.position = "inherit";
        element.style.padding = "0px";
        return element;
    }
    newPosition(x,y){
        this.position = [x,y];
    }
    getPosition(){
        return this.position;
    }
    getID(){
        return this.identifier;
    }
    placeBomb(terrain){
        terrain.explode(this.position[0], this.position[1], this.playerBomb.radius)
    }
    getBomb(){
        return this.playerBomb;
    }
}
export {Player};