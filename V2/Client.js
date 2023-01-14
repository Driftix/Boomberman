import { Player } from './Player.js';
import { Terrain } from './Terrain.js';

// Créer une instance de WebSocket en spécifiant l'URL du serveur
var socket = new WebSocket("ws://localhost:8001/");

//Récupération du joueur
let player;
let playerID;
let terrain;

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
      terrain = new Terrain(50,50);
      document.body.appendChild(terrain.getTable());
      //Créer le joueur sur le plateau createPlayer(identifier)
      createPlayer(data.identifier);
      //Et on rattache le client à son ID
      playerID = data.identifier;
      let event = {
        "event" : "iKnowMyName"
      }
      //On envoie l'event comme quoi le player est bien initialisé et se connait
      socket.send(JSON.stringify(event));
      break;
    case "newPlayer":
      createPlayer(data.identifier)
      console.log(data.identifier)
      break;
    case "move" :
      console.log("move")
      move(data.key, data.identifier);
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
 /*
  if(move(event.key, playerID)){
    let move = {
      "event" : "move",
      "key": event.key,
      "identifier" : playerID,
    }
    socket.send(JSON.stringify(move));
  }

  */
});

function createPlayer(identifier){
  //On va mettre le joueur dans une cellule
  //Voir pour modifier plus tard les coordonnées
  player = new Player(0,0, identifier);
  terrain.addPlayer(player);
  /*
  var elemDiv = document.createElement('a');
  elemDiv.style.cssText = 'background-color:black; width:50px';
  elemDiv.id = identifier;
  elemDiv.textContent = identifier;
  document.body.appendChild(elemDiv);
  player = document.getElementById(identifier);
  player.style.position = "absolute";*/
}



function move(key, identifier){
  let p = document.getElementById(identifier);
  switch(key){
      case 'z':
          p.style.top = p.getBoundingClientRect().top - 5 + 'px';
          return true;
      case 's':
          p.style.top = p.getBoundingClientRect().top + 5 + 'px';
          return true;
      case 'd':
          p.style.left = p.getBoundingClientRect().left + 5 + 'px';
          return true;
      case 'q':
          p.style.left = p.getBoundingClientRect().left - 5 + 'px';
          return true;
  }
}

function updatePosition(key,player){
  
  let position = player.getPosition();
  switch(key){
    case 'z':
      //Pour pouvoir remonter
      player.newPosition(position[0] -1, position[1]);
      return true;
    case 's':
      player.newPosition(position[0] +1, position[1]);
      return true;
    case 'd':
      player.newPosition(position[0], position[1]+1);
      return true;
    case 'q':
      player.newPosition(position[0], position[1])-1;
      return true;
  }
}
