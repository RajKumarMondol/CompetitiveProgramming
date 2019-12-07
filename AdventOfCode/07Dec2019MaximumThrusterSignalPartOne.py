from Common import assertEqual
from _07Dec2019Amplifier import Amplifier, generateAmplifierPhaseSettings


def runAllAmplifierInSeries(amplifierProgram, phaseSettings):
    amplifierList = list([Amplifier(amplifierProgram[:], phaseSettings[i]) for i in range(0, 5)])
    nextInput = 0
    for amplifier in amplifierList:
        result = amplifier.runIntComputerForOutputForGiven(nextInput)
        if result == "HLT" or result == "INP":
            return None
        nextInput = result
    return nextInput


def maximumAmplifierOutput(computerProgram):
    maximumOutput = 0
    maximumOutputPhaseSettings = []
    for phaseSettings in generateAmplifierPhaseSettings(0, 5):
        outPut = runAllAmplifierInSeries(computerProgram, phaseSettings)
        if outPut > maximumOutput:
            maximumOutput = outPut
            maximumOutputPhaseSettings = phaseSettings
    return maximumOutput, maximumOutputPhaseSettings


assertEqual((43210, (4, 3, 2, 1, 0)), maximumAmplifierOutput([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]))
assertEqual((54321, (0, 1, 2, 3, 4)), maximumAmplifierOutput([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]))
assertEqual((65210, (1, 0, 4, 3, 2)), maximumAmplifierOutput([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]))

print(maximumAmplifierOutput([3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 34, 51, 64, 81, 102, 183, 264, 345, 426, 99999, 3, 9, 102, 2, 9, 9, 1001, 9, 4, 9, 4, 9, 99, 3, 9, 101, 4, 9, 9, 102, 5, 9, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 101, 3, 9, 9, 1002, 9, 5, 9, 4, 9, 99, 3, 9, 102, 3, 9, 9, 101, 3, 9, 9, 1002, 9, 4, 9, 4, 9, 99, 3, 9, 1002, 9, 3, 9, 1001, 9, 5, 9, 1002, 9, 5, 9, 101, 3, 9, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9,
                              4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 99]))
