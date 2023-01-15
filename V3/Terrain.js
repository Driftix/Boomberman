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
    }
    getPlayers(){
        return this.players;
    }
    
    movePlayer(identifier,x,y){
        this.players.forEach((player) =>{
            if(player.identifier == identifier)
            {
                //On met à jour le joueur
                player.position[0] = x;
                player.position[1] = y;
                //on met à jour sa position sur le tableau
                this.table.rows[player.position[0]].cells[player.position[1]].appendChild(player.playerElement);
            }
        })
    }
    placeBomb(x,y){
        let bomb = new Bomb(x,y)
        this.table.rows[x].cells[y].appendChild(bomb.bombElement);
    }

    async animate(destroyed_blocs){
        destroyed_blocs.forEach((bloc) =>{
           
                //On verifie que la case soit accessible, sinon l'erreur coupe le script
                if(this.table.rows[bloc[0]].cells[bloc[1]] != undefined && this.table.rows[bloc[0]].cells != undefined){
                    this.table.rows[bloc[0]].cells[bloc[1]].style.backgroundColor = "red";
                }
                console.log("animation timeout")
    
        })
    }
    update(destroyed_blocs){
        setInterval(() => {
        destroyed_blocs.forEach((bloc) =>{
            //On verifie que la case soit accessible, sinon l'erreur coupe le script
            if(this.table.rows[bloc[0]].cells[bloc[1]] != undefined && this.table.rows[bloc[0]].cells != undefined){
                this.table.rows[bloc[0]].cells[bloc[1]].className = "air";
                this.table.rows[bloc[0]].cells[bloc[1]].style.backgroundColor = "";

            }
        })
        }, 200);
    }
}
export {Terrain};
