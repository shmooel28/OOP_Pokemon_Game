import json

import pygame
from pygame import *
from pygame import gfxdraw

from src.Game_Algo import Game_Algo
from src.client import Client

WIDTH, HEIGHT = 1080, 720
# save the image source
image_pokemon = "game_photo/Charmander.jpg"
image_pikachu = "game_photo/Pikachu.jpg"
image_ash = "game_photo/Ash.jpg"
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

moves = " "
grade = " "
FONT = pygame.font.SysFont('Arial', 20, bold=True)
text4 = FONT.render("STOP", True, (255, 255, 255), (0, 0, 0))
text_render4 = text4.get_rect()
text_render4.center = (30, 20)


class GUI:
    # display the graph with pygame
    def __init__(self, game: Game_Algo, client: Client):
        self.game = game
        self.client = client
        self.min_x = float('inf')
        self.min_y = float('inf')
        self.max_x = float('-inf')
        self.max_y = float('-inf')

        for n in self.game.graph.graph.node_dic.values():
            x = n.pos[0]
            y = n.pos[1]
            self.min_x = min(self.min_x, x)
            self.min_y = min(self.min_y, y)
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, screen.get_height() - 50, self.min_y, self.max_y)

    def run(self):
        # refresh surface
        screen.fill(Color(255, 255, 255))

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        mouse = pygame.mouse.get_pos()
        if 0 <= mouse[0] <= 50 and 0 <= mouse[1] <= 40:
            if pygame.mouse.get_pressed()[0]:
                self.client.stop()
        # draw nodes
        for n in self.game.graph.graph.node_dic.values():
            x = self.my_scale(n.pos[0], x=True)
            y = self.my_scale(n.pos[1], y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  15, Color(64, 80, 174))
            gfxdraw.aacircle(screen, int(x), int(y),
                             15, Color(255, 255, 255))
            # draw the node id
            id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

        # draw edges
        for e in self.game.graph.graph.edge_dic:
            # find the edge nodes
            src = next(n for n in self.game.graph.graph.node_dic.values() if n.id == e[0])
            dest = next(n for n in self.game.graph.graph.node_dic.values() if n.id == e[1])

            # scaled positions
            src_x = self.my_scale(src.pos[0], x=True)
            src_y = self.my_scale(src.pos[1], y=True)
            dest_x = self.my_scale(dest.pos[0], x=True)
            dest_y = self.my_scale(dest.pos[1], y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126),
                             (src_x, src_y), (dest_x, dest_y))

            # draw agents
        for agent in self.game.Agent.values():
            x = self.my_scale(agent.pos[0], x=True)
            y = self.my_scale(agent.pos[1], y=True)
            img = pygame.image.load(image_ash)
            screen.blit(img, (int(x - 10), int(y - 10)))
        # draw Pokemon's
        for p in self.game.Pokemon:
            if p.type > 0:
                img = pygame.image.load(image_pikachu)
            else:
                img = pygame.image.load(image_pokemon)
            x = self.my_scale(p.pos[0], x=True)
            y = self.my_scale(p.pos[1], y=True)
            screen.blit(img, (int(x - 10), int(y - 10)))
        # self.update_text()
        grade = json.loads(self.client.get_info())["GameServer"]["grade"]
        moves = json.loads(self.client.get_info())["GameServer"]["moves"]
        text1 = FONT.render("time left:" + str(int(self.client.time_to_end()) // 1000), True, (255, 255, 255),
                            (0, 0, 0))
        text2 = FONT.render("grade: " + str(grade), True, (255, 255, 255), (0, 0, 0))
        text3 = FONT.render("moves: " + str(moves), True, (255, 255, 255), (0, 0, 0))
        text_render1 = text1.get_rect()
        text_render2 = text2.get_rect()
        text_render3 = text3.get_rect()
        text_render1.center = (50, 50)
        text_render2.center = (50, 80)
        text_render3.center = (50, 110)
        screen.blit(text1, text_render1)
        screen.blit(text2, text_render2)
        screen.blit(text3, text_render3)
        screen.blit(text4, text_render4)
        # update screen changes
        display.update()
        # refresh rate
        clock.tick(60)
        pygame.time.wait(28)
