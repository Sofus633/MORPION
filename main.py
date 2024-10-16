import pygame
from usefulfunctions import *
import time
import random

COLORS = [
    (0, 0, 64),       # Very Dark Blue
    (0, 0, 90),       # Deep Dark Blue
    (0, 0, 128),      # Navy
    (0, 0, 139),      # Dark Blue
    (25, 25, 112),    # Midnight Blue
    (0, 51, 102),     # Deep Teal Blue
    (0, 64, 128),     # Dark Slate Blue
    (0, 76, 153),     # Darkened Steel Blue
    (25, 25, 89),     # Shadow Blue
    (30, 60, 90)      # Muted Blue
]




def mainloop():
    global running
    global screen
    timerball = pygame.time.get_ticks() + 200
    while running:
        timer = pygame.time.get_ticks()
        if timer > timerball:
            timerball = timer + 200
            createaball()
        getclose()
        updateball()
        board.display()
        inputs()
        win = board.checkall()
        
        if win != None:
            board.clear()
            if win in ["croix", "cercle"]:
                rendertext(f'{win} a gagner', (255, 255, 255), (10, 10), screen)
            else:
                rendertext(f"{win}.", (255, 255, 255), (10, 10), screen)
            pygame.display.flip()
            screen.fill(0)
            time.sleep(1)
            replay = asknumber(screen, (1, 3), "Rejouer ? Y/N", "str")
            if replay in ("y", "Y", "yes", "YES"):
                pass
            elif replay in ('n', "N", "no", "NO"):
                running = False
        clock.tick(60)
            

def updateball():
    for ball in balls:
        ball.update()
        ball.display()

def createaball():
    randomx = random.randint(0, board.size * 200)
    color = random.randint(0, len(COLORS) - 1)
    balls.append(Fallingsphere(randomx, -50 , COLORS[color], balls, board))



def inputs():
    global turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            x, y = (position[0] // 200, position[1] // 200)
            if board[y][x] == None:
                board.set_case(y, x, turn)
            turn = "cercle" if turn == "croix" else "croix"

def getclose():
    mousepos = pygame.mouse.get_pos()
    for ball in balls:
        distance = abs(ball.position[0] - mousepos[0]) + abs(ball.position[1] - mousepos[1])
        if distance < 10000:
            ball.traceline(mousepos, distance)

class Fallingsphere:
    def __init__(self, x, y, color, liste, board):
        self.board = board
        self.liste = liste
        self.position = [x, y]
        self.size = random.randint(7, 50)
        self.dirrection = Vector2(0, 3)
        self.color = color
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #javou c'est une abération cette ligne
        self.dirrection = Vector2(((self.board.size * 200) //2 - mouse_pos[0]) * -2, 1000 + mouse_pos[1])
        self.dirrection = self.dirrection.normalize()
        self.position =  self.dirrection + self.position
        if self.position[1] > (self.board.size * 200) + 50 * 2 + 1:
            self.liste.remove(self)
    def display(self):
        pygame.draw.circle(screen, self.color, self.position, self.size)

            
    def traceline(self, mousepos, distance):
        print(distance)
        size = int((100 - distance / 2) / 2)
        pygame.draw.line(screen, self.color, self.position, mousepos, size if size < 7 else int(size / 3)) 



class Board:
    def __init__(self):
        self.screen  = pygame.display.set_mode((200 * 3, 200* 3))
        pygame.display.set_caption('Morpion')
        programIcon = pygame.image.load('icon.png')
        pygame.display.set_icon(programIcon)
        self.size = asknumber(self.screen ,(0, 5), "Enter a size", "int")
        self.screen  = pygame.display.set_mode((200 * self.size, 200* self.size))
        
        self.actualboard = [[None for i in range(self.size)]for i in range(self.size)]
    def __getitem__(self, key):
        return self.actualboard[key]
    
    def clear(self):
        self.actualboard = [[None for i in range(self.size)]for i in range(self.size)]
    
    def set_case(self, y, x, pion):
        if self.actualboard[y][x] == None:
            self.actualboard[y][x] = pion
    
    def display(self):
        mousepos = pygame.mouse.get_pos()
        transparent_surface = pygame.Surface((200, 200))
        transparent_surface.fill((25, 25, 25))
        transparent_surface.set_alpha(128) 
        screen.blit(transparent_surface, ((mousepos[0]//200) * 200, (mousepos[1]//200)* 200))
        for y in range(len(self.actualboard)):
            for x in range(len(self.actualboard[y])):

                drawthings(self.actualboard[y][x], (self.screen , (255, 255, 255), (x*200 + 25, y*200+ 25), 150))
        pygame.display.flip()
        screen.fill(0)
        
    def checklines(self):
        for row in self.actualboard:
            possible = row[0]  
            for value in row:
                if possible != value:  
                    possible = None
                    break
            if possible is not None: 
                return possible
        return None

    def checkcolumn(self):
        for col in range(self.size):
            first_value = self.actualboard[0][col]
            if first_value != None and all(self.actualboard[row][col] == first_value for row in range(self.size)):
                return first_value 
        return None 

    def checkall(self):
        colones = self.checkcolumn()
        lines = self.checklines()
        diag = self.checkdiagonals()
        full = self.checkfull()
        if full is not None:
            return full
        if colones is not None:
            return colones
        if lines is not None:
            return lines
        if diag is not None:
            return diag
        return None

    def checkdiagonals(self):
        first_value_main = self.actualboard[0][0]
        if first_value_main != None and all(self.actualboard[i][i] == first_value_main for i in range(self.size)):
            return first_value_main 
        
        first_value_anti = self.actualboard[0][2]
        if first_value_anti != None and all(self.actualboard[i][2 - i] == first_value_anti for i in range(self.size)):
            return first_value_main  
        
        return None 

    def checkfull(self):
        for raw in self.actualboard:
            for value in raw:
                if value == None:
                    return None
        else:
            return "Egalité"

if __name__ == "__main__":
    clock = pygame.time.Clock()
    board = Board()
    screen = board.screen
    turn = "cercle"
    running = True
    balls = []
    mainloop()