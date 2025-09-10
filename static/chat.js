window.onload = async () => {
try {
const voice= await navigator.mediaDevices.getUserMedia({
audio: true, video: false });
}
catch (error) {
console.log(error);
}
}