# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
from pygame.locals import *
import numpy as np
import sys
import textwrap

from mst_classes import *
from kruskals import *
# Simple pygame program

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from random import randrange, choice
pygame.init()

# Define constants for the screen width and height
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



def text_objects(text, font):
    black = (0,0,0)
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
def checkMessage(screen, mes_count, message = None, clusters = False, numClusters = 0):
    next_graph = False
    text = 'You have found a minimum spanning tree!  You may now move on.'
    centerX = SCREEN_WIDTH/ 2
    centerY = SCREEN_HEIGHT / 2
    large_font = pygame.font.SysFont('chalkduster.ttf', 40)
    boxWidth = 200
    boxHeight = 100
    check_rect = Rect((centerX-boxWidth, centerY-boxHeight), (2*boxWidth, 2*boxHeight))
    check_rect_border1 = check_rect.inflate(20,20)
    check_rect_border2 = check_rect_border1.inflate(5,5)
    offsetX = 7
    offsetY = 10
    yes_rect = Rect((centerX-boxWidth+offsetX, centerY), (180,100))
    no_rect = Rect((centerX +boxWidth -  offsetX-180, centerY), (180, 100))
    yes_text = large_font.render('Continue', True, NODECOLOR)
    yes_width = yes_text.get_rect().width
    yes_height = yes_text.get_rect().height
    no_text = large_font.render('Back', True, NODECOLOR)
    no_width = no_text.get_rect().width
    no_height = no_text.get_rect().height
    if message != None:
        wrong_text = message
    elif mes_count ==3:
        wrong_text = "Oops!  You can find a tree with a smaller cost."
    elif mes_count ==2:
        wrong_text = "Oops!  Your tree does not span all the nodes."
    ok_rect = Rect((centerX-90, centerY-20), (180,100))
    ok_text = large_font.render('Try Again!', True, (255,255,255))
    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    img3 = font_biggest.render(str(numClusters), True, NODECOLOR)

    check = True
    while check:
        if clusters:
            screen.blit(img2, (5, 150))
            screen.blit(img3, (175, 200))
        x,y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (255,255,255), check_rect)
        pygame.draw.rect(screen, (255,255,255), check_rect_border1)
        pygame.draw.rect(screen, (0, 0, 0), check_rect_border2,5)
        if mes_count ==1:
            pygame.draw.rect(screen, (0, 230, 0), yes_rect)
            pygame.draw.rect(screen, (230, 0, 0), no_rect)
            if yes_rect.left< x< yes_rect.right:
                if yes_rect.top< y< yes_rect.bottom:
                    pygame.draw.rect(screen, (0, 255, 0), yes_rect)

            if no_rect.left< x< no_rect.right:
                if no_rect.top< y< no_rect.bottom:
                    pygame.draw.rect(screen, (255, 0, 0), no_rect)

            drawText(screen, text, (0,0,0), check_rect, large_font)
            screen.blit(yes_text, (yes_rect.center[0] - yes_width/2, yes_rect.center[1]- yes_height/2))
            screen.blit(no_text, (no_rect.center[0] - no_width / 2, no_rect.center[1] - no_height / 2))
        else:
            drawText(screen, wrong_text, (0, 0, 0), check_rect, large_font)
            pygame.draw.rect(screen, (0, 0, 0), ok_rect)
            if ok_rect.left < x < ok_rect.right:
                if ok_rect.top < y < ok_rect.bottom:
                    pygame.draw.rect(screen, (40, 40, 40), ok_rect)
            screen.blit(ok_text, (ok_rect.center[0] - ok_text.get_rect().width / 2,
                                  ok_rect.center[1] - ok_text.get_rect().height/ 2))
        #screen.blit(TextSurf, TextRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if mes_count ==1:
                    if yes_rect.left < x < yes_rect.right:
                        if yes_rect.top < y < yes_rect.bottom:
                            check = False
                            next_graph = True
                    elif no_rect.left < x < no_rect.right:
                        if no_rect.top < y < no_rect.bottom:
                            check = False
                else:
                    if ok_rect.left < x < ok_rect.right:
                        if ok_rect.top < y < ok_rect.bottom:
                            check = False


        pygame.display.update()
    return next_graph

def create_graph(type):
    # create new graph and populate nodes:
    pygame.font.init()
    graph = Graph()
    # locallist for adding neighbors:
    nodes = []
    radius = 250
    centerX = SCREEN_WIDTH *2 //3 -20
    centerY = SCREEN_HEIGHT//2
    if type ==1 or type ==2:
        t = 2 * np.pi /5
        offset = np.pi / 25
    if type ==3:
        t = 2 * np.pi / 4.7
        offset = 0

    node1 = Node(1)
    x = centerX+ radius * np.cos(offset)
    y = centerY + radius * np.sin(offset)
    graph.placeNode(node1, x,y)
    node2= Node(2)
    x = centerX+ radius * np.cos(t + offset)
    y = centerY+ radius * np.sin(t+ offset)
    graph.placeNode(node2, x, y)
    node3 = Node(3)
    x = centerX + radius * np.cos(2*t+ offset)
    y = centerY+ radius * np.sin(2*t+ offset)
    graph.placeNode(node3, x, y)
    node4 = Node(4)
    x = centerX + radius * np.cos(3*t+ offset)
    y = centerY+ radius * np.sin(3*t)+ offset
    graph.placeNode(node4, x, y)
    node5 = Node(5)
    x = centerX+ radius * np.cos(4*t+ offset)
    y = centerY + radius * np.sin(4*t+ offset)
    graph.placeNode(node5, x, y)

    if type ==1:
        edge1 = Edge(node1, node2,1)
        edge2 = Edge(node1, node3,5)
        edge3 = Edge(node1, node4,3)
        edge4 = Edge(node2, node3,10)
        edge5 = Edge(node2, node5,8)
        edge6 = Edge(node4, node5,2)
        edge7 = Edge(node2, node4,6)
        edge8 = Edge(node3, node4,4)
        path_total = 10
    if type ==2:
        edge1 = Edge(node1, node2, 2)
        edge2 = Edge(node1, node3, 7)
        edge3 = Edge(node1, node4, 5)
        edge4 = Edge(node2, node3, 4)
        edge5 = Edge(node2, node5, 1)
        edge6 = Edge(node4, node5, 4)
        edge7 = Edge(node3, node4, 6)
        edge8 = Edge(node1, node5, 3)
        path_total = 11
    if type ==3:
        node6 = Node(6)
        x = centerX
        y = centerY
        graph.placeNode(node6, x, y)
        edge1 = Edge(node1, node2, 8)
        edge2 = Edge(node1, node6, 10)
        edge3 = Edge(node1, node3, 4)
        edge4 = Edge(node2, node3, 2)
        edge5 = Edge(node1, node4, 1)
        edge6 = Edge(node4, node5, 7)
        edge7 = Edge(node3, node4, 6)
        edge8 = Edge(node6, node5, 5)
        edge9 = Edge(node3, node6, 6)
        edge10 = Edge(node4, node6, 3)
        graph.placeEdge(edge9)
        graph.placeEdge(edge10)
        path_total= 15
    graph.placeEdge(edge1)
    graph.placeEdge(edge2)
    graph.placeEdge(edge3)
    graph.placeEdge(edge4)
    graph.placeEdge(edge5)
    graph.placeEdge(edge6)
    graph.placeEdge(edge7)
    graph.placeEdge(edge8)

    return graph, path_total

def runGraph(num):
    graph, minTreeCost = create_graph(num)
    selected = None
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    img = font_big.render('Instructions: Click on edges to make a minimum spanning tree!', True, NODECOLOR)
    img1 = font_big.render('When you are done, click the "Check" button.', True, NODECOLOR)
    top_left = (730, 630)
    check_height = 60
    check_width = 250
    running = True
    if num ==1 or num ==2:
        numnodes = 5
    if num ==3:
        numnodes = 6
    w=250
    h = 60
    f_button = False
    while running:
        total = graph.update((255,0,0))
        pygame.event.pump()
        mouse = pygame.mouse.get_pos()
        screen.blit(img, (10, 20))
        screen.blit(img1,(10,60))

        edges = graph.edges
        numedges = 0
        if f_button:
            check_button_display((730, 630), w,h, 'Kruskals', (50, 205, 50), (50, 220, 100))
            check_button_display((20, 630), w, h, 'Main', (255, 182, 193), (255, 192, 203))

        else:
            check_button_display((730, 630), w, h, 'Check', (50, 205, 50), (50, 220, 100))


        for edge in edges:
            if edge.clicked:
                numedges+=1
            points = edge.getPoints()
            for i in range(points[0].size):
                if points[0][i] - 20 < mouse[0] < points[0][i] + 20:
                    if points[1][i] - 20 < mouse[1] < points[1][i] + 20:
                        edge.setColor((255, 0, 0))
                    else:
                        edge.setColor((0, 0, 0))
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if f_button:
                    if top_left[1] < y < top_left[1] + check_height:
                        if top_left[0] < x < top_left[0] + check_width:
                            graph, minTreeCost = create_graph(3)
                            introduction(graph)
                        if 20 < x < 20 + w:
                                menu()
                else:
                    if top_left[1] < y < top_left[1] + check_height:
                        if top_left[0] < x < top_left[0] + check_width:
                            if total ==minTreeCost and numedges ==numnodes-1:
                                next_graph = checkMessage(screen, 1)
                                if next_graph and num !=3:
                                    running = False
                                if next_graph and num ==3:
                                    f_button = True

                            elif total <minTreeCost or numedges <numnodes-1:
                                checkMessage(screen, 2)
                            else:
                                checkMessage(screen,3)

                for edge in edges:
                    points = edge.getPoints()
                    for i in range(points[0].size):
                        if points[0][i] - 20 < x < points[0][i] + 20:
                            if points[1][i] - 20 < y < points[1][i] + 20:
                                edge.setColor((255, 0, 0))
                                edge.toggleClicked()
                                break
                    if edge.clicked:
                        edge.setColor((255, 0, 0))


        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)

def menu():
    graph, minTreeCost = create_graph(3)
    SCREEN.fill(BGCOLOR)
    running = True
    font_big = pygame.font.SysFont('chalkduster.ttf', 80)
    font = pygame.font.SysFont('chalkduster.ttf', 60)
    img = font_big.render('Finding A Minimum Spanning Tree', True, NODECOLOR)
    boxWidth = 250
    boxHeight = 50
    centerX = SCREEN_WIDTH/2
    centerY = SCREEN_HEIGHT /2
    vert_space = 120

    intro_button = Rect((centerX - boxWidth, centerY - boxHeight-vert_space), (2 * boxWidth, 2 * boxHeight))
    intro_text = font.render('Introduction', True, (0,0,0))
    intro_width = intro_text.get_rect().width
    intro_height = intro_text.get_rect().height
    title_width = img.get_rect().width
    examples_button = Rect((centerX - boxWidth, centerY - boxHeight), (2 * boxWidth, 2 * boxHeight))
    examples_text = font.render('Examples', True, (0, 0, 0))
    examples_width = examples_text.get_rect().width
    examples_height = examples_text.get_rect().height
    kruskals_button = Rect((centerX - boxWidth, centerY - boxHeight+ vert_space), (2 * boxWidth, 2 * boxHeight))
    kruskals_text  = font.render('Kruskals Algorithm', True, (0, 0, 0))
    kruskals_width = kruskals_text.get_rect().width
    kruskals_height = kruskals_text.get_rect().height
    prims_button = Rect((centerX - boxWidth, centerY - boxHeight+ 2*vert_space), (2 * boxWidth, 2 * boxHeight))
    prims_text = font.render('Prims Algorithm', True, (0, 0, 0))
    prims_width = prims_text.get_rect().width
    prims_height = prims_text.get_rect().height
    while running:
        x,y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (0,150,150), intro_button)
        pygame.draw.rect(screen, (147,112,219),examples_button)
        pygame.draw.rect(screen, (107,142,35), kruskals_button)
        pygame.draw.rect(screen, (240,128,128), prims_button)

        if centerX-boxWidth/2 < x < centerX + boxWidth/2:
            if intro_button.top < y < intro_button.bottom:
                pygame.draw.rect(screen, (0, 180, 180), intro_button)
            if examples_button.top < y < examples_button.bottom:
                pygame.draw.rect(screen, (160,130,240), examples_button)
            if kruskals_button.top < y < kruskals_button.bottom:
                pygame.draw.rect(screen, (120, 160, 50), kruskals_button)
            if prims_button.top < y < prims_button.bottom:
                pygame.draw.rect(screen, (240, 150, 150), prims_button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if intro_button.top < y < intro_button.bottom:
                    continue
                if examples_button.top < y < examples_button.bottom:
                    runGraph(1)
                    runGraph(2)
                    runGraph(3)
                if kruskals_button.top < y < kruskals_button.bottom:
                    introduction(graph)
                if prims_button.top < y < prims_button.bottom:
                    pygame.draw.rect(screen, (240, 150, 150), prims_button)

        screen.blit(img, (centerX-title_width/2, centerY-boxHeight-2*vert_space))
        screen.blit(intro_text,(centerX-intro_width/2, centerY-vert_space-intro_height/2))
        screen.blit(examples_text, (centerX - examples_width / 2, centerY - examples_height / 2))
        screen.blit(kruskals_text, (centerX - kruskals_width / 2, centerY +vert_space - kruskals_height / 2))
        screen.blit(prims_text, (centerX - prims_width / 2, centerY + 2* vert_space - prims_height / 2))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)


def init():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode(SIZE)


def quit():
    pygame.quit()


def main():
    graph, minTreeCost = create_graph(3)
    running = True
    try:
        init()
        while running:
            menu()
            runGraph(1)
            runGraph(2)
            runGraph(3)
            introduction(graph)
            pygame.event.pump()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                    running = False
            pygame.display.update()
            pygame.display.flip()
            pygame.time.delay(FR)
    finally:
        quit()


# Set up the drawing window
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
