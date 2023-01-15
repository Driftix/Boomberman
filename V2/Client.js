import { Player } from './Player.js';
import { Terrain } from './Terrain.js';

// Créer une instance de WebSocket en spécifiant l'URL du serveur
var socket = new WebSocket("ws://localhost:8001/");

//Récupération du joueur
let player;
let terrain;
//C'est les autres joueurs en gros
let guest = [];

// Lorsque la connexion est établie
socket.onopen = function() {
  // Envoyer un événement "connection" au serveur
  let connect = {
    "event" : "connect",
  }
  socket.send(JSON.stringify(connect));
};

// Lorsque le serveur envoie un message
socket.onmessage = function({data}) {
  data = JSON.parse(data)
  console.log("Reçu : " +data.event);
  switch(data.event){
    case "initPlayer":
      //Création du Terrain:
      //terrain = new Terrain(50,50);
      document.body.appendChild(terrain.getTable());
      //Créer le joueur sur le plateau createPlayer(identifier)
      createPlayer(data.identifier,true,0,0);
      //Et on rattache le client à son ID
      let event = {
        "event" : "iKnowMyName"
      }
      //On envoie l'event comme quoi le player est bien initialisé et se connait
      socket.send(JSON.stringify(event));
      break;
    case "newPlayer":
      createPlayer(data.identifier,false,0,0)
      break;
    case "move" :
      console.log("move")
      guest.forEach((g)=>{
        if(g.identifier == data.identifier){
          g.newPosition(data.x, data.y);
          terrain.movePlayer(g);
        }
      })
      //move(data.key, data.identifier);
      break;
    case "initTerrain":
      let body = document.getElementsByTagName("body")[0];
      body.innerHTML += data.terrain
      //document.body.appendChild(test);
      terrain = new Terrain();
      break;
  }
 
};

// Lorsque la connexion est fermée
socket.onclose = function() {
  console.log("Connexion fermée");
};

// Ajouter un écouteur d'événement pour détecter les touches du clavier
document.addEventListener("keydown", function(event) {
  //MoveClient déplace le joueur sur sa vue
  //si le client bouge on prépare ses coordonnées
  //En on envoie au serveur
  //Si on met à jour la position du joueur
  if(updatePosition(event.key, player)){
    //On met à jour sa position sur le terrain
    terrain.movePlayer(player);
    //On envoie au serveur sa nouvelle position
    let move = {
      "event" : "move",
      "x" : player.position[0],
      "y" : player.position[1],
      "identifier" : player.identifier
    }
    socket.send(JSON.stringify(move))
  }

});

function createPlayer(identifier,playable,x,y){
  //On va mettre le joueur dans une cellule
  //Voir pour modifier plus tard les coordonnées
  if(playable){
    player = new Player(x,y, identifier);
    terrain.addPlayer(player);
  }else{
    let guestPlayer = new Player(x,y,identifier);
    terrain.addPlayer(guestPlayer);
    guest.push(guestPlayer)
  }
}


function updatePosition(key,player){
  let position = player.getPosition();
  switch(key){
    case 'z':
      return move(position[0]-1, position[1]);
    case 's':
      return move(position[0]+1, position[1]);
    case 'd':
      return move(position[0] , position[1]+1);
    case 'q':
      return move(position[0],position[1]-1);
    default:
      action(key,player);
    /*
      player.newPosition(position[0], position[1]-1);
      return true;
    */
  }
}

function move(x,y){
    
  if(terrain.getTable().rows[x].cells[y].className != "wall" && terrain.getTable().rows[x].cells[y].className != "brick" ){
    //console.log(x + ":" + y);
    player.newPosition(x, y);
    return true;
  }else{
   return false; 
  }
}


function action(key,player){
  switch(key){
    case 'f':
      //createPlayer(2,false,x,y);
      setTimeout(function() {
        console.log("box  explode");
      }, 3000);
      if(player.getBomb().getQuantity() > 0){
        player.placeBomb(terrain);
      }
      break;
  }
}
