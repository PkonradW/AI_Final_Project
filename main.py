# import pygame
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas
import numpy
import random

import robot
from robot import Robot
import copy
import imageio

ENV_WIDTH = 50
ENV_HEIGHT = 50
NUM_ROBOTS = 4
NUM_CONFIGS = 150


def main():
    # initialize environment to all unknown
    env = [[0 for x in range(0, ENV_WIDTH)] for y in range(0, ENV_HEIGHT)]
    # add obstacles, box for now
    obstacleList = []
    for i in range(0, 3):
        for j in range(0, 3):
            xPos = int(ENV_WIDTH / 2 - 2 + i)
            yPos = int(ENV_HEIGHT / 2 - 2 + j)
            obstacleList.append((xPos, yPos))

    # add robots, spread out a bit
    robotsList = []
    for n in range(0, NUM_ROBOTS):
        robotsList.append(robot.Robot(1, n, ENV_WIDTH, ENV_HEIGHT))

    # make frontierlist
    frontierlist = []
    templistlol = []
    templistlol.append((0,0))
    for r in robotsList:
        r.setFrontierNodes(frontierlist, obstacleList, templistlol, ENV_WIDTH, ENV_HEIGHT)

    # make visitedlist
    visitedlist = []
    visitedlist.append((0,0))
    for r in robotsList:
        r.setVisitedNodes(visitedlist, frontierlist)

    #display(env, visitedlist, frontierlist, obstacleList, robotsList)


    # main loop, figure out how/when to terminate later
    population = []     # consists of moves for each robot
    previousutil = 0
    for r in robotsList:
        previousutil += r.utility(obstacleList,robotsList,frontierlist)

    for n in range (0, 15000):
        #generate a population
        population = []
        for k in range (0, NUM_CONFIGS):
            # deep copy the list
            config = copy.deepcopy(robotsList)
            for r in config:
                r.randomMove()
            # add config to population
            population.append(config)
        bestConfig = population[0]
        bestUtil = 0
        for r in population[0]:
            bestUtil += r.utility(obstacleList,population[0],frontierlist)

        for c in population: # list of [list of [robots] ]
            utilval = 0
            for r in c:
                utilval += r.utility(obstacleList, c, frontierlist)
            if utilval >= bestUtil:
                bestUtil = utilval
                bestConfig = c
        #print("best is: ", bestUtil)

        # move robots to new positions, update all the things
        safetylist = copy.deepcopy(robotsList)
        robotsList = bestConfig
        for r in robotsList:
            r.setFrontierNodes(frontierlist, obstacleList, visitedlist, ENV_WIDTH, ENV_HEIGHT)
            if (r.setVisitedNodes(visitedlist, frontierlist) == -1):
                robotsList = safetylist

        if len(frontierlist) == 0:
            break
    finalutil = 0
    for r in robotsList:
        finalutil += r.utility(obstacleList,robotsList,frontierlist)
        print(r.distToFront(frontierlist))
    print("sizeof visitedlist: ", len(visitedlist))
    print("finalutil: ", finalutil)
    display(env, visitedlist, frontierlist, obstacleList, robotsList)




    # first set visited
def display(env, visitedlist, frontierlist, obstacleList, robotsList):
    for x in range(0, ENV_WIDTH):
        for y in range(0, ENV_HEIGHT):
            if (x, y) in visitedlist:
                env[x][y] = 1
            else:
                env[x][y] = 0
    for x, y in frontierlist:
        env[x][y] = 3
    for x, y in obstacleList:
        env[x][y] = 2
    for r in robotsList:
        print(r.x, r.y, len(frontierlist))
        env[r.x][r.y] = 4
    #  unknown: 0 = gray
    #  visited: 1 = green
    # obstacle: 2 = black
    # frontier: 3 = yellow
    #    robot: 4 = blue
    colormap = colors.ListedColormap(["gray", "green", "black", "yellow", "blue"])
    plt.figure(figsize=(5, 5))
    plt.imshow(env, cmap=colormap)
    plt.show()
    plt.clf()
    plt.xticks([x for x in range(ENV_WIDTH)], [])
    plt.yticks([y for y in range(ENV_HEIGHT)], [])
    plt.grid(True, linewidth=0.5)
    plt.xlim(0, ENV_WIDTH)
    plt.ylim(0, ENV_HEIGHT)
    plt.title('Multi-robot exploration')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/

    # data = [[random.randint(a=0, b=1) for x in range(0, 8)],  # row 1
    #         [random.randint(a=0, b=1) for x in range(0, 8)],  # row 2
    #         [random.randint(a=0, b=1) for x in range(0, 8)],  # row 3
    #         [random.randint(a=0, b=1) for x in range(0, 8)],  # row 4
    #         [random.randint(a=0, b=1) for x in range(0, 8)],  # row 5
    #         [random.randint(a=0, b=1) for x in range(0, 8)],  # row 6
    #         [random.randint(a=0, b=1) for x in range(0, 8)],  # row 7
    #         [random.randint(a=0, b=1) for x in range(0, 8)]]  # row 8
    # env = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
