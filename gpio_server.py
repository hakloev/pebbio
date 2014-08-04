from flask import Flask
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

@app.route("/")
def hello():
	return "Hello, Verden!"

@app.route("/led/<int:pin>/<state>")
def changePin(pin, state):
	pinToChange = pin
	GPIO.setup(23, GPIO.OUT) # check this one, make dict or something
	if state == "on":
		GPIO.output(pinToChange, True)
	if state == "off":
		GPIO.output(pinToChange, False)
	
	return "Worked, %s set %s" % (pin, state)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
