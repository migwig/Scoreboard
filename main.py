from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from timer import *
from rpi_ws281x import *
from led import *
import argparse
import threading
import time
from settings import *

app = Flask(__name__)

timer = CountdownTimer()

def background_update():  #this runs the physical display
	while True:
		print (state.timer_status)
		if state.timer_status:
			displayTimeRemaining(strip, int(state.display_time))
		else:
			displayTemperature()
		time.sleep(1)

@app.route('/')
def settings_page():
	timer.running = False
	timer.paused = False
	return render_template('settings.html', settings=state.settings, page='settings')

@app.route('/settings' ,methods=['POST'])
def save_settings():
	state.settings['period_time'] = int(request.form['period_time'])
	state.settings['num_periods'] = int(request.form['num_periods'])
	state.settings['break_time'] = int(request.form['break_time'])
	state.settings['home_team'] = request.form['home_team']
	state.settings['away_team'] = request.form['away_team']
	state.start_time = state.settings['period_time']
	state.strip_status = True
	return redirect(url_for('scoreboard_page'))

@app.route('/scoreboard')
def scoreboard_page():
    remaining_time = timer.get_remaining_time()
    minutes, seconds = divmod(int(remaining_time), 60)
    return render_template("index.html",home_Score=state.home_score,away_Score=state.away_score, page='scoreboard')

@app.route('/update')
def update():
	minutes, seconds = divmod(int(state.display_time), 60)
	return jsonify({
		'remaining_time': f"{minutes:02}:{seconds:02}",
		'home_Score': state.home_score,
		'away_Score': state.away_score,
		'home_Team': state.settings['home_team'],
		'away_Team': state.settings['away_team']
	})
	print (state.strip_status)
	
def get_remaining_time_details():
	if timer.running or timer.paused:
		remaining_time = state.display_time
	else:
		state.start_time = state.settings['period_time']
		remaining_time = state.start_time * 60
	minutes, seconds = divmod(int(remaining_time), 60)
	return remaining_time, minutes, seconds

#    timer.set_countdown_minutes(state.start_time)
#    timer.start()

@app.route("/timerStart")
def timerStart():
	if state.timer_status:
		print("timer status true")
		start_button_press_callback()
	else:
		state.timer_status = True
		run_timers_with_interval(state.settings['num_periods'], state.settings['period_time'], state.settings['break_time'], start_button_press_callback)
	return Response(status = 204)

@app.route("/timerPause")
def timerPause():
    timer.pause()
    return Response(status = 204)

@app.route("/timerStop")
def timerStop():
#    state.stripStatus = False
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

@app.route('/displayTemperature')
def display_temperature():
	displayTemperature()
	state.strip_status = False
	return "Temperature displayed"

@app.route('/displayTimeRemaining')
def display_time_remaining():
	state.strip_status = True
	remaining_time = state.remaining_time
	print(remaining_time)
	displayTimeRemaining(strip, int(remaining_time))
	return "Time Remaining Displayed"

def update_score(team, value):
	if team == 'home':
		state.home_score = max(0, state.home_score + value)
	elif team == 'away':
		state.away_score = max(0, state.away_score + value)

if __name__ == '__main__':
	#background update to display on the LEDs
	thread = threading.Thread(target=background_update)
	thread.daemon = True
	thread.start()
	
	#start the web app
	app.run(host="0.0.0.0")