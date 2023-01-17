import pygame
from pygame.locals import *
import sys


pygame.init()
BLANCO = (255, 255, 255)


pygame.init()
BLANCO = (255, 255, 255)


def fontsize(size):
    fuente = pygame.font.Font(
        "./src/fuentes/AliceandtheWickedMonster.ttf", size)
    return fuente


font_default = fontsize(20)

labels = []


class Label:

    ''' CLASS FOR TEXT LABELS ON THE WIN SCREEN SURFACE '''

    def __init__(self, screen, text, x, y, size=20, color="white"):
        if size != 20:
            self.font = fontsize(size)
        else:
            self.font = font_default
        self.image = self.font.render(text, 1, color)
        _, _, w, h = self.image.get_rect()
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.text = text
        labels.append(self)

    def change_text(self, newtext, color="white"):
        self.image = self.font.render(newtext, 1, color)

    def change_font(self, size, color="white"):
        #self.font = pygame.font.SysFont(font, size)
        self.change_text(self.text, color)

    def draw(self):
        self.screen.blit(self.image, (self.rect))


def show_labels():
    for _ in labels:
        _.draw()


def main():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icono = pygame.image.load("./src/imagenes/icono.jpg")
    pygame.display.set_icon(icono)
    pygame.display.set_caption("JUEGO TERMINADO")
    screen.fill(BLANCO)
    titulo = Label(
        screen, "JUEGO TERMINADO", 80, 150, 80, color="green")
    ganaste = Label(
        screen, "PERDISTE :(", 120, 300, 100, color="red")

    show_labels()

    pygame.display.flip()

    while True:
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    main()
