from IntComputer import IntComputerInstructions, assertEqual


def runIntComputer(computerProgram,  inputIterator, opcodeIndex, diagonasticOutput):
    opCode = computerProgram[opcodeIndex] % 100
    # print(f"opcodeIndex : {opcodeIndex} ,opCode : {opCode} , computerProgram : {computerProgram}")
    if opCode == 99:
        # print(diagonasticOutput)
        return diagonasticOutput[len(diagonasticOutput)-1]
    elif opCode in IntComputerInstructions.keys():
        nextOpcodeIndex = IntComputerInstructions[opCode](computerProgram, inputIterator, opcodeIndex, diagonasticOutput)
        return runIntComputer(computerProgram, inputIterator, nextOpcodeIndex, diagonasticOutput)


def runAllAmplifier(computerProgram, phaseSettings):
    nextInput = 0
    for phaseSetting in phaseSettings:
        amplifilerMemory = computerProgram[:]
        nextInput = runIntComputer(amplifilerMemory, iter([phaseSetting, nextInput]), 0, [])
    return nextInput


def maximumAmplifierOutput(computerProgram):
    maximumOutput = 0
    maximumOutputPhaseSettings = []
    allPossiblePhases = list(range(0, 5))
    for amplifierAPhaseValue in allPossiblePhases:
        phaseSettingsA = [amplifierAPhaseValue]
        for amplifierBPhaseValue in [x for x in allPossiblePhases if x not in phaseSettingsA]:
            phaseSettingsAB = phaseSettingsA[:]
            phaseSettingsAB.append(amplifierBPhaseValue)
            for amplifierCPhaseValue in [x for x in allPossiblePhases if x not in phaseSettingsAB]:
                phaseSettingsABC = phaseSettingsAB[:]
                phaseSettingsABC.append(amplifierCPhaseValue)
                for amplifierDPhaseValue in [x for x in allPossiblePhases if x not in phaseSettingsABC]:
                    phaseSettingsABCD = phaseSettingsABC[:]
                    phaseSettingsABCD.append(amplifierDPhaseValue)
                    for amplifierEPhaseValue in [x for x in allPossiblePhases if x not in phaseSettingsABCD]:
                        phaseSettingsABCDE = phaseSettingsABCD[:]
                        phaseSettingsABCDE.append(amplifierEPhaseValue)
                        outPut = runAllAmplifier(computerProgram, phaseSettingsABCDE)
                        # print(f"outPut : {outPut}, phaseSettings : {phaseSettingsABCDE}")
                        if outPut > maximumOutput:
                            maximumOutput = outPut
                            maximumOutputPhaseSettings = phaseSettingsABCDE
    return maximumOutput, maximumOutputPhaseSettings


assertEqual((43210, [4, 3, 2, 1, 0]), maximumAmplifierOutput([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]))
assertEqual((54321, [0, 1, 2, 3, 4]), maximumAmplifierOutput([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]))
assertEqual((65210, [1, 0, 4, 3, 2]), maximumAmplifierOutput([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]))

print(maximumAmplifierOutput([3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 34, 51, 64, 81, 102, 183, 264, 345, 426, 99999, 3, 9, 102, 2, 9, 9, 1001, 9, 4, 9, 4, 9, 99, 3, 9, 101, 4, 9, 9, 102, 5, 9, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 101, 3, 9, 9, 1002, 9, 5, 9, 4, 9, 99, 3, 9, 102, 3, 9, 9, 101, 3, 9, 9, 1002, 9, 4, 9, 4, 9, 99, 3, 9, 1002, 9, 3, 9, 1001, 9, 5, 9, 1002, 9, 5, 9, 101, 3, 9, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9,
                              4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 99]))
