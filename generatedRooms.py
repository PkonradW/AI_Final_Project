import matplotlib.pyplot as plt
from matplotlib import colors
import robot
import copy
import imageio

ENV_WIDTH = 50
ENV_HEIGHT = 50
NUM_ROBOTS = 7
NUM_CONFIGS = 100
BASE_STATION = (9, 16)
TIMESTEPS = 3000


def main():
    # initialize environment to all unknown
    env = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5,
         0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0],
        [0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # add obstacles from mess
    obstacleList = []
    for x in range(0, ENV_WIDTH):
        for y in range(0, ENV_HEIGHT):
            if env[x][y] == 0:
                obstacleList.append((x, y))

    # add robots, spread out a bit
    robotsList = []
    for n in range(0, NUM_ROBOTS):
        robotsList.append(robot.Robot(1, n + 1, ENV_WIDTH, ENV_HEIGHT))

    # make frontierlist
    frontierlist = []
    templistlol = []
    templistlol.append((0, 0))
    for r in robotsList:
        r.setFrontierNodes(frontierlist, obstacleList, templistlol, ENV_WIDTH, ENV_HEIGHT)

    # make visitedlist
    visitedlist = []
    visitedlist.append((0, 0))
    for r in robotsList:
        r.setVisitedNodes(visitedlist, frontierlist)
    for r in robotsList:
        r.setFrontierNodes(frontierlist, obstacleList, visitedlist, ENV_WIDTH, ENV_HEIGHT)


    population = []  # consists of moves for each robot
    previousutil = 0
    for r in robotsList:
        previousutil += r.utility(obstacleList, robotsList, frontierlist, BASE_STATION)

    for n in range(0, TIMESTEPS):
        # generate a population
        population = []
        for k in range(0, NUM_CONFIGS):
            # deep copy the list
            config = copy.deepcopy(robotsList)
            for r in config:
                r.randomMove()
            # add config to population
            population.append(config)
        bestConfig = population[0]
        bestUtil = 0
        for r in population[0]:  # init the best util value
            bestUtil += r.utility(obstacleList, population[0], frontierlist, BASE_STATION)
        for c in population:  # list of [list of [robots] ]
            utilval = 0
            for r in c:
                utilval += r.utility(obstacleList, c, frontierlist, BASE_STATION)
            if utilval >= bestUtil:
                bestUtil = utilval
                bestConfig = c
        # move robots to new positions, update all the things
        # safety first, hard rejects impossible actions that visit a nodes off the frontier
        safetylist = copy.deepcopy(robotsList)
        safetyFrontList = copy.deepcopy(frontierlist)
        safetyVisitedList = copy.deepcopy(visitedlist)
        robotsList = bestConfig
        for r in robotsList:
            if r.setVisitedNodes(visitedlist, frontierlist) == -1:
                robotsList = safetylist
                frontierlist = safetyFrontList
                visitedlist = safetyVisitedList
            else:
                r.setFrontierNodes(frontierlist, obstacleList, visitedlist, ENV_WIDTH, ENV_HEIGHT)
        # send frame to gif machine
        make_frame(env, visitedlist, frontierlist, obstacleList, robotsList, n)
        if len(frontierlist) == 0:
            print("we finished the thingy")
            break
        # end of mainloop
    finalutil = 0
    for r in robotsList:
        finalutil += r.utility(obstacleList, robotsList, frontierlist, BASE_STATION)
        print(r.distToFront(frontierlist))
    print("sizeof visitedlist: ", len(visitedlist))
    print("finalutil: ", finalutil)
    make_frame(env, visitedlist, frontierlist, obstacleList, robotsList, n, last=True)
    frames = []
    for t in range(0, n):
        image = imageio.v2.imread(f'./mazepics/img_{t}.png')
        frames.append(image)
    imageio.mimsave(f'./{NUM_ROBOTS}robot_{ENV_WIDTH}x{ENV_HEIGHT}_{TIMESTEPS}steps_range{robot.RANGE}_maze.gif',
                    frames,
                    # duration= (60000/TIMESTEPS),
                    loop=False)




# following this tutorial https://towardsdatascience.com/how-to-create-a-gif-from-matplotlib-plots-in-python-6bec6c0c952c
def make_frame(env, visitedlist, frontierlist, obstacleList, robotsList, time, last=False):
    for x in range(0, ENV_WIDTH):
        for y in range(0, ENV_HEIGHT):
            env[x][y] = 5
    for x, y in visitedlist:
        env[x][y] = 1
    for x, y in frontierlist:
        env[x][y] = 4
    for x, y in obstacleList:
        env[x][y] = 0
    for r in robotsList:
        # print(r.x, r.y, len(frontierlist))
        if r.x >= ENV_WIDTH or r.y >= ENV_HEIGHT or r.x < 0 or r.y < 0:
            print("fell off the table, find me at ", r.x, r.y)
        else:
            env[r.x][r.y] = 2
    env[BASE_STATION[0]][BASE_STATION[1]] = 3

    fig = plt.figure(figsize=(6, 6))
    #  unknown: 0 = gray = 5
    #  visited: 1 = green = 1
    # obstacle: 2 = black = 0
    # frontier: 3 = yellow = 4
    #    robot: 4 = blue = 2
    #     base: 5 = red = 3
    colormap = colors.ListedColormap(["black", "green", "blue", "red", "yellow", "gray"])
    plt.imshow(env, cmap=colormap)
    plt.grid(True, linewidth=.5)
    plt.xlim(0, ENV_WIDTH)
    plt.ylim(0, ENV_HEIGHT)
    plt.title('Multi-robot exploration')
    plt.savefig(f'./mazepics/img_{time}.png',
                transparent=False,
                facecolor='white')

    if last:
        if len(frontierlist) == 0:
            colormap = colors.ListedColormap(["black", "green", "blue", "red"])
            plt.imshow(env, cmap=colormap)
            plt.grid(True, linewidth=.5)
            plt.xlim(0, ENV_WIDTH)
            plt.ylim(0, ENV_HEIGHT)
            plt.title('Multi-robot exploration')
        plt.savefig(f'./lastframe_{NUM_ROBOTS}bot_{ENV_WIDTH}x{ENV_HEIGHT}_{TIMESTEPS}steps_range{robot.RANGE}.png',
                    transparent=False,
                    facecolor='white'
                    )
    plt.clf()
    plt.close(fig)
    del fig


if __name__ == '__main__':
    main()
