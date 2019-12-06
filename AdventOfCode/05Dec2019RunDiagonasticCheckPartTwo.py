import math


def assertEqual(x, y):
    if(x != y):
        print("FAILED assertEqual : "+str(x)+" != "+str(y))
    assert x == y


def getParameterMode(number, paramOffset):
    nThDigit = math.pow(10, (paramOffset+1))
    return math.floor((number % (nThDigit*10)/nThDigit))


assertEqual(0, getParameterMode(2, 1))
assertEqual(1, getParameterMode(102, 1))
assertEqual(0, getParameterMode(2, 2))
assertEqual(1, getParameterMode(1002, 2))


def getValueByParameterMode(computerMemory, opCodeIndex, paramOffset):
    paramMode = getParameterMode(computerMemory[opCodeIndex], paramOffset)
    if paramMode == 0:
        return computerMemory[computerMemory[opCodeIndex+paramOffset]]
    return computerMemory[opCodeIndex+paramOffset]


assertEqual(10, getValueByParameterMode([2, 2, 10], 0, 1))
assertEqual(2, getValueByParameterMode([102, 2, 10], 0, 1))
assertEqual(10, getValueByParameterMode([2, 10, 1], 0, 2))
assertEqual(2, getValueByParameterMode([102, 10, 2], 0, 2))


def add(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    firstArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 2)
    computerMemory[computerMemory[opcodeIndex+3]] = firstArgumentValue+secondArgumentValue
    return opcodeIndex+4


opcodes = [1101, 2, 10, 3]
nextOpcodeIndex = add(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([1101, 2, 10, 12], opcodes)

opcodes = [1, 3, 2, 3]
nextOpcodeIndex = add(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([1, 3, 2, 5], opcodes)


def mul(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    firstArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 2)
    computerMemory[computerMemory[opcodeIndex+3]] = firstArgumentValue*secondArgumentValue
    return opcodeIndex+4


opcodes = [1102, 2, 10, 3]
nextOpcodeIndex = mul(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([1102, 2, 10, 20], opcodes)

opcodes = [2, 3, 2, 3]
nextOpcodeIndex = mul(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([2, 3, 2, 6], opcodes)


def input(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    computerMemory[computerMemory[opcodeIndex+1]] = inputValue
    return opcodeIndex+2


opcodes = [3, 1]
nextOpcodeIndex = input(opcodes, 5, 0, [])
assertEqual(2, nextOpcodeIndex)
assertEqual([3, 5], opcodes)


def output(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    firstArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 1)
    diagonasticOutput.append(firstArgumentValue)
    return opcodeIndex+2


diagnosticOutput = []
nextOpcodeIndex = output([104, 1], 0, 0, diagnosticOutput)
assertEqual(2, nextOpcodeIndex)
assertEqual([1], diagnosticOutput)


def jumpIfTrue(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    firstArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 1)
    if firstArgumentValue != 0:
        return getValueByParameterMode(computerMemory, opcodeIndex, 2)
    return opcodeIndex+3


assertEqual(10, jumpIfTrue([1105, 1, 10], 0, 0, []))
assertEqual(3, jumpIfTrue([1105, 0, 10], 0, 0, []))


def jumpIfFalse(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    firstArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 1)
    if firstArgumentValue == 0:
        return getValueByParameterMode(computerMemory, opcodeIndex, 2)
    return opcodeIndex+3


assertEqual(10, jumpIfFalse([1106, 0, 10], 0, 0, []))
assertEqual(3, jumpIfFalse([1106, 1, 10], 0, 0, []))


def lessThan(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    firstArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 2)
    computerMemory[computerMemory[opcodeIndex+3]] = 1 if firstArgumentValue < secondArgumentValue else 0
    return opcodeIndex+4


opcodes = [1107, 2, 10, 3]
nextOpcodeIndex = lessThan(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([1107, 2, 10, 1], opcodes)

opcodes = [1107, 10, 10, 3]
nextOpcodeIndex = lessThan(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([1107, 10, 10, 0], opcodes)

opcodes = [7, 1, 2, 3]
nextOpcodeIndex = lessThan(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([7, 1, 2, 1], opcodes)


def isEquals(computerMemory, inputValue, opcodeIndex, diagonasticOutput):
    firstArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerMemory, opcodeIndex, 2)
    computerMemory[computerMemory[opcodeIndex+3]] = 1 if firstArgumentValue == secondArgumentValue else 0
    return opcodeIndex+4


opcodes = [1107, 10, 10, 3]
nextOpcodeIndex = isEquals(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([1107, 10, 10, 1], opcodes)

opcodes = [7, 1, 2, 3]
nextOpcodeIndex = isEquals(opcodes, 0, 0, [])
assertEqual(4, nextOpcodeIndex)
assertEqual([7, 1, 2, 0], opcodes)

IntCodeInstructions = {
    1: add,
    2: mul,
    3: input,
    4: output,
    5: jumpIfTrue,
    6: jumpIfFalse,
    7: lessThan,
    8: isEquals,
}


def runDiagonasticCheck(computerMemory, inputValue, opcodeIndex=0, diagonasticOutput=[]):
    opCode = computerMemory[opcodeIndex] % 100
    # print(f"opcodeIndex : {opcodeIndex} ,opCode : {opCode} , computerMemory : {computerMemory}")
    if opCode == 99:
        return diagonasticOutput[len(diagonasticOutput)-1]
    elif opCode in IntCodeInstructions.keys():
        nextOpcodeIndex = IntCodeInstructions[opCode](computerMemory, inputValue, opcodeIndex, diagonasticOutput)
        return runDiagonasticCheck(computerMemory, inputValue, nextOpcodeIndex, diagonasticOutput)


assertEqual(1, runDiagonasticCheck([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8))
assertEqual(0, runDiagonasticCheck([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7))
assertEqual(1, runDiagonasticCheck([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7))
assertEqual(0, runDiagonasticCheck([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8))

assertEqual(1, runDiagonasticCheck([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8))
assertEqual(0, runDiagonasticCheck([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7))
assertEqual(1, runDiagonasticCheck([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7))
assertEqual(0, runDiagonasticCheck([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8))

assertEqual(0, runDiagonasticCheck([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0))
assertEqual(1, runDiagonasticCheck([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 6))

assertEqual(0, runDiagonasticCheck([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0))
assertEqual(1, runDiagonasticCheck([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 6))

assertEqual(999, runDiagonasticCheck([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                      1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],  7))
assertEqual(1000, runDiagonasticCheck([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                       1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                       999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],  8))
assertEqual(1001, runDiagonasticCheck([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                       1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                       999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],  9))

print(runDiagonasticCheck([3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1102, 57, 23, 224, 101, -1311, 224,
                           224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1, 223, 224, 223, 1102, 57, 67, 225,
                           102, 67, 150, 224, 1001, 224, -2613, 224, 4, 224, 1002, 223, 8, 223, 101, 5, 224, 224,
                           1, 224, 223, 223, 2, 179, 213, 224, 1001, 224, -469, 224, 4, 224, 102, 8, 223, 223, 101,
                           7, 224, 224, 1, 223, 224, 223, 1001, 188, 27, 224, 101, -119, 224, 224, 4, 224, 1002, 223,
                           8, 223, 1001, 224, 7, 224, 1, 223, 224, 223, 1, 184, 218, 224, 1001, 224, -155, 224, 4, 224,
                           1002, 223, 8, 223, 1001, 224, 7, 224, 1, 224, 223, 223, 1101, 21, 80, 224, 1001, 224, -101,
                           224, 4, 224, 102, 8, 223, 223, 1001, 224, 1, 224, 1, 224, 223, 223, 1101, 67, 39, 225, 1101,
                           89, 68, 225, 101, 69, 35, 224, 1001, 224, -126, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 1,
                           224, 1, 224, 223, 223, 1102, 7, 52, 225, 1102, 18, 90, 225, 1101, 65, 92, 225, 1002, 153, 78,
                           224, 101, -6942, 224, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 223, 224, 223, 1101,
                           67, 83, 225, 1102, 31, 65, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105,
                           0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106,
                           227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105,
                           1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0,
                           300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 1007, 226,
                           226, 224, 102, 2, 223, 223, 1005, 224, 329, 1001, 223, 1, 223, 108, 677, 226, 224, 1002, 223,
                           2, 223, 1005, 224, 344, 1001, 223, 1, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1005, 224,
                           359, 1001, 223, 1, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 374, 1001, 223, 1,
                           223, 8, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 389, 101, 1, 223, 223, 8, 677, 677, 224,
                           102, 2, 223, 223, 1006, 224, 404, 1001, 223, 1, 223, 1008, 226, 226, 224, 102, 2, 223, 223,
                           1006, 224, 419, 1001, 223, 1, 223, 107, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 434, 101,
                           1, 223, 223, 7, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 449, 1001, 223, 1, 223, 1107, 226,
                           226, 224, 1002, 223, 2, 223, 1006, 224, 464, 1001, 223, 1, 223, 1107, 226, 677, 224, 1002, 223,
                           2, 223, 1005, 224, 479, 1001, 223, 1, 223, 8, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 494,
                           1001, 223, 1, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 509, 101, 1, 223, 223, 1008,
                           677, 677, 224, 1002, 223, 2, 223, 1006, 224, 524, 1001, 223, 1, 223, 1008, 677, 226, 224, 102, 2,
                           223, 223, 1006, 224, 539, 1001, 223, 1, 223, 1108, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 554,
                           101, 1, 223, 223, 108, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 569, 101, 1, 223, 223, 1108, 677,
                           226, 224, 102, 2, 223, 223, 1005, 224, 584, 1001, 223, 1, 223, 108, 226, 226, 224, 1002, 223, 2, 223,
                           1005, 224, 599, 1001, 223, 1, 223, 1007, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 614, 1001, 223, 1,
                           223, 7, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 629, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2,
                           223, 223, 1005, 224, 644, 101, 1, 223, 223, 7, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 659, 101, 1,
                           223, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226], 5))
