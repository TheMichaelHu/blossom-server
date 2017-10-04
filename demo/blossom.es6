const tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
const firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

const {videoId, triggers} = emotions;
const times = Object.keys(triggers).map(key => triggers[key].time)
const server_url = "10.148.10.186"
const server_port = "5555"

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
let player = undefined;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '720',
    width: '1280',
    videoId,
    events: {
      'onReady': onPlayerReady,
    }
  });
}

let timeupdater = null;
let clearEmotion = null;
let videotime = 0;
let nextEmotion = 0;
let endEmotion = 0;

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
  event.target.playVideo();

  function updateTime() {
    var oldTime = videotime;
    if(player && player.getCurrentTime) {
      videotime = player.getCurrentTime();
    }
    if(videotime !== oldTime) {
      timecode.innerHTML = pad(videotime.toFixed(1),5);
      checkEmotion(Math.round(videotime * 1000));
    }
  }

  timeupdater = setInterval(updateTime, 100);
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done = false;

function pad(num, size) {
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}

function checkEmotion(time) {
  if (time > triggers[nextEmotion].time) {
    nextEmotion = getNextEmotion(time);
  }

  em = triggers[nextEmotion];
  if (Math.abs(em.time - time) <= 150) {
    console.log(em);
    triggerEmotion(em);
  }
}

// bin search for next emotion
function getNextEmotion(time) {
  let [start, end] = [nextEmotion, times.length - 1];
  while(end - start > 1) {
    const mid = Math.floor((start + end)/2)
    if (times[mid] < time) {
      start = mid;
    } else {
      end = mid;
    }
  }
  return end;
}

function triggerEmotion(em) {
  clearTimeout(clearEmotion);
  emotion.innerHTML = em.emotion;
  handleEmotion(em)

  if (!em.duration) {
    em.duration = 99999999;
  }
  clearEmotion = setTimeout(triggerEmotion, em.duration, {"emotion": "*", "gesture": "idle", "duration": 999999999});
}

function handleEmotion(em) {
  console.log(em);
  url = server_url+':'+server_port;
  msg = "http://"+url+"/s/" + em.gesture;

  emotion.innerHTML = em.emotion + " -> " + msg;
  $.get(msg, function(data, status){});
}
