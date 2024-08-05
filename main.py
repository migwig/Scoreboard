from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from timer import CountdownTimer
from rpi_ws281x import *
from led import *
import argparse

app = Flask(__name__)

class AppState:
	def __init__(self):
		self.settings = {
			"period_time": 20, 
			"num_periods": 3,
			"break_time" : 15,
			"home_team" : "Home",
			"away_team" : "Away"
		}
		self.home_score = 0
		self.away_score = 0
		self.strip_status = False
		self.start_time = 0

state = AppState()
timer = CountdownTimer()

@app.route('/')
def settings_page():
	
	return render_template('settings.html', settings=state.settings)

@app.route('/settings' ,methods=['POST'])
def save_settings():
	state.settings['period_time'] = int(request.form['period_time'])
	state.settings['num_periods'] = int(request.form['num_periods'])
	state.settings['break_time'] = int(request.form['break_time'])
	state.settings['home_team'] = request.form['home_team']
	state.settings['away_team'] = request.form['away_team']
	state.start_time = state.settings['period_time']
	timer.running = False
	timer.paused = False
	return redirect(url_for('scoreboard_page'))

@app.route('/scoreboard')
def scoreboard_page():
    remaining_time = timer.get_remaining_time()
    minutes, seconds = divmod(int(remaining_time), 60)
    return render_template("index.html",home_Score=state.home_score,away_Score=state.away_score)

@app.route('/update')
def update():
	remaining_time, minutes, seconds = get_remaining_time_details()
	if state.strip_status:
		displayTimeRemaining(strip, int(remaining_time))
	else:
		displayTemerpature()
	return jsonify({
		'remaining_time': f"{minutes:02}:{seconds:02}",
		'home_Score': state.home_score,
		'away_Score': state.away_score,
		'home_Team': state.settings['home_team'],
		'away_Team': state.settings['away_team']
	})
	
def get_remaining_time_details():
	if timer.running or timer.paused:
		remaining_time = timer.get_remaining_time()
	else:
		state.start_time = state.settings['period_time']
		remaining_time = state.start_time * 60
	minutes, seconds = divmod(int(remaining_time), 60)
	return remaining_time, minutes, seconds
	
@app.route("/timerStart")
def timerStart():
    state.strip_status = True
    timer.set_countdown_minutes(state.start_time)
    timer.start()
    return Response(status = 204)

@app.route("/timerPause")
def timerPause():
    timer.pause()
    return Response(status = 204)

@app.route("/timerStop")
def timerStop():
    state.stripStatus = False
    timer.stop()
    return Response(status = 204)

@app.route("/homePlus")
def homePlus():
	update_score('home', 1)
	return Response(status = 204)

@app.route("/homeMinus")
def homeMinus():
    update_score('home', -1)
    return Response(status = 204)

@app.route("/awayPlus")
def awayPlus():
    update_score('away', 1)
    return Response(status = 204)

@app.route("/awayMinus")
def awayMinus():
    update_score('away', -1)
    return Response(status = 204)

@app.route("/clearLEDs")
def clearLEDs():
    state.strip_status = False
    clearStrip(strip)
    return Response(status = 204)

def update_score(team, value):
	if team == 'home':
		state.home_score += value
	elif team == 'away':
		state.away_score += value
	print(f"{team.capitalize()} Score:", state.home_score if team == 'home' else state.away_score)

if __name__ == '__main__':
	app.run(host="0.0.0.0")