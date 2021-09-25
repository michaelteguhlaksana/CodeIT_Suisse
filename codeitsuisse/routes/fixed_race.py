import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

#Edit starts
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

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



def minutely_req (counting):

	data = request.data(as_text=True)
	logging.info("data sent for evaluation {}".format(data))

	racers = data.split(",")
	counter(racers, counting)

	counting = {k: v for k, v in sorted(counting.items(), key=lambda item: item[1])}
	result = ""
	for i in range(9):
		result  = result + counting.keys()[i] + ','

	result = result + counting.keys()[9]

	logging.info("My result :{}".format(result))
	return json.dumps(result)




@app.route('/fixedrace', methods=['POST'])
def evaluate():
	sched = BackgroundScheduler(daemon=True)
	sched.add_job(minutely_req,'interval',minutes=60)

	while check_start():
		pass

	now = datetime.today()
	now_hour = now.hour

	sched.start()

	if now_hour > datetime.today:
		counting = {}
	







	



