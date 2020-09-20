from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite

class AbstractObject(ABC):

    def __init__(self, sprite_size):
        self.sprite_size = sprite_size

    def draw(self, display):
        n = 480 / self.sprite_size
        m = 640 / self.sprite_size
        n = n / 2
        m = m / 2
        n = int(n)
        m = int(m)
        min_x = max(0, self.position[0] - m)
        min_y = max(0, self.position[1] - n)
        min_x = min(min_x, 41 - 640 / self.sprite_size)
        min_y = min(min_y, 41 - 480 / self.sprite_size)
        min_x = int(min_x)
        min_y = int(min_y)
        display.blit(self.sprite, ((self.position[0] - min_x) * self.sprite_size, (self.position[1] - min_y) * self.sprite_size))

class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position, sprite_size, tp):
        self.sprite = icon
        self.action = action
        self.position = position
        self.type = tp
        AbstractObject.__init__(self, sprite_size)

    def interact(self, engine, hero):
        engine.delete_object(self)
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position, sprite_size):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.max_hp = 0
        self.calc_max_HP()
        self.hp = self.max_hp
        super().__init__(sprite_size)

    def calc_max_HP(self):
        self.max_hp = max(5 + self.stats["endurance"] * 2, self.max_hp)


class Hero(Creature):

    def __init__(self, stats, icon, sprite_size):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos, sprite_size)

    def level_up(self, engine):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            engine.notify("level up!")
            engine.score += 5
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp

class Enemy(Creature, Interactive):
    
    def __init__(self, icon, stats, xp, position, sprite_size):
        self.exp = xp
        Creature.__init__(self, icon, stats, position, sprite_size)

    def interact(self, engine, hero):
        if self.stats['endurance'] < hero.stats['strength']:
            hero.hp -= max(self.stats['strength'] - hero.stats['endurance'], 0)
            hero.stats['intelligence'] += self.stats['intelligence']
            hero.stats['luck'] += self.stats['luck']
            hero.exp += self.stats['experience'] / 2
            engine.delete_object(self)
            hero.level_up(engine)
            engine.score += self.stats['experience'] / 10
        else:
            hero.hp -= self.stats['strength'] - hero.stats['endurance']
            if hero.hp <= 0:
                hero.hp = 0
                engine.hero_died()

class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @property
    def sprite_size(self):
        return self.base.sprite_size

    @abstractmethod
    def apply_effect(self):
        pass

class Berserk(Effect):

    def apply_effect(self):
        self.max_hp = self.max_hp + 50
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["luck"] += 7
        self.stats["intelligence"] -= 3

class Blessing(Effect):

    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["luck"] += 2
        self.stats["intelligence"] += 2

class Weakness(Effect):

    def apply_effect(self):
        self.stats["strength"] -= 4
        self.stats["endurance"] -= 4

class EvilEye(Effect):

    def apply_effect(self):
        self.stats['luck'] -= 5