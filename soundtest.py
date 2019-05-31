import os
import datetime
import time

def callCommand():
	os.system("omxplayer -o local Work2.m4a")

def setTimer():
	sched_time = datetime.datetime(2019, 5, 30, 0, 0, 0)
	loopflag = 0
	while True:
		now = datetime.datetime.now()
		if sched_time<now<(sched_time+datetime.timedelta(seconds=1)):
			loopflag = 1
			time.sleep(1)
		if loopflag == 1:s
			callCommand()
			loopflag = 0
			sched_time = now+datetime.timedelta(hours=1)
setTimer()

