document.addEventListener("DOMContentLoaded", () => {
	const timerStart = document.getElementById("timerStart");
	const timerPause = document.getElementById("timerPause");
	const timerStop = document.getElementById("timerStop");
	const homePlus = document.getElementById("homePlus");
	const homeMinus = document.getElementById("homeMinus");
	const awayPlus = document.getElementById("awayPlus");
	const awayMinus = document.getElementById("awayMinus");
	const outcomeText = document.getElementById("outcomeText");
	const clearLEDs = document.getElementById("clearLEDs");
			
	const fetchAndUpdate = (url, button, text) => {
		button.innerHTML = "Loading..";
		button.setAttribute("disabled", "true");
					
		fetch(url).then(res => {
			if (res.status !==204){
				throw new Error(`Got a ${res.status} status code response.`);
			}
			updateScores();
			outcomeText.innerHTML = "Request handled successfully!";
		})
		.catch(err => {
			outcomeText.innerHTML = `An error occurred: ${err.message}`;
		})
		.finally(() => {
			button.innerHTML = text;
			button.removeAttribute("disabled");
		});
	};
				
	const updateScores = () =>{
		fetch('/update')
			.then(response => response.json())
			.then(data => {
				document.getElementById('home_Score').textContent = data.home_Score;
				document.getElementById('away_Score').textContent = data.away_Score;
				document.getElementById('home_Team').textContent = data.home_Team;
				document.getElementById('away_Team').textContent = data.away_Team;
		})
		.catch(error => console.error('Error fetching time:', error));
	};
	timerStart.addEventListener("click", () => fetchAndUpdate("/timerStart", timerStart, "Start Timer"));
	timerPause.addEventListener("click", () => fetchAndUpdate("/timerPause", timerPause, "Pause Timer"));
	timerStop.addEventListener("click", () => fetchAndUpdate("/timerStop", timerStop, "Stop Timer"));
	homePlus.addEventListener("click", () => fetchAndUpdate("/homePlus", homePlus, "Home +"));
	homeMinus.addEventListener("click", () => fetchAndUpdate("/homeMinus", homeMinus, "Home -"));
	awayPlus.addEventListener("click", () => fetchAndUpdate("/awayPlus", awayPlus, "Away +"));
	awayMinus.addEventListener("click", () => fetchAndUpdate("/awayMinus", awayMinus, "Away -"));
	clearLEDs.addEventListener("click", () => fetchAndUpdate("/clearLEDs", clearLEDs, "Clear LEDs"));
	
	function updateTimer() {
		fetch('/update')
			.then(response => response.json())
			.then(data => {
				document.getElementById('timer').textContent = data.remaining_time;					
			})
			.catch(error => console.error('Error fetching time:', error));
     };
        
	setInterval(updateTimer, 1000);
	window.onload = updateTimer;
});