from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from timer import CountdownTimer
from rpi_ws281x import *
from led import *
import argparse

app = Flask(__name__)

#Default Settings
settings = {
	"period_time": 20, 
	"num_periods": 3,
	"break_time" : 15,
	"home_team" : "Home",
	"away_team" : "Away"
}

#Variables
home_Score = 0
away_Score = 0
stripStatus = False
startTime = 0

timer = CountdownTimer()

@app.route('/')
def settings_page():
	return render_template('settings.html', settings=settings)

@app.route('/settings' ,methods=['POST'])
def save_settings():
	global settings, startTime
	settings['period_time'] = int(request.form['period_time'])
	settings['num_periods'] = int(request.form['num_periods'])
	settings['break_time'] = int(request.form['break_time'])
	settings['home_team'] = request.form['home_team']
	settings['away_team'] = request.form['away_team']
	startTime = settings['period_time']
	timer.running = False
	timer.paused = False
	return redirect(url_for('scoreboard_page'))

@app.route('/scoreboard')
def scoreboard_page():
    remaining_time = timer.get_remaining_time()
    minutes, seconds = divmod(int(remaining_time), 60)
    return render_template("index.html",home_Score=home_Score,away_Score=away_Score)
#	return render_template('indexcopy.html', settings=settings)

@app.route('/update')
def update():
    global startTime
    if timer.running == True or timer.paused == True:
        remaining_time = timer.get_remaining_time()
        minutes, seconds = divmod(int(remaining_time), 60)
        if stripStatus == True:
            displayTimeRemaining(strip, int(remaining_time))
        else:
            clearStrip(strip)
        return jsonify({'remaining_time': f"{minutes:02}:{seconds:02}",'home_Score': home_Score, 'away_Score': away_Score, 'home_Team': settings['home_team'], 'away_Team': settings['away_team']})
    elif timer.running == False and timer.paused == False:
        print(f"Period Time:",settings['period_time'])
        startTime = settings['period_time']
        remaining_time = startTime*60
        print(remaining_time)
        print(startTime)
        minutes, seconds = divmod(int(remaining_time), 60)
    return jsonify({'remaining_time': f"{minutes:02}:{seconds:02}",'home_Score': home_Score, 'away_Score': away_Score, 'home_Team': settings['home_team'], 'away_Team': settings['away_team']})

@app.route("/timerStart")
def timerStart():
    global stripStatus
    stripStatus = True
    timer.set_countdown_minutes(startTime)
    timer.start()
    return Response(status = 204)

@app.route("/timerPause")
def timerPause():
    timer.pause()
    return Response(status = 204)

@app.route("/timerStop")
def timerStop():
    global stripStatus
    stripStatus = False
    timer.stop()
    return Response(status = 204)

@app.route("/homePlus")
def homePlus():
    global home_Score
    home_Score += 1
    print("Home Score:", home_Score)
    return Response(status = 204)

@app.route("/homeMinus")
def homeMinus():
    global home_Score
    home_Score -= 1
    print("Home Score:", home_Score)
    return Response(status = 204)

@app.route("/awayPlus")
def awayPlus():
    global away_Score
    away_Score += 1
    print("Away Score:", away_Score)
    return Response(status = 204)

@app.route("/awayMinus")
def awayMinus():
    global away_Score
    away_Score -= 1
    print("Away Score:", away_Score)
    return Response(status = 204)

@app.route("/clearLEDs")
def clearLEDs():
    global stripStatus
    stripStatus = False
    clearStrip(strip)
    return Response(status = 204)

if __name__ == '__main__':
	app.run(host="0.0.0.0")