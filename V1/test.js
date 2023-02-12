// Créer une instance de WebSocket en spécifiant l'URL du serveur
var socket = new WebSocket("ws://localhost:8001/");

// Lorsque la connexion est établie
socket.onopen = function() {
  // Envoyer un événement "connection" au serveur
  socket.send("connection");
};

// Lorsque le serveur envoie un message
socket.onmessage = function(event) {
  console.log("Reçu : " + event.data);
};

// Lorsque la connexion est fermée
socket.onclose = function() {
  console.log("Connexion fermée");
};

// Ajouter un écouteur d'événement pour détecter les touches du clavier
document.addEventListener("keydown", function(event) {
  // Envoyer l'événement "keydown" au serveur avec la touche appuyée
    if(socket.readyState === WebSocket.OPEN){
        console.log("keydown");
        socket.send("keydown:" + event.key);
    }
});
