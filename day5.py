def intcode(array,inp1=0):
	outputs = []
	i = 0
	while i < len(array):
		if array[i] == 99:
			return outputs
        
		# convert number to array of 4 digits
		digits = [int(digit) for digit in str(array[i]).rjust(4,'0')]
		# position mode or immediate mode for first parameter
		mode1 = lambda x: array[array[i+1]] if x == 0 else array[i+1]
		# position mode or immediate mode for second parameter
		mode2 = lambda x: array[array[i+2]] if x == 0 else array[i+2]

 		# all opcode variations
		if digits[-1] == 1: 
			array[array[i+3]] = mode1(digits[1]) + mode2(digits[0])
			i += 4
		elif digits[-1] == 2:
			array[array[i+3]] = mode1(digits[1]) * mode2(digits[0])
			i += 4
		elif digits[-1] == 3:
			array[array[i+1]] = inp1
			i += 2 
		elif digits[-1] == 4:
			outputs.append(mode1(digits[1]))
			i += 2
		elif digits[-1] == 5:
			i = mode2(digits[0]) if mode1(digits[1]) != 0 else i + 3
		elif digits[-1] == 6:
			i = mode2(digits[0]) if mode1(digits[1]) == 0 else i + 3
		elif digits[-1] == 7:
			array[array[i+3]] = 1 if mode1(digits[1]) < mode2(digits[0]) else 0
			i += 4
		elif digits[-1] == 8:
			array[array[i+3]] = 1 if mode1(digits[1]) == mode2(digits[0]) else 0
			i += 4
		else:
			raise ValueError('Unknown opcode')

f = open('day5_input.txt').read().strip().split(',')
array = list(map(int, f))

print(intcode(array,5))