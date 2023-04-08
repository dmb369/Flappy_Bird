#sprites.py

import pygame as pg
from settings import *
from random import choice, randint

class BG(pg.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        
        bg_image = pg.image.load('/Users/devmbandhiya/Desktop/Flappy_Bird/Graphics/Environment/background.png').convert() #don't need alpha as there are no alpha values

        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pg.transform.scale(bg_image, (full_width, full_height)) #to fit the image

        self.image = pg.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_width,0))
        
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pg.math.Vector2(self.rect.topleft)     #have to use this as dt gives many floating points

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

        #-#-#-#-#

class Ground(pg.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'

        #image
        ground_surf = pg.image.load('/Users/devmbandhiya/Desktop/Flappy_Bird/Graphics/Environment/ground.png').convert_alpha()
        self.image = pg.transform.scale(ground_surf, pg.math.Vector2(ground_surf.get_size()) * scale_factor)

        #positon
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.pos = pg.math.Vector2(self.rect.topleft)

        #mask
        self.mask = pg.mask.from_surface(self.image) #same problem of mask is tackled here

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

        #-#-#-#-#

class Plane(pg.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        #image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/20, WINDOW_HEIGHT/2))
        self.pos = pg.math.Vector2(self.rect.topleft)

        #movement
        self.gravity = 600
        self.direction = 0

        #mask
        self.mask = pg.mask.from_surface(self.image) #same problem of mask is tackled here

        #sound
        self.jump_sound = pg.mixer.Sound('/Users/devmbandhiya/Desktop/Flappy_Bird/Sound/sounds_jump.wav')
        self.jump_sound.set_volume(0.2) #1 is max and 0 is min volume

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            surf = pg.image.load(f'/Users/devmbandhiya/Desktop/Flappy_Bird/Graphics/Plane/red{i}.png').convert_alpha()
            scaled_surface = pg.transform.scale(surf, pg.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self, dt):
        self.frame_index += 9 *  dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):  #rotates the plane when it goes up and down due to gravity
        rotated_plane = pg.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        self.mask = pg.mask.from_surface(self.image) #same problem of mask is tackled here

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()
        #the order matters here

        #-#-#-#-#

class Obstacle(pg.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle' 

        orientation = choice(('up','down'))
        surf = pg.image.load(f'/Users/devmbandhiya/Desktop/Flappy_Bird/Graphics/Obstacles/{choice((0,1))}.png').convert_alpha()
        self.image = pg.transform.scale(surf, pg.math.Vector2(surf.get_size()) * scale_factor)

        x = WINDOW_WIDTH + randint(40, 100)        

        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom = (x,y)) 
        
        else:
            y = randint(-50, -10)
            self.image = pg.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x,y))

        self.pos = pg.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)

        if self.rect.right <= -100:
            self.kill()
        

            
        

            

        


        
