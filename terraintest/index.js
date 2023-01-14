
import { Terrain } from './Terrain.js';
let rect = document.createElement("div");
rect.style.width = "10px";
rect.style.height = "10px";
rect.style.background = "red";
rect.style.position = "inherit";
rect.style.padding = "0px";
let table = document.getElementById("table");
let currPos = [0,0];

let t = new Terrain(50,50);
document.body.appendChild(t.getTable());
t.addPlayer(rect);


/*
document.addEventListener("keydown", function(event) {
    switch (event.keyCode) {
        case 37: // left arrow
            moveLeft();
            break;
        case 38: // up arrow
            moveUp();
            break;
        case 39: // right arrow
            moveRight();
            break;
        case 40: // down arrow
            moveDown();
            break;
    }
});

function moveLeft() {
    if(currPos[1] > 0) {
        table.rows[currPos[0]].cells[currPos[1]].removeChild(rect);
        currPos[1]--;
        table.rows[currPos[0]].cells[currPos[1]].appendChild(rect);
    }
}

function moveUp() {
    if(currPos[0] > 0) {
        table.rows[currPos[0]].cells[currPos[1]].removeChild(rect);
        currPos[0]--;
        table.rows[currPos[0]].cells[currPos[1]].appendChild(rect);
    }
}

function moveRight() {
    if(currPos[1] < 4) {
        table.rows[currPos[0]].cells[currPos[1]].removeChild(rect);
        currPos[1]++;
        table.rows[currPos[0]].cells[currPos[1]].appendChild(rect);
    }
}

function moveDown() {
    if(currPos[0] < 4) {
        table.rows[currPos[0]].cells[currPos[1]].removeChild(rect);
        currPos[0]++;
        table.rows[currPos[0]].cells[currPos[1]].appendChild(rect);
    }
}
*/