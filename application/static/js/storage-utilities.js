function setUsername(username){
    localStorage.setItem("username", username);
}

function getUsername(){
    localStorage.getItem("username");
}

function setRoomName(roomName){
    localStorage.setItem("roomName", roomName);
}

function getRoomName(){
    localStorage.getItem("roomName");
}

function clearLocalStorage(){
    localStorage.removeItem("username");
    localStorage.removeItem("roomName");
}