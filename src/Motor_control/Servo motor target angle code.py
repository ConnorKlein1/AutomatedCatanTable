#pip install gpiozero
from gpiozero import AngularServo
from time import sleep

# Define the GPIO pin where your servo is connected
servo = AngularServo(17)  # Replace with your specific GPIO pin number

# Define the angle to which you want to move the servo (0 to 180 degrees)
target_angle = 90  # Adjust to your desired angle

# Move the servo to the target angle
servo.angle = target_angle

# Wait for a moment (you can adjust the duration)
sleep(2)

# Cleanup the GPIO
servo.close()