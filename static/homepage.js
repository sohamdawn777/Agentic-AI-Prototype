async function send(event) {
let userQuery= document.getElementById("text").value;
let dataSent= await fetch("/query", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({"query": userQuery})});
let dataReceived= await dataSent.json();

document.getElementById("text").value="";
document.getElementById("textPlace").innerHTML+=`${dataReceived.resp}<br>`;
}

document.getElementById("b1").addEventListener("click", send);
