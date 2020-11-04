import pygame
from pygame.locals import *
import numpy as np
import sys
import textwrap
from mst_classes import *
from main import *
NODESIZE = 20
NUM_CLUSTERS = 0
def check_button_display(top_left, check_width, check_height, text, color, color2):

    mouse = pygame.mouse.get_pos()
    check_button = Rect(top_left, (check_width, check_height))
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 60)
    check_text = font_biggest.render(text, True, NODECOLOR)
    check_width = check_text.get_rect().width
    check_height = check_text.get_rect().height
    pygame.draw.rect(screen, color, check_button)
    screen.blit(check_text, (check_button.centerx-check_width/2, check_button.centery- check_height/2))
    if top_left[0] < mouse[0] < top_left[0] + check_width:
        if top_left[1] < mouse[1] < top_left[1] + check_height:
            pygame.draw.rect(screen, color2, check_button)
            screen.blit(check_text, (check_button.centerx-check_width/2, check_button.centery- check_height/2))


def introduction(graph):
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    top_left = (820, 630)
    check_height = 60
    check_width = 160
    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest =  pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    img = font_big.render('Separate each node into its own cluster by clicking the node.', True, NODECOLOR)
    img1 = font_big.render('Then click "Next".', True, NODECOLOR)
    running = True

    nodes = graph.nodes
    while running:
        total = graph.update((255,0,0))
        screen.blit(img2, (5, 150))
        screen.blit(img, (10, 20))
        screen.blit(img1, (10, 50))

        count = 0
        check_button_display((820, 630),160,60, 'Next', (50,205,50), (50,220,100))
        for node in nodes:
            if node.click:
                pygame.draw.circle(screen, (255, 0, 0), node.circ.center, NODESIZE + 20,5)
                count +=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for node in nodes:
                    distance = np.sqrt((x-node.circ.center[0])**2+(y - node.circ.center[1])**2)
                    if distance < NODESIZE:
                        node.toggleClicked()

                if top_left[0] < x < top_left[0] + check_width:
                    if top_left[1] < y < top_left[1] + check_height:
                        if count <6:
                            checkMessage(screen, 2, "Oops!  You haven't selected all the nodes into their own cluster.", True, count)
                        else:
                            first_node(graph)
        img3 = font_biggest.render(str(count), True, NODECOLOR)
        screen.blit(img3, (175, 200))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)

def first_node(graph):

    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    text = 'Next, we add edges to our set to combine clusters until we get one cluster. ' \
           ' Click the cheapest edge' \
           ' crossing the boundary of the green cluster and absorb it and the connected nodes into the same cluster.'
    running = True
    nodes = graph.nodes
    edges= graph.edges
    screen_rect = Rect((10, 10), (980, 100))
    for edge in edges:
        if edge.weight ==1:
            first = edge.start
    while running:
        count = 0
        edge_count = 0
        total = graph.update((0,0,255))
        mouse = pygame.mouse.get_pos()
        make_clusters(graph, 0)
        highlight_edge(graph,1,None)
        drawText(screen, text, (0, 0, 0), screen_rect, font_big)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                highlight_edge(graph,1,event)
        img3 = font_biggest.render(str(6), True, NODECOLOR)
        screen.blit(img2, (5, 150))
        screen.blit(img3, (175, 200))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)

def second_node(graph):
    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    text = 'Now those two nodes are part of the same cluster.  Repeat the process for the new green cluster.  Note that added edges are now colored blue.'
    running = True
    edges = graph.edges
    screen_rect = Rect((10, 10), (1000, 100))

    while running:
        edge_count = 0
        total = graph.update((0, 0, 255))
        mouse = pygame.mouse.get_pos()
        make_clusters(graph, 1)
        highlight_edge(graph,2,None)
        drawText(screen, text, (0, 0, 0), screen_rect, font_big)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                highlight_edge(graph,2, event)

        img3 = font_biggest.render(str(5), True, NODECOLOR)
        screen.blit(img2, (5, 150))
        screen.blit(img3, (175, 200))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)
def make_clusters(graph, order):
    for node in graph.nodes:
        if node.label == 1:
            node1 = node
        if node.label ==4:
            node2 = node
        if node.label ==3:
            node3 = node
        if node.label ==2:
            node4 = node
        if node.label ==6:
            node5 = node
        if node.label ==5:
            node6 = node
        if order ==0:
            pygame.draw.circle(screen, (255, 0, 0), node.circ.center, NODESIZE + 20, 5)
    if order ==0:
        pygame.draw.circle(screen, (0, 255, 0), node1.circ.center, NODESIZE + 20, 5)
    if order ==1:
        pygame.draw.circle(screen, (0, 255, 0), node3.circ.center, NODESIZE + 20, 5)
        pygame.draw.circle(screen, (255, 0, 0), node5.circ.center, NODESIZE + 20, 5)
        pygame.draw.circle(screen, (255, 0, 0), node6.circ.center, NODESIZE + 20, 5)
        pygame.draw.circle(screen, (255, 0, 0), node4.circ.center, NODESIZE + 20, 5)
    if order ==2:
        pygame.draw.circle(screen, (255, 0, 0), node5.circ.center, NODESIZE + 20, 5)
        pygame.draw.circle(screen, (0, 255, 0), node6.circ.center, NODESIZE + 20, 5)
    for i in range(order):
        color = (255, 0, 0)
        if order ==4 and i ==0:
            continue
        if order ==4 and i ==2:
            continue
        if i ==0:
            color = (255,0,0)
            first = node1
            second = node2
            angle1 = np.pi/2 -np.pi/32
            angle2 = 3*np.pi/2-np.pi/32
            top1 = (487,121)
            bottom1 = (902,313)
            top2 = (480,197)
            bottom2=(894,388)
        if i ==1:
            first = node3
            second = node4
            angle1 = 3*np.pi/2 -np.pi/32
            angle2 = np.pi/2 -np.pi/32
            top1 = (425, 425)
            bottom1 = (707, 556)
            top2 = (418, 500)
            bottom2=(699, 630)
        if i ==2:
            first = node5
            second = node6
            angle1 = 0-np.pi/4
            angle2 = np.pi -np.pi/4
            top1 = (820, 176)
            bottom1 = (673, 379)
            top2 = (767, 122)
            bottom2=(619, 324)
        if i ==3:
            first = node1
            second = node6
            third = node2
            fourth = node5
            angle1 = np.pi/2
            angle2 = np.pi + np.pi / 4
            top1 = (second.circ.center[0], second.circ.center[1]-39)
            bottom1 = (third.circ.center[0], third.circ.center[1]-40)
            top2 = (457, 186)
            bottom2 = (618, 378)
            top3 = (first.circ.center[0], first.circ.center[1]+38)
            bottom3 = (fourth.circ.center[0], fourth.circ.center[1]+38)
            top4 = (first.circ.center[0]+38, first.circ.center[1])
            bottom4 = (818, 115)
            square_rect = Rect((third.circ.center[0] - 40, third.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
            square_rect2 = Rect((fourth.circ.center[0] - 40, fourth.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
            square_rect3 = Rect((second.circ.center[0] - 40, second.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
            square_rect4 = Rect((first.circ.center[0] - 40, first.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
            pygame.draw.line(screen, color, top1, bottom1, 5)
            pygame.draw.line(screen, color, top2, bottom2, 5)
            pygame.draw.line(screen, color, top3, bottom3, 5)
            pygame.draw.line(screen, color, top4, bottom4, 5)
            pygame.draw.arc(screen, color, square_rect, angle1, angle1 + 3*np.pi/4, 5)
            pygame.draw.arc(screen, color, square_rect2, angle2, angle2 + np.pi/4, 5)
            pygame.draw.arc(screen, color, square_rect4, 3*np.pi/2, 0, 5)
            pygame.draw.arc(screen, color, square_rect3, np.pi/4, np.pi/2, 5)
            continue

        square_rect = Rect((second.circ.center[0] - 40, second.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
        square_rect2 = Rect((first.circ.center[0] - 40, first.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
        pygame.draw.line(screen, color, top1, bottom1, 5)
        pygame.draw.line(screen, color, top2, bottom2, 5)
        pygame.draw.arc(screen, color, square_rect, angle1, angle1+np.pi, 5)
        pygame.draw.arc(screen, color, square_rect2, angle2, angle2+np.pi, 5)


def highlight_edge(graph, order, event):
    edges = graph.edges
    mouse =pygame.mouse.get_pos()
    round5 = False
    for edge in edges:
        if edge.weight ==1:
            first1 = edge.start
            second = edge.end
            correct1 = edge
        if edge.weight ==2:
            first2 = edge.end
            correct2 = edge
        if edge.weight == 5:
            first3 = edge.end
            correct3= edge
        if edge.weight ==3:
            correct4 = edge
        if edge.weight ==4:
            correct5 = edge

    if order ==1:
        first = first1
        correct = correct1
        end_node = first
    if order ==2:
        first = first2
        correct = correct2
        end_node = first
    if order ==3:
        first = first3
        correct = correct3
        end_node = first
    if order ==4:
        first = first1
        end_node = second
        correct = correct4
    if order ==5:
        first = Node(100)
        end_node = first
        correct = correct5

    for edge in edges:
        round5 = False
        if order ==5 and (edge.weight ==6 or edge.weight == 4 or edge.weight ==8):
            round5= True
        if edge.start == first or edge.end == first or edge.start == end_node or edge.end == end_node or round5:
            points = edge.getPoints()
            for i in range(points[0].size):
                if points[0][i] - 20 < mouse[0] < points[0][i] + 20:
                    if points[1][i] - 20 < mouse[1] < points[1][i] + 20:
                        edge.setColor((0, 255, 0))
                        if event != None:
                            if edge == correct:
                                if points[0][i] - 20 < event.pos[0] < points[0][i] + 20:
                                    if points[1][i] - 20 < event.pos[1] < points[1][i] + 20:
                                        edge.toggleClicked()
                                        edge.setColor((0, 255, 0))
                                        if order ==1:
                                            second_node(graph)
                                        if order ==2:
                                            third_node(graph)
                                        if order ==3:
                                            fourth_node(graph)
                                        if order ==4:
                                            fifth_node(graph)
                                        if order == 5:
                                            finishing_graph(graph)
                                            graph.update((0,0,255))
                                            checkMessage(screen, 1)
                            else:
                                checkMessage(screen, 2, "You can find a cheaper edge!", True, 7-order)
                    else:
                        edge.setColor((0, 0, 0))


def third_node(graph):
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    text = 'Continue adding edges into the set until there is only one cluster, at which point we will have our MST!'
    running = True
    screen_rect = Rect((10, 10), (1000, 100))
    while running:
        total = graph.update((0, 0, 255))
        make_clusters(graph,2)
        highlight_edge(graph, 3, None)
        drawText(screen, text, (0, 0, 0), screen_rect, font_big)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x,y)
                highlight_edge(graph,3,event)
        img3 = font_biggest.render(str(4), True, NODECOLOR)
        screen.blit(img2, (5, 150))
        screen.blit(img3, (175, 200))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)

def fourth_node(graph):
    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    text = 'Continue adding edges into the set until there is only one cluster, at which point we will have our MST!'
    running = True
    screen_rect = Rect((10, 10), (1000, 100))
    for node in graph.nodes:
        if node.label ==1:
            node1 = node
        if node.label ==4:
            node2 = node
    while running:
        total = graph.update((0, 0, 255))
        make_clusters(graph, 3)
        first = node1
        second = node2
        angle1 = np.pi / 2 - np.pi / 32
        angle2 = 3 * np.pi / 2 - np.pi / 32
        top1 = (487, 121)
        bottom1 = (902, 313)
        top2 = (480, 197)
        bottom2 = (894, 388)
        color = (0,255,0)
        square_rect = Rect((second.circ.center[0] - 40, second.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
        square_rect2 = Rect((first.circ.center[0] - 40, first.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
        pygame.draw.line(screen, color, top1, bottom1, 5)
        pygame.draw.line(screen, color, top2, bottom2, 5)
        pygame.draw.arc(screen, color, square_rect, angle1, angle1 + np.pi, 5)
        pygame.draw.arc(screen, color, square_rect2, angle2, angle2 + np.pi, 5)
        highlight_edge(graph, 4, None)
        drawText(screen, text, (0, 0, 0), screen_rect, font_big)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x,y)
                highlight_edge(graph, 4, event)
        img3 = font_biggest.render(str(3), True, NODECOLOR)
        screen.blit(img2, (5, 150))
        screen.blit(img3, (175, 200))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)

def fifth_node(graph):
    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    text = 'Continue adding edges into the set until there is only one cluster, at which point we will have our MST!'
    running = True
    screen_rect = Rect((10, 10), (1000, 100))
    for node in graph.nodes:
        if node.label == 1:
            node1 = node
        if node.label ==4:
            node2 = node
        if node.label ==3:
            node3 = node
        if node.label ==2:
            node4 = node
        if node.label ==6:
            node5 = node
        if node.label ==5:
            node6 = node
    first = node1
    second = node6
    third = node2
    fourth = node5
    angle1 = np.pi / 2
    angle2 = np.pi + np.pi / 4
    top1 = (second.circ.center[0], second.circ.center[1] - 39)
    bottom1 = (third.circ.center[0], third.circ.center[1] - 40)
    top2 = (457, 186)
    bottom2 = (618, 378)
    top3 = (first.circ.center[0], first.circ.center[1] + 38)
    bottom3 = (fourth.circ.center[0], fourth.circ.center[1] + 38)
    top4 = (first.circ.center[0] + 38, first.circ.center[1])
    bottom4 = (818, 115)
    square_rect = Rect((third.circ.center[0] - 40, third.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
    square_rect2 = Rect((fourth.circ.center[0] - 40, fourth.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
    square_rect3 = Rect((second.circ.center[0] - 40, second.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
    square_rect4 = Rect((first.circ.center[0] - 40, first.circ.center[1] - 40), (4 * NODESIZE, 4 * NODESIZE))
    color = (0,255,0)
    while running:
        total = graph.update((0, 0, 255))
        make_clusters(graph, 4)
        pygame.draw.line(screen, color, top1, bottom1, 5)
        pygame.draw.line(screen, color, top2, bottom2, 5)
        pygame.draw.line(screen, color, top3, bottom3, 5)
        pygame.draw.line(screen, color, top4, bottom4, 5)
        pygame.draw.arc(screen, color, square_rect, angle1, angle1 + 3 * np.pi / 4, 5)
        pygame.draw.arc(screen, color, square_rect2, angle2, angle2 + np.pi / 4, 5)
        pygame.draw.arc(screen, color, square_rect4, 3 * np.pi / 2, 0, 5)
        pygame.draw.arc(screen, color, square_rect3, np.pi / 4, np.pi / 2, 5)
        highlight_edge(graph, 5, None)
        drawText(screen, text, (0, 0, 0), screen_rect, font_big)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                highlight_edge(graph, 5, event)
        img3 = font_biggest.render(str(2), True, NODECOLOR)
        screen.blit(img2, (5, 150))
        screen.blit(img3, (175, 200))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)

def finishing_graph(graph):
    font_bigger = pygame.font.SysFont('chalkduster.ttf', 65)
    font_biggest = pygame.font.SysFont('chalkduster.ttf', 70)
    img2 = font_bigger.render('Number of Clusters', True, NODECOLOR)
    font_big = pygame.font.SysFont('chalkduster.ttf', 40)
    text = 'Congrats!  You have found the minimum spanning tree.'
    running = True
    screen_rect = Rect((10, 10), (1000, 100))
    for node in graph.nodes:
        if node.label == 1:
            node1 = node
        if node.label ==4:
            node2 = node
        if node.label ==3:
            node3 = node
        if node.label ==2:
            node4 = node
        if node.label ==6:
            node5 = node
        if node.label ==5:
            node6 = node
    first = node1
    second = node6
    third = node2
    fourth = node5
    color = (255,0,0)
    while running:
        total = graph.update((0, 0, 255))
        w= 250
        h=60
        check_button_display((730, 630), w,h, 'Prims', (50, 205, 50), (50, 220, 100))
        check_button_display((SCREEN_WIDTH/2-w/2, 630), w,h,'Menu', (135,206,235), (173,216,230))
        check_button_display((20, 630),w,h, 'Start Over', (255,182,193), (255,192,203))
        centerX, centerY = node5.circ.center
        radius = 300
        offset = 0
        t = 2 * np.pi / 4.7

        for i in range(0,4):
            pygame.draw.line(screen, color, (centerX + radius*np.cos(i*t), centerY + radius*np.sin(i*t)),
                             (centerX + radius*np.cos((i+1)*t), centerY + radius*np.sin((i+1)*t)),5)
        pygame.draw.line(screen, color, (centerX + radius*np.cos(0), centerY + radius*np.sin(0)),(centerX + radius*np.cos((4)*t), centerY + radius*np.sin((4)*t)),5)

        drawText(screen, text, (0, 0, 0), screen_rect, font_big)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if 630<y<690:
                    if 20<x<250:
                        graph,cost = create_graph(3)
                        introduction(graph)
                    if 375<x< 625:
                        menu()
                    if 730<x<980:
                        continue

        img3 = font_biggest.render(str(1), True, NODECOLOR)
        screen.blit(img2, (5, 150))
        screen.blit(img3, (175, 200))
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(FR)



