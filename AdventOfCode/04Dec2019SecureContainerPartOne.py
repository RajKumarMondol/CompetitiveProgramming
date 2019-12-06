
def getPasswordCount(startNumber, lastNumber):
    passwordCount = 0
    for passWord in range(startNumber, lastNumber+1):
        if(isValidPassword(passWord)):
            passwordCount += 1
    return passwordCount


def isValidPassword(number):
    lastDigit = 0
    isSameAdjasentDigits = False
    for currentDigit in [int(d) for d in str(number)]:
        if(lastDigit > currentDigit):
            return False
        elif lastDigit == currentDigit:
            isSameAdjasentDigits = True
        lastDigit = currentDigit
    return isSameAdjasentDigits


assert(2 == getPasswordCount(111111, 111112))

print(getPasswordCount(246540, 787419))
