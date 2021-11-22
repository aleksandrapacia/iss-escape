import pygame
import sys
import json

from pygame.constants import MOUSEBUTTONDOWN
from station import Station
import pygame.mixer
import random

from enemy import Enemy
from bullet import Bullet
from button import Button


# initialazing pygame
pygame.init()

# constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 486
STATION_HEIGHT = 371
HW, HH = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# screen
(width, height) = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
intro_background = pygame.image.load("assets/textures/intro_bg.jpg").convert()
pygame.display.set_caption("ISS Escape")

# an image of the window after PAUSE BUTTON is clicked or after player's loss
win_after_pausing = pygame.image.load("assets/textures/window.png")

# MASKS
# station
station_file = open("assets/textures/iss.png")
station_texture = pygame.image.load(station_file)
station = Station(200, int(STATION_HEIGHT), station_texture)
# station's mask
station_texture_mask = pygame.mask.from_surface(station_texture)
station_rect = station_texture.get_rect()

# enemy
enemy_file = open("assets/textures/stone_2.png")
enemy_texture = pygame.image.load(enemy_file).convert_alpha()
# enemy's mask
enemy_texture_mask = pygame.mask.from_surface(enemy_texture)
enemy_rect = enemy_texture.get_rect()
enemies: list[Enemy] = []

# bullets
bullet_x = 90
bullet_file = open("assets/textures/bullet2.png")
bullet_texture = pygame.image.load("assets/textures/bullet2.png").convert_alpha()
bullets: list[Bullet] = []
# bullet's mask
bullet_texture_mask = pygame.mask.from_surface(bullet_texture)
bullet_rect = bullet_texture.get_rect()
ox = bullet_x + station.pos_x
oy = STATION_HEIGHT + 10

# time setup
clock = pygame.time.Clock()

# start button
start_button = pygame.image.load("assets/textures/start_button.png").convert()
start_button = Button(230, 200, start_button, 0.9)
# light start button
start_light = pygame.image.load("assets/textures/start_light.png").convert()
start_light = Button(230, 200, start_light, 0.9)

# quit button
quit_button = pygame.image.load("assets/textures/quit_button.png").convert()
quit_button = Button(230, 300, quit_button, 0.9)
# light quit button
quit_light = pygame.image.load("assets/textures/quit_light.png").convert()
quit_light = Button(230, 300, quit_light, 0.9)

# levels button
levels_button = pygame.image.load("assets/textures/levels_button.png").convert()
levels_button = Button(230, 400, levels_button, 0.9)
# light levels' button
levels_light = pygame.image.load("assets/textures/levels_light.png").convert()
levels_light = Button(230, 400, levels_light, 0.9)

# restart button
restart_button = pygame.image.load("assets/textures/resume_button.png").convert()
restart_button = Button(215, 300, restart_button, 1)
# light restart button
restart_light = pygame.image.load("assets/textures/resume_light.png").convert()
restart_light = Button(215, 300, restart_light, 1)

# menu button
menu_button = pygame.image.load("assets/textures/menu_button.png").convert()
menu_button = Button(215, 220, menu_button, 1)
# light menu buttons
menu_button_light = pygame.image.load("assets/textures/menu_light.png").convert()
menu_button_light_levels = Button(514, 2, menu_button_light, 0.5)
menu_button_light = Button(215, 220, menu_button_light, 1)
menu_button_levels_surface = pygame.image.load("assets/textures/menu_button.png").convert()
menu_button_levels = Button(514, 2, menu_button_levels_surface, 0.5)

# pause button
pause_button = pygame.image.load("assets/textures/pause_button.png").convert()
pause_button = Button(514, 2, pause_button, 0.5)
# light pause button
pause_light = pygame.image.load("assets/textures/pause_light.png").convert()
pause_light = Button(514, 2, pause_light, 0.5)

# retry button
retry_button = pygame.image.load("assets/textures/retry_button.png").convert()
retry_button = Button(215, 320, retry_button, 1)
# light retry button
retry_light = pygame.image.load("assets/textures/retry_light.png").convert()
retry_light = Button(215, 320, retry_light, 1)

# sounds
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")

# fonts
largetext = pygame.font.SysFont("Arial", 80)
smalltext = pygame.font.SysFont("freesansbold.ttf", 50)
mediumtext = pygame.font.SysFont("freesansbold.ttf", 30)

# score text's position
text_x = int(227)
text_y = int(177)

# colors
black = (0, 0, 0)
white = (255, 255, 255)
violet = (155, 96, 214)

# menu title
menu_title = largetext.render("ISS Escape", True, (45, 48, 144))

# mouse
mouse = pygame.mouse.get_pos()
score = Bullet.score = 0

# background setup
bg = pygame.image.load("assets/textures/bg.png").convert()
y_axis = 0

data = {
    'level': 0
}
try:
    with open('database.txt') as data_file:
        data = json.load(data_file)
except:
    print('no file created yet')

def show_score(x: int, y: int):
    '''shows the whole amount of scores during the game'''
    score_value = mediumtext.render("Score: " + str(Bullet.score), True, white)
    screen.blit(score_value, (x, y))

col1 = pygame.image.load("assets/textures/exp1.png")
col2 = pygame.image.load("assets/textures/exp2.png")
col3 = pygame.image.load("assets/textures/exp3.png")
col4 = pygame.image.load("assets/textures/exp4.png")
col5 = pygame.image.load("assets/textures/exp5.png")

class LevelState:
    def __init__(self):
        self.level = data['level']
        # how many points you have to achieve to score one level up
        self.achieve_score_for_l1 = 5

        self.window = False
        self.bullet_speed = 0
        self.enemy_speed = 0
        self.enemy_num = 0
        self.shoot_again = 0
        self.station_speed = 0
        # rise_speed_n = confirmed points
        self.rise_speed_a = 5
        self.rise_speed_b = 9
        self.rise_speed_c = 16
        self.rise_speed_d = 21
        self.rise_speed_e = 38
        self.rise_speed_f = 46
        self.rise_speed_g = 56
        self.rise_speed_h = 77
        self.rise_speed_i = 84
        self.rise_speed_j = 92
        self.rise_speed_k = 106
    #TODO: when achieve_scrore_for_l1 == Bullet score -> if lvl = 8 -> achieve_score_for_l2 = 8 * 5
    def level_change(self):
        # scoring level 1
        if lvl.achieve_score_for_l1 == Bullet.score:
            data['level'] +=1
            state.when_completed_level()
            pygame.display.update()
        if data['level'] == 1 and (lvl.achieve_score_for_l1-1) == Bullet.score:
            lvl.achieve_score_for_l1 +=2

        
def show_level(x: int, y: int):
    level_value = mediumtext.render('Level: ' + str(data['level']), True, white)
    screen.blit(level_value, (x, y))

class State(object):
    def __init__(self):
        self.game = False
        self.pause = False
        self.pause_after_collision = False
        self.levels = False
        self.intro = False
        self.update = False
        self.y_axis = 0
        self.win = False

    def when_completed_level(self):
        '''window displas when a level is completed'''
        self.win = True
        while self.win:
            state.update_screen()
            screen.blit(win_after_pausing, (0, 0))
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    with open('database.txt', 'w') as data_file:
                        json.dump(data, data_file)
                        pygame.quit()
                        sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0]:
                        if menu_button.rect.collidepoint(x, y):
                            self.issue = True
                            click_sound.play()
                            self.intro = True
                            self.game = False
                            self.update = True
                            Bullet.score = 0
                            state.intro_loop()

            level_window_1_title = largetext.render(
                'Level' + ' '  + str(data['level']) + ' ' + 'completed!', True, white
            )
            window_position1 = (28, 4)
            screen.blit(level_window_1_title, window_position1)
            menu_button.draw(screen)
            mouse = pygame.mouse.get_pos()
            if menu_button.rect.collidepoint(mouse):
                menu_button_light.draw(screen)
            pygame.display.update()

    def pause_button_clicked(self):
        'window displayed when you click on the pause button'
        self.pause = True
        while self.pause:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    with open('database.txt', 'w') as data_file:
                        json.dump(data, data_file)
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # clicking on the buttons
                    if pygame.mouse.get_pressed()[0]:
                        if restart_button.rect.collidepoint(x, y):
                            click_sound.play()
                            self.game = True
                            self.pause = False
                            state.game_loop()
                        if menu_button.rect.collidepoint(x, y):
                            Bullet.score=0
                            self.issue = True
                            state.update_screen()
                            click_sound.play()
                            self.intro = True
                            self.game = False
                            self.update = True
                            Bullet.score = 0
                            state.update_screen()
                            state.intro_loop()
                        mouse = pygame.mouse.get_pos()

            screen.blit(win_after_pausing, (0, 0))
            pause_title = largetext.render('Paused', True, white)
            pause_title_position = (190, 4)
            screen.blit(pause_title, pause_title_position)
            restart_button.draw(screen)
            menu_button.draw(screen)

            mouse = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if self.pause == True:
                    if menu_button.rect.collidepoint(mouse):
                        state.update_screen()

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if menu_button.rect.collidepoint(mouse):
                menu_button_light.draw(screen)
            if restart_button.rect.collidepoint(mouse):
                restart_light.draw(screen)
            pygame.display.update(screen_rect)

    # what happens after collision: between enemy and station, enemy and the edge
    # of the screen
    def pause_after_collision_loop(self):
        '''displaying loss window after player looses'''
        state.update_screen()
        pause_after_collision = True
        while pause_after_collision:
            state.update_screen()
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    with open('database.txt', 'w') as data_file:
                        json.dump(data, data_file)
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # clicking on the buttons
                    if pygame.mouse.get_pressed()[0]:
                        if menu_button.rect.collidepoint(x, y):
                            Bullet.score=0
                            self.intro = True
                            self.pause_after_collision = False
                            click_sound.play()
                            state.update_screen()
                            state.intro_loop()
                        # TODO: add retry button
                        if retry_button.rect.collidepoint(x, y):
                            Bullet.score=0
                            self.game = True
                            self.pause_after_collision = False
                            click_sound.play()
                            state.update_screen()
                            state.game_loop()

            screen.blit(intro_background, (0, 0))
            pause_title = largetext.render("Loss", True, white)
            pause_title_position = (230, 4)
            screen.blit(pause_title, pause_title_position)
            score_text = mediumtext.render(
                f"Scores gained in this round: {Bullet.score}", True, white
            )
            scoretext_position = (160, 100)
            screen.blit(score_text, scoretext_position)
            menu_button.draw(screen)
            retry_button.draw(screen)

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if menu_button.rect.collidepoint(mouse):
                menu_button_light.draw(screen)
            if retry_button.rect.collidepoint(mouse):
                retry_light.draw(screen)
            pygame.display.update(screen_rect)

    # menu (intro)
    def intro_loop(self):
        '''the game's menu shows up'''
        intro = True
        while intro:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    with open('database.txt', 'w') as data_file:
                        json.dump(data, data_file)
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # what happens when you click on the specific button
                    if pygame.mouse.get_pressed()[0]:
                        if start_button.rect.collidepoint(x, y):
                            click_sound.play()
                            self.game = True
                            self.intro = False
                            self.pause_after_collision = False
                            state.game_loop()
                        if quit_button.rect.collidepoint(x, y):
                            click_sound.play()
                            sys.exit()
                        if levels_button.rect.collidepoint(x, y):
                            click_sound.play()
                            self.levels = True
                            self.intro = False
                            state.levels_loop()

            screen.blit(intro_background, (0, 0))

            intro_title = largetext.render('ISS Escape', True, white)
            text_position = (134, 4)
            screen.blit(intro_title, text_position)
            start_button.draw(screen)
            quit_button.draw(screen)
            levels_button.draw(screen)

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if levels_button.rect.collidepoint(mouse):
                levels_light.draw(screen)
            if start_button.rect.collidepoint(mouse):
                start_light.draw(screen)
            if quit_button.rect.collidepoint(mouse):
                quit_light.draw(screen)
            pygame.display.update(screen_rect)

    # information about levels and list of them
    def levels_loop(self):
        '''displaying list of levels'''
        self.levels = True
        while self.levels:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    with open('database.txt', 'w') as data_file:
                        json.dump(data, data_file)
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # clicking buttons
                    if pygame.mouse.get_pressed()[0]:
                        # going to intro loop
                        if menu_button_levels.rect.collidepoint(x, y):
                            click_sound.play()
                            self.intro = True
                            self.leves = False
                            state.intro_loop()

            screen.blit(intro_background, (0, 0))
            menu_button_levels.draw(screen)
            levels_title = largetext.render("Levels", True, white)
            text_position = (178, 4)
            screen.blit(levels_title, text_position)

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if menu_button_levels.rect.collidepoint(mouse):
                menu_button_light_levels.draw(screen)
            pygame.display.update(screen_rect)

    def shoot(self):
        for bullet in range(1):
            bullet = Bullet(
                bullet_x + int(station.pos_x),
                STATION_HEIGHT + 10,
                bullet_texture,
                lvl.bullet_speed,
                0.0,
            )
            # moving the bullet
            bullets.append(bullet)
            bullet.move()
            # playing the shoot sound
            shot_sound.play()

    # main loop of the game
    def game_loop(self):
        shootTime = 0
        start_time = 0
        while self.game:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    with open('database.txt', 'w') as data_file:
                        json.dump(data, data_file)
                        pygame.quit()
                        sys.exit()

            # scrolling screen
            rel_y = self.y_axis % bg.get_rect().height
            screen.blit(bg, (0, rel_y - bg.get_rect().height))
            if rel_y < 486:
                screen.blit(bg, (0, rel_y))
            self.y_axis -= 1

            show_score(5, 5)
            lvl.level_change()
            show_level(5, 24)

            if Bullet.score <= lvl.rise_speed_a:
                lvl.bullet_speed = 11
                lvl.enemy_speed = 0.1
                lvl.enemy_num = 1
                lvl.shoot_again = 0.5
                lvl.station_speed = 0.5
            if Bullet.score == lvl.rise_speed_b:
                print('xdddd')
                lvl.bullet_speed = 10
                lvl.enemy_speed = 0.1
                lvl.enemy_num = 1
                lvl.shoot_again = 0.5
                lvl.station_speed = 0.7
            if Bullet.score == lvl.rise_speed_c:
                lvl.bullet_speed = 7
                lvl.enemy_speed = 0.2
                lvl.enemy_num = 1
                lvl.shoot_again = 0.5
                lvl.station_speed = 0.7
            if Bullet.score == lvl.rise_speed_d:
                lvl.bullet_speed = 6
                lvl.enemy_speed = 0.3
                lvl.enemy_num = 2
                lvl.shoot_again = 0.5
                lvl.station_speed = 0.8
            if Bullet.score == lvl.rise_speed_e:
                lvl.bullet_speed = 6
                lvl.enemy_speed = 0.3
                lvl.enemy_num = 2
                lvl.shoot_again = 0.5
                lvl.station_speed = 0.8
            if Bullet.score == lvl.rise_speed_f:
                lvl.bullet_speed = 5
                lvl.enemy_speed = 0.3
                lvl.enemy_num = 2
                lvl.shoot_again = 0.5
                lvl.station_speed = 1
            if Bullet.score == lvl.rise_speed_g:
                lvl.bullet_speed = 5
                lvl.enemy_speed = 0.4
                lvl.enemy_num = 2
                lvl.shoot_again = 0.5
                lvl.station_speed = 1.5
            if Bullet.score == lvl.rise_speed_h:
                lvl.bullet_speed = 5
                lvl.enemy_speed = 0.5
                lvl.enemy_num = 2
                lvl.shoot_again = 0.5
                lvl.station_speed = 1.6
            if Bullet.score == lvl.rise_speed_i:
                lvl.bullet_speed = 5
                lvl.enemy_speed = 0.7
                lvl.enemy_num = 4
                lvl.shoot_again = 0.5
                lvl.station_speed = 2
            if Bullet.score == lvl.rise_speed_j:
                lvl.bullet_speed = 4
                lvl.enemy_speed = 0.8
                lvl.enemy_num = 4
                lvl.shoot_again = 0.5
                lvl.station_speed = 2.1
            if Bullet.score == lvl.rise_speed_k:
                lvl.bullet_speed = 4
                lvl.enemy_speed = 0.8
                lvl.enemy_num = 4
                lvl.shoot_again = 0.5
                lvl.station_speed = 2.7

            # controlling shooting
            shootTime += lvl.shoot_again
            if shootTime == 60:  # 100 - beginning
                state.shoot()
                shootTime = 0

            # creating multiple enemies'
            for i in range(lvl.enemy_num):
                enemy = Enemy(
                    random.randrange(67, 515), -20, enemy_texture, lvl.enemy_speed
                )
                start_time += 1
                if start_time > 200:
                    enemies.append(enemy)
                    start_time = 0

            # enemies' and bullets' movements
            for bullet in bullets:
                bullet.move()
            for enemy in enemies:
                enemy.move()

            # when game is finished (after collision)
            for enemy in enemies:
                if enemy.pos_y > SCREEN_HEIGHT:
                    self.game = False
                    pause_after_collision = True
                    state.pause_after_collision_loop()
                    state.update_screen()

                if enemy.pos_y == station.pos_y:
                    self.game = False
                    state.pause_after_collision_loop()
                    state.update_screen()

                # collision between bullet and enemy
                for bullet in bullets:
                    offset = (
                        int(enemy.pos_x) - int(bullet.pos_x),
                        int(enemy.pos_y) - int(bullet.pos_y),
                    )
                    result = bullet_texture_mask.overlap(enemy_texture_mask, offset)
                    if result:
                        screen.blit(col1, (int(enemy.pos_x-17.5), int(enemy.pos_y-17.5)))
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        Bullet.score += 1

                # collision between station and enemies
                for enemy in enemies:
                    offset = (
                        int(enemy.pos_x) - int(station.pos_x),
                        int(enemy.pos_y) - int(station.pos_y),
                    )
                    result = station_texture_mask.overlap(enemy_texture_mask, offset)
                    if result:
                        self.game = False
                        state.pause_after_collision_loop()
                        state.update_screen()

            # station's movement
            all_keys = pygame.key.get_pressed()
            if all_keys[pygame.K_LEFT]:
                station.pos_x -= lvl.station_speed
            elif all_keys[pygame.K_RIGHT]:
                station.pos_x += lvl.station_speed

            # removing enemy when it goes off screen
            for bullet in bullets[:]:
                if bullet.pos_x < 0:
                    bullets.remove(bullet)
            for i in range(len(bullets)):
                bullet = bullets[i]

            # keeping player on screen
            if station.pos_x < 0:
                station.pos_x = 0
            if station.pos_x > 420:
                station.pos_x = 420

            # displaying enemies
            for enemy in enemies:
                screen.blit(enemy.texture, pygame.Rect(enemy.pos_x, enemy.pos_y, 0, 0))

            # displaying station
            screen.blit(station.texture, (station.pos_x, station.pos_y))

            for bullet in bullets:
                screen.blit(
                    bullet_texture, pygame.Rect(bullet.pos_x, bullet.pos_y, 0, 0)
                )

            # drawing pause button on screen
            mouse = pygame.mouse.get_pos()
            pause_button.draw(screen)
            if pause_button.rect.collidepoint(mouse):
                pause_light.draw(screen)

            x, y = pygame.mouse.get_pos()
            # what happens when pause button is cklicked
            if pygame.mouse.get_pressed()[0]:
                if pause_button.rect.collidepoint(x, y):
                    click_sound.play()
                    self.game = False
                    self.pause_after_collision = False
                    self.pause = True
                    state.pause_button_clicked()

            clock.tick(100)

            pygame.display.update(screen_rect)

    def update_screen(self):
        """updating screen after player's loss"""

        # scrolling background
        bg = pygame.image.load("assets/textures/bg.png").convert()
        rel_y = self.y_axis % bg.get_rect().height
        screen.blit(bg, (0, rel_y - bg.get_rect().height))
        if rel_y < 486:
            screen.blit(bg, (0, rel_y))
        self.y_axis -= 1

        # removing old bullets and displaying new ones
        for bullet in bullets:
            bullets.remove(bullet)
            num_of_b = len(bullets)
            num_of_b-=num_of_b
            Bullet.pos_y = 2 + int(station.pos_x)

        # removing old enemies and displaying new ones
        for enemy in enemies:
            enemies.remove(enemy)
            num_of_e = len(enemies)
            print(num_of_e)
            num_of_e-=num_of_e

        # restarting station's position
        station.pos_x = 200

        self.y_axis = 0

        pygame.display.update(screen_rect)


lvl = LevelState()
state = State()
# main loop
while True:
    state.intro_loop()
    all_event = pygame.event.get()    
    pygame.display.update()

# TODO: add other enemies
