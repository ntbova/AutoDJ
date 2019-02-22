window.onload = function() {
  document.getElementById('setTopicButton').onclick = function() {
    const topic = document.getElementById('topicName').value;
    document.getElementById('topicName').value = '';

    document.getElementById('playlist-text').innerText = 'Creating a playlist...'

    $.ajax({
      url: "https://gateway-wdc.watsonplatform.net/discovery/api/v1/environments/4b24f2d8-d802-4b28-bec2-bc4104ebb8b4/collections/60f87acf-22e1-4677-aae7-23645d3beccd/query?version=2018-12-03&query=enriched_lyrics.concepts.text%3A%22" + encodeURI(topic) + "%22%7Clyrics%3A%22" + encodeURI(topic) + "%22",
      beforeSend: function(xhr) {
        xhr.setRequestHeader("Authorization", "Basic " + btoa("apikey:ltytYzYR-49NwvrxbnIDILPe_9fUqOn86MMEIYDhdgHB"));
      },

      success: function (data) {
        // console.log(JSON.stringify(data)); data.results: [{ song, artist, lyrics, other watson stuff }]
        // const songs = data.results.slice(0, 9);
        const songs = data.results;

        if (Object.keys(songs).length == 0) {
          output = 'Sorry, no relevant results found.'
          document.getElementById('spotify-player').innerHTML = output;
        } else {
          $.post({
            url: "http://127.0.0.1:5000/playlist/",
            data: {
              'songs': JSON.stringify(songs),
              'topic': topic,
            },
            success: function (result) {
              parsed = JSON.parse(result);
              document.getElementById('playlist-text').innerText = "Here's your playlist:";
              const iframeSrc = parsed.embed_link;
              document.getElementById('player-frame').src = iframeSrc;
            }
          });
        }
      },

    });
  }
}