class Terrain{
    constructor(width, height){
        this.table = document.createElement("table");
        this.table.setAttribute("id", "table");
        this.table.setAttribute("border", "1");
        this.table.setAttribute("cellpadding", "5");
        this.table.setAttribute("cellspacing", "0");

        this.tbody = document.createElement("tbody");
        this.table.appendChild(this.tbody);

        for (let i = 0; i < width; i++) {
            let tr = document.createElement("tr");
            for (let j = 0; j < height; j++) {
                let td = document.createElement("td");
                td.setAttribute("id", i + "," + j);
                tr.appendChild(td);
            }
            this.tbody.appendChild(tr);
        }
    }
    addPlayer(player){
        console.log(player.position)
        table.rows[player.position[0]].cells[player.position[1]].appendChild(player.playerElement);
    }
    movePlayer(player){
        table.rows[player.position[0]].cells[player.position[1]].appendChild(player.playerElement);
    }
    getTable(){
        return this.table;
    }
}
export {Terrain};
