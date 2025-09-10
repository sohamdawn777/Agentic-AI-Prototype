window.onload = async () => {

let fillerWords= ["uh", "um", "er", "ah", "hmm", "like", "so", "well", "actually", "basically", "literally", "right", "ok", "okay"];

try {
const voice= await navigator.mediaDevices.getUserMedia({
audio: true, video: false });
}
catch (error) {
console.log(error);
}

const SpeechRecognition= window.SpeechRecognition || window.webkitSpeechRecognition; 

const recognition= new SpeechRecognition(); 
recognition.lang= "en-US"; 
recognition.interimResults= true; 
recognition.continuous= true; 

let text=""; 
let textList;
let lastText="";
let splitArray;

const utterance= new SpeechSynthesisUtterance();
utterance.lang= "en-US";
utterance.pitch= "1.0";
utterance.rate= "1.0";
utterance.volume= "1.0";

recognition.onresult = (event) => {
textList= event.results;
for (let i=0; i<=textList.length-1; i++) {
if (textList[i].isFinal===true) {
text+=textList[i][0].transcript;
}
else {
lastText= textList[i][0].transcript.slice(lastText.length, textList[i][0].transcript.length);

document.getElementById("chatSubs").textContent+= lastText;

splitArray= lastText.split(" ");
for (let j of splitArray) {
if (fillerWords.includes(j.toLowerCase)) {
document.getElementById("fillerWords").textContent+=1;
}
}
}
}
}

recognition.onspeechend = async () => {

const response= await fetch("/query", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({"query": text})});

utterance.text= text;
speechSynthesis.speak(utterance);

}
}