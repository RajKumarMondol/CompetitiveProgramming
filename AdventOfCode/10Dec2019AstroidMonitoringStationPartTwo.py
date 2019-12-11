from Common import assertEqual
import math


def calculateVisibilityAngle(astroidA, astroidB):
    ax, ay = astroidA
    bx, by = astroidB
    degree = math.degrees(math.atan2((bx-ax), (ay-by)))
    if degree < 0:
        degree += 360
    return degree


assertEqual(0, calculateVisibilityAngle((10, 10), (10, 0)))
assertEqual(90, calculateVisibilityAngle((10, 10), (20, 10)))
assertEqual(180, calculateVisibilityAngle((10, 10), (10, 20)))
assertEqual(270, calculateVisibilityAngle((10, 10), (0, 10)))


def distanseSqr(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB
    return (ax-bx)**2 + (ay-by)**2


def getAstroidOrderbyVisibilityAngles(coordinate, astroidCoordinates):
    visibilityAngles = {}
    for astroidCoordinate in astroidCoordinates:
        if astroidCoordinate != coordinate:
            angle = calculateVisibilityAngle(coordinate, astroidCoordinate)
            if angle in visibilityAngles.keys():
                visibilityAngles[angle].append(astroidCoordinate)
            else:
                visibilityAngles[angle] = [astroidCoordinate]
    for key in visibilityAngles:
        visibilityAngles[key].sort(key=lambda item: distanseSqr(item, coordinate), reverse=True)
    return visibilityAngles


assertEqual({180.0: [(0, 4)], 135.0: [(1, 2)]}, getAstroidOrderbyVisibilityAngles((0, 1), [(0, 1), (0, 4), (1, 2)]))


def getAstroidCoordinateForNthAstroidToVepourise(n, fromAstroid, inputMap):
    astroidList = []
    for row in range(len(inputMap)):
        for col in range(len(inputMap[row])):
            if inputMap[row][col] == "#":
                astroidList.append((col, row))
    astroidVisibilityAngles = getAstroidOrderbyVisibilityAngles(fromAstroid, astroidList)
    veporisedAstroidCoordinate = 0
    count = 0
    while count < n:
        anglesWhereAstroidArePresent = list(astroidVisibilityAngles.keys())
        anglesWhereAstroidArePresent.sort()
        for angle in anglesWhereAstroidArePresent:
            astroidInCurrentAngle = astroidVisibilityAngles[angle]
            veporisedAstroidCoordinate = astroidInCurrentAngle.pop()
            # print((angle, veporisedAstroidCoordinate))
            if len(astroidInCurrentAngle) == 0:
                astroidVisibilityAngles.pop(angle, None)
            count += 1
            if count == n:
                break

    return veporisedAstroidCoordinate


inputMap = [
    ".#..##.###...#######",
    "##.############..##.",
    ".#.######.########.#",
    ".###.#######.####.#.",
    "#####.##.#.##.###.##",
    "..#####..#.#########",
    "####################",
    "#.####....###.#.#.##",
    "##.#################",
    "#####.##.###..####..",
    "..######..##.#######",
    "####.##.####...##..#",
    ".#####..#.######.###",
    "##...#.##########...",
    "#.##########.#######",
    ".####.#.###.###.#.##",
    "....##.##.###..#####",
    ".#.#.###########.###",
    "#.#.#.#####.####.###",
    "###.##.####.##.#..##", ]

assertEqual((11, 12), getAstroidCoordinateForNthAstroidToVepourise(1, (11, 13), inputMap))
assertEqual((12, 1), getAstroidCoordinateForNthAstroidToVepourise(2, (11, 13), inputMap))
assertEqual((12, 2), getAstroidCoordinateForNthAstroidToVepourise(3, (11, 13), inputMap))
assertEqual((12, 8), getAstroidCoordinateForNthAstroidToVepourise(10, (11, 13), inputMap))
assertEqual((16, 0), getAstroidCoordinateForNthAstroidToVepourise(20, (11, 13), inputMap))
assertEqual((16, 9), getAstroidCoordinateForNthAstroidToVepourise(50, (11, 13), inputMap))
assertEqual((10, 16), getAstroidCoordinateForNthAstroidToVepourise(100, (11, 13), inputMap))
assertEqual((9, 6), getAstroidCoordinateForNthAstroidToVepourise(199, (11, 13), inputMap))
assertEqual((8, 2), getAstroidCoordinateForNthAstroidToVepourise(200, (11, 13), inputMap))
assertEqual((10, 9), getAstroidCoordinateForNthAstroidToVepourise(201, (11, 13), inputMap))

print(getAstroidCoordinateForNthAstroidToVepourise(200, (31, 20), [
    "##.###.#.......#.#....#....#..........#.",
    "....#..#..#.....#.##.............#......",
    "...#.#..###..#..#.....#........#......#.",
    "#......#.....#.##.#.##.##...#...#......#",
    ".............#....#.....#.#......#.#....",
    "..##.....#..#..#.#.#....##.......#.....#",
    ".#........#...#...#.#.....#.....#.#..#.#",
    "...#...........#....#..#.#..#...##.#.#..",
    "#.##.#.#...#..#...........#..........#..",
    "........#.#..#..##.#.##......##.........",
    "................#.##.#....##.......#....",
    "#............#.........###...#...#.....#",
    "#....#..#....##.#....#...#.....#......#.",
    ".........#...#.#....#.#.....#...#...#...",
    ".............###.....#.#...##...........",
    "...#...#.......#....#.#...#....#...#....",
    ".....#..#...#.#.........##....#...#.....",
    "....##.........#......#...#...#....#..#.",
    "#...#..#..#.#...##.#..#.............#.##",
    ".....#...##..#....#.#.##..##.....#....#.",
    "..#....#..#........#.#.......#.##..###..",
    "...#....#..#.#.#........##..#..#..##....",
    ".......#.##.....#.#.....#...#...........",
    "........#.......#.#...........#..###..##",
    "...#.....#..#.#.......##.###.###...#....",
    "...............#..#....#.#....#....#.#..",
    "#......#...#.....#.#........##.##.#.....",
    "###.......#............#....#..#.#......",
    "..###.#.#....##..#.......#.............#",
    "##.#.#...#.#..........##.#..#...##......",
    "..#......#..........#.#..#....##........",
    "......##.##.#....#....#..........#...#..",
    "#.#..#..#.#...........#..#.......#..#.#.",
    "#.....#.#.........#............#.#..##.#",
    ".....##....#.##....#.....#..##....#..#..",
    ".#.......#......#.......#....#....#..#..",
    "...#........#.#.##..#.#..#..#........#..",
    "#........#.#......#..###....##..#......#",
    "...#....#...#.....#.....#.##.#..#...#...",
    "#.#.....##....#...........#.....#...#...",
]))
