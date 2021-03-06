from omxplayer.player import OMXPlayer
from time import sleep
import time
import VL53L0X
import RPi.GPIO as GPIO
import os
import datetime

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 16

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
tof = VL53L0X.VL53L0X(address=0x2B)
tof1 = VL53L0X.VL53L0X(address=0x2D)

# Set shutdown pin high for the first VL53L0X then 
# call to start ranging 
GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Set shutdown pin high for the second VL53L0X then 
# call to start ranging 
GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

count_BEST = 0
count_BETTER = 0
count_GOOD = 0


ledPinGreen = 24
ledPinRed = 23
GPIO.setup(ledPinGreen, GPIO.OUT)
GPIO.setup(ledPinRed, GPIO.OUT)

# def callCommand():
#     os.system("omxplayer -o local inhale_sound.m4a")

# def setTimer():
#     now = datetime.datetime.now()
#     sched_time = now+datetime.timedelta(seconds=2)
#     loopflag = 0
#     while True:
#         now = datetime.datetime.now()
#         if sched_time<now<(sched_time+datetime.timedelta(seconds=1)):
#             loopflag = 1
#             time.sleep(1)
#         if loopflag == 1:
#             callCommand()
#             loopflag = 0
#             sched_time = now+datetime.timedelta(hours=1)


now = datetime.datetime.now()
sched_time = now+datetime.timedelta(seconds=2)
loopflag = 0

for count in range(1,10000):
    
    now = datetime.datetime.now()
    if sched_time<now<(sched_time+datetime.timedelta(seconds=1)):
        loopflag = 1
        time.sleep(1)
    if loopflag == 1:
        os.system("omxplayer -o local inhale_sound.m4a")
        loopflag = 0
        sched_time = now+datetime.timedelta(hours=1)

    distance = tof.get_distance()
    if 50 < distance < 55:
        count_BEST+=1
        print ("sensor ", tof.my_object_number, distance, 'cm', "BEST")
        GPIO.output(ledPinRed, GPIO.LOW)
        GPIO.output(ledPinGreen, GPIO.HIGH)
    elif 55 <= distance < 60:
        count_BETTER+=1
        print ("sensor ", tof.my_object_number, distance, 'cm', "BETTER")
        GPIO.output(ledPinRed, GPIO.LOW)
        GPIO.output(ledPinGreen, GPIO.HIGH)
    elif 60 <= distance < 65:
        count_GOOD+=1
        print ("sensor ", tof.my_object_number, distance, 'cm', "GOOD")
        GPIO.output(ledPinRed, GPIO.LOW)
        GPIO.output(ledPinGreen, GPIO.HIGH)
    else:
        print ("sensor ", tof.my_object_number, distance, 'cm', "NOT GOOD")
        GPIO.output(ledPinGreen, GPIO.LOW) 
        GPIO.output(ledPinRed, GPIO.HIGH)


    distance1 = tof1.get_distance()
    if (distance > 0):
        print ("sensor %d - %d mm, %d cm, iteration %d" % (tof1.my_object_number, distance1, (distance1/10), count))
    else:
        print ("%d - Error" % tof.my_object_number)

    time.sleep(timing/1000000.00)

tof1.stop_ranging()
GPIO.output(sensor2_shutdown, GPIO.LOW)
tof.stop_ranging()
GPIO.output(sensor1_shutdown, GPIO.LOW)

