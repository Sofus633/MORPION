import pygame
import time
import gif_pygame
import math
pygame.font.init()
my_font = pygame.font.SysFont('IBM Plex Mono', 50)

def rendertext(text, color, pos ,screen):
    text_surface = my_font.render(text, False, color)
    screen.blit(text_surface, (pos))
    
def asknumber(screen, rangee, text, type):
    running = True
    input = ""
    screen.fill((0, 0, 0))
    rendertext(text, (255, 255, 255), (((2 * 200) / 2) - 100 , ((2 * 200) / 2) - 100), screen)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input = input[:-1]
                if event.key == pygame.K_RETURN:
                    print(input)
                    if type == 'str':
                        if len(input) >= rangee[0] and len(input) <= rangee[1]: 
                            running = False
                        else:
                            input = ''
                    if type == 'int':
                        try:
                            print(int(input))
                            if int(input) >= rangee[0] and int(input) <= rangee[1]:
                                input = int(input)
                                running = False
                            else:
                                input =  ''
                        except:
                            input = ''
                        
                
                if -128 <= event.key < 127 and event.key not in (8, 13):
                    input += chr(event.key)
                rendertext(str(input), (255, 255, 255), (((2 * 200) / 2) - 100, (2 * 200) / 2), screen)
                rendertext(text, (255, 255, 255), (((2 * 200) / 2) - 100 , ((2 * 200) / 2) - 100), screen)
                pygame.display.flip()
                screen.fill((0, 0, 0))
        time.sleep(.1)
    return input

def getGif(gif):
    a = gif_pygame.load(gif)
    return a 


def drawthings(thingtodraw, arguments):
    if thingtodraw == "croix":
        drawCross(*arguments)
    if thingtodraw == "cercle":
        drawCircle(*arguments)
    if thingtodraw == None:
        pass


def drawCross(screen, color, top_left, size):
    x, y = top_left
    pygame.draw.line(screen, color, (x, y), (x + size, y+ size), 5)
    pygame.draw.line(screen, color, (x + size , y), (x , y + size), 5)
    
    
    
def drawCircle(screen, color, center, radius):
    pygame.draw.circle(screen, color, (center[0] + radius/2 , center[1] + radius/2), radius/2, width=5)
    
    
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return [self.x + other[0], self.y + other[1]]
    
    def __sub__(self, other):
        return  Vector2(self.x + other[0], self.y + other[1])
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)  
        return Vector2(self.x / mag, self.y / mag)