// global variable that is used to hold the cells where ships are placed
var onboard = Object();
onboard.shiplist = new Array(5);


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

function sendJSON(object){
    $.post("http://127.0.0.1:5000/create-board-endpoint", object, function(data,status){console.log("oop");document.location='/gameroom'},"json");
    };

function getBoard(){
    var cells = getCells();
    var board = Object();
    board.name = getUsername();
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
    sendJSON(JSON.stringify(board));

    console.log(JSON.stringify(board));

}

// function to add a ship with a specific type and it's associated cells to the board, the global variable
function add_ship_to_board(type,cells){
    // check validity of cells in future
    var ship = Object();
    ship.type = type;
    ship.cells = cells;
    window.onboard.shiplist.push(ship);
}