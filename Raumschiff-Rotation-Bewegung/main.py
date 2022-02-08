import pygame
import os
from random import randint, randrange, uniform
from pygame.mask import from_surface

class Settings(object):
    window_height = 690
    window_width = 1060
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    #path_sound = os.path.join(path_file, "sound")
    title = "Raumschiff (Rotation und Bewegung"

    spaceship_size = (80, 50)
    spaceship_st_rotation = 0
    spaceship_rotation = 22


class Background(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.spaceship_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = (Settings.window_width // 2) - self.rect.width // 2
        self.rect.top = (Settings.window_height // 2) - self.rect.height // 2
    
    def update(self):
        pass

    def rotate_left(self):
        self.image = pygame.transform.rotate(self.image, Settings.spaceship_st_rotation + Settings.spaceship_rotation)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_right(self):
        self.image = pygame.transform.rotate(self.image, Settings.spaceship_st_rotation + Settings.spaceship_rotation)
        self.rect = self.image.get_rect()
        #self.center = 
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    
    
class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("star.jpg")
        self.spaceship = Spaceship("4.png")

        self.running = True

    def run(self): 
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.draw()
            self.update()

        pygame.quit()

    def watch_for_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.spaceship.rotate_left()
        if pressed[pygame.K_d]:
            self.spaceship.rotate_right()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p:
                    self.pause = not self.pause

                if event.key == pygame.K_k:
                    self.spaceship.rotate_left()
                if event.key == pygame.K_l:
                    self.spaceship.rotate_right()


    def update(self):
        self.spaceship.update()
        #self.rock.update()

    def draw(self):
        self.background.draw(self.screen)
        self.spaceship.draw(self.screen)
        #self.rock.draw(self.screen)
        pygame.display.flip()
    
if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "170, 50"

    game = Game()
    game.run()