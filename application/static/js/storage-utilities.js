function setUsername(username){
    sessionStorage.setItem("username", username);
}

function getUsername(){
    return sessionStorage.getItem("username");
}

function setRoomName(roomName){
    sessionStorage.setItem("roomName", roomName);
}

function getRoomName(){
    return sessionStorage.getItem("roomName");
}

function clearLocalStorage(){
    sessionStorage.removeItem("username");
    sessionStorage.removeItem("roomName");
}