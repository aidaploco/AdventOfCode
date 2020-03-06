def countOrbitsRecursively(key,space_objects):
	if key == 'COM':
		return 0
	return countOrbitsRecursively(space_objects[key], space_objects) + 1

def countTransfers(space_objects):
	you, santa = set(), set()
	current_y, current_s = space_objects['YOU'], space_objects['SAN']
	while current_y != 'COM':
		you.add(current_y)
		current_y = space_objects[current_y]
	while current_s != 'COM':
		santa.add(current_s)
		current_s = space_objects[current_s]
	return len(you ^ santa)


f = open('day6_input.txt').read().strip().split('\n')
space_objects = {}
for line in f:
	space_objects[line.split(')')[1]] = line.split(')')[0]

sum_orbits = 0
for key in space_objects.keys():
	sum_orbits += countOrbitsRecursively(key, space_objects)

print(sum_orbits)
print(countTransfers(space_objects))