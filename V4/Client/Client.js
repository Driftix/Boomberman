
// Créer une instance de WebSocket en spécifiant l'URL du serveur
var socket = new WebSocket("ws://localhost:8001/");

let key;
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
    //Pour join ou start on renvoie l'event join
    case "start":
      alert("Party Code: " +  data.key)
      socket.send(JSON.stringify({"event":"join","key":data.key}))
      document.getElementById("pre-game").style.display = "none";
      document.getElementById("game-stats").style.display = "block";
      //On met à jour la clé du jeu
      key = data.key
      break;
    case "updateTerrain":
      if(document.getElementById("table") == undefined){
        //Si le terrain existe pas on l'ajoute
        let body = document.getElementsByTagName("body")[0];
        body.innerHTML += data.terrain
      }else{
        //Si le terrain existe on le met à jour
        document.getElementById("table").remove();
        let body = document.getElementsByTagName("body")[0];
        body.innerHTML += data.terrain
      }
    break;
    case "animate":
      data.destroyed.forEach((bloc) => {
        try{
            document.getElementById("table").rows[bloc[0]].cells[bloc[1]].className = "anim";
        }catch (undefined){
          console.log("skip")
        }
        
    })
    break;
    case "updateBomb":
      document.getElementById("bombquantity").textContent = data.qty;
  }
};

/*Mouvements */
document.addEventListener("keydown", function(event) {
  console.log(key)
  if(key != undefined){
    let direction = "none";
    switch(event.key){
      case 'z':
        direction="up"
        break;d
      case 's':
        direction="down"
        break;
      case 'd':
        direction="right"
        break;
      case 'q':
        direction="left"
        break;
      case 'f':
        let placeBomb ={
          "event" : "placeBomb",
        }
        socket.send(JSON.stringify(placeBomb))
      break;
    }
    let updateMove = {
      "event" : "move",
      "direction" : direction,
      "key" : key
    }
    socket.send(JSON.stringify(updateMove))
  }
});

/* Gestion lancement du jeu */
document.getElementById("createGame").addEventListener("click",()=>{
  socket.send(JSON.stringify({
    "event": "start",
  }))
})
document.getElementById("joinGame").addEventListener("click",()=>{
  key = document.getElementById("joinURL").value
  socket.send(JSON.stringify({
    "event":"join",
    "key" : key
  }));
  document.getElementById("pre-game").style.display = "none";
  document.getElementById("game-stats").style.display = "block";
})

  
