import pygame
import collections

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}

# class ScreenEngine:

#     def __enter__(self):
#         return self

#     def __exit__(self, *args):
#         pass


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        self.game_engine = engine


class GameSurface(ScreenHandle):

    def connect_engine(self, engine):
        self.game_engine = engine
        self.successor.connect_engine(engine)

    def draw_hero(self):
        self.game_engine.hero.draw(self)

    def draw_map(self):

        # FIXME || calculate (min_x,min_y) - left top corner

        min_x = 0
        min_y = 0

    ##

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][0], 
                        (i * self.game_engine.sprite_size, j * self.game_engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size
    # FIXME || calculate (min_x,min_y) - left top corner

        min_x = 0
        min_y = 0

    ##
        self.blit(sprite, ((coord[0] - min_x) * self.game_engine.sprite_size,
                           (coord[1] - min_y) * self.game_engine.sprite_size))

    def draw(self, canvas):
        size = self.game_engine.sprite_size
    # FIXME || calculate (min_x,min_y) - left top corner

        min_x = 0
        min_y = 0

    ##
        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * self.game_engine.sprite_size,
                                      (obj.position[1] - min_y) * self.game_engine.sprite_size))
        self.draw_hero()
        self.successor.draw(canvas)

    # draw next surface in chain


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.game_engine = engine
        self.successor.connect_engine(engine)
        # FIXME save engine and send it to next in chain

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["wooden"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["wooden"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
                         "red"], (50, 30, 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.game_engine.hero.exp / (100 * (2**(self.game_engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.game_engine.hero.position}', True, colors["green"]),
                  (250, 0))

        self.blit(font.render(f'{self.game_engine.level} floor', True, colors["red"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["red"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["red"]),
                  (10, 70))

        self.blit(font.render(f'{self.game_engine.hero.hp}/{self.game_engine.hero.max_hp}', True, colors["red"]),
                  (60, 30))
        self.blit(font.render(f'{self.game_engine.hero.exp}/{(100*(2**(self.game_engine.hero.level-1)))}', True, colors["red"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["red"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["red"]),
                  (300, 70))

        self.blit(font.render(f'{self.game_engine.hero.level}', True, colors["red"]),
                  (360, 30))
        self.blit(font.render(f'{self.game_engine.hero.gold}', True, colors["red"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["red"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["red"]),
                  (420, 70))

        self.blit(font.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["red"]),
                  (480, 30))
        self.blit(font.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["red"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["red"]),
                  (550, 30))
        self.blit(font.render(f'{self.game_engine.score:.4f}', True, colors["red"]),
                  (550, 70))
        self.successor.draw(canvas)
    # draw next surface in chain


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", 10)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["red"]),
                      (5, 20 + 18 * i))
        self.successor.draw(canvas)
    # FIXME
    # draw next surface in chain

    def connect_engine(self, engine):
        self.game_engine = engine
        self.successor.connect_engine(engine)
        # FIXME set this class as Observer to engine and send it to next in
        # chain


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
    # FIXME You can add some help information

    def connect_engine(self, engine):
        self.game_engine = engine
        self.successor.connect_engine(engine)
        # FIXME save engine and send it to next in chain

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.game_engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))

        self.successor.draw(canvas)
    # FIXME
    # draw next surface in chain
