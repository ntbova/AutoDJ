const sources = {
  'rain': 'https://open.spotify.com/embed/user/1224963539/playlist/2b2F19SPplHxbrDPBUN9XG',
  'new york': 'https://open.spotify.com/embed/user/1224963539/playlist/3pS0p7Lrqu4DFMpFkKhUVp',
  'places': 'https://open.spotify.com/embed/user/1224963539/playlist/36DfTg9bztkYD1DN91N3tk',
  'happy': 'https://open.spotify.com/embed/user/spotify/playlist/37i9dQZF1DXdPec7aLTmlC',
  'sad': 'https://open.spotify.com/embed/user/spotify/playlist/37i9dQZF1DX7qK8ma5wgG1',
}

window.onload = function() {
  document.getElementById('setTopicButton').onclick = function() {
    const topic = document.getElementById('topicName').value;
    document.getElementById('topicName').value = '';
    
    const iframeSrc = sources[topic.toLowerCase()];
    if(iframeSrc === undefined) {
      document.getElementById('spotify-player').innerHTML = '<h4>Unable to create a playlist for that topic. Sorry!</h4>'
    } else {
      document.getElementById('spotify-player').innerHTML = '<iframe id="player-frame" src='+iframeSrc+' width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>';
    }
  }
}