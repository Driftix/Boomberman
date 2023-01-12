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

const websocket = new WebSocket("ws://localhost:8001/");

function connecting(websocket){
    websocket.addEventListener("open",(e) =>{
        let event = {type:"connect"}
        websocket.send(JSON.stringify(event));
    });
}
/*
async function disconnect(websocket){
    let event = {type:"disconnect"}
    websocket.send(JSON.stringify(event))
}*/

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