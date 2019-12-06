
def getPasswordCount(startNumber, lastNumber):
    passwordCount = 0
    for passWord in range(startNumber, lastNumber+1):
        if(isValidPassword(passWord)):
            passwordCount += 1
    return passwordCount


def isValidPassword(number):
    lastDigit = 0
    adjasentDigitCountList = []
    adjasentDigitCount = 1
    for currentDigit in [int(d) for d in str(number)]:
        if(lastDigit > currentDigit):
            return False
        elif lastDigit == currentDigit:
            adjasentDigitCount += 1
        else:
            adjasentDigitCountList.append(adjasentDigitCount)
            adjasentDigitCount = 1
        lastDigit = currentDigit
    adjasentDigitCountList.append(adjasentDigitCount)
    return 2 in adjasentDigitCountList


assert(isValidPassword(112233))
assert(not isValidPassword(123444))
assert(isValidPassword(111122))

print(getPasswordCount(246540, 787419))
