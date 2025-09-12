window.onload = async () => {

let fillerWords= ["uh", "um", "er", "ah", "hmm", "like", "so", "well", "actually", "basically", "literally", "right", "ok", "okay"];

function endChat(event) {
recognition.stop();
//window.location.href="/results";
}

const SpeechRecognition= window.SpeechRecognition || window.webkitSpeechRecognition; 

const recognition= new SpeechRecognition(); 
recognition.lang= "en-US"; 
recognition.interimResults= true; 
recognition.continuous= true; 

let a=0;
let b=0;
let text=""; 
let textList;
let lastText="";
let paceText="";
let splitArray;
let splitArray2;
let count=0;

document.getElementById("chatSubs").textContent="";

const utterance= new SpeechSynthesisUtterance();
utterance.lang= "en-US";
utterance.pitch= "1.0";
utterance.rate= "1.0";
utterance.volume= "1.0";

recognition.start();

recognition.onresult = (event) => {
textList= event.results;
for (let i=0; i<=textList.length-1; i++) {
if (textList[i].isFinal===true) {
text+= textList[i][0].transcript;
}
else {
lastText= textList[i][0].transcript.slice(lastText.length, textList[i][0].transcript.length);

paceText+= lastText;

document.getElementById("chatSubs").textContent+= lastText;

splitArray= lastText.split(" ");
for (let j of splitArray) {
if (fillerWords.includes(j.toLowerCase())) {
count++;
document.getElementById("fillerWords").textContent= `Filler Word Count: ${count}`;
}
}
}
}
}

setInterval(() => {
splitArray2= paceText.split(" ");
paceText="";
let paceDiv= document.createElement("div");
paceDiv.id= "paceDiv";
paceDiv.textContent= `Pace (Last 30s) ${(splitArray2.length)*4}`;
document.body.appendChild(paceDiv);
a+=(splitArray2.length)*4;
b+=1;
},15000);

recognition.onspeechend = async () => {

let finalPace= document.createElement("div");
finalPace.id= "finalPace";
finalPace.textContent= `Average Pace: ${a/b}`;
document.body.appendChild(finalPace);

const response= await fetch("/query", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({"query": text})});

const res= await response.json();

utterance.text= res.resp;
speechSynthesis.speak(utterance);

}

document.getElementById("b2").addEventListener("click", endChat);
}