import random
import pygame
import tkinter as tk
from tkinter import messagebox
from cube import Cube
from snake import Snake

# GLOBALS VARIABLES
width = 500
height = 600
play_width = 500
play_height = 500

top_left_x = (width - play_width) // 2
top_left_y = width - play_height


def draw_grid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for line in range(rows):
        x += size_between
        y += size_between

        pygame.draw.line(surface, (200, 200, 200), (x, 0), (x, w))
        pygame.draw.line(surface, (200, 200, 200), (0, y), (w, y))


'''def startWindow(surface):
    surface.fill((0,0,0))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Space for new game, Q to quit.', True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (width // 2, width // 2)
    surface.blit(text, textRect)
    pygame.display.update()
'''


def redraw_window(surface, score=0, high_score=0):
    global rows, width, s
    surface.fill((169, 169, 169))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)

    font = pygame.font.SysFont('courier', 20, bold=False)
    label = font.render('Score: {}'.format(score), True, (255, 255, 255))
    surface.blit(label, (top_left_x + 10, height - label.get_height() - 20))

    label = font.render('High Score: {}'.format(high_score), True, (255, 255, 255))
    surface.blit(label, (width - label.get_width() - 10, height - label.get_height() - 20))
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(
                filter(lambda z: z.pos == (x, y), positions))) > 0:  # generate snack anywhere but on the snake's body
            continue  # if a snack ended on the body, try again
        else:
            break  # if we hit a location not on the body, we did good, so exit the loop
    return x, y


def message_box(subject, content):
    root = tk.Tk()  # New Tk window
    root.attributes("-topmost", True)  # Make sure window comes on top
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


'''
Writes any new high score in a text file - scores.txt stores all 
high scores scored
'''


def update_scores(new_score):
    score = get_max_score()
    with open('scores.txt', 'a') as f:
        if int(new_score) > int(score):
            f.write('\n')
            f.write(str(new_score))


'''
Reads current high score from a text file
'''


def get_max_score():
    with open('scores.txt', 'r') as f:
        data = [int(x) for x in f.readlines()]
    return max(data)


'''
Draws text right in the middle of the window, on top of whatever is there
'''


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('courier', size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))


'''
Main menu - lets the player rest between the games. 
Player must hit any keyboard key in order to start playing.
Main menu shows as first game window and every time we loose the game. 
'''


def main_menu(win):
    run = True
    while run:
        pygame.event.clear()
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press any key to play", 30, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()


'''
Main window functionalities
'''


def main(win):
    global rows, s, snack
    rows = 20  # the higher, the harder the game
    s = Snake((0, 39, 0), (10, 10))  # starting position of snake
    snack = Cube(random_snack(rows, s), color=(204, 0, 0))
    clock = pygame.time.Clock()
    s.reset((10, 10))
    score = 1
    run = True
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:  # if snake's head touches the snack
            s.addCube()  # prolongate body
            score += 1
            snack = Cube(random_snack(rows, s), color=(204, 0, 0))  # new random snack

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[
                                                          x + 1:])):  # looping through every cube in our body, checking if we are not hitting it with head
                score = len(s.body)
                update_scores(score)
                draw_text_middle(win, 'Game over! Total score: {}'.format(score), 30, (0, 0, 0))
                # message_box('Game over!', 'Total score: ' + str(score) + '. Play again.')
                pygame.display.update()
                pygame.time.delay(2000)
                run = False
                break
        redraw_window(win, score, get_max_score())

    pass


def run_program():
    # win = pygame.display.set_mode((width, width))
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Game')
    main_menu(win)


if __name__ == '__main__':
    run_program()
