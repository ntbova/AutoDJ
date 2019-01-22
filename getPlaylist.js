const sources = {
  'rain': 'https://open.spotify.com/embed/user/1224963539/playlist/2b2F19SPplHxbrDPBUN9XG',
  'new york': 'https://open.spotify.com/embed/user/1224963539/playlist/3pS0p7Lrqu4DFMpFkKhUVp',
  'places': 'https://open.spotify.com/embed/user/1224963539/playlist/36DfTg9bztkYD1DN91N3tk',
}
window.onload = function() {
  document.getElementById('setTopicButton').onclick = function() {
    const topic = document.getElementById('topicName').value;
    document.getElementById('topicName').value = '';
    const iframeSrc = sources[topic.toLowerCase()];
    document.getElementById('player-frame').src = iframeSrc;
  }
}