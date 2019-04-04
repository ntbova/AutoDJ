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

		// random 1-3
		const index = Math.floor(Math.random() * categories.length);
		console.log("Concept to use: " + categories[index]);

		// get one song for category
		// if song playing a song, add to queue
		// else play the song

	} else {
		console.log("No url present");
	}
});