def intcode(array,inp1=0):
    outputs = []
    i, base = 0, 0
    memory = {}
    for index, number in enumerate(array):
        memory[index] = number

    while i < len(array):
        if array[i] == 99:
            return outputs
        
		# convert number to array of 5 digits
        digits = [int(digit) for digit in str(array[i]).rjust(5,'0')]

        # position or relative mode for input parameter
        def selectInputMode(x):
            if x == 0:
                return array[i+1]
            elif x == 2:
                return array[i+1]+base
            else:
                raise ValueError('Unknown mode for input parameter')

        # position, immediate or relative mode for first parameter
        def selectMode1(x):
            if x == 0:
                return memory.get(array[i+1], 0)
            elif x == 1:
                return memory.get(i+1, 0)
            elif x == 2:
                return memory.get(array[i+1]+base, 0)
            else:
                raise ValueError('Unknown mode for parameter 1')
        
        # position, immediate or relative mode for second parameter
        def selectMode2(x):
            if x == 0:
                return memory.get(array[i+2], 0)
            elif x == 1:
                return memory.get(i+2, 0)
            elif x == 2:
                return memory.get(array[i+2]+base, 0)
            else:
                raise ValueError('Unknown mode for parameter 2')

        # position or relative mode for third parameter
        def selectMode3(x):
            if x == 0:
                return array[i+3]
            elif x == 2:
                return array[i+3]+base
            else:
                raise ValueError('Unknown mode for parameter 3')

 		# all opcode variations
        if digits[-1] == 1:
            if selectMode3(digits[0]) < len(array):
                array[selectMode3(digits[0])] = selectMode1(digits[2]) + selectMode2(digits[1])
            memory[selectMode3(digits[0])] = selectMode1(digits[2]) + selectMode2(digits[1])
            i += 4
        elif digits[-1] == 2:
            if selectMode3(digits[0]) < len(array):
                array[selectMode3(digits[0])] = selectMode1(digits[2]) * selectMode2(digits[1])
            memory[selectMode3(digits[0])] = selectMode1(digits[2]) * selectMode2(digits[1])
            i += 4
        elif digits[-1] == 3:
            if selectInputMode(digits[2]) < len(array):
                array[selectInputMode(digits[2])] = inp1
            memory[selectInputMode(digits[2])] = inp1 
            i += 2 
        elif digits[-1] == 4:
            outputs.append(selectMode1(digits[2]))
            i += 2
        elif digits[-1] == 5:
            i = selectMode2(digits[1]) if selectMode1(digits[2]) != 0 else i + 3
        elif digits[-1] == 6:
            i = selectMode2(digits[1]) if selectMode1(digits[2]) == 0 else i + 3
        elif digits[-1] == 7:
            if selectMode3(digits[0]) < len(array):
                array[selectMode3(digits[0])] = 1 if selectMode1(digits[2]) < selectMode2(digits[1]) else 0
            memory[selectMode3(digits[0])] = 1 if selectMode1(digits[2]) < selectMode2(digits[1]) else 0 
            i += 4
        elif digits[-1] == 8:
            if selectMode3(digits[0]) < len(array):
                array[selectMode3(digits[0])] = 1 if selectMode1(digits[2]) == selectMode2(digits[1]) else 0
            memory[selectMode3(digits[0])] = 1 if selectMode1(digits[2]) == selectMode2(digits[1]) else 0 
            i += 4
        elif digits[-1] == 9:
            base += selectMode1(digits[2]) 
            i += 2
        else:
            raise ValueError('Unknown opcode')

f = open('day9_input.txt').read().strip().split(',')
array = list(map(int, f))

print(intcode(array,2))