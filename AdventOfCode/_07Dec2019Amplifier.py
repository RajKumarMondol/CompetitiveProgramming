from _IntComputer import IntComputerInstructions, takeInput, giveOutput
from Common import conditionalPrint, assertEqual
from itertools import permutations


class Amplifier:
    def __init__(self, amplifierProgram, phaseSetting):
        self.amplifierProgram = amplifierProgram
        self.phaseSetting = phaseSetting
        self.opcodeIndex = 0
        self.lastOutput = 0
        self.isHaulted = False
        self.inputSequence = [self.phaseSetting]
        self.nextInputIndex = 0

    def runIntComputerForOutputForGiven(self, inputValue):
        self.inputSequence.append(inputValue)
        result = self.runIntComputerForOutput()
        return result

    def runIntComputerForOutput(self):
        opCode = self.amplifierProgram[self.opcodeIndex] % 100
        if opCode == 99:
            self.isHaulted = True
            return "HLT"
        elif opCode == 3:
            if len(self.inputSequence) > self.nextInputIndex:
                self.opcodeIndex = takeInput(self.amplifierProgram, self.opcodeIndex, self.inputSequence[self.nextInputIndex])
                self.nextInputIndex += 1
            else:
                return "INP"
        elif opCode == 4:
            self.opcodeIndex, self.lastOutput = giveOutput(self.amplifierProgram, self.opcodeIndex)
            return self.lastOutput
        elif opCode in IntComputerInstructions.keys():
            self.opcodeIndex = IntComputerInstructions[opCode](self.amplifierProgram, self.opcodeIndex)
        return self.runIntComputerForOutput()


def generateAmplifierPhaseSettings(start, end):
    allPossiblePhases = list(range(start, end))
    return list(permutations(allPossiblePhases, 5))
