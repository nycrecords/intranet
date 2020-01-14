let vid = document.getElementById("orientation-video");

function setCurTime(minutes, seconds) {
    vid.currentTime = (minutes * 60) + seconds;
}