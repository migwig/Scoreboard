#from flask import Flask, Response, render_template, jsonify
from flask import Flask, Response, render_template, redirect, url_for, request, jsonify
from timer import CountdownTimer
from rpi_ws281x import *
from led import *
import argparse

#Variables
home_Score = 0
away_Score = 0
stripStatus = False

app = Flask(__name__)

timer = CountdownTimer()

@app.route("/")
def index():
    remaining_time = timer.get_remaining_time()
    minutes, seconds = divmod(int(remaining_time), 60)
    return render_template("index.html",home_Score=home_Score,away_Score=away_Score)

# return render_template('index.html', remaining_time=f"{minutes:02}:{seconds:02}")
#def view():
	

@app.route('/update')
def update():
    remaining_time = timer.get_remaining_time()
    minutes, seconds = divmod(int(remaining_time), 60)
    if stripStatus == True:
        displayTimeRemaining(strip, int(remaining_time))
    else:
        clearStrip(strip)
    return jsonify({'remaining_time': f"{minutes:02}:{seconds:02}",'home_Score': home_Score, 'away_Score': away_Score})

@app.route("/timerStart")
def timerStart():
    global stripStatus
    stripStatus = True
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

app.run(host="0.0.0.0")
