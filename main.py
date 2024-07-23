from flask import Flask, Response, render_template
from led_layer import interact_with_leds

app = Flask(__name__)

@app.route("/")
def view():
	return render_template("index.html")

@app.route("/interact")
def interaction():
	interact_with_leds()
	return Response(status = 204)
