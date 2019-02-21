window.onload = function() {
  document.getElementById('setTopicButton').onclick = function() {
    const topic = document.getElementById('topicName').value;
    document.getElementById('topicName').value = '';

    document.getElementById('playlist-text').innerText = 'Creating a playlist...'

    $.ajax({
      url: "https://gateway-wdc.watsonplatform.net/discovery/api/v1/environments/9bc54cbf-7b02-45a7-b221-87ff46c5de33/collections/956657c4-b81d-46c9-b192-53151075d828/query?version=2018-12-03&count=20&natural_language_query= " + encodeURI(topic),
      beforeSend: function(xhr) {
        xhr.setRequestHeader("Authorization", "Basic " + btoa("apikey:O8_fdyrpsmnK-COj_guUNFZ3jfCKh8hko1mraRCxeJ5f"));
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