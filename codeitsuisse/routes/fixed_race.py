import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

#Edit starts
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit

def counter(racers, counting):
	logging.info("Counting...")
	for racer in racers:
		if racer in counting.keys():
			counting[racer] += 1
		else:
			counting[racer] = 1

def check_start():
	now = datetime.today()
	if now.minute == 0:
		return False
	return True

counting = {}

def minutely_req ():
	global counting

	result = []
	data = request.data(as_text=True)
	logging.info("data sent for evaluation {}".format(data))

	racers = data.split(",")
	counter(racers, counting)

	counting = {k: v for k, v in sorted(counting.items(), key=lambda item: item[1])}
	result.append(counting.keys()[:10])
	return result


@app.route('/fixedrace', methods=['POST'])
def evaluate():
	global counting

	result = minutely_req(counting)

	
	for res in result[:9]:
	results  = results + res + ','

	results = results + result[9]

	return results


sched = BackgroundScheduler(daemon=True)
sched.add_job(evaluate,'interval',seconds=60)

while check_start():
	pass

sched.start()


atexit.register(lambda: sched.shutdown(wait=False))


	



