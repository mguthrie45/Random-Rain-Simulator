import random
import matplotlib.pyplot as plt 
import numpy as np

VW, VH = 2, 2

PW, PH, PC = 10, 60, 'red'
WINW, WINH = 600, 500

RW, RH, RC = 2, 2, 'blue'
RV = 8

def make_person(v):
	return {'x': 0, 'y': WINH-PH, 'w': PW,'h': PH,'c': PC, 'v': v}

def make_rain_drop(x, y):
	return {'x': x, 'y': y, 'w': RW, 'h': RH, 'c': RC, 'v': RV}

def spawn_rain(rain_list, interval):
	for x in range(0, WINW, interval):
		rdev = interval // 2 - 1
		rx = random.randint(-rdev, rdev) + x
		ry = 0
		raindrop = make_rain_drop(rx, ry)
		rain_list.append(raindrop)

def is_colliding(raindrop, person):
	if (person['x'] < raindrop['x'] + RW and person['x'] + PW > raindrop['x'] and person['y'] < raindrop['y'] + RH and person['y'] + PH > raindrop['y']): 
		return True
	return False

def update_rain(t, t_spawned, run_player, rain_list, person, interval):
	collisions = 0
	for i, raindrop in enumerate(rain_list):
		if is_colliding(raindrop, person):
			collisions += 1
			rain_list.remove(raindrop)
			continue

		if raindrop['y'] >= WINH:
			if not run_player:
				run_player = True
			rain_list.remove(raindrop)
			continue

		raindrop['y'] += RV

	if RV * (t-t_spawned) >= interval:
		spawn_rain(rain_list, interval)
		t_spawned = t

	return collisions, t_spawned, run_player

def update_person(person, run_player):
	if run_player:
		person['x'] += person['v']


def run_sim(person, interval):
	num_t = int((WINW - PW) / person['v'] + WINH / RV) + 1
	rain_list = []
	t_spawned = - (1 + interval / RV)
	collisions = 0
	run_player = False
	for t in range(num_t):
		cols, t_spawned, run_player = update_rain(t, t_spawned, run_player, rain_list, person, interval)
		update_person(person, run_player)
		collisions += cols

	return collisions


if __name__ == "__main__":
	
	#velocity
	interval = 24
	max_v = 6
	npts = 48
	vel = np.linspace(max_v/npts, max_v, npts)
	cols = np.array([run_sim(make_person(v), interval) for v in vel])
	plt.title(f'Wetness vs. Velocity interval={interval}')
	plt.xlabel('Speed (still to running)')
	plt.ylabel('Num Collisions')
	plt.plot(vel, cols)
	plt.show()

	ints = [10, 15, 20, 25, 30, 35, 40, 45, 50]
	colsRun = np.array([run_sim(make_person(4), i) for i in ints])
	colsWalk = np.array([run_sim(make_person(1), i) for i in ints])
	plt.title('Wetness vs. Rain Density')
	plt.xlabel('Interval')
	plt.ylabel('Num Collisions')
	plt.plot(ints, colsRun)
	plt.plot(ints, colsWalk)
	plt.legend(['Running', 'Walking'])
	plt.show()



