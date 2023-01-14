/*
let move = document.getElementById("move")
move.style.position = "absolute";

document.addEventListener("keypress", function(event) {
    switch(event.key){
        case 'z':
            move.style.top = move.getBoundingClientRect().top - 5 + 'px';
            break;
        case 's':
            move.style.top = move.getBoundingClientRect().top + 5 + 'px';
            break;
        case 'd':
            move.style.left = move.getBoundingClientRect().left + 5 + 'px';
            break;
        case 'q':
            move.style.left = move.getBoundingClientRect().left - 5 + 'px';
            break;
    }
});*/
/*
function initGame(websocket){
    websocket.addEventListener("open",() =>{
        const params = new URLSearchParams(window.location.search);
        let event = {type:"init"}
        if(params.has("join")){
            event.join = params.get("join");
        }else{

        }
        console.log(event)
        websocket.send(JSON.stringify(event));
    });
}



window.addEventListener("DOMContentLoaded",()=>{
    const websocket = new WebSocket("ws://10.132.149.18:8001/");
    initGame(websocket);
});*/

/*
async function disconnect(websocket){
    let event = {type:"disconnect"}
    websocket.send(JSON.stringify(event))
}*/



/*
const websocket = new WebSocket("ws://localhost:8001/");
//On fait genre de générer un cookie
document.cookie = Math.floor(Math.random() * 10000000000000);

window.addEventListener("DOMContentLoaded",()=>{
    connecting(websocket);
});

function connecting(websocket){
    websocket.addEventListener("open",(e) =>{
        let connectEvent = {
            "event" : "Connect",
            "identifier" : document.cookie
        }
        websocket.send(JSON.stringify(connectEvent));
    });
}

document.addEventListener("keypress", function(event) {
    switch(event.key){
        case 'z':
            move.style.top = move.getBoundingClientRect().top - 5 + 'px';
            break;
        case 's':
            move.style.top = move.getBoundingClientRect().top + 5 + 'px';
            break;
        case 'd':
            move.style.left = move.getBoundingClientRect().left + 5 + 'px';
            break;
        case 'q':
            move.style.left = move.getBoundingClientRect().left - 5 + 'px';
            break;
    }
    let moveEvent = {
        "event" : "Move",
        "identifier" : document.cookie,
        "x" : 2,
        "y" : 5
    }
        websocket.send(JSON.stringify(moveEvent));
  });


*/


/*-----------------*\
/*
const websocket = new WebSocket("ws://localhost:8001/");

function connecting(websocket){
    websocket.addEventListener("open",(e) =>{
        let event = {type:"connect"}
        websocket.send(JSON.stringify(event));
    });
}
window.addEventListener("DOMContentLoaded",()=>{
    connecting(websocket);
   
});

function receiveMoves(board,websocket){
    websocket.addEventListener("message",({data})=>{
        const event = JSON.parse(data);
        switch(event.type){
            case "init":
                move(event.coo_x, event.coo_y, event.id);
        }

    });
}
*/
let socketIP = "ws://localhost:8001/";
let socket = new WebSocket(socketIP);
//On fait genre de générer un cookie
document.cookie = Math.floor(Math.random() * 10000000000000);


//Au chargement de la page, event de connection
window.addEventListener("DOMContentLoaded",()=>{    
    socket.onopen = function(e) {
        let connectEvent = {
            "event" : "Connect",
            "identifier" : document.cookie
        }   
        socket.send(JSON.stringify(connectEvent)); 
        //essayer de lettre l'event listener keypressed ici 
        document.addEventListener("keypress",function(event){
            console.log("keypressed");
            socket.send("tarace");
        }); 
    };
});


document.addEventListener("keypress", function(event) {
    moveClient(event.key);
    console.log(event.key);
    let moveEvent = {
        "event" : "Move",
        "identifier" : document.cookie,
        "x" : 2,
        "y" : 5
    }
    //Obligé de réouvrir la connexion WebSocket
    let socket = new WebSocket(socketIP);    
    socket.onopen = function(e) {
        socket.send(JSON.stringify(moveEvent));
        console.log("Data sent")
    };
    socket.onmessage = function({data}){
        data = JSON.parse(data);
        console.log(IsPlayer(data.identifier));
        //console.log(IsPlayer(JSON.parse(e)[]));
    }
    
});

function moveClient(key){
    switch(key){
        case 'z':
            move.style.top = move.getBoundingClientRect().top - 5 + 'px';
            break;
        case 's':
            move.style.top = move.getBoundingClientRect().top + 5 + 'px';
            break;
        case 'd':
            move.style.left = move.getBoundingClientRect().left + 5 + 'px';
            break;
        case 'q':
            move.style.left = move.getBoundingClientRect().left - 5 + 'px';
            break;
    }
}

function IsPlayer(playerID){
    return (playerID == document.cookie)?  true :  false;
}

socket.onmessage = function(event) {
  alert(`[message] Data received from server: ${event.data}`);
};

socket.onclose = function(event) {
    if (event.wasClean) {
        console.log("Connexion fermée");
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log("Erreur de fermeture");
    }
};

socket.onerror = function(error) {
  alert(`[error]`);
};