from Common import conditionalPrint, assertEqual
from itertools import permutations
import math


class PrintingRobot:
    def __init__(self, programCode):
        self.programCode = {v: k for v, k in enumerate(programCode)}
        self.opcodeIndex = 0
        self.isHaulted = False
        self.outputSequence = []
        self.nextInputIndex = 0
        self.relativeBase = 0
        self.instructionMap = {
            1: self.add,
            2: self.mul,
            5: self.jumpIfTrue,
            6: self.jumpIfFalse,
            7: self.lessThan,
            8: self.isEquals,
            9: self.changeRelativeBase,
        }

    def readMemory(self, address):
        return self.programCode.get(address, 0)

    def readArray(self, startAddress, endAddress):
        return [self.programCode.get(i, 0) for i in range(startAddress, endAddress)]

    def writeMemory(self, address, value):
        self.programCode[address] = value

    def getParameterMode(self, number, paramOffset):
        nThDigit = math.pow(10, (paramOffset+1))
        return math.floor((number % (nThDigit*10)/nThDigit))

    def getValueByParameterMode(self, paramOffset):
        paramMode = self.getParameterMode(self.readMemory(self.opcodeIndex), paramOffset)
        paramValue = self.readMemory(self.opcodeIndex+paramOffset)
        if paramMode == 0:
            return self.readMemory(paramValue)
        elif paramMode == 1:
            return paramValue
        elif paramMode == 2:
            # print(f"\t\t\tparam mode : {paramMode}, relativeBase : {self.relativeBase}, paramValue : {paramValue}")
            return self.readMemory(self.relativeBase + paramValue)

    def setValueByParameterMode(self, paramOffset, value):
        paramMode = self.getParameterMode(self.readMemory(self.opcodeIndex), paramOffset)
        outputAddress = self.readMemory(self.opcodeIndex+paramOffset)
        if paramMode == 2:
            outputAddress = self.relativeBase + outputAddress
        self.writeMemory(outputAddress, value)
        return outputAddress

    def add(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        secondArgumentValue = self.getValueByParameterMode(2)
        output = firstArgumentValue+secondArgumentValue
        outputAddress = self.setValueByParameterMode(3, output)
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>add{self.readArray(self.opcodeIndex,self.opcodeIndex+4)}\t[{outputAddress}]{output}=({firstArgumentValue},{secondArgumentValue})")
        return self.opcodeIndex+4

    def mul(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        secondArgumentValue = self.getValueByParameterMode(2)
        output = firstArgumentValue*secondArgumentValue
        outputAddress = self.setValueByParameterMode(3, output)
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>mul{self.readArray(self.opcodeIndex,self.opcodeIndex+4)}\t[{outputAddress}]{output}=({firstArgumentValue},{secondArgumentValue})")
        return self.opcodeIndex+4

    def takeInput(self, inputValue):
        self.setValueByParameterMode(1, inputValue)
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>inp{self.readArray(self.opcodeIndex,self.opcodeIndex+2)}\t\t\t\t>>{inputValue}")
        return self.opcodeIndex+2

    def giveOutput(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>out{self.readArray(self.opcodeIndex,self.opcodeIndex+2)}\t\t\t\t>>({firstArgumentValue})")
        return self.opcodeIndex+2, firstArgumentValue

    def jumpIfTrue(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        secondArgumentValue = self.getValueByParameterMode(2)
        newOpcodeAddress = secondArgumentValue if firstArgumentValue != 0 else self.opcodeIndex+3
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>jnz{self.readArray(self.opcodeIndex,self.opcodeIndex+3)}\t\t[{newOpcodeAddress}]=({firstArgumentValue},{secondArgumentValue})")
        return newOpcodeAddress

    def jumpIfFalse(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        secondArgumentValue = self.getValueByParameterMode(2)
        newOpcodeAddress = secondArgumentValue if firstArgumentValue == 0 else self.opcodeIndex+3
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>jsz{self.readArray(self.opcodeIndex,self.opcodeIndex+3)}\t\t[{newOpcodeAddress}]=({firstArgumentValue},{secondArgumentValue})")
        return newOpcodeAddress

    def lessThan(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        secondArgumentValue = self.getValueByParameterMode(2)
        output = 1 if firstArgumentValue < secondArgumentValue else 0
        outputAddress = self.setValueByParameterMode(3, output)
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>lt {self.readArray(self.opcodeIndex,self.opcodeIndex+4)}\t[{outputAddress}]{output}=({firstArgumentValue},{secondArgumentValue})")
        return self.opcodeIndex+4

    def isEquals(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        secondArgumentValue = self.getValueByParameterMode(2)
        output = 1 if firstArgumentValue == secondArgumentValue else 0
        outputAddress = self.setValueByParameterMode(3, output)
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>eql{self.readArray(self.opcodeIndex,self.opcodeIndex+4)}\t[{outputAddress}]{output}=({firstArgumentValue},{secondArgumentValue})")
        return self.opcodeIndex+4

    def changeRelativeBase(self):
        firstArgumentValue = self.getValueByParameterMode(1)
        conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>crb{self.readArray(self.opcodeIndex,self.opcodeIndex+2)}\t\t({self.relativeBase}>{firstArgumentValue})>>{self.relativeBase+firstArgumentValue}")
        self.relativeBase += firstArgumentValue
        return self.opcodeIndex+2

    def doPrint(self,startPanelColor):
        printedPanels = {(0, 0): startPanelColor}
        x = 0
        y = 0
        direction = "^"
        while True:
            opCode = self.readMemory(self.opcodeIndex) % 100
            if opCode == 99:
                self.isHaulted = True
                conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>hlt[99]")
                return printedPanels
            elif opCode == 3:
                panelColorCode = printedPanels.get((x, y), 0)
                self.opcodeIndex = self.takeInput(panelColorCode)
            elif opCode == 4:
                self.opcodeIndex, output = self.giveOutput()
                self.outputSequence.append(output)
                if len(self.outputSequence) % 2 == 1:
                    printedPanels[(x, y)] = output
                else:
                    # print(f"output>>{[(direction, x, y), printedPanels[(x, y)], output]}")
                    if output == 0:
                        direction, x, y = turnLeft[direction](x, y)
                    else:
                        direction, x, y = turnRight[direction](x, y)
            elif opCode in self.instructionMap.keys():
                self.opcodeIndex = self.instructionMap[opCode]()


turnLeft = {
    "^": lambda x, y: ("<", x-1, y),
    "<": lambda x, y: ("v", x, y+1),
    "v": lambda x, y: (">", x+1, y),
    ">": lambda x, y: ("^", x, y-1),
}
assertEqual(("<", 0, 1), turnLeft["^"](1, 1))
assertEqual(("v", 1, 2), turnLeft["<"](1, 1))
assertEqual((">", 2, 1), turnLeft["v"](1, 1))
assertEqual(("^", 1, 0), turnLeft[">"](1, 1))

turnRight = {
    "^": lambda x, y: (">", x+1, y),
    "<": lambda x, y: ("^", x, y-1),
    ">": lambda x, y: ("v", x, y+1),
    "v": lambda x, y: ("<", x-1, y),
}

assertEqual((">", 2, 1), turnRight["^"](1, 1))
assertEqual(("^", 1, 0), turnRight["<"](1, 1))
assertEqual(("v", 1, 2), turnRight[">"](1, 1))
assertEqual(("<", 0, 1), turnRight["v"](1, 1))
