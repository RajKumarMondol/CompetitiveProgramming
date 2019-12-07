import math
from Common import conditionalPrint, assertEqual

def getParameterMode(number, paramOffset):
    nThDigit = math.pow(10, (paramOffset+1))
    return math.floor((number % (nThDigit*10)/nThDigit))


# assertEqual(0, getParameterMode(2, 1))
# assertEqual(1, getParameterMode(102, 1))
# assertEqual(0, getParameterMode(2, 2))
# assertEqual(1, getParameterMode(1002, 2))


def getValueByParameterMode(computerProgram, opCodeIndex, paramOffset):
    paramMode = getParameterMode(computerProgram[opCodeIndex], paramOffset)
    if paramMode == 0:
        return computerProgram[computerProgram[opCodeIndex+paramOffset]]
    return computerProgram[opCodeIndex+paramOffset]


# assertEqual(10, getValueByParameterMode([2, 2, 10], 0, 1))
# assertEqual(2, getValueByParameterMode([102, 2, 10], 0, 1))
# assertEqual(10, getValueByParameterMode([2, 10, 1], 0, 2))
# assertEqual(2, getValueByParameterMode([102, 10, 2], 0, 2))


def add(computerProgram,  opcodeIndex):
    firstArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 2)
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>add{computerProgram[opcodeIndex:opcodeIndex+4]}\t({firstArgumentValue},{secondArgumentValue})")
    computerProgram[computerProgram[opcodeIndex+3]] = firstArgumentValue+secondArgumentValue
    return opcodeIndex+4


# opcodes = [1101, 2, 10, 3]
# nextOpcodeIndex = add(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([1101, 2, 10, 12], opcodes)

# opcodes = [1, 3, 2, 3]
# nextOpcodeIndex = add(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([1, 3, 2, 5], opcodes)


def mul(computerProgram,  opcodeIndex):
    firstArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 2)
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>mul{computerProgram[opcodeIndex:opcodeIndex+4]}\t({firstArgumentValue},{secondArgumentValue})")
    computerProgram[computerProgram[opcodeIndex+3]] = firstArgumentValue*secondArgumentValue
    return opcodeIndex+4


# opcodes = [1102, 2, 10, 3]
# nextOpcodeIndex = mul(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([1102, 2, 10, 20], opcodes)

# opcodes = [2, 3, 2, 3]
# nextOpcodeIndex = mul(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([2, 3, 2, 6], opcodes)


def takeInput(computerProgram,  opcodeIndex, firstArgumentValue):
    computerProgram[computerProgram[opcodeIndex+1]] = firstArgumentValue
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>inp{computerProgram[opcodeIndex:opcodeIndex+2]}\t\t({firstArgumentValue})")
    # conditionalPrint(f"Input : {computerProgram[computerProgram[opcodeIndex+1]]}")
    return opcodeIndex+2


# opcodes = [3, 1]
# nextOpcodeIndex = takeInput(opcodes, 5, 0, [])
# assertEqual(2, nextOpcodeIndex)
# assertEqual([3, 5], opcodes)


def giveOutput(computerProgram,  opcodeIndex):
    firstArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 1)
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>out{computerProgram[opcodeIndex:opcodeIndex+2]}\t\t({firstArgumentValue})")
    return opcodeIndex+2, firstArgumentValue


# diagnosticOutput = []
# nextOpcodeIndex = giveOutput([104, 1], 0, 0, diagnosticOutput)
# assertEqual(2, nextOpcodeIndex)
# assertEqual([1], diagnosticOutput)


def jumpIfTrue(computerProgram,  opcodeIndex):
    firstArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 2)
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>jnz{computerProgram[opcodeIndex:opcodeIndex+3]}\t\t({firstArgumentValue},{secondArgumentValue})")
    if firstArgumentValue != 0:
        return secondArgumentValue
    return opcodeIndex+3


# assertEqual(10, jumpIfTrue([1105, 1, 10], 0, 0, []))
# assertEqual(3, jumpIfTrue([1105, 0, 10], 0, 0, []))


def jumpIfFalse(computerProgram,  opcodeIndex):
    firstArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 2)
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>jsz{computerProgram[opcodeIndex:opcodeIndex+3]}\t\t({firstArgumentValue},{secondArgumentValue})")
    if firstArgumentValue == 0:
        return secondArgumentValue
    return opcodeIndex+3


# assertEqual(10, jumpIfFalse([1106, 0, 10], 0, 0, []))
# assertEqual(3, jumpIfFalse([1106, 1, 10], 0, 0, []))


def lessThan(computerProgram,  opcodeIndex):
    firstArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 2)
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>lt {computerProgram[opcodeIndex:opcodeIndex+4]}\t({firstArgumentValue},{secondArgumentValue})")
    computerProgram[computerProgram[opcodeIndex+3]] = 1 if firstArgumentValue < secondArgumentValue else 0
    return opcodeIndex+4


# opcodes = [1107, 2, 10, 3]
# nextOpcodeIndex = lessThan(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([1107, 2, 10, 1], opcodes)

# opcodes = [1107, 10, 10, 3]
# nextOpcodeIndex = lessThan(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([1107, 10, 10, 0], opcodes)

# opcodes = [7, 1, 2, 3]
# nextOpcodeIndex = lessThan(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([7, 1, 2, 1], opcodes)


def isEquals(computerProgram,  opcodeIndex):
    firstArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 1)
    secondArgumentValue = getValueByParameterMode(computerProgram, opcodeIndex, 2)
    conditionalPrint(f"opcodeIndex : {opcodeIndex}>>eql{computerProgram[opcodeIndex:opcodeIndex+4]}\t({firstArgumentValue},{secondArgumentValue})")
    computerProgram[computerProgram[opcodeIndex+3]] = 1 if firstArgumentValue == secondArgumentValue else 0
    return opcodeIndex+4


# opcodes = [1107, 10, 10, 3]
# nextOpcodeIndex = isEquals(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([1107, 10, 10, 1], opcodes)

# opcodes = [7, 1, 2, 3]
# nextOpcodeIndex = isEquals(opcodes, 0, 0, [])
# assertEqual(4, nextOpcodeIndex)
# assertEqual([7, 1, 2, 0], opcodes)

IntComputerInstructions = {
    1: add,
    2: mul,
    5: jumpIfTrue,
    6: jumpIfFalse,
    7: lessThan,
    8: isEquals,
}
