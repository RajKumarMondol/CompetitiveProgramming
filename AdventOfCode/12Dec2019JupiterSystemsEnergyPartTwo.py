from Common import assertEqual
import math


def calculateVelocityChange(a, b):
    return 0 if a == b else (1 if a < b else -1)


def getLCM(a, b):
    return a*b//math.gcd(a, b)


def getCycleTimeForMoon(x, y, z):
    return getLCM(getLCM(x, y), z)


assertEqual(30, getCycleTimeForMoon(6, 10, 15))


def getCycleTimeForAllMoons(a, b, c, d):
    return getLCM(getLCM(getLCM(a, b), c), d)


class Point:
    def __init__(self, position):
        self.position = self.initialPosition = position
        self.velocity = self.initialVelocity = 0
        self.cycleStepsCount = 0

    def calculateEffectiveVelocity(self, effectingPoints):
        for point in effectingPoints:
            if self != point:
                self.velocity += calculateVelocityChange(self.position, point.position)

    def isBackToInitialPosition(self):
        return self.position == self.initialPosition and self.velocity == self.initialVelocity

    def move(self):
        self.position += self.velocity

    def __str__(self):
        return f"pos=<A={self.position:3} >, vel=<A={self.velocity:3} >"


def calculateTimeStepsToComeToInitialPosition(moonAxises):
    axisCycleCounts = []
    for axis in moonAxises:
        points = [Point(i) for i in axis]
        detectedCycles = []
        steps = 0
        while len(detectedCycles) < 4:
            for point in points:
                point.calculateEffectiveVelocity(points)
            steps += 1
            for point in points:
                point.move()

            detectedCycles = [steps for point in points if point.isBackToInitialPosition()]
        axisCycleCounts.append(steps)

    # print(axisCycleCounts)
    return getCycleTimeForMoon(axisCycleCounts[0], axisCycleCounts[1], axisCycleCounts[2])


assertEqual(2772, calculateTimeStepsToComeToInitialPosition([
    [-1, 2, 4, 3],
    [0, -10, -8, 5],
    [2, -7, 8, -1]
]))


assertEqual(4686774924, calculateTimeStepsToComeToInitialPosition([
    [-8, 5, 2, 9],
    [-10, 5, -7, -8],
    [0, 10, 3, -3],
]))

print(calculateTimeStepsToComeToInitialPosition([
    [1, -14, -4, 6],
    [-4, 9, -6, -9],
    [3, -4, 7, -11]
]))
