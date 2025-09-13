async function send(event) {
let userQuery= document.getElementById("text").value;
let dataSent= await fetch("/query", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({"query": userQuery})});
let dataReceived= await dataSent.json();
document.getElementById("textPlace").textContent+=`${dataReceived}<br>`;
}

document.getElementById("b1").addEventListener("click", send);
