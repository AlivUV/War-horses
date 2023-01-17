import pygame
from pygame.locals import *
import sys
from clases.tablero2 import main as tablero


pygame.init()
BLANCO = (255, 255, 255)
nivel = 1


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
    pygame.display.set_caption("WAR HORSES")
    screen.fill(BLANCO)

    titulo = Label(
        screen, "WAR HORSES", 150, 150, 80, color="blue")
    selecciona_dificultad = Label(
        screen, "Selecciona la dificultad:", 160, 300, 40, color="black")
    principiante = Label(
        screen, "Principiante", 90, 400, 30, color="black")
    amateur = Label(
        screen, "Amateur", 270, 400, 30, color="black")
    experto = Label(
        screen, "Experto", 430, 400, 30, color="black")
    iniciar = Label(
        screen, "INICIAR", 220, 500, 50, color="black")

    caballo1 = pygame.image.load(
        "./src/imagenes/caballo_inicio1.png").convert_alpha()
    caballo1 = pygame.transform.scale(caballo1, [80, 80])
    screen.blit(caballo1, (40, 135))

    caballo2 = pygame.image.load(
        "./src/imagenes/caballo_inicio2.png").convert_alpha()
    caballo2 = pygame.transform.scale(caballo2, [80, 80])
    screen.blit(caballo2, (455, 135))

    show_labels()
    # se muestran lo cambios en pantalla
    pygame.display.flip()

    while True:
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (90 <= pygame.mouse.get_pos()[0] <= 200 and 400 <= pygame.mouse.get_pos()[1] <= 440):
                    principiante.change_font(30, color="blue")
                    amateur.change_font(30, color="black")
                    experto.change_font(30, color="black")
                    nivel = 2
                    show_labels()
                    pygame.display.flip()
                if (270 <= pygame.mouse.get_pos()[0] <= 360 and 400 <= pygame.mouse.get_pos()[1] <= 440):
                    amateur.change_font(30, color="blue")
                    principiante.change_font(30, color="black")
                    experto.change_font(30, color="black")
                    show_labels()
                    nivel = 3
                    pygame.display.flip()
                if (430 <= pygame.mouse.get_pos()[0] <= 520 and 400 <= pygame.mouse.get_pos()[1] <= 440):
                    experto.change_font(30, color="blue")
                    principiante.change_font(30, color="black")
                    amateur.change_font(30, color="black")
                    show_labels()
                    pygame.display.flip()
                    nivel = 4
                if (220 <= pygame.mouse.get_pos()[0] <= 350 and 500 <= pygame.mouse.get_pos()[1] <= 550):
                    iniciar.change_font(30, color="blue")
                    show_labels()
                    pygame.display.flip()
                    print(nivel)
                    tablero(nivel)
                    pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                if (90 <= pygame.mouse.get_pos()[0] <= 200 and 400 <= pygame.mouse.get_pos()[1] <= 440):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif (270 <= pygame.mouse.get_pos()[0] <= 360 and 400 <= pygame.mouse.get_pos()[1] <= 440):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif (430 <= pygame.mouse.get_pos()[0] <= 520 and 400 <= pygame.mouse.get_pos()[1] <= 440):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                elif (220 <= pygame.mouse.get_pos()[0] <= 350 and 500 <= pygame.mouse.get_pos()[1] <= 550):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


if __name__ == "__main__":
    main()
