from itertools import permutations

def intcode(array,i,inp1=0,inp2=0,flag=''):
    output = 0
    while i < len(array):
        if array[i] == 99:
            flag = ''
            return output, i, flag
        
        # convert number to array of 4 digits
        digits = [int(digit) for digit in str(array[i]).rjust(4,'0')]
        # position mode or immediate mode for first parameter
        mode1 = lambda x: array[array[i+1]] if x == 0 else array[i+1]
        # position mode or immediate mode for second parameter
        mode2 = lambda x: array[array[i+2]] if x == 0 else array[i+2]

        # if continuing intcode after a halt, start with input
        if flag == 'halt' and digits[-1] == 4:
            digits[-1] = 3

        # all opcode variations
        if digits[-1] == 1: 
            array[array[i+3]] = mode1(digits[1]) + mode2(digits[0])
            i += 4
        elif digits[-1] == 2:
            array[array[i+3]] = mode1(digits[1]) * mode2(digits[0])
            i += 4
        elif digits[-1] == 3:
            array[array[i+1]] = inp1 if i == 0 or flag == 'halt' else inp2
            flag = ''
            i += 2 
        elif digits[-1] == 4:
            output = mode1(digits[1])
            flag = 'halt'
            return output, i, flag
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

def amplificationCircuit(array,arrayA,arrayB,arrayC,arrayD,arrayE):
    signals = []
    combos = list(permutations([5,6,7,8,9], 5))
    for combo in combos:
        assert len(combo) == 5
        # reset all variables to initial state
        arrayA, arrayB, arrayC, arrayD, arrayE = list(array), list(array), list(array), list(array), list(array)
        A, B, C, D, E = 0, 0, 0, 0, 0
        a, b, c, d, e = 0, 0, 0, 0, 0
        flagA, flagB, flagC, flagD, flagE = '', '', '', '', ''

        A, a, flagA = intcode(arrayA,a,combo[0],0,flagA)
        while flagA != '':
            B, b, flagB = intcode(arrayB,b,combo[1],A,flagB)
            C, c, flagC = intcode(arrayC,c,combo[2],B,flagC)
            D, d, flagD = intcode(arrayD,d,combo[3],C,flagD)
            E, e, flagE = intcode(arrayE,e,combo[4],D,flagE)
            A, a, flagA = intcode(arrayA,a,combo[0],E,flagA)
        signals.append(E)

    return max(signals)


f = open('day7_input.txt').read().strip().split(',')
array = list(map(int, f))
arrayA = list(map(int, f))
arrayB = list(map(int, f))
arrayC = list(map(int, f))
arrayD = list(map(int, f))
arrayE = list(map(int, f))

print(amplificationCircuit(array,arrayA,arrayB,arrayC,arrayD,arrayE))