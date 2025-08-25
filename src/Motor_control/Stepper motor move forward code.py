from gpiozero import Motor
from time import sleep

# Define the GPIO pins for your stepper motor
motor = Motor(forward=17, backward=18)  # Replace with your specific GPIO pin numbers

# Define parameters for your stepper motor
steps_per_revolution = 200  # Number of steps per full revolution
distance_to_move = 10  # Specify the distance you want to move (in some units)

# Calculate the number of steps required to cover the desired distance
# (This calculation depends on your motor and mechanical setup)
steps_to_move = int(steps_per_revolution * (distance_to_move / 360.0))  # Adjust as needed

# Function to move the motor a specified number of steps
def move_stepper(steps, direction):
    for _ in range(steps):
        motor.forward() if direction == "forward" else motor.backward()
        sleep(0.01)  # Adjust the delay as needed for your motor's speed
        motor.stop()

# Move the stepper motor to cover the desired distance
move_stepper(steps_to_move, direction="forward")

# Cleanup the GPIO
motor.close()
# NEMA 17 (17HS4023) Raspberry Pi Tests
# --- rotating the NEMA 17 clockwise
# --- and counterclockwise in a loop
#
#
#######################################
#
#import RPi.GPIO as GPIO
#from RpiMotorLib import RpiMotorLib
#import time

################################
# RPi and Motor Pre-allocations
################################
#
#define GPIO pins
#direction= 22 # Direction (DIR) GPIO Pin
#step = 23 # Step GPIO Pin
#EN_pin = 24 # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
#mymotortest = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "DRV8825")
#GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

###########################
# Actual motor control
###########################
#
#dir_array = [False,True]
#GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
#for ii in range(10):
   # mymotortest.motor_go(dir_array[ii%2], # False=Clockwise, True=Counterclockwise
                         #"Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         #200, # number of steps
                         #.0005, # step delay [sec]
                         #False, # True = print verbose output 
                         #.05) # initial delay [sec]
    #time.sleep(1)

#GPIO.cleanup() # clear GPIO allocations after run