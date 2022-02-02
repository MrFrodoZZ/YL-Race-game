import pygame
import os
import random
import sys

pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((700, 1000))
BG = pygame.image.load(os.path.join("Assets/Other", "bg.png"))
car = pygame.image.load(os.path.join("Assets/Car", "car.png"))
car_left = pygame.image.load(os.path.join("Assets/Car", "car_left.png"))
car_right = pygame.image.load(os.path.join("Assets/Car", "car_right.png"))
assets = [pygame.image.load(os.path.join("Assets/Obstacles", "Obstacle1.png")),
          pygame.image.load(os.path.join("Assets/Obstacles", "Obstacle2.png")),
          pygame.image.load(os.path.join("Assets/Obstacles", "Obstacle3.png"))]
cup = pygame.image.load(os.path.join("Assets/Other", "cup.png"))
assets[0] = pygame.transform.scale(assets[0], (40, 80))
leader = []
bord1 = pygame.Rect(10, 0, 1, 1000)
bord2 = pygame.Rect(699, 0, 1, 1000)


class Car:
    x_car_pos = 350
    y_car_pos = 800

    def __init__(self):
        self.car_in_move = True
        self.step_index = 0
        self.image = car
        self.car_rect = self.image.get_rect()
        self.car_rect.x = self.x_car_pos
        self.car_rect.y = self.y_car_pos

    def update(self, userInput, alive):
        if self.car_in_move and alive:
            self.in_move()
        if self.step_index >= 10:
            self.step_index = 0
        if userInput[pygame.K_UP]:
            self.car_in_move = False
        elif userInput[pygame.K_DOWN]:
            self.car_in_move = False
        elif not (userInput[pygame.K_DOWN]):
            self.car_in_move = True
        if userInput[pygame.K_RIGHT]:
            if not self.car_rect.colliderect(bord2):
                self.x_car_pos += 15
                self.image = car_right
        if userInput[pygame.K_LEFT]:
            if not self.car_rect.colliderect(bord1):
                self.x_car_pos += -15
                self.image = car_left

    def in_move(self):
        self.image = car
        self.car_rect = self.image.get_rect()
        self.car_rect.x = self.x_car_pos
        self.car_rect.y = self.y_car_pos
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.car_rect.x, self.car_rect.y))


class Obstacle:
    def __init__(self, image):
        self.type = random.randint(0, 2)
        self.image = image
        self.rect = self.image[self.type].get_rect()
        self.rect.x = random.randint(10, 540)

    def update(self):
        self.rect.y += speed
        if self.rect.y > 1000:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Button(pygame.sprite.Sprite):
    def __init__(self, img, scale, x, y):
        super(Button, self).__init__()
        self.image = img
        self.scale = scale
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, SCREEN):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                print(1)
                action = True
                self.clicked = True

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        SCREEN.blit(self.image, self.rect)
        return action


def game(n):
    engine = pygame.mixer.Sound('Assets/Sounds/engine.wav')
    background_music = pygame.mixer.Sound('Assets/Sounds/fon_music.mp3')
    engine.set_volume(0.3)
    background_music.set_volume(0.5)
    engine.play(-1, 0)
    background_music.play(-1, 0)
    global speed, x_bg_pos, y_bg_pos, count, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Car()
    speed = 30
    x_bg_pos = 0
    y_bg_pos = 380
    count = 0
    font = pygame.font.Font('font.ttf', 20)
    obstacles = []
    deaths = n

    def score():
        global count, speed
        count += 1
        if count % 100 == 0:
            speed += 1

    alive = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        SCREEN.blit(BG, (0, 0))
        userInput = pygame.key.get_pressed()
        player.draw(SCREEN)
        if alive:
            player.update(userInput, alive)
        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(Obstacle(assets))
            elif random.randint(0, 1) == 1:
                obstacles.append(Obstacle(assets))
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            if alive:
                obstacle.update()
            if player.car_rect.colliderect(obstacle.rect):
                pygame.mixer.Sound('Assets/Sounds/bonk.mp3').play()
                deaths += 1
                alive = False
                engine.stop()
                background_music.stop()
        score()
        clock.tick(30)
        if alive:
            pygame.display.update()
        else:
            leader.append("TRY " + str(deaths) + ": " + str(count))
            leader.append("\n")
            print(leader)
            menu(deaths)
    menu(deaths)


def menu(deaths):
    sound_btn = Button(cup, (60, 60), 310, 400)
    pressed = False
    global count
    run = True
    while run:
        font = pygame.font.Font('font.ttf', 60)
        if deaths == 0:
            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(car, (330, 800))
            text = font.render("PRESS TO START", True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (350, 500)
            SCREEN.blit(text, textRect)
        elif deaths > 0:
            text = font.render("PRESS TO RESTART", True, (255, 255, 255))
            if sound_btn.draw(SCREEN):
                SCREEN.blit(BG, (0, 0))
                pressed = not pressed
                print(pressed)
            if pressed == False:
                textRect = text.get_rect()
                textRect.center = (350, 500)
                score_text = font.render("SCORE: " + str(count), True, (255, 255, 255))
                score_text_Rect = score_text.get_rect()
                score_text_Rect.center = (350, 550)
                SCREEN.blit(score_text, score_text_Rect)
                SCREEN.blit(text, textRect)
            else:
                hei = 500
                for i in leader:
                    text = font.render(i, True, (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.center = (350, hei)
                    SCREEN.blit(text, textRect)
                    hei += 20
                pygame.display.update()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                game(deaths)


menu(deaths=0)
