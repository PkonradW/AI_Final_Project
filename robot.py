import random

RANGE = 50
BASE_RANGE = RANGE # can be set different for testing or display purposes



class Robot:

    def __init__(self, x, y, wide, tall):
        self.x = x
        self.y = y
        self.wide = wide
        self.tall = tall

    def setFrontierNodes(self, frontier_list, obstaclelist, visitedlist, wide, tall):
        for dx in range(-1, 2):  # because the second argument is exclusive  -_-
            for dy in range(-1, 2):  # which makes the code look dumb
                newx = self.x + dx
                newy = self.y + dy
                if (newx >= 0) and (newy >= 0) and (newx < wide) and (newy < tall):
                    if (newx, newy) not in obstaclelist and (self.x, self.y) not in obstaclelist:
                        if (newx, newy) not in frontier_list and (newx, newy) not in visitedlist:
                            frontier_list.append((newx, newy))

    def setVisitedNodes(self, visitedlist, frontierlist):
        x = self.x
        y = self.y
        if (x, y) not in visitedlist:
            if (x < self.wide) and (y < self.tall):
                if (x, y) in frontierlist:
                    visitedlist.append((x, y))
                    frontierlist.remove((x, y))
                else:
                    return -1

    def distToFront(self, frontierlist):
        shortest = self.tall + self.wide
        if len(frontierlist) == 0:
            return -100
        for (x, y) in frontierlist:
            distance = abs(self.x - x) + abs(self.y - y)
            if distance < shortest:
                shortest = distance
            # print("frontier coords", x, y)
            # print("robot coords:  ", self.x, self.y)
            # print("dist found:    ", distance)
            # print("shortest: ", shortest)
            # print()
        return shortest

    def utility(self, obstacleList, robotlist, frontierlist, base):
        # if loss of communication
        for r in robotlist:
            distance = abs(self.x - r.x) + abs(self.y - r.y)
            if distance >= RANGE:
                return -(self.tall + self.wide + 1)
            # if robots on top of each other
            if r != self and self.x == r.x and self.y == r.y:
                return -(self.tall + self.wide + 1)
            baseDist = abs(r.x - base[0]) + abs(r.y - base[1])
            if baseDist >= BASE_RANGE:
                return -(self.tall + self.wide + 1)
        # if impossible position
        for x, y in obstacleList:
            if (self.x == x) and (self.y == y):
                # print("THEY'RE IN THE WALLS: ", x, y)
                # print("distance to frontier: ", self.distToFront(frontierlist))
                return -(self.tall + self.wide + 1)
        # because I don't have walls, the edge of the planet needs a weight
        if (self.x < 0) or (self.y < 0) or (self.x >= self.wide) or (self.y >= self.tall):
            # print("fell off the table")
            return -(self.tall + self.wide + 1)
        if (self.x, self.y) in frontierlist:
            return 20
        return -(self.distToFront(frontierlist))

    def randomMove(self):
        self.x = self.x + random.randint(-1, 1)
        self.y = self.y + random.randint(-1, 1)
