def findCrosses(wire1, wire2):
	prev1, prev2, crosses = [], [], []
	dist1, dist2 = {}, {}
	prev1.append((0,0))
	prev2.append((0,0))
	last_combo = (0,0)
	counter = 1
	for path in wire1:
		number = 1
		while number <= int(path[1:]):
			if path[0] == 'R':
				prev1.append((last_combo[0]+number,last_combo[1]))
				if(prev1[-1]) not in dist1:
					dist1.update({prev1[-1]: counter})
			if path[0] == 'L':
				prev1.append((last_combo[0]-number,last_combo[1]))
				if(prev1[-1]) not in dist1:
					dist1.update({prev1[-1]: counter})
			if path[0] == 'U':
				prev1.append((last_combo[0],last_combo[1]+number))
				if(prev1[-1]) not in dist1:
					dist1.update({prev1[-1]: counter})
			if path[0] == 'D':
				prev1.append((last_combo[0],last_combo[1]-number))
				if(prev1[-1]) not in dist1:
					dist1.update({prev1[-1]: counter})
			number += 1
			counter += 1
		last_combo = prev1[-1]

	counter = 1
	last_combo = (0,0)
	for path in wire2:
		number = 1
		while number <= int(path[1:]):
			if path[0] == 'R':
				prev2.append((last_combo[0]+number,last_combo[1]))
				if(prev2[-1]) not in dist2:
					dist2.update({prev2[-1]: counter})
			if path[0] == 'L':
				prev2.append((last_combo[0]-number,last_combo[1]))
				if(prev2[-1]) not in dist2:
					dist2.update({prev2[-1]: counter})
			if path[0] == 'U':
				prev2.append((last_combo[0],last_combo[1]+number))
				if(prev2[-1]) not in dist2:
					dist2.update({prev2[-1]: counter})
			if path[0] == 'D':
				prev2.append((last_combo[0],last_combo[1]-number))
				if(prev2[-1]) not in dist2:
					dist2.update({prev2[-1]: counter})
			number += 1
			counter += 1
		last_combo = prev2[-1]

	s1 = set(prev1)
	s2 = set(prev2)
	crosses = s1 & s2
	crosses.remove((0,0))

	dist = min(dist1[(x,y)] + dist2[(x,y)] for (x,y) in crosses)

	return crosses, dist

def Manhattan(wire1, wire2):
	crosses, _ = findCrosses(wire1, wire2)
	distances = []
	for cross in crosses:
		distances.append(abs(cross[0]) + abs(cross[1]))
	if len(distances) > 0:
		return min(distances)


f1, f2 = open('day3_input.txt').read().strip().split('\n')
wire1 = f1.split(',')
wire2 = f2.split(',')

print(Manhattan(wire1, wire2))
_, dist = findCrosses(wire1, wire2)
print(dist)