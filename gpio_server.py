from flask import Flask, render_template
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

pins = {
	23: {'name': 'led-light', 'state': False},
	12: {'name': 'temperature-sensor', 'state': False} #TODO: this is wrong, just placeholder text
}

for pin in pins:
	GPIO.setup(pin, GPIO.OUT) #TODO: in for temp-sensor
	GPIO.output(pin, False)

@app.route("/")
def hello():
	for pin in pins:
		pins[pin]['state'] = GPIO.input(pin)
	templateData = {
		'pins': pins
	}
	return render_template('index.html', **templateData)

@app.route("/led/<int:pin>/<state>")
def changePin(pin, state):
	pinToChange = pin
	if state == "on":
		GPIO.output(pinToChange, True)
	if state == "off":
		GPIO.output(pinToChange, False)
	
	return "Worked, %s set %s" % (pin, state)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
