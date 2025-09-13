async function send(event) {
let userQuery= document.getElementById("text").value;
let dataSent= await fetch("/query", 
}

document.getElementById("b1").addEventListener("click", send);
