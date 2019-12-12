from Common import assertEqual


def calculateVelocityChange(a, b):
    return 0 if a == b else (1 if a < b else -1)


class Moon:
    def __init__(self, position):
        self.x, self.y, self.z = position
        self.velocityX = 0
        self.velocityY = 0
        self.velocityZ = 0

    def calculateEffectiveVelocity(self, effectingMoons):
        for moon in effectingMoons:
            if self != moon:
                self.velocityX += calculateVelocityChange(self.x, moon.x)
                self.velocityY += calculateVelocityChange(self.y, moon.y)
                self.velocityZ += calculateVelocityChange(self.z, moon.z)

    def move(self):
        self.x += self.velocityX
        self.y += self.velocityY
        self.z += self.velocityZ

    def energy(self):
        return (abs(self.x)+abs(self.y)+abs(self.z))*(abs(self.velocityX)+abs(self.velocityY)+abs(self.velocityZ))

    def __str__(self):
        return f"pos=<x={self.x:3}, y={self.y:3}, z={self.z:3}>, vel=<x={self.velocityX:3}, y={self.velocityY:3}, z={self.velocityZ:3}>"


def calculateMoonEnergyAfterTime(n, moons):
    for i in range(1, n+1):
        for moon in moons:
            moon.calculateEffectiveVelocity(moons)

        for moon in moons:
            moon.move()

        # print(f"After {i} steps:")
        # for moon in moons:
        #     print(moon)

    totalEnergy = 0
    for moon in moons:
        # print(moon.energy())
        totalEnergy += moon.energy()

    return totalEnergy


assertEqual(179, calculateMoonEnergyAfterTime(10, [
    Moon((-1, 0, 2)),
    Moon((2, -10, -7)),
    Moon((4, -8, 8)),
    Moon((3, 5, -1))
]))

assertEqual(1940, calculateMoonEnergyAfterTime(100, [
    Moon((-8, -10, 0)),
    Moon((5, 5, 10)),
    Moon((2, -7, 3)),
    Moon((9, -8, -3))
]))

print(calculateMoonEnergyAfterTime(1000, [
    Moon((1, -4, 3)),
    Moon((-14, 9, -4)),
    Moon((-4, -6, 7)),
    Moon((6, -9, -11)),
]))
