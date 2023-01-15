import { Terrain } from "./Terrain.js";

// Créer une instance de WebSocket en spécifiant l'URL du serveur
var socket = new WebSocket("ws://localhost:8001/");

let terrain;

// Lorsque la connexion est établie
socket.onopen = function() {
  // Envoyer un événement "connection" au serveur
  let connect = {
    "event" : "connect",
  }
  console.log("Connecting...")
  socket.send(JSON.stringify(connect));
};

// Lorsque le serveur envoie un message
socket.onmessage = function({data}) {
  data = JSON.parse(data)
  console.log("Reçu : " +data.event);
  switch(data.event){
    case "explode":
      //on récupère la partie de la carte détruite pour faire une anim à l'endroit de l'explosion
      //puis on met à jour le visuel de la carte côté client !
      terrain.animate(data.destroyed).then(()=>terrain.update(data.terrain));
      break;
    case "updateTerrain":
      terrain.update(data.terrain);
      break;
    case "bombPlaced":
      terrain.placeBomb(data.x, data.y);
      break;
    case "initPlayer":
      terrain.addPlayer(data.identifier, data.x, data.y, data.playable);
      break;
    case "confirmMove" :
      terrain.movePlayer(data.identifier, data.x, data.y);
      break;
    case "initTerrain":
      console.log("InitTerrain...")
      let body = document.getElementsByTagName("body")[0];
      body.innerHTML += data.terrain
      //On met juste en memoire le terrain envoyé par le serveur
      //Pour pouvoir faire des actions dessus
      terrain = new Terrain()
    break;
  }
};

document.addEventListener("keydown", function(event) {
  terrain.getPlayers().forEach((player) => {
    if(player.playable){
      let positionX = player.position[0];
      let positionY = player.position[1];
      switch(event.key){
        case 'z':
          positionX--;
          break;
        case 's':
          positionX ++;
          break;
        case 'd':
          positionY++;
          break;
        case 'q':
          positionY--;
          break;
        case 'f':
            let placeBomb ={
              "event" : "placeBomb",
              "x" : positionX,
              "y" : positionY,
            }
            socket.send(JSON.stringify(placeBomb))
          break;
      }
      let move = {
        "event" : "move",
        "x" : positionX,
        "y" : positionY,
      }
      socket.send(JSON.stringify(move))
    }
  });

});

