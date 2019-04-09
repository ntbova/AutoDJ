let currentUrl = "";

chrome.tabs.onUpdated.addListener(async function(tabId, changeInfo, tab) {
	//alert('updated from background');
	console.log("Changeinfo: ", changeInfo)

	// TODO: find a way to only grab the focused/ last focused tab ^^

	console.log("Tab: " + tab.url)

	const apikey = "1ZIBX_VcVfTupEJ4N9WgYDz_RHC3Nd70iYSglgiJwWMJ";
	const url = "https://gateway-wdc.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-11-16";
	const headers = {
		"Authorization": "Basic YXBpa2V5OjFaSUJYX1ZjVmZUdXBFSjROOVdnWUR6X1JIQzNOZDcwaVlTZ2xnaUp3V01K",
		"Content-Type": "application/json"
	}

	if(tab.url) {
		if(tab.url == currentUrl) {
			return;
		}
		currentUrl = tab.url;
		// get concepts from this page
		const data = {
			"url": tab.url,
			"features": {
				"categories": {
					"limit": 3
				}
			}
		}
		console.log("Fetching!")
		const response = await fetch(url, {
			method: "POST",
			headers: headers,
			body: JSON.stringify(data)
		}).then(response => response.json())
		.catch(error => console.log("Error: ", error))

		const categories = response.categories;
		console.log(categories);

		// random concept from the categories
		const index = Math.floor(Math.random() * categories.length);
		console.log("Concept to use: ", categories[index].label);
		const topic = categories[index].label;

		var scrubbedInput = JSON.stringify(topic).replace(/[^\w\s]/gi, '')

    if (scrubbedInput === '') {
      return;
    }

    var input = scrubbedInput.split(" ")

		var fullURL = "https://gateway-wdc.watsonplatform.net/discovery/api/v1/environments/4b24f2d8-d802-4b28-bec2-bc4104ebb8b4/collections/60f87acf-22e1-4677-aae7-23645d3beccd/query?version=2018-12-03"
    
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
          console.log('Sorry, no relevant results found.');
          // document.getElementById('playlist-text').innerHTML = output;
        } else {
          $.post({
            url: "http://127.0.0.1:5000/song",
            data: {
              'songs': JSON.stringify(songs),
            },
            success: function (result) {
							console.log("Response from song: ", result);
              //parsed = JSON.parse(result);
              //document.getElementById('playlist-text').innerText = "Here's your playlist:";
              //const iframeSrc = parsed.embed_link;
              //document.getElementById('player-frame').src = iframeSrc;
            }
          });
        }
      },

    });

		// get one song for category
		// if song playing a song, add to queue
		// else play the song

	} else {
		console.log("No url present");
	}
});