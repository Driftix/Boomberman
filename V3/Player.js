
class Player{
    constructor(posX, posY, identifier, playable){
        this.playable = playable
        this.position = [posX,posY];
        this.identifier = identifier;
        this.playerElement = this.createElement();
    }
    
    createElement(){
        let playerElement = document.createElement("div");
        playerElement = this.addElementStyle(playerElement);
        playerElement.id = this.identifier;
        return playerElement;
    }
    addElementStyle(element){
        element.style.width = "10px";
        element.style.height = "10px";
        element.style.background = "blue";
        element.style.position = "inherit";
        element.style.padding = "0px";
        return element;
    }
    isPlayable(){
        return this.playable;
    }
}
export {Player};