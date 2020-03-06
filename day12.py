from math import gcd
from functools import reduce

class Moon: 
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def updateVelocity(self, velocities):
        self.velocity[0] += velocities[0]
        self.velocity[1] += velocities[1]
        self.velocity[2] += velocities[2]

    def updatePosition(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[2] += self.velocity[2]

    def updateX(self, velocity_x):
        self.velocity[0] += velocity_x
        self.position[0] += self.velocity[0]

    def updateY(self, velocity_y):
        self.velocity[1] += velocity_y
        self.position[1] += self.velocity[1]

    def updateZ(self, velocity_z):
        self.velocity[2] += velocity_z
        self.position[2] += self.velocity[2]


def timeProgress(moons, steps):
    # Simulate time steps
    for _ in range(steps):
        velocities = []
        for i in range(4):
            # Create temporary variable to store changes in velocity
            temp_velocities = [0, 0, 0]
            for j in range(4):
                if i == j:
                    continue
                for k in range(3):
                    if moons[i].position[k] == moons[j].position[k]:
                        continue
                    elif moons[i].position[k] < moons[j].position[k]:
                        temp_velocities[k] += 1
                    else:
                        temp_velocities[k] -= 1
            velocities.append(temp_velocities)
        
        # Update velocity and position of all moons
        for i in range(4):
            moons[i].updateVelocity(velocities[i])
            moons[i].updatePosition()


def calculateEnergy(moons):
    total_energy = []
    for i in range(4):
        potential = abs(moons[i].position[0]) + abs(moons[i].position[1]) + abs(moons[i].position[2])
        kinetic = abs(moons[i].velocity[0]) + abs(moons[i].velocity[1]) + abs(moons[i].velocity[2])
        total_energy.append(potential * kinetic)

    return sum(total_energy)


#------------- SPLIT CODE INTO 3 AXES TO IMPROVE EFFICIENCY -------------#

def updateXaxis(moons):
    back_to_zero = False
    steps = 0

    while not back_to_zero:
        velocities = []
        for i in range(4):
            temp_velocity = 0
            for j in range(4):
                if i == j:
                    continue
                if moons[i].position[0] < moons[j].position[0]:
                    temp_velocity += 1
                elif moons[i].position[0] > moons[j].position[0]:
                    temp_velocity -= 1
            velocities.append(temp_velocity)
        
        for i in range(4):
            moons[i].updateX(velocities[i])

        # Check whether velocities are back to zero
        back_to_zero = True
        for i in range(4):
            if moons[i].velocity[0] != 0:
                back_to_zero = False
        
        steps += 1

    return steps

def updateYaxis(moons):
    back_to_zero = False
    steps = 0

    while not back_to_zero:
        velocities = []
        for i in range(4):
            temp_velocity = 0
            for j in range(4):
                if i == j:
                    continue
                if moons[i].position[1] < moons[j].position[1]:
                    temp_velocity += 1
                elif moons[i].position[1] > moons[j].position[1]:
                    temp_velocity -= 1
            velocities.append(temp_velocity)
        
        for i in range(4):
            moons[i].updateY(velocities[i])

        # Check whether velocities are back to zero
        back_to_zero = True
        for i in range(4):
            if moons[i].velocity[1] != 0:
                back_to_zero = False
        
        steps += 1

    return steps

def updateZaxis(moons):
    back_to_zero = False
    steps = 0

    while not back_to_zero:
        velocities = []
        for i in range(4):
            temp_velocity = 0
            for j in range(4):
                if i == j:
                    continue
                if moons[i].position[2] < moons[j].position[2]:
                    temp_velocity += 1
                elif moons[i].position[2] > moons[j].position[2]:
                    temp_velocity -= 1
            velocities.append(temp_velocity)
        
        for i in range(4):
            moons[i].updateZ(velocities[i])

        # Check whether velocities are back to zero
        back_to_zero = True
        for i in range(4):
            if moons[i].velocity[2] != 0:
                back_to_zero = False
        
        steps += 1

    return steps


# Least common multiple
def lcm(a, b):
    return abs(a*b) // gcd(a, b)

# Least common multiple where n > 2
def lcm_n(*args):
    return reduce(lcm, args)



io = Moon([-4, -9, -3])             
europa = Moon([-13, -11, 0])
ganymede = Moon([-17, -7, 15])
callisto = Moon([-16, 4, 2])

moons = [io, europa, ganymede, callisto]

#steps = 1000
#timeProgress(moons, steps)
#print(calculateEnergy(moons))

x_result = updateXaxis(moons)
y_result = updateYaxis(moons)
z_result = updateZaxis(moons)
print(lcm_n(x_result, y_result, z_result) * 2)