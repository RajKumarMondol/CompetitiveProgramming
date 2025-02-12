from Common import conditionalPrint, assertEqual
from itertools import permutations
import math


class ArchadeCabinet:
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

    def doPrint(self):
        printedPanels = {i: [] for i in range(5)}
        while True:
            opCode = self.readMemory(self.opcodeIndex) % 100
            if opCode == 99:
                self.isHaulted = True
                conditionalPrint(f"opcodeIndex : {self.opcodeIndex}>>hlt[99]")
                return printedPanels
            elif opCode == 3:
                panelColorCode = 0
                self.opcodeIndex = self.takeInput(panelColorCode)
            elif opCode == 4:
                self.opcodeIndex, output = self.giveOutput()
                self.outputSequence.append(output)
                if len(self.outputSequence) == 3:
                    printedPanels[output].append((self.outputSequence[0], self.outputSequence[1]))
                    self.outputSequence.clear()
            elif opCode in self.instructionMap.keys():
                self.opcodeIndex = self.instructionMap[opCode]()


printedPanels=ArchadeCabinet([1,380,379,385,1008,2415,504308,381,1005,381,12,99,109,2416,1101,0,0,383,1102,1,0,382,20101,0,382,1,20102,1,383,2,21102,1,37,0,1106,0,578,4,382,4,383,204,1,1001,382,1,382,1007,382,37,381,1005,381,22,1001,383,1,383,1007,383,24,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1105,1,161,107,1,392,381,1006,381,161,1101,-1,0,384,1105,1,119,1007,392,35,381,1006,381,161,1101,0,1,384,20102,1,392,1,21102,22,1,2,21102,1,0,3,21101,0,138,0,1106,0,549,1,392,384,392,21002,392,1,1,21102,1,22,2,21102,1,3,3,21102,1,161,0,1105,1,549,1102,0,1,384,20001,388,390,1,20101,0,389,2,21101,0,180,0,1106,0,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,21002,389,1,2,21102,205,1,0,1105,1,393,1002,390,-1,390,1102,1,1,384,21002,388,1,1,20001,389,391,2,21102,228,1,0,1106,0,578,1206,1,261,1208,1,2,381,1006,381,253,20101,0,388,1,20001,389,391,2,21101,253,0,0,1105,1,393,1002,391,-1,391,1102,1,1,384,1005,384,161,20001,388,390,1,20001,389,391,2,21101,279,0,0,1106,0,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21101,0,304,0,1106,0,393,1002,390,-1,390,1002,391,-1,391,1102,1,1,384,1005,384,161,21001,388,0,1,21001,389,0,2,21101,0,0,3,21102,1,338,0,1105,1,549,1,388,390,388,1,389,391,389,20102,1,388,1,20102,1,389,2,21101,0,4,3,21101,0,365,0,1105,1,549,1007,389,23,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,286,16,19,1,1,18,109,3,22102,1,-2,1,22102,1,-1,2,21101,0,0,3,21101,0,414,0,1106,0,549,21202,-2,1,1,22101,0,-1,2,21102,429,1,0,1105,1,601,2101,0,1,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2106,0,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,21201,-3,0,-7,109,-8,2105,1,0,109,4,1202,-2,37,566,201,-3,566,566,101,639,566,566,2102,1,-1,0,204,-3,204,-2,204,-1,109,-4,2106,0,0,109,3,1202,-1,37,594,201,-2,594,594,101,639,594,594,20101,0,0,-2,109,-3,2106,0,0,109,3,22102,24,-2,1,22201,1,-1,1,21101,449,0,2,21102,721,1,3,21101,888,0,4,21102,1,630,0,1105,1,456,21201,1,1527,-2,109,-3,2106,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,2,2,0,2,2,2,0,2,2,2,0,2,2,2,2,0,0,2,2,0,2,0,0,2,0,2,2,2,2,0,2,0,0,1,1,0,0,2,0,0,0,2,0,2,2,0,0,0,2,2,2,0,0,0,2,2,2,0,2,2,0,0,0,0,0,0,0,2,0,0,1,1,0,0,2,0,2,0,2,0,2,0,2,2,0,2,0,2,0,2,2,2,0,0,2,2,2,0,2,0,2,2,2,2,0,0,0,1,1,0,0,2,0,0,0,0,2,0,0,0,2,0,0,2,2,2,2,2,2,2,0,0,0,0,2,2,2,2,2,0,2,2,2,0,1,1,0,2,2,2,0,0,2,2,2,2,2,2,0,2,0,0,0,2,0,0,2,2,2,0,2,0,2,0,2,0,0,2,2,2,0,1,1,0,0,2,2,2,2,0,2,0,2,0,0,2,0,2,2,2,2,2,0,2,0,2,2,0,2,0,2,2,2,0,2,2,0,0,1,1,0,0,0,0,2,2,2,2,2,0,0,2,0,0,0,0,2,0,2,2,0,2,2,2,2,2,0,2,2,0,0,0,2,2,0,1,1,0,2,0,2,2,2,0,0,0,0,0,0,0,2,2,2,2,2,2,2,0,2,0,2,2,0,2,0,2,0,0,0,0,0,0,1,1,0,0,0,2,2,0,0,2,0,0,2,2,2,2,2,0,0,2,2,2,2,0,2,0,0,0,2,2,2,0,2,2,2,2,0,1,1,0,0,0,0,0,2,0,2,2,2,0,0,2,2,2,0,2,2,2,0,0,2,2,0,2,2,2,2,0,0,2,2,2,0,0,1,1,0,0,2,0,2,2,2,2,0,0,0,0,2,0,0,0,2,0,0,0,0,2,0,0,0,0,2,2,0,0,0,2,2,2,0,1,1,0,0,2,0,2,2,2,2,0,0,0,0,0,2,2,2,2,2,2,0,0,2,2,0,2,0,0,2,2,2,2,2,2,0,0,1,1,0,0,2,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,2,2,2,0,2,0,2,2,2,2,0,2,0,2,0,1,1,0,0,2,2,2,0,2,2,2,2,0,2,0,2,0,2,0,0,0,0,0,0,2,2,0,2,2,2,2,0,0,2,2,0,0,1,1,0,0,0,2,0,2,2,2,0,0,2,2,2,0,2,0,0,2,2,2,0,2,0,2,2,0,2,2,2,2,0,0,0,0,0,1,1,0,2,2,0,2,2,0,2,0,2,2,2,2,0,2,2,0,2,2,2,0,2,0,0,0,2,0,2,0,0,0,0,0,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,72,24,61,53,70,95,17,71,27,25,75,75,9,41,47,87,93,47,92,11,93,87,16,9,94,89,5,46,23,64,39,44,23,93,27,28,10,82,54,70,26,84,86,88,64,20,6,8,8,27,46,80,6,57,15,35,55,86,30,72,88,50,49,11,31,76,89,50,24,13,71,45,35,46,57,14,84,36,1,41,48,87,67,92,83,28,41,7,33,60,66,16,46,42,49,47,53,27,60,84,63,32,23,17,67,61,56,7,31,68,43,50,37,36,56,6,65,35,9,56,15,32,64,68,7,52,30,15,55,71,57,97,31,60,37,35,85,96,59,14,83,76,47,71,65,39,37,22,77,90,60,38,29,72,11,49,40,20,26,19,80,83,58,67,50,94,79,62,86,57,76,44,36,37,55,67,6,26,34,63,80,33,64,45,39,93,70,26,4,71,79,71,21,70,31,48,58,50,54,74,53,31,89,78,57,70,52,70,85,68,5,1,55,12,25,74,81,36,3,3,8,97,9,62,58,80,45,87,45,17,80,62,25,63,29,97,84,55,11,28,86,55,39,81,93,48,67,46,62,79,58,63,87,66,89,23,81,95,22,41,29,87,30,14,67,94,13,7,32,56,66,29,89,77,17,54,12,82,59,83,89,65,72,56,78,97,5,24,20,27,5,37,66,68,77,16,9,66,41,43,18,94,84,86,42,25,47,72,7,8,93,28,68,6,75,55,44,36,15,71,9,49,66,80,77,81,13,7,73,1,86,17,80,36,12,57,42,1,50,87,74,37,60,91,92,46,75,1,17,83,65,49,61,44,13,69,36,90,10,35,61,53,66,11,62,33,14,58,24,82,11,68,48,20,96,68,56,57,77,71,24,41,46,81,43,55,96,30,69,63,23,86,55,83,1,23,88,88,20,66,39,23,26,2,21,80,57,68,3,88,68,1,76,67,84,63,89,45,84,20,97,29,97,7,92,84,65,49,31,93,63,30,89,96,93,37,15,97,30,69,39,1,22,68,5,75,38,39,62,19,24,30,38,36,27,93,1,3,27,39,69,3,86,42,92,81,18,37,16,94,1,94,47,81,51,25,11,6,25,28,78,50,89,39,6,41,27,31,22,17,33,76,2,36,64,79,14,81,91,11,45,12,17,57,70,17,49,54,45,83,71,68,25,89,62,4,55,73,77,98,1,1,36,11,12,78,56,71,96,55,85,71,49,57,68,14,76,63,22,60,79,11,61,49,39,36,33,59,73,85,8,38,3,21,65,21,31,69,54,85,38,26,5,73,43,87,15,44,80,10,92,54,75,96,26,53,84,37,1,76,53,77,68,13,67,64,11,31,32,86,85,71,98,37,53,45,3,3,87,20,20,36,95,87,41,74,23,76,78,19,45,57,41,89,1,11,42,85,74,13,3,72,19,20,64,25,51,82,97,45,55,37,86,2,25,40,26,78,76,16,11,14,36,96,89,90,64,96,79,32,17,47,79,80,53,19,26,59,74,54,53,58,32,48,9,64,96,3,20,88,1,92,44,45,10,4,67,91,81,26,40,89,83,53,83,84,18,53,6,94,51,59,27,38,41,63,2,8,48,64,4,90,88,21,14,37,68,46,1,73,21,14,41,65,81,97,56,90,24,30,81,68,19,16,47,65,53,68,26,54,26,56,15,25,83,89,20,92,4,49,37,42,5,54,7,27,43,36,85,41,59,44,33,93,45,46,23,19,52,20,87,25,85,21,22,20,43,70,35,33,27,17,23,9,56,33,53,55,22,91,69,73,20,23,86,95,14,24,59,60,37,48,94,69,86,63,39,50,84,85,46,65,4,42,97,12,66,37,89,47,29,59,25,47,74,44,24,22,73,45,60,70,11,40,83,49,95,17,9,85,2,27,90,60,32,87,62,36,91,38,19,92,2,33,30,17,43,13,81,53,93,75,14,67,97,95,53,20,63,5,45,63,84,92,65,65,70,33,11,79,82,89,36,59,90,74,6,74,17,96,40,72,89,84,51,17,40,42,504308]).doPrint()

print(len(printedPanels[2]))
