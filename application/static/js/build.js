function getCells(){
    var cells = new Array(10);
    for(var i = 0; i < 10; i++){
        cells[i] = new Array(10);
        for(var j = 0; j < 10; j++){
            var row = (i+1).toString();
            var col = (j+1).toString();
            cells[i][j] = document.getElementById(row + "," + col);
        }
    }
    return cells;
}

function getBoard(){
    console.log("Got Here.");
    var cells = getCells();
    var board = Object();
    board.name = "Alex";
    board.ships = new Array();
    for(var i = 0; i < 10; i++){
        for(var j = 0; j < 10; j++){
            if(cells[i][j].checked){
                var ship = Object();
                ship.type = "fighter";
                ship.cells = Array.of({row:i,col:j});
                board.ships.push(ship);
            }
        }
    }
    console.log(JSON.stringify(board));
}