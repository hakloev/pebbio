from flask import Flask, render_template, redirect, url_for
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
	23: {'name': 'led-light', 'state': False},
}

for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

@app.route("/")
def index():
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)
	templateData = {
		'pins': pins,
		'temp': showTemp()
	}
	return render_template('index.html', **templateData)

@app.route("/led/<int:pin>/<state>")
def changePin(pin, state):
	pinToChange = pin
	if state == "on":
		GPIO.output(pinToChange, GPIO.HIGH)
	if state == "off":
		GPIO.output(pinToChange, GPIO.LOW)
	
	#return "Pin %s set %s" % (pin, state)
	return redirect(url_for('index')) #return 200 OK?

@app.route("/temp")
def showTemp():
	tempfile = open("/sys/bus/w1/devices/28-000005c720ea/w1_slave")
	tempraw = tempfile.read()
	tempfile.close()
	templine = tempraw.split("\n")[1]
	tempdata = templine.split(" ")[9]
	temp = float(tempdata[2:])
	temp = temp / 1000
	return "The temperature is %s" % (temp)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
