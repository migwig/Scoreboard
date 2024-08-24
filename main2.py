from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from timer import *
from rpi_ws281x import *
from led import *
import threading
import time
from settings import *

app = Flask(__name__)

timer = CountdownTimer()
timer_thread = None
update_thread = None
update_event = threading.Event()

class TimerManager:
	def __init__(self):
		self.num_iterations = 0
		self.current_iteration = 0
		self.countdown_minutes = 0
		self.countdown_seconds = 0
		self.interval_seconds = 0
		self.timer = None
		self.running = False
		
	def start_timer_sequence(self, num_iterations, countdown_minutes, interval_seconds):
		self.num_iterations = num_iterations
		self.countdown_minutes = countdown_minutes
		self.interval_seconds = interval_seconds
		self.current_iteration = 0
		self.running = True
		print(f"[DEBUG] Starting timer sequence with {self.num_iterations} iterations")
		self.run_next_timer()
		
	def run_next_timer(self):
		while self.running and self.current_iteration < self.num_iterations:
			print(f"[DEBUG] waiting for button press to start timer {self.current_iteration + 1}")
			button_press_event.wait()
			button_press_event.clear()
			print(f"[DEBUG] Button pressed, starting timer {self.current_iteration + 1}")
			
			self.current_iteration += 1
			self.timer = CountdownTimer(self.countdown_minutes)
			self.timer.start()
			print(f"Timer {self.current_iteration} initialised")
			
			while self.timer.get_remaining_time() > 0:
				state.display_time = self.timer.get_remaining_time()
				print(f"[DEBUG] Timer {self.current_iteration} running: {state.display_time} seconds left")
				time.sleep(1)
				update_event.set()
			
			self.timer.stop()
			state.display_time = 0
			print(f"Timer {self.current_iteration} completed")
			update_event.set()
			
			if self.current_iteration < self.num_iterations:
				for remaining_interval in range(self.interval_seconds, 0, -1):
					state.display_time = remaining_interval
					time.sleep(1)
					update_event.set()
						
		self.running = False
		print("All timers completed")
		
	def stop(self):
		self.running = False
		button_press_event.set()
		
timer_manager = TimerManager()
	
# Utility function for time formatting
def format_time(seconds):
	minutes, seconds = divmod(int(seconds),60)
	return f"{minutes:02}:{seconds:02}"
	
def update_score(team, value):
	if team == 'home':
		state.home_score = max(0, state.home_score + value)
	elif team == 'away':
		state.away_score = max(0, state.away_score + value)
		
def background_update():
	while True:
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

@app.route('/settings', methods=['POST'])
def save_settings():
	try:
		state.settings['period_time'] = int(request.form['period_time'])
		state.settings['num_periods'] = int(request.form['num_periods'])
		state.settings['break_time'] = int(request.form['break_time'])
		state.settings['home_team'] = request.form['home_team']
		state.settings['away_team'] = request.form['away_team']
		state.start_time = state.settings['period_time']
		state.strip_status = True
	except ValueError:
		return "Invalid Input", 400
	return redirect(url_for('scoreboard_page'))

@app.route('/scoreboard')
def scoreboard_page():
	remaining_time = timer.get_remaining_time()
	minutes, seconds = divmod(int(remaining_time), 60)
	return render_template ("index.html", home_Score=state.home_score, away_Score=state.away_score, page='scoreboard')

@app.route('/update')
def update():
	return jsonify({
		'remaning_time': format_time(state.display_time),
		'home_Score': state.home_score,
		'away_Score': state.away_score,
		'home_Team': state.settings['home_team'],
		'away_Team': state.settings['away_team']
	})

@app.route("/timerStart")
def timerStart():
	global timer_thread
				  
	if not button_press_event.is_set():
		button_press_event.set()
		if timer_thread is None or not timer_thread.is_alive():
			timer_thread = threading.Thread(target=timer_manager.start_timer_sequence, args=(state.settings['num_periods'], state.settings['period_time'], state.settings['break_time']))
			timer_thread.start()
	
	return Response(status=204)
				  
def start_button_press_callback():
	button_press_event.set()
				  
				  
'''	if state.timer_status:
		start_button_press_callback()
	else:
		state.timer_status = True
		run_timers_with_interval(
			state.settings['num_periods'],
			state.settings['period_time'],
			state.settings['break_time'],
			start_button_press_callback
		)
	return Response(status=204)
'''
@app.route("/timerPause")
def timerPause():
	timer.pause()
	return Repsonse(status=204)

@app.route("/timerStop")
def timerStop():
    timer_manager.stop()
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

@app.route('/displayTemperature')
def display_temperature():
	displayTemperature()
	state.strip_status = False
	return "Temperature displayed"

@app.route('/displayTimeRemaining')
def display_time_remaining():
	state.strip_status = True
	displayTimeRemaining(strip, int(state.remaining_time))
	return "Time Remaining Displayed"

def background_update():
	while True:
		update_event.wait()
		update_event.clear()
		if state.strip_status:
			displayTimeRemaining(strip, int(state.display_time))
		else:
			displayTemperature()
		time.sleep(1)

if __name__ == '__main__':
	button_press_event = threading.Event()
	update_event = threading.Event()
	
	update_thread = threading.Thread(target=background_update)
	update_thread.daemon = True
	update_thread.start()
	
	app.run(host="0.0.0.0")