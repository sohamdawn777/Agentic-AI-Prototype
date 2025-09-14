window.addEventListener("DOMContentLoaded", (event) => {

function log(msg) {
    const container = document.getElementById("textPlace"); // or any div you want
    if (!container) return;

    const messageElement = document.createElement("div");
    messageElement.textContent = msg;
    container.appendChild(messageElement);
}

async function userCheck() {
let uid;
const firebase_api= await fetch("/apiKey");
const firebase_Api= await firebase_api.text();

const firebase_domain= await fetch("/authDomain");
const firebase_Domain= await firebase_domain.text();

const firebase_id= await fetch("/projectId");
const firebase_ID= await firebase_id.text();

const firebase_Id= await fetch("/appId");
const Firebase_Id= await firebase_Id.text();

const firebaseConfig={apiKey: firebase_Api,
  authDomain: firebase_Domain,
  projectId: firebase_ID,
  appId: Firebase_Id,
};
if (firebase.apps.length===0) {
firebase.initializeApp(firebaseConfig);
log("initialized");
}
try {
let alreadyFetched=false;
firebase.auth().onAuthStateChanged(async function (user) {
if (alreadyFetched===true) {
return;
}
else {
alreadyFetched=true;
if (user!==null) {
log("Logged In Anonymously.");
uid=user.uid;
}
else {
let userCreds=await firebase.auth().signInAnonymously();
log("Signed in with uid:",userCreds.user.uid);
uid=userCreds.user.uid;
}
log("ganga teri maili",uid);
let uidSent= await fetch("/users", {method: "POST", headers:{"Content-Type": "application/json"}, body:JSON.stringify({"uid":uid})});
}
});
}
}
catch (error) {
log(error);
}

async function send(event) {
let userQuery= document.getElementById("text").value;
document.getElementById("text").value="";
let dataSent= await fetch("/query", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({"query": userQuery})});
let dataReceived= await dataSent.json();

document.getElementById("textPlace").innerHTML+=`${dataReceived.resp}<br><br>`;
}

document.getElementById("b1").addEventListener("click", send);

userCheck();

});