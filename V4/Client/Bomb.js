
class Bomb{
    constructor(posX, posY){
        this.bombElement = this.createElement();
    }
    
    createElement(){
        let bombElement = document.createElement("div");
        bombElement = this.addElementStyle(bombElement);
        return bombElement;
    }
    addElementStyle(element){
        element.style.width = "10px";
        element.style.height = "10px";
        element.style.background = "red";
        element.style.position = "inherit";
        element.style.padding = "0px";
        return element;
    }
}
export {Bomb};