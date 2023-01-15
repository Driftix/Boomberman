class Bomb{
    constructor(){
        this.radius = 2;
        this.quantity = 2;
    }

    addRadius(radius){
        this.radius += radius;
    }
    setRadius(radius){
        this.radius = radius;
    }
    getQuantity(){
        return this.quantity;
    }
}
export {Bomb};