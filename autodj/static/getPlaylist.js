window.onload = function() {
  
  var moods = ['Negative', 'Neutral', 'Positive'];

  var output = 1;
  var activated = false;

  // Function for slider changes.
  document.getElementById('myRange').oninput = function() {
    output = this.value;

    document.getElementById('sentiment').innerText = moods[output];
  }

  // Function for slider checkbox changes.
  document.getElementById('sliderBox').onclick = function() {
    activated = this.checked;
  }

  // Function for button which uses Discovery query based on input text.
  document.getElementById('setTopicButton').onclick = function() {
    const topic = document.getElementById('topicName').value;
    document.getElementById('topicName').value = '';
    
    var scrubbedInput = JSON.stringify(topic).replace(/[^\w\s]/gi, '')
    scrubbedInput = scrubbedInput.replace(/_/g, '')

    if (scrubbedInput === '') {
      return;
    }

    var input = scrubbedInput.split(" ")

    document.getElementById('playlist-text').innerText = 'Creating a playlist...'

    var fullURL = "https://gateway-wdc.watsonplatform.net/discovery/api/v1/environments/4b24f2d8-d802-4b28-bec2-bc4104ebb8b4/collections/60f87acf-22e1-4677-aae7-23645d3beccd/query?version=2018-12-03"

    if (activated) {
      fullURL = fullURL + "&filter=enriched_lyrics.sentiment.document.label%3A%3A\"" + moods[output].toLowerCase() + "\"";
    }
    
    for (i = 0; i < input.length; i++) {
      if(i == 0) { 
        fullURL = fullURL + "&query=enriched_lyrics.concepts.text%3A%22" + encodeURI(input[i]) + "%22%7Clyrics%3A%22" + encodeURI(input[i]) + "%22";
      } else {
        fullURL = fullURL + "%7Cenriched_lyrics.concepts.text%3A%22" + encodeURI(input[i]) + "%22%7Clyrics%3A%22" + encodeURI(input[i]) + "%22";
      }
    }

    $.ajax({
      url: fullURL,
      beforeSend: function(xhr) {
        xhr.setRequestHeader("Authorization", "Basic " + btoa("apikey:ltytYzYR-49NwvrxbnIDILPe_9fUqOn86MMEIYDhdgHB"));
      },

      success: function (data) {
        // console.log(JSON.stringify(data)); data.results: [{ song, artist, lyrics, other watson stuff }]
        // const songs = data.results.slice(0, 9);
        const songs = data.results;

        if (Object.keys(songs).length == 0) {
          output = 'Sorry, no relevant results found.'
          document.getElementById('playlist-text').innerHTML = output;
        } else {
          $.post({
            url: "http://127.0.0.1:5000/playlist",
            data: {
              'songs': JSON.stringify(songs),
              'topic': scrubbedInput,
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