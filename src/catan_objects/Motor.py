from abc import abstractmethod, ABC
import json
import time
import os

if os.name == 'nt':
    # WINDOWS CLASSES 
    class MotorKit():
        def __init__(self, address):
            self.address = address
            self.stepper1 = stepper("A")
            self.stepper2 = stepper("B")
            self.motor1 = Basic_DC_Motor("M1")
            self.motor2 = Basic_DC_Motor("M2")
            self.motor3 = Basic_DC_Motor("M3")
            self.motor4 = Basic_DC_Motor("M4")
            
    class Basic_DC_Motor():
        def __init__(self, type) -> None:
            self.type = type
            self.throttle = 0
            
    class stepper():
        FORWARD = "F"
        BACKWARD = "B"
        MICROSTEP = 0
        SINGLE = 1
        DOUBLE = 2
        
        def __init__(self, type):
            self.type = type
        
        def onestep(self, direction, style):
            pass
            
    class GPIO():
        BCM = 0
        OUT = 0
        LOW = 0
        HIGH = 0
            
        def __init__(self):
            pass
            
        def setmode(self, *args):
            pass
        def setup(self, *args):
            pass
        def output(self, *args):
            pass
        
    def gpio_cleanup():
        pass
    
    class Picamera2():
        def __init__(self):
            pass
        def capture_file(self, path):
            pass
        def start(self):
            pass
        
    class neopixel():
        def __init__(self):
            pass
        
        class NeoPixel():
            def __init__(self, pin, number, brightness):
                pass
            def fill(self, color):
                pass
            
    class board():
        D10 = 10
        def __init__(self):
            pass
else:
    import RPi.GPIO as GPIO
    from adafruit_motorkit import MotorKit
    from adafruit_motor import stepper
    from picamera2 import Picamera2
    import neopixel
    import board

def GPIO_SETUP(*args):
    GPIO.setmode(GPIO.BCM)
    for arg in args:
        GPIO.setup(arg, GPIO.OUT)  # PIN

def GPIO_CONTROL_STEPPER(steps, MOTOR_DIRECTION_PIN, MOTOR_STEP_PIN):
    if steps < 0:
        GPIO.output(MOTOR_DIRECTION_PIN, GPIO.LOW)   # Set to LOW for counterclockwise
    else:
        GPIO.output(MOTOR_DIRECTION_PIN, GPIO.HIGH)  # Set to HIGH for clockwise
    
    steps = abs(int(steps))
    
    for i in range(steps):
        GPIO.output(MOTOR_STEP_PIN, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(MOTOR_STEP_PIN, GPIO.LOW)
        time.sleep(0.001)
        
    time.sleep(0.25)
        
def GPIO_CONTROL_GATE(MOTOR_DIRECTION_PIN, level):
    GPIO.output(MOTOR_DIRECTION_PIN, level)

def GPIO_DESTRUCTOR():
    # call on __del__()
    gpio_cleanup()

def HAT_SETUP(type, address = 0x60):
    if address not in Motor.s_hats:
        Motor.s_hats[address] = MotorKit(address=address)
        
    try:
        motor = getattr(Motor.s_hats[address], type)
    except AttributeError:
        motor = None
        
    return motor

def HAT_CONTROL(motor, steps, delay = 0.001):
    if steps > 0:
        direction = stepper.FORWARD
    else:
        direction = stepper.BACKWARD
        
    steps = abs(int(steps))
    
    for i in range(steps):
        motor.onestep(direction=direction, style=stepper.DOUBLE)
        time.sleep(delay)

def LINKED_HAT_CONTROL(motor_1, motor_2, steps_1, steps_2):
    if steps_1 > 0:
        direction_1 = stepper.BACKWARD
    else:
        direction_1 = stepper.FORWARD
        
    if steps_2 > 0:
        direction_2 = stepper.BACKWARD
    else:
        direction_2 = stepper.FORWARD
        
    steps_1 = abs(int(steps_1))
    steps_2 = abs(int(steps_2))
    
    for i in range(max(steps_1, steps_2)):
        if i <= steps_1:
            motor_1.onestep(direction=direction_1, style=stepper.DOUBLE)
                
        if i <= steps_2:
                motor_2.onestep(direction=direction_2, style=stepper.DOUBLE)
                
        time.sleep(0.001)
        
    time.sleep(0.25)

class Motor(ABC):
    
    s_hats = {}
    
    def __init__(self, setup):
        self.motor = setup

class Stepper(Motor):
    # The translator is the attachment to the motor, example a timing pully has 20 teeth per rotation
    # each spaced 2 mm. So the translator is 20 teeth/rotation * 2 mm/tooth = 40 mm/rotation
    def __init__(self, steps_per_rotation, translator, setup_function, control_function = None, *args):
        super().__init__(setup_function)
        self.distance_per_step = translator / steps_per_rotation # mm/step
        self.current_cartisan = 0.0
        self.control_function = control_function
        self.control_args = args
        
    def move_to(self, value):
        steps = self.position_to_steps(value)
        
        self.control_function(self.motor, steps, *self.control_args)
        
        self._set_current_cartisan(value)
           
    def position_to_steps(self, coordinate):
        return (coordinate - self.current_cartisan) / self.distance_per_step # steps
    
    def _set_current_cartisan(self, value):
        self.current_cartisan = value
        
class Gate_Valve(Motor):
    def __init__(self, setup_function, control_function, pin):
        super().__init__(setup_function)
        self.control_function = control_function
        self.pin = pin
        
    def high(self):
        self.control_function(self.pin, GPIO.HIGH)
        
    def low(self):
        self.control_function(self.pin, GPIO.LOW)
        
class DCMotor(Motor):
    def __init__(self, setup_function):
       super().__init__(setup_function)
    
    def start(self, throttle):
        self.motor.throttle = throttle
    
    def stop(self):
        self.motor.throttle = 0
    
class LinkedMotor():
    def __init__(self, motor_1: Motor, motor_2: Motor, linking_function):
        self.motor_1 = motor_1
        self.motor_2 = motor_2
        self.control_function = linking_function
        
    def move_to(self, value : list):
        steps_1 = self.motor_1.position_to_steps(value[0])
        steps_2 = self.motor_2.position_to_steps(value[1])
        
        self.control_function(self.motor_1.motor, self.motor_2.motor, steps_1, steps_2)
        
        self.motor_1._set_current_cartisan(value[0])
        self.motor_2._set_current_cartisan(value[1])
        
class Lights():
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D10, 32, brightness=1)
        
    def start(self):
        self.pixels.fill((255, 255, 255))
        time.sleep(1)
        
    def stop(self):
        self.pixels.fill((0,0,0))
        
class CameraModuleCatan(): # Hopefully don't run into a name clashes, we also don't need this; its just a wrapper for now
    def __init__(self):
        self.camera = Picamera2()
        self.camera.start()
        time.sleep(0.5)
    
    def take_picture(self, path = 'Catable_Image.jpg'):
        self.camera.capture_file(path)
        time.sleep(2)
