import numpy as np

def intcode(array,memory,inp1=0,i=0,base=0):
    outputs = []

    while i < len(array):
        if array[i] == 99:
            return [99], i, base
        
		# convert number to array of 5 digits
        digits = [int(digit) for digit in str(array[i]).rjust(5,'0')]

        # position or relative mode for input and 3rd parameter
        def oneParameterMode(x,increment):
            if x == 0:
                return array[i+increment]
            elif x == 2:
                return array[i+increment]+base
            else:
                raise ValueError('Unknown parameter mode')
        
        # position, immediate or relative mode for 1st and 2nd parameter
        def threeParametersMode(x,increment):
            if x == 0:
                return memory.get(array[i+increment], 0)
            elif x == 1:
                return memory.get(i+increment, 0)
            elif x == 2:
                return memory.get(array[i+increment]+base, 0)
            else:
                raise ValueError('Unknown parameter mode')

 		# all opcode variations
        if digits[-1] == 1:
            if oneParameterMode(digits[0],3) < len(array):
                array[oneParameterMode(digits[0],3)] = threeParametersMode(digits[2],1) + threeParametersMode(digits[1],2)
            memory[oneParameterMode(digits[0],3)] = threeParametersMode(digits[2],1) + threeParametersMode(digits[1],2)
            i += 4
        elif digits[-1] == 2:
            if oneParameterMode(digits[0],3) < len(array):
                array[oneParameterMode(digits[0],3)] = threeParametersMode(digits[2],1) * threeParametersMode(digits[1],2)
            memory[oneParameterMode(digits[0],3)] = threeParametersMode(digits[2],1) * threeParametersMode(digits[1],2)
            i += 4
        elif digits[-1] == 3:
            if oneParameterMode(digits[2],1) < len(array):
                array[oneParameterMode(digits[2],1)] = inp1
            memory[oneParameterMode(digits[2],1)] = inp1 
            i += 2 
        elif digits[-1] == 4:
            outputs.append(threeParametersMode(digits[2],1))
            i += 2
            if len(outputs) % 2 == 0:
                return outputs, i, base
        elif digits[-1] == 5:
            i = threeParametersMode(digits[1],2) if threeParametersMode(digits[2],1) != 0 else i + 3
        elif digits[-1] == 6:
            i = threeParametersMode(digits[1],2) if threeParametersMode(digits[2],1) == 0 else i + 3
        elif digits[-1] == 7:
            if oneParameterMode(digits[0],3) < len(array):
                array[oneParameterMode(digits[0],3)] = 1 if threeParametersMode(digits[2],1) < threeParametersMode(digits[1],2) else 0
            memory[oneParameterMode(digits[0],3)] = 1 if threeParametersMode(digits[2],1) < threeParametersMode(digits[1],2) else 0 
            i += 4
        elif digits[-1] == 8:
            if oneParameterMode(digits[0],3) < len(array):
                array[oneParameterMode(digits[0],3)] = 1 if threeParametersMode(digits[2],1) == threeParametersMode(digits[1],2) else 0
            memory[oneParameterMode(digits[0],3)] = 1 if threeParametersMode(digits[2],1) == threeParametersMode(digits[1],2) else 0 
            i += 4
        elif digits[-1] == 9:
            base += threeParametersMode(digits[2],1) 
            i += 2
        else:
            raise ValueError('Unknown opcode')


def assignDirection(x,y,direction,value):
    if value == 0:
        if direction == 'up':
            x, y = x, y - 1
            direction = 'left'
        elif direction == 'down':
            x, y = x, y + 1
            direction = 'right'
        elif direction == 'right':
            x, y = x - 1, y
            direction = 'up'
        else:
            x, y = x + 1, y
            direction = 'down'
    elif value == 1:
        if direction == 'up':
            x, y = x, y + 1
            direction = 'right'
        elif direction == 'down':
            x, y = x, y - 1
            direction = 'left'
        elif direction == 'right':
            x, y = x + 1, y
            direction = 'down'
        else:
            x, y = x - 1, y
            direction = 'up'
    else:
        raise ValueError('Wrong direction value')

    return x, y, direction


def paintingRobot(grid,array):
    inp, i, base = 1, 0, 0
    outputs = [None]
    x, y = 50, 50
    direction = 'up'
    visited = [(x,y)]

    memory = {}
    for index, number in enumerate(array):
        memory[index] = number

    while outputs[0] != 99:
        outputs, i, base = intcode(array,memory,inp,i,base)
        if outputs[0] == 99:
            break
        grid[x][y] = '#' if outputs[0] == 1 else '.'

        # determine next direction of robot
        x, y, direction = assignDirection(x,y,direction,outputs[1])   
        inp = 1 if grid[x][y] == b'#' else 0     
        visited.append((x,y))

    visited = visited[:-1]
    visits = set(visited)

    return len(visits)



f1 = open('day11_input.txt').read().strip().split(',')
array = list(map(int, f1))

grid = np.chararray((101,101))
grid[:] = '.'

print(paintingRobot(grid,array))

#f2 = open('day11_output.txt','w+')
#string_matrix = np.char.decode(grid)

#for string in string_matrix:
#    f2.write(str(string) + '\n')

#f2.close()