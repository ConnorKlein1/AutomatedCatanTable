#pip install RPi.GPIO
import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin you want to set high
gpio_pin = 17  # Replace with the GPIO pin number you're using

# Set the pin as an output
GPIO.setup(gpio_pin, GPIO.OUT)

# Set the pin high (1)
GPIO.output(gpio_pin, GPIO.HIGH)

# Wait for a few seconds (you can adjust the duration)
time.sleep(2)

# Clean up GPIO
GPIO.cleanup()

#sudo is used as admin to access GPIO pins
#sudo python your_script.py
#runs code on pi from python interper 