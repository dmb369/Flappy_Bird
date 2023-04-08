#main.py

import pygame as pg, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
    def __init__(self):

        #setup
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Flappy Bird')
        self.clock = pg.time.Clock()
        self.active = True

        #sprite groups
        self.all_sprites = pg.sprite.Group()
        self.collision_sprites = pg.sprite.Group()

        #scale factor
        bg_height = pg.image.load('/Users/devmbandhiya/Desktop/Flappy_Bird/Graphics/Environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        #sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)

        #timer
        self.obstacle_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.obstacle_timer, 1400)

        #text
        self.font = pg.font.Font('/Users/devmbandhiya/Desktop/Flappy_Bird/Graphics/Font/font.ttf', 30)
        self.score = 0
        self.start_offset = 0

        #menu
        self.menu_surf = pg.image.load('/Users/devmbandhiya/Desktop/Flappy_Bird/Graphics/UI/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        #music
        self.music = pg.mixer.Sound('/Users/devmbandhiya/Desktop/Flappy_Bird/Sound/sounds_music.wav')
        self.music.play(loops = -1)  #tells pygame to run the loop continuously
        

    def collisions(self):
        #Note: game was quitting after sometime as pg considers mountains as rectangle
        #Tackled using masks
        if pg.sprite.spritecollide(self.plane, self.collision_sprites, False, pg.sprite.collide_mask) or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()      #every fuction which ran while plane was active  will terminate
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            #self.score = pg.time.get_ticks() // 1000 #always starts from zero... #won't restart even if the game is
            #tackled using...
            self.score = (pg.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)
 
        score_surf = self.font.render(str(self.score), True,  'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)
 
    def run(self):
        last_time = time.time()
        while True:

            #delta time_It accounts for different framerates
            dt = time.time() - last_time 
            last_time = time.time()

            #event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                        
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7) #need the plane in starting positon also
                        self.active = True  #won't restart by itself...
                        self.start_offset = pg.time.get_ticks()
                        

                if event.type == self.obstacle_timer and self.active:
                    #makes sure no obstacle is spawned and destroying all the existing obstacles
                    #will also destroy the ground
                    #problem tackled by initiating sprite_types
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.05)

            #game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions() # if True then I have to check for ...

            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect )
                    
            pg.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__': #checking if our current file is main.py file
    game = Game()
    game.run()
