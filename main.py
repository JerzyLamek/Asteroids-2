from tkinter import CENTER
import pygame
import os
from random import randint
from math import cos, sin, radians

class Settings(object):
    window_height = 1000#590
    window_width = 1800#900
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    title = "Asteroids 2"

    spaceship_size = (50, 50)
    spaceship_max_speed = 2

    asteroid_size = (50, 50)
    asteroid_speed = (-5, 5)

class Background(pygame.sprite.DirtySprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Spaceship(pygame.sprite.DirtySprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.spaceship_size)
        self.rect = self.image.get_rect()
        self.copy_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = (Settings.window_width // 2) - self.rect.width // 2
        self.rect.top = (Settings.window_height // 2) - self.rect.height // 2

        self.bullets = pygame.sprite.Group()

        self.rotation = 0
        self.speed_x = 0
        self.speed_y = 0

    def rotate_left(self):
        self.rotation += 5
        center = self.rect.center 
        self.image = self.copy_image
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def rotate_right(self):
        self.rotation -= 5
        center = self.rect.center 
        self.image = self.copy_image
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self):
        rotation = radians(self.rotation)

        new_speed_x = self.speed_x - sin(rotation)
        new_speed_y = self.speed_y - cos(rotation)

        if abs(new_speed_x) < 10 and abs(new_speed_y) < 10:
            self.speed_x = new_speed_x
            self.speed_y = new_speed_y

    def speed_up(self):
        self.rect.move_ip(self.speed_x, self.speed_y)

    def border(self):
        if self.rect.left >= Settings.window_width:
            self.rect.left = 0
        if self.rect.top >= Settings.window_height:
            self.rect.top = 0
        if self.rect.right <= 0:
            self.rect.left = Settings.window_width
        if self.rect.bottom <= 0:
            self.rect.top = Settings.window_height

    def collision(self):
        if pygame.sprite.spritecollide(self, game.asteroids, False, pygame.sprite.collide_mask):
            game.running = False
            print('Spaceship hat einen Asteroiden berührt!')

    def shoot(self):
        self.bullets.add(Bullet("5.png", self.rect.center, self.rotation))

    def update(self):
        self.speed_up()
        self.border()
        self.collision()

        self.bullets.update()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

class Bullet(pygame.sprite.DirtySprite):
    def __init__(self, filename, center, rotation):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.spaceship_size)
        self.rect = self.image.get_rect()
        self.copy_image = self.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center

        self.timer_bullet = Timer(5000, False)

        self.rotation_value = rotation
        self.speed_x = 0
        self.speed_y = 0

        self.rotation(center)

    def rotation(self, center):
        rotation_value = radians(self.rotation_value)

        self.new_speed_x = self.speed_x - sin(rotation_value)
        self.new_speed_y = self.speed_y - cos(rotation_value)

        self.image = pygame.transform.rotate(self.image, self.rotation_value)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self):
        self.rect.move_ip(self.new_speed_x, self.new_speed_y)

    def update(self):
        if self.timer_bullet.is_next_stop_reached():
            self.kill()

        self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Asteroid(pygame.sprite.DirtySprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.asteroid_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.find_position()
        self.speed = (randint(*Settings.asteroid_speed), randint(*Settings.asteroid_speed)) # * löst Tupel in zwei Zeilen

    def move_asteroids(self):
        self.rect.move_ip(self.speed)

    def border(self):
        if self.rect.left >= Settings.window_width:
            self.rect.left = 0
        if self.rect.top >= Settings.window_height:
            self.rect.top = 0
        if self.rect.right <= 0:
            self.rect.left = Settings.window_width
        if self.rect.bottom <= 0:
            self.rect.top = Settings.window_height

    def find_position(self):
        pos = (randint(0, Settings.window_width - self.rect.width),randint(0, Settings.window_height - self.rect.height))
        self.rect.top = pos[1]
        self.rect.left = pos[0]
        self.spawn_collission()

    def spawn_collission(self):
        hit = pygame.sprite.spritecollide(self, game.spaceship, False, pygame.sprite.collide_circle_ratio(1.75))
        if len(hit) > 0:
            self.find_position()

    def update(self):
        self.move_asteroids()
        self.border()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Timer:
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("star.jpg")
        self.spaceship = pygame.sprite.GroupSingle(Spaceship("4.png"))
        self.asteroids = pygame.sprite.Group()

        self.running = True
        
        self.timer_bullet = Timer(3000, False)

    def spawn_asteroids(self):
        if self.timer_bullet.is_next_stop_reached() and len(self.asteroids) < 5:
            self.asteroids.add(Asteroid("0.png"))

    def run(self): 
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.draw()
            self.update()
            self.spawn_asteroids()
        pygame.quit()

    def watch_for_events(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.spaceship.sprite.rotate_right()
        if pressed[pygame.K_LEFT]:
            self.spaceship.sprite.rotate_left()
        if pressed[pygame.K_UP]:
            self.spaceship.sprite.move()
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                if event.key == pygame.K_RETURN:
                    self.spaceship.sprite.shoot()
                
    def update(self):
        self.asteroids.update()
        self.spaceship.sprite.update()

    def draw(self):
        self.background.draw(self.screen)
        self.spaceship.sprite.draw(self.screen)
        self.asteroids.draw(self.screen)
        pygame.display.flip()
    
if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "170, 50"

    game = Game()
    game.run()