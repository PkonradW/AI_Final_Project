import matplotlib.pyplot as plt
from matplotlib import colors
import random
import robot
import copy
import imageio

ENV_WIDTH = 250
ENV_HEIGHT = 250
NUM_ROBOTS = 10
NUM_CONFIGS = 80
BASE_STATION = (int(robot.BASE_RANGE / 3), int(robot.BASE_RANGE / 3))
TIMESTEPS = 45000


def main():
    # initialize environment to all unknown
    env = [[5 for x in range(0, ENV_WIDTH)] for y in range(0, ENV_HEIGHT)]

    # add obstacles, box for now
    obstacleList = []
    for x in range(0, ENV_WIDTH):
        for y in range(0, ENV_HEIGHT):
            if x == 0 or y == 0 or y == ENV_HEIGHT - 1 or x == ENV_WIDTH - 1:
                obstacleList.append((x, y))
    for i in range(0, 3):  # make a box
        for j in range(0, 3):
            xPos = int((robot.BASE_RANGE / 3) + 1 - i)
            yPos = int((robot.BASE_RANGE / 3) + 1 - j)
            obstacleList.append((xPos, yPos))
    for k in range(0, random.randint(40, 90)):
        boxSize = random.randint(3, 15)
        boxXPos = random.randint(10, ENV_WIDTH - boxSize)  # starting position of the box along the x-axis
        boxYPos = random.randint(10, ENV_HEIGHT - boxSize)  # starting position of the box along the y-axis
        for i in range(0, boxSize):
            for j in range(0, boxSize):
                xPos = boxXPos + i
                yPos = boxYPos + j
                obstacleList.append((xPos, yPos))
                # can't make empty boxes

    # add robots, spread out a bit
    robotsList = []
    for n in range(0, NUM_ROBOTS):
        robotsList.append(robot.Robot(3, 2 + n, ENV_WIDTH, ENV_HEIGHT))

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

    # display(env, visitedlist, frontierlist, obstacleList, robotsList)

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
        for r in population[0]:
            bestUtil += r.utility(obstacleList, population[0], frontierlist, BASE_STATION)

        for c in population:  # list of [list of [robots] ]
            utilval = 0
            for r in c:
                utilval += r.utility(obstacleList, c, frontierlist, BASE_STATION)
            if utilval >= bestUtil:
                bestUtil = utilval
                bestConfig = c
        # print("best is: ", bestUtil)

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
    finalutil = 0
    for r in robotsList:
        finalutil += r.utility(obstacleList, robotsList, frontierlist, BASE_STATION)
        print(r.distToFront(frontierlist))
    print("sizeof visitedlist: ", len(visitedlist))
    print("finalutil: ", finalutil)
    make_frame(env, visitedlist, frontierlist, obstacleList, robotsList, n, last=True)
    frames = []

    # make the gif
    for t in range(0, n):
        image = imageio.v2.imread(f'./randomsquarepics/img_{t}.png')
        frames.append(image)
    imageio.mimsave(f'./{NUM_ROBOTS}bot_{ENV_WIDTH}x{ENV_HEIGHT}_range{robot.RANGE}_{TIMESTEPS}step_squares.gif',
                    frames,
                    loop=False)
    # duration=60000/n) # limit gif length to 1 minute
    # total time = timesteps * duration
    # doesn't work good for longer runs

    # first set visited


def display(env, visitedlist, frontierlist, obstacleList, robotsList):
    for x in range(0, ENV_WIDTH):
        for y in range(0, ENV_HEIGHT + 1):
            env[x][y] = 5
    for x, y in visitedlist:
        env[x][y] = 1
    for x, y in frontierlist:
        env[x][y] = 3
    for x, y in obstacleList:
        env[x][y] = 2
    for r in robotsList:
        print(r.x, r.y, len(frontierlist))
        env[r.x][r.y] = 4
    env[BASE_STATION[0]][BASE_STATION[1]] = 5
    #  unknown: 0 = gray = 5
    #  visited: 1 = green = 0
    # obstacle: 2 = black = 1
    # frontier: 3 = yellow = 2
    #    robot: 4 = blue = 3
    #     base: 5 = red = 4
    colormap = colors.ListedColormap(["gray", "green", "black", "yellow", "blue", "red"])
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
        if (r.x >= ENV_WIDTH or r.y >= ENV_HEIGHT or r.x < 0 or r.y < 0):
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
    plt.savefig(f'./randomsquarepics/img_{time}.png',
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
