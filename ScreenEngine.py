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

def create_sprite(sprite, size):
    new_sprite = pygame.transform.scale(sprite, (size, size))
    return new_sprite

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

    def calc_mn(self):
        n = 480 / self.game_engine.sprite_size
        m = 640 / self.game_engine.sprite_size
        n = n / 2
        m = m / 2
        n = int(n)
        m = int(m)
        min_x = max(0, self.game_engine.hero.position[0] - m)
        min_y = max(0, self.game_engine.hero.position[1] - n)
        min_x = min(min_x, 41 - 640 / self.game_engine.sprite_size)
        min_y = min(min_y, 41 - 480 / self.game_engine.sprite_size)
        min_x = int(min_x)
        min_y = int(min_y)
        return (min_x, min_y)

    def draw_map(self):

        min_x = self.calc_mn()[0]
        min_y = self.calc_mn()[1]

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
        min_x = self.calc_mn()[0]
        min_y = self.calc_mn()[1]

        self.blit(sprite, ((coord[0] - min_x) * self.game_engine.sprite_size,
                           (coord[1] - min_y) * self.game_engine.sprite_size))

    def draw(self, canvas):
        size = self.game_engine.sprite_size
        min_x = self.calc_mn()[0]
        min_y = self.calc_mn()[1]

        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * self.game_engine.sprite_size,
                                      (obj.position[1] - min_y) * self.game_engine.sprite_size))
        if self.game_engine.hero.sprite != None:
            self.draw_hero()
        canvas.blit(self.successor, self.next_coord)
        self.successor.draw(canvas)



class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.game_engine = engine
        self.successor.connect_engine(engine)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
                         "red"], (50, 30, 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.game_engine.hero.exp / (100 * (2**(self.game_engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.game_engine.hero.position}', True, colors["black"]),
                  (250, 0))

        self.blit(font.render(f'{self.game_engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{self.game_engine.hero.hp}/{self.game_engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))
        self.blit(font.render(f'{self.game_engine.hero.exp}/{(100*(2**(self.game_engine.hero.level-1)))}', True, colors["black"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.game_engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.game_engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.game_engine.score:.4f}', True, colors["black"]),
                  (550, 70))
        canvas.blit(self.successor, self.next_coord)
        self.successor.draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")
        if 20 + (len(self.data) - 1) * 18 + 10 >= 440:
            self.data.popleft()

    def draw(self, canvas):
        self.fill(colors["wooden"])
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", 10)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["red"]),
                      (5, 20 + 18 * i))
        canvas.blit(self.successor, self.next_coord)
        self.successor.draw(canvas)

    def connect_engine(self, engine):
        engine.subscribe(self)
        self.game_engine = engine
        self.successor.connect_engine(engine)

class MiniMap(ScreenHandle):

    def connect_engine(self, engine):
        self.game_engine = engine
        self.successor.connect_engine(engine)

    def calc_mn(self):
        size = 12
        n = 160 / size 
        m = n
        n = n / 2
        m = m / 2
        n = int(n)
        m = int(m)
        min_x = max(0, self.game_engine.hero.position[0] - m)
        min_y = max(0, self.game_engine.hero.position[1] - n)
        min_x = min(min_x, 41 - int(160 / 12))
        min_y = min(min_y, 41 - int(160 / 12))
        return (min_x, min_y)


    def draw_map(self):

        min_x = self.calc_mn()[0]
        min_y = self.calc_mn()[1]

    ##

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][0], 
                        (i * 12, j * 12))
        else:
            self.fill(colors["white"])

    def draw_hero(self):
        min_x = self.calc_mn()[0]
        min_y = self.calc_mn()[1]
        self.blit(create_sprite(self.game_engine.hero.sprite, 12), 
            ((self.game_engine.hero.position[0] - min_x) * 12, (self.game_engine.hero.position[1] - min_y) * 12))

    def draw(self, canvas):
        min_x = self.calc_mn()[0]
        min_y = self.calc_mn()[1]
        size = 20
        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(create_sprite(obj.sprite[0], 12), ((obj.position[0] - min_x) * 12,
                                      (obj.position[1] - min_y) * 12))
        if self.game_engine.hero.sprite != None:
            self.draw_hero()
        canvas.blit(self.successor, self.next_coord)
        self.successor.draw(canvas)

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

    def connect_engine(self, engine):
        self.game_engine = engine
        self.successor.connect_engine(engine)

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
        canvas.blit(self.successor, self.next_coord)
        self.successor.draw(canvas)
