class Terrain{
    constructor(){
        this.table = document.getElementById("table");
    }
    addPlayer(player){
        console.log(player.position)
        this.table.rows[player.position[0]].cells[player.position[1]].appendChild(player.playerElement);
    }
    movePlayer(player){
        this.table.rows[player.position[0]].cells[player.position[1]].appendChild(player.playerElement);
    }
    getTable(){
        return this.table;
    }
    explode(x,y,r){
        console.log(x + ":"+y);
        console.log(this.table.rows[x].cells[y].className);
        //à modifier totalement
        for(let xmax = x; xmax < x + r; xmax++){
            if(this.table.rows[xmax].cells[y].className == "brick" && this.table.rows[xmax].cells[y].className == "air"){
                this.table.rows[xmax].cells[y].className = "air";
                break;
            }
        }
        for(let xmin = x; xmin < x - r; xmin--){
            if(this.table.rows[xmin].cells[y].className == "brick" && this.table.rows[xmin].cells[y].className == "air"){
                this.table.rows[xmin].cells[y].className = "air";
                break;
            }
        }
        for(let ymax = y; ymax < y + r; ymax++ ){
            if(this.table.rows[x].cells[ymax].className == "brick" && this.table.rows[x].cells[ymax].className == "air"){
                this.table.rows[x].cells[ymax].className = "air";
                break;
            }
        }
        for(let ymin = y; ymin < y- r; ymin++ ){
            if(this.table.rows[x].cells[ymin].className == "brick" && this.table.rows[x].cells[ymin].className == "air"){
                this.table.rows[x].cells[ymin].className = "air";
                break;
            }
        }
    }
   
}
export {Terrain};
