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

let text; 

const utterance= new SpeechSynthesisUtterance(text);
utterance.lang= "en-US";
utterance.pitch= "1.0";
utterance.rate= "1.0";
utterance.volume= "1.0";


recognition.onspeechend = async () => {

recognition.onresult = async (event) => {
text= await event.results;
}

const response= await fetch("/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({"query": text})});

speechSynthesis.speak(utterance);

}
}