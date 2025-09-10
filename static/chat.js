async function onSuccess () {

}

window.onload = () => {
navigator.mediaDevices.getUserMedia({
audio: true, video: false, onSuccess, onError
});
}