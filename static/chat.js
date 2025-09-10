window.onload = async () => {

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

const utterance= new SpeechSynthesisUtterance(text);
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
document.getElementById("chatSubs").textContent+=`${textList[i][0].transcript} `;
}
}
}

recognition.onspeechend = async () => {

const response= await fetch("/query", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({"query": text})});

speechSynthesis.speak(utterance);

}
}