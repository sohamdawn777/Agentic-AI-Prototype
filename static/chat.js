window.onload = async () => {

//Asking the User for Microphone Access

try {
const voice= await navigator.mediaDevices.getUserMedia({
audio: true, video: false });
}
catch (error) {
console.log(error);
}

//Web Speech API Setup (Voice--->Text)

const SpeechRecognition= window.SpeechRecognition || window.webkitSpeechRecognition; //some browsers expose the web speech api directly or some with the webkit prefix...the || sign is bitwise OR so if direct Web Speech is found exposed it uses that otherwise it falls back to the webkit prefix fallback


const recognition= new SpeechRecognition(); //Creating A Web Speech API voice recognition class

recognition.lang= "en-US"; //the language code of the voice to be recognized

recognition.interimResults= true; //

recognition.continuous= true; //does not let the voice capturing stop after one sentence

let text; 

const utterance= new SpeechSynthesisUtterance(text);
utterance.lang= "en-US";
utterance.pitch= "1.0";
utterance.rate= "1.0";
utterance.volume= "1.0";


recognition.onspeechend = async () => {

recognition.onresult = async(event) => {
text= await event.results;
}

const response= await fetch("/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({"query": text})});

speechSynthesis.speak(utterance);

}

recognition.start();

}