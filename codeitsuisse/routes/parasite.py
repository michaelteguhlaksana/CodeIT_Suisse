import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)




@app.route('/parasite', methods=['POST'])
def evaluate():
	x_counter = 0

	def check_position (room, nc, nr, result, new_room, times, t):
		for adj_r, adj_c in ((nr-1, nc), (nr+1, nc), (nr, nc-1), (nr, nc+1)):
			if (0 <= adj_r < len(room) and 0 <= adj_c < len(room[0])) and room[adj_r][adj_c] == 1:
				new_room[adj_r][adj_c] = 3
				times[adj_r][adj_c] = t + 1
				result.append((adj_r, adj_c))
		return result, new_room, times


	def check_positionB (room, nc, nr, result, new_room, times, t):
		for adj_r, adj_c in ((nr-1, nc), (nr+1, nc), (nr, nc-1), (nr, nc+1), (nr-1, nc-1), (nr+1, nc-1), (nr+1, nc+1), (nr-1, nc+1)):
			if (0 <= adj_r < len(room) and 0 <= adj_c < len(room[0])) and room[adj_r][adj_c] == 1:
				new_room[adj_r][adj_c] = 3
				times[adj_r][adj_c] = t + 1
				result.append((adj_r, adj_c))
		return result, new_room, times

	def check_positionX (room, nc, nr, result, new_room, times, t):
		for adj_r, adj_c in ((nr-1, nc), (nr+1, nc), (nr, nc-1), (nr, nc+1)):
			if (0 <= adj_r < len(room) and 0 <= adj_c < len(room[0])) and (room[adj_r][adj_c] == 1 or room[adj_r][adj_c] == 0) :
				new_room[adj_r][adj_c] = 3
				if room[adj_r][adj_c] == 0:
					times[adj_r][adj_c] = t + 1
				result.append((adj_r, adj_c))
		return result, new_room, times

	def first_get_all_edge_source(room, times, t, check_position = check_position):
		new_room = room
		result = []
		for nr, r in enumerate(room):
			for nc, c in enumerate(r):
				if c == 3:
					result, new_room, times = check_position (room, nc, nr, result, new_room, times, t)
					return result, new_room, times


	def step_once (room, to_check, times, t, check_position = check_position):
		new_to_check = []
		for nr, nc  in to_check:
			new_to_check, new_room, times = check_position (room, nc, nr, new_to_check, new_room, times, t)
		return new_to_check, new_room, times



	def check_room(room, check_position_funct):
		times = [[0] * len(room[0]) ] * len(room)
		t = 0

		to_check, new_room = first_get_all_edge_source(room, times, t, check_position_funct)

		while to_check != []:
			new_to_check, new_room, times =  step_once(room, to_check, times, t, check_position_funct)
			t += 1

		return new_room, times

	def get_interest_time (times, nr, nc):
		result = times[nr][nc]

		if result == 0:
			return -1
		return result

	def get_maxi_time (times, final_room):
		maxi = 0
		for row in final_room:
			if 1 in row:
				return -1

		for row in times:
			maxi = max(maxi, max(row))

		return maxi


	logging.info("-------STARTING APP-------")
	data = request.get_json()
	logging.info("data sent for evaluation {}".format(data))

	result = []

	for case in data:
		logging.info("STARTING ON CASE: " + case)
		room_num = case.get("room")
		room = case.get("grid")
		interest = case.get("interestedIndividuals")

		A_room, A_times = check_room(room = room, check_position_funct = check_position)
		logging.info("FINISH WORKING ON A")
		B_room, B_times = check_room(room = room, check_position_funct = check_positionB)
		logging.info("FINISH WORKING ON B")
		X_room, X_times = check_room(room = room, check_position_funct = check_positionX)
		logging.info("FINISH WORKING ON X")

		p1 = {}
		for person in interest:
			r, c = person.split(",")
			r, c = int(r), int(c)

			p1[person] =  get_interest_time (A_times, r, c)

		p2 = get_maxi_time(A_times, A_room)

		p3 = get_maxi_time(B_times, B_room)

		p4 = get_maxi_time(X_times, X_room)


		case_result = {
			"room" : room_num,
			"p1" : p1,
			"p2" : p2,
			"p3" : p3,
			"p4" : p4
		}

		result.append(case_result)



	logging.info("My result :{}".format(result))
	return json.dumps(result)



