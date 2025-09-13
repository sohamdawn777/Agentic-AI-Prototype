window.onload = async() => {

function endChat(event) {
recognition.stop();
}

const SpeechRecognition= window.SpeechRecognition || window.webkitSpeechRecognition; 

const recognition= new SpeechRecognition(); 
recognition.lang= "en-US"; 
recognition.interimResults= true; 
recognition.continuous= true; 

let text=""; 
let textList;
let interimText="";

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
if (i===textList.length-1) {
interimText= textList[i][0].transcript;
document.getElementById("chatSubs").textContent= interimText;
}
}
}
}

recognition.onspeechend = async () => {

const response= await fetch("/query", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({"query": text})});

const res= await response.json();

utterance.text= res.resp;
await speechSynthesis.speak(utterance);

recognition.start();

}

document.getElementById("b2").addEventListener("click", endChat);
}