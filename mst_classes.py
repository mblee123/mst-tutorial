import pygame
from pygame.locals import *
import numpy as np
import sys
import textwrap
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FR = 30
SIZE = 1000, 700
BGCOLOR = (216, 190, 216)
NODECOLOR = (0, 0, 0)
NODESIZE = 20
GRIDSPACING = 50
MAXTRIES = 1000
STARTINGNODES = 5
SCREEN = pygame.display.set_mode(SIZE)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()


class Edge:
    def __init__(self, start, end, weight, clicked=False, color=(0, 0, 0)):
        self.start = start
        self.end = end
        self.weight = weight
        self.clicked = clicked
        middle = ((start.circ.center[0] + end.circ.center[0]) // 2, (start.circ.center[1] + end.circ.center[1]) // 2)
        slope = (start.circ.center[1] - end.circ.center[1]) / (start.circ.center[0] - end.circ.center[0])

        if slope < 3 and slope > -3:
            self.label = (middle[0] - slope * 30, middle[1] - 30)
        else:
            self.label = (middle[0] - 30, middle[1])
        start.neighbors.add(end)
        end.neighbors.add(start)
        self.color = color

    def toggleClicked(self):
        if self.clicked == True:
            self.clicked = False
        else:
            self.clicked = True

    def getPoints(self):
        intervalx = np.linspace(self.start.circ.center[0], self.end.circ.center[0], 20)
        intervaly = np.linspace(self.start.circ.center[1], self.end.circ.center[1], 20)

        return (intervalx, intervaly)

    def setColor(self, color):
        self.color = color

    def display(self):
        pygame.draw.line(SCREEN, self.color,
                         self.start.circ.center, self.end.circ.center, 4)


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 0)
        self.thickness = 20
        self.center = (self.x, self.y)

    def display(self):
        pygame.draw.circle(SCREEN, self.colour, self.center, self.size, self.thickness)


class Graph(object):
    def __init__(self):
        self.nodes = set()
        # record positions of each node, so that we can check for overlaps
        self.positions = dict()
        self.edges = set()

    def placeEdge(self, edge):
        self.edges.add(edge)

    def placeNode(self, node, x, y):
        self.nodes.add(node)
        node.setpos((x, y), self)

    def update(self, color):
        SCREEN.fill(BGCOLOR)
        font = pygame.font.SysFont('chalkduster.ttf', 30)
        font_big = pygame.font.SysFont('chalkduster.ttf', 75)
        img = font_big.render('Path Total', True, NODECOLOR)
        screen.blit(img, (70, 300))
        total = 0
        for node in self.nodes:
            node.circ.display()
        for edge in self.edges:
            if edge.clicked:
                edge.setColor(color)
                total += edge.weight
            edge.display()
            img = font.render(str(edge.weight), True, edge.color)
            screen.blit(img, edge.label)
        img_total = font_big.render(str(total), True, NODECOLOR)
        screen.blit(img_total, (175, 350))
        return total


class Node(object):
    # Class variable, incremented with each
    # instance so that each node has a unique ID that
    # can be used as its hash:
    creation_counter = 0

    def __init__(self, label, click= False):
        self.id = self.__class__.creation_counter
        self.__class__.creation_counter += 1
        # We don't  set this attribute here, but by adding then here,
        # we indicate that it "exists" for readers of the code:
        self.circ = None
        self.color = NODECOLOR
        self.neighbors = set()
        self.click = click
        self.label = label

    def setpos(self, pos, graph=None):
        if self.circ and graph:
            # remove self from previous position in the graph:
            graph.positions.pop((self.circ.x, self.circ.y), None)

        self.circ = Particle(pos[0], pos[1], NODESIZE)
        if graph:
            graph.positions[pos] = self
    def toggleClicked (self):
        if self.click:
            self.click = False
        else:
            self.click = True

    def __hash__(self):
        return self.id
