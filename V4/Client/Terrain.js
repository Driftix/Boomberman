import { Player } from "./Player.js";
import {Bomb} from "./Bomb.js";

class Terrain{
    constructor(){
        this.table = document.getElementById("table");
        this.players = [];
    }
    addPlayer(identifier,x,y,playable){
        let player = new Player(x,y,identifier,playable)
        this.players.push(player);
        this.table.rows[player.position[0]].cells[player.position[1]].appendChild(player.playerElement);
        this.table.rows[player.position[0]].cells[player.position[1]].style.background = "blue";
        //console.log(this.table.rows[player.position[0]].cells[player.position[1]].style.backgr)
    }   
    getPlayers(){
        return this.players;
    }
    
    movePlayer(identifier,x,y){
        this.players.forEach((player) =>{
            if(player.identifier == identifier)
            {
                //On met à jour le joueur
                this.table.rows[player.position[0]].cells[player.position[1]].style.background = "";

                player.position[0] = x;
                player.position[1] = y;
                //on met à jour sa position sur le tableau
                this.table.rows[player.position[0]].cells[player.position[1]].appendChild(player.playerElement);
                this.table.rows[player.position[0]].cells[player.position[1]].style.background = "blue";

            }
        })
    }
    placeBomb(x,y){
        let bomb = new Bomb(x,y)
        this.table.rows[x].cells[y].className = "bomb";
    }

    async animate(destroyed_bloc){
        destroyed_bloc.forEach((bloc) => {
            if(this.table.rows[bloc[0]].cells[bloc[1]] != undefined && this.table.rows[bloc[0]].cells != undefined){
                //this.table.rows[bloc[0]].cells[bloc[1]].style.backgroundColor = "red";
                this.table.rows[bloc[0]].cells[bloc[1]].className = "anim";
            }
        })
    }
    update(terrain){
             /*la config de terrain est la suivante => 
            terrain[0] => ligne du tableau
            terrain[0][0] => colonne
            => retourne un nom de classe
            */
            setTimeout(() => {
            const size = [terrain.length, terrain[0].length]
            for(let i = 0; i < size[1]; i++){
                for(let j=0; j < size[0]; j++){
                   
                    let cell = this.table.rows[i].cells[j];
                    if(cell.className != terrain[i][j]){
                        this.table.rows[i].cells[j].className = "air";

                        /*
                        if(!this.table.rows[i].cells[j].className == "bomb"){
                            this.table.rows[i].cells[j].className = "air";
                        }*/
                    }
                }
            }
        }, 200);
    }
}
export {Terrain};
