import math, random, pygame, sys
import tkinter as tk
from tkinter import messagebox

pygame.init()

# GLOBALS VARIABLES
width = 500
height = 600
play_width = 500 
play_height = 500


top_left_x = (width - play_width) // 2
top_left_y = width - play_height

class Cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(0,179,89)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self,dirnx,dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self,surface,eyes=False):
        distance = self.w // self.rows # distance between grid lines
        r = self.pos[0] # current row
        c = self.pos[1] # current column
        
        pygame.draw.rect(surface, self.color, (r*distance+1, c*distance+1, distance-2, distance-2)) # draw a cube that is, on each side, just one pixel width smaller than the grid, so we can still see the grid

        # Eyes drawing - small black dots only on the head
        if eyes:
            center = distance//2 # center of our cube
            radius = 3
            middle = (r*distance + center - radius, c*distance + 8) # center of first eye
            middle2 = (r*distance + distance - radius*2, c*distance + 8) # center of first eye

            pygame.draw.circle(surface, (0,0,0), middle, radius)
            pygame.draw.circle(surface, (0,0,0), middle2, radius)



class Snake(object):
    body = []
    turns = {}
    def __init__(self,color,pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    '''
    Snake body movement
    TO DO: Block right movement when already moving left etc
    '''
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            for key in keys:
                # turning left
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                # turning right
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                # turning up
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                # turning down
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
        # remember the path head travelled
        for i, cube in enumerate(self.body):
            position = cube.pos[:] #for each object grab their position
            if position in self.turns:
                turn = self.turns[position]
                cube.move(turn[0],turn[1])
                if i == len(self.body)-1: #if we are at the last cube we do not need to remember
                    self.turns.pop(position)
            
            else: # ifs handle screen egdes, else handles normal movement
                if cube.dirnx == -1 and cube.pos[0] <= 0: cube.pos = (cube.rows-1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows-1: cube.pos = (0,cube.pos[1])
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows-1: cube.pos = (cube.pos[0], 0)
                elif cube.dirny == -1 and cube.pos[1] <= 0: cube.pos = (cube.pos[0], cube.rows-1)
                else: cube.move(cube.dirnx, cube.dirny)
    """ 
    Reset the snake's body for a new game 
    """
    def reset(self,pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    """ 
    After eating a snack, prolongate the snake's body. 
    Adding a new cube depends on which direction the snake is moving. 
    """
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        # if snake is moving right
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        # if snake is moving left
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
        # if snake is moving down
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
        # if snake is moving up
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self,surface):
        for i, cube in enumerate(self.body):
            if i == 0:
              cube.draw(surface, True)
            else:
                cube.draw(surface)

def drawGrid(w,rows,surface):
    sizeBetween = w // rows
    x = 0
    y = 0
    for line in range(rows):
        x += sizeBetween
        y += sizeBetween

        pygame.draw.line(surface, (200,200,200),(x,0),(x,w))
        pygame.draw.line(surface, (200,200,200),(0,y),(w,y))

'''def startWindow(surface):
    surface.fill((0,0,0))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Space for new game, Q to quit.', True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (width // 2, width // 2)
    surface.blit(text, textRect)
    pygame.display.update()
'''
def redrawWindow(surface, score = 0, high_score = 0):
    global rows, width, s
    surface.fill((169,169,169))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)

    font = pygame.font.SysFont('courier', 20, bold = False)
    label = font.render('Score: {}'.format(score), 1, (255,255,255))
    surface.blit(label,(top_left_x + 10, height - label.get_height() - 20))

    label = font.render('High Score: {}'.format(high_score), 1, (255,255,255))
    surface.blit(label,(width - label.get_width() - 10, height - label.get_height() - 20))
    pygame.display.update()

def randomSnack(rows,item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: # generate snack anywhere but on the snake's body
            continue # if a snack ended on the body, try again
        else:
            break # if we hit a location not on the body, we did good, so exit the loop
    return (x,y)

def message_box(subject, content):
    root = tk.Tk() # New Tk window
    root.attributes("-topmost", True) # Make sure window comes on top
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
'''
Draws text right in the middle of the window, on top of whatever is there
'''
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('courier', size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label,(top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))

def main_menu(win):
    run = True
    while run:
        pygame.event.clear()
        win.fill((0,0,0))
        draw_text_middle(win, "Press any key to play", 30, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()

def main(win):
    global rows, s, snack
    rows = 20 #the higher the harder the game
    s = Snake((0,39,0), (10,10)) # starting position of snake
    snack = Cube(randomSnack(rows, s), color=(204,0,0))
    clock = pygame.time.Clock()
    s.reset((10,10))
    score = 1
    run = True
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos: # if snake's head touches the snack
            s.addCube() # prolongate body
            score += 1
            snack = Cube(randomSnack(rows, s), color=(204,0,0)) # new random snack

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])): #looping through every cube in our body, checking if we are not hitting it with head
                score = len(s.body)
                draw_text_middle(win, 'Game over! Total score: {}'.format(score),30,(0,0,0))
                #message_box('Game over!', 'Total score: ' + str(score) + '. Play again.')
                pygame.display.update()
                pygame.time.delay(2000)
                run = False
                break
        redrawWindow(win, score)

    pass

#win = pygame.display.set_mode((width, width))
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
main_menu(win)