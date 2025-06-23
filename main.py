import pygame
import sys
import time
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 700))
pygame.display.set_caption("Street Fighter")

BLACK = (0, 0, 0)
RED_DARK = (139, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

big_font = pygame.font.SysFont("arial", 100, bold=True)
menu_font = pygame.font.SysFont("arial", 50)
char_font = pygame.font.SysFont(None, 40)
timer_font = pygame.font.SysFont("arial", 36, bold=True)

menu_background = pygame.image.load("picture/background/yy.png")
game_background = pygame.image.load("picture/background/imo5.png")

menu_buttons = ["Start Game", "Options", "Exit"]

# Sound effects
try:
    sounds = {
        'punch': pygame.mixer.Sound("sounds/punch.wav"),
        'punchr': pygame.mixer.Sound("sounds/punchr.wav"),
        'fpunch': pygame.mixer.Sound("sounds/fpunch.wav"),
        'legr': pygame.mixer.Sound("sounds/legr.wav"),
        'legfor': pygame.mixer.Sound("sounds/legfor.wav"),
        'hit': pygame.mixer.Sound("sounds/hit.wav"),
        'victory2': pygame.mixer.Sound("sounds/victory.wav")
    }
    pygame.mixer.set_num_channels(10)
except:
    sounds = {name: pygame.mixer.Sound(buffer=bytearray(100)) for name in [
        'punch', 'punchr', 'fpunch', 'legr', 'legfor', 'hit', 'victory2'
    ]}

class Fighter:
    def __init__(self, start_x=100, start_y=340, jump_height=150, direction="right"):
        self.char_x, self.char_y = start_x, start_y
        self.ground_level = start_y
        self.char_speed = 2
        self.frame_index = 0
        self.frame_delay = 100
        self.last_update_time = pygame.time.get_ticks()
        self.direction = direction
        self.moving = False
        self.is_jumping = False
        self.jump_index = 0
        self.jump_height = jump_height
        self.jump_up = True
        self.is_blocking_down = False
        self.is_blocking_shift = False
        self.is_punching = False
        self.punch_index = 0
        self.punch_delay = 80
        self.last_punch_time = 0
        self.is_fpunching = False
        self.fpunch_index = 0
        self.fpunch_delay = 100
        self.last_fpunch_time = 0
        self.is_punchr = False
        self.punchr_index = 0
        self.punchr_delay = 100
        self.last_punchr_time = 0
        self.is_legr = False
        self.legr_index = 0
        self.legr_delay = 100
        self.last_legr_time = 0
        self.is_legforward = False
        self.legfor_index = 0
        self.legfor_delay = 100
        self.last_legfor_time = 0
        self.health = 100
        self.max_health = 100
        self.is_hit = False
        self.hit_index = 0
        self.hit_delay = 100
        self.last_hit_time = 0
        self.is_ko = False
        self.ko_index = 0
        self.ko_delay = 150
        self.last_ko_time = 0
        self.is_timeout = False
        self.timeout_index = 0
        self.timeout_delay = 150
        self.last_timeout_time = 0
        self.is_victory = False
        self.victory_index = 0
        self.victory_delay = 150
        self.last_victory_time = 0
        self.ai_timer = 0
        self.ai_action_delay = random.randint(500, 1500)
        self.is_cpu = False

    def take_hit(self, damage):
        if not (self.is_blocking_down or self.is_blocking_shift):
            self.health -= damage
            self.is_hit = True
            self.hit_index = 0
            self.last_hit_time = pygame.time.get_ticks()
           # sounds['hit'].play()
            if self.health <= 0:
                self.health = 0
                self.is_ko = True
                self.ko_index = 0
                self.last_ko_time = pygame.time.get_ticks()
    
    def update(self, keys, current_time, opponent=None):
        if self.is_ko or self.is_timeout or self.is_victory:
            return
            
        self.moving = False
        self.is_blocking_down = keys[pygame.K_DOWN] if not self.is_cpu else False
        self.is_blocking_shift = keys[pygame.K_LSHIFT] if not self.is_cpu else False

        if not self.is_cpu:
            # Player controls
            if not any([self.is_jumping, self.is_punching, self.is_fpunching, 
                       self.is_punchr, self.is_legr, self.is_legforward, self.is_hit]):
                if keys[pygame.K_RIGHT] and self.char_x < 1280 - 150:
                    self.char_x += self.char_speed
                    self.direction = "right"
                    self.moving = True
                elif keys[pygame.K_LEFT] and self.char_x > 0:
                    self.char_x -= self.char_speed
                    self.direction = "left"
                    self.moving = True

            if keys[pygame.K_UP] and not any([self.is_jumping, self.is_punching, 
                                             self.is_fpunching, self.is_punchr, 
                                             self.is_legr, self.is_legforward]):
                self.is_jumping = True
                self.jump_index = 0
                self.jump_up = True

            if keys[pygame.K_a] and not any([self.is_punching, self.is_jumping, 
                                            self.is_fpunching, self.is_punchr, 
                                            self.is_legr, self.is_legforward]):
                self.is_punching = True
                self.punch_index = 0
                self.last_punch_time = current_time
                sounds['punch'].play()

            if keys[pygame.K_s] and not any([self.is_fpunching, self.is_jumping, 
                                            self.is_punching, self.is_punchr, 
                                            self.is_legr, self.is_legforward]):
                self.is_fpunching = True
                self.fpunch_index = 0
                self.last_fpunch_time = current_time
                sounds['fpunch'].play()

            if keys[pygame.K_d] and not any([self.is_punchr, self.is_fpunching, 
                                            self.is_jumping, self.is_punching, 
                                            self.is_legr, self.is_legforward]):
                self.is_punchr = True
                self.punchr_index = 0
                self.last_punchr_time = current_time
                sounds['punchr'].play()

            if keys[pygame.K_z] and not any([self.is_legr, self.is_fpunching, 
                                           self.is_punching, self.is_punchr, 
                                           self.is_jumping, self.is_legforward]):
                self.is_legr = True
                self.legr_index = 0
                self.last_legr_time = current_time
                sounds['legr'].play()

            if keys[pygame.K_x] and not any([self.is_legforward, self.is_legr, 
                                            self.is_fpunching, self.is_punchr, 
                                            self.is_punching, self.is_jumping]):
                self.is_legforward = True
                self.legfor_index = 0
                self.last_legfor_time = current_time
                sounds['legfor'].play()
        else:
            # AI controls - Improved version
            if current_time - self.ai_timer > self.ai_action_delay and opponent:
                self.ai_timer = current_time
                distance = abs(self.char_x - opponent.char_x)
                
                # More aggressive AI based on distance
                if distance < 100:  # Very close
                    if random.random() < 0.7:
                        attack_type = random.choice(["punch", "fpunch", "leg"])
                        if attack_type == "punch":
                            self.is_punching = True
                            self.punch_index = 0
                            self.last_punch_time = current_time
                        elif attack_type == "fpunch":
                            self.is_fpunching = True
                            self.fpunch_index = 0
                            self.last_fpunch_time = current_time
                        else:
                            self.is_legforward = True
                            self.legfor_index = 0
                            self.last_legfor_time = current_time
                    else:
                        self.is_blocking_down = random.random() < 0.5
                        self.is_blocking_shift = not self.is_blocking_down
                
                elif distance < 200:  # Medium range
                    rand_val = random.random()
                    if rand_val < 0.5:
                        attack_type = random.choice(["punch", "leg"])
                        if attack_type == "punch":
                            self.is_punching = True
                            self.punch_index = 0
                            self.last_punch_time = current_time
                        else:
                            self.is_legforward = True
                            self.legfor_index = 0
                            self.last_legfor_time = current_time
                    elif rand_val < 0.8:
                        if self.health < opponent.health and distance < 150:
                            move_dir = -1 if opponent.char_x < self.char_x else 1
                        else:
                            move_dir = 1 if opponent.char_x < self.char_x else -1
                        
                        self.char_x += move_dir * self.char_speed * 2
                        self.direction = "left" if move_dir > 0 else "left"
                        self.moving = True
                    else:
                        self.is_jumping = True
                        self.jump_index = 0
                        self.jump_up = True
                
                else:  # Far range
                    if random.random() < 0.7:
                        move_dir = 1 if opponent.char_x < self.char_x else -1
                        self.char_x += move_dir * self.char_speed * 1.2
                        self.direction = "left" if move_dir > 0 else "left"
                        self.moving = True
                    else:
                        self.is_jumping = True
                        self.jump_index = 0
                        self.jump_up = True
                
                self.ai_action_delay = random.randint(300, 1000)

        # Update jumping state
        if self.is_jumping:
            if current_time - self.last_update_time >= self.frame_delay:
                if self.jump_index < len(self.jump_right_frames) - 1:
                    self.jump_index += 1
                self.last_update_time = current_time
            if self.jump_up:
                self.char_y -= 5
                if self.char_y <= self.ground_level - self.jump_height:
                    self.jump_up = False
            else:
                self.char_y += 0.8
                if self.char_y >= self.ground_level:
                    self.char_y = self.ground_level
                    self.is_jumping = False
                    self.jump_index = 0

        # Update punching state
        if self.is_punching:
            if current_time - self.last_punch_time >= self.punch_delay:
                self.punch_index += 1
                self.last_punch_time = current_time
                if self.punch_index >= len(self.punch_right_frames):
                    self.punch_index = 0
                    self.is_punching = False

        if self.is_fpunching:
            if current_time - self.last_fpunch_time >= self.fpunch_delay:
                self.fpunch_index += 1
                self.last_fpunch_time = current_time
                if self.fpunch_index >= len(self.fpunch_right_frames):
                    self.fpunch_index = 0
                    self.is_fpunching = False

        if self.is_punchr:
            if current_time - self.last_punchr_time >= self.punchr_delay:
                self.punchr_index += 1
                self.last_punchr_time = current_time
                if self.punchr_index >= len(self.punchr_right_frames):
                    self.punchr_index = 0
                    self.is_punchr = False
                    
        if self.is_legr:
            if current_time - self.last_legr_time >= self.legr_delay:
                self.legr_index += 1
                self.last_legr_time = current_time
                if self.legr_index >= len(self.legr_right_frames):
                    self.legr_index = 0
                    self.is_legr = False

        if self.is_legforward:
            if current_time - self.last_legfor_time >= self.legfor_delay:
                self.legfor_index += 1
                self.last_legfor_time = current_time
                if self.legfor_index >= len(self.legfor_right_frames):
                    self.legfor_index = 0
                    self.is_legforward = False

        if current_time - self.last_update_time >= self.frame_delay and not any([self.is_jumping, self.is_blocking_down, self.is_blocking_shift, self.is_punching, self.is_fpunching, self.is_punchr, self.is_legr, self.is_legforward, self.is_hit]):
            if self.moving:
                self.frame_index = (self.frame_index + 1) % len(self.right_frames)
            else:
                self.frame_index = 0
            self.last_update_time = current_time
    
    def draw(self, screen, background):
        # Draw health bar
        if self.direction == "right":
            health_x = self.char_x
        else:
            health_x = self.char_x - 150 + self.right_frames[0].get_width()
            
        pygame.draw.rect(screen, (255, 0, 0), (health_x, self.char_y - 20, 150, 10))
        pygame.draw.rect(screen, (0, 255, 0), (health_x, self.char_y - 20, 150 * (self.health / self.max_health), 10))
        
        # Determine the appropriate frame based on state
        if self.is_ko:
            current_frame = self.ko_right_frames[self.ko_index] if self.direction == "right" else self.ko_left_frames[self.ko_index]
            if pygame.time.get_ticks() - self.last_ko_time >= self.ko_delay:
                self.ko_index += 1
                self.last_ko_time = pygame.time.get_ticks()
                if self.ko_index >= len(self.ko_right_frames):
                    self.ko_index = len(self.ko_right_frames) - 1
        elif self.is_timeout:
            current_frame = self.timeout_right_frames[self.timeout_index] if self.direction == "right" else self.timeout_left_frames[self.timeout_index]
            if pygame.time.get_ticks() - self.last_timeout_time >= self.timeout_delay:
                self.timeout_index += 1
                self.last_timeout_time = pygame.time.get_ticks()
                if self.timeout_index >= len(self.timeout_right_frames):
                    self.timeout_index = len(self.timeout_right_frames) - 1
        elif self.is_victory:
            current_frame = self.victory_right_frames[self.victory_index] if self.direction == "right" else self.victory_left_frames[self.victory_index]
            if pygame.time.get_ticks() - self.last_victory_time >= self.victory_delay:
                self.victory_index += 1
                self.last_victory_time = pygame.time.get_ticks()
                if self.victory_index >= len(self.victory_right_frames):
                    self.victory_index = len(self.victory_right_frames) - 1
        elif self.is_hit:
            current_frame = self.hit_right_frames[self.hit_index] if self.direction == "right" else self.hit_left_frames[self.hit_index]
            if pygame.time.get_ticks() - self.last_hit_time >= self.hit_delay:
                self.hit_index += 1
                self.last_hit_time = pygame.time.get_ticks()
                if self.hit_index >= len(self.hit_right_frames):
                    self.hit_index = 0
                    self.is_hit = False
        elif self.is_jumping:
            current_frame = self.jump_right_frames[self.jump_index] if self.direction == "right" else self.jump_left_frames[self.jump_index]
        elif self.is_fpunching:
            current_frame = self.fpunch_right_frames[self.fpunch_index] if self.direction == "right" else self.fpunch_left_frames[self.fpunch_index]
        elif self.is_punching:
            current_frame = self.punch_right_frames[self.punch_index] if self.direction == "right" else self.punch_left_frames[self.punch_index]
        elif self.is_punchr:
            current_frame = self.punchr_right_frames[self.punchr_index] if self.direction == "right" else self.punchr_left_frames[self.punchr_index]
        elif self.is_legr:
            current_frame = self.legr_right_frames[self.legr_index] if self.direction == "right" else self.legr_left_frames[self.legr_index]
        elif self.is_legforward:
            current_frame = self.legfor_right_frames[self.legfor_index] if self.direction == "right" else self.legfor_left_frames[self.legfor_index]
        elif self.is_blocking_down:
            current_frame = self.block0r if self.direction == "right" else self.block0l
        elif self.is_blocking_shift:
            current_frame = self.block1r if self.direction == "right" else self.block1l
        else:
            current_frame = self.right_frames[self.frame_index] if self.direction == "right" else self.left_frames[self.frame_index]

        # Flip the character if facing left
        if self.direction == "left":
            draw_x = self.char_x - current_frame.get_width() + 150
        else:
            draw_x = self.char_x
            
        screen.blit(current_frame, (draw_x, self.char_y))

class Ryu(Fighter):
    def __init__(self, start_x, start_y, jump_height=150, direction="right"):
        super().__init__(start_x, start_y, jump_height, direction)
        
        # Load walking frames
        right_image_names = ["walk0r", "walk1r", "walk2r","walk3r", "walk4r", "walk5r"]
        self.right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/walk/{name}.png"), (150, 350)) for name in right_image_names]
        
        left_image_names = ["walk0l", "walk1l", "walk2l", "walk3l", "walk4l", "walk5l"]
        self.left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/walk/{name}.png"), (150, 350)) for name in left_image_names]
        
        # Jumping
        jump_right_names = ["jump0r", "jump1r", "jump2r", "jump3r", "jump4r", "jump5r", "jump6r"]
        jump_left_names = ["jump0l", "jump1l", "jump2l", "jump3l", "jump4l", "jump5l", "jump6l"]
        self.jump_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/jump/{name}.png"), (150, 350)) for name in jump_right_names]
        self.jump_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/jump/{name}.png"), (150, 350)) for name in jump_left_names]
        
        # Blocking
        self.block0r = pygame.transform.scale(pygame.image.load("ryu/block/block0r.png"), (150, 350))
        self.block0l = pygame.transform.scale(pygame.image.load("ryu/block/block0l.png"), (150, 350))
        self.block1r = pygame.transform.scale(pygame.image.load("ryu/block/block1r.png"), (150, 350))
        self.block1l = pygame.transform.scale(pygame.image.load("ryu/block/block1l.png"), (150, 350))
        
        # Punching
        punch_right_names = ["punch0r", "punch1r", "punch2r", "punch3r", "punch4r"]
        punch_left_names = ["punch0l", "punch1l", "punch2l", "punch3l", "punch4l"]
        self.punch_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/punch/{name}.png"), (150, 350)) for name in punch_right_names]
        self.punch_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/punch/{name}.png"), (150, 350)) for name in punch_left_names]
        
        # Strong punch
        fpunch_right_names = ["fpunch0r", "fpunch1r", "fpunch2r"]
        fpunch_left_names = ["fpunch0l", "fpunch1l", "fpunch2l"]
        self.fpunch_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/fpunch/{name}.png"), (150, 350)) for name in fpunch_right_names]
        self.fpunch_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/fpunch/{name}.png"), (150, 350)) for name in fpunch_left_names]
        
        # Side punch
        punchr_right_names = ["punchr0r", "punchr1r", "punchr2r"]
        punchr_left_names = ["punchr0l", "punchr1l", "punchr2l"]
        self.punchr_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/punchr/{name}.png"), (150, 350)) for name in punchr_right_names]
        self.punchr_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/punchr/{name}.png"), (150, 350)) for name in punchr_left_names]
        
        # Side kick
        legr_right_names = ["legr0r", "legr1r", "legr2r"]
        legr_left_names = ["legr0l", "legr1l", "legr2l"]
        self.legr_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/legr/{name}.png"), (150, 350)) for name in legr_right_names]
        self.legr_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/legr/{name}.png"), (150, 350)) for name in legr_left_names]
        
        # Forward kick
        legfor_right_names = ["legfor0r", "legfor1r", "legfor2r"]
        legfor_left_names = ["legfor0l", "legfor1l", "legfor2l"]
        self.legfor_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/legfor/{name}.png"), (150, 350)) for name in legfor_right_names]
        self.legfor_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/legfor/{name}.png"), (150, 350)) for name in legfor_left_names]
        
        # Hit frames
        hit_right_names = ["hit0r", "hit1r","hit2r", "hit3r"]
        hit_left_names = ["hit0l", "hit1l","hit2l", "hit3l"]
        self.hit_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/hit/{name}.png"), (150, 350)) for name in hit_right_names]
        self.hit_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/hit/{name}.png"), (150, 350)) for name in hit_left_names]
        
        # KO frames
        ko_right_names = ["ko0r", "ko1r", "ko2r"]
        ko_left_names = ["ko0l", "ko1l", "ko2l"]
        self.ko_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/k.o/{name}.png"), (150, 350)) for name in ko_right_names]
        self.ko_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/k.o/{name}.png"), (150, 350)) for name in ko_left_names]
        
        # Timeout frames
        timeout_right_names = ["timeoutr"]
        timeout_left_names = ["timeoutl"]
        self.timeout_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/timeout/{name}.png"), (150, 350)) for name in timeout_right_names]
        self.timeout_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/timeout/{name}.png"), (150, 350)) for name in timeout_left_names]
        
        # Victory frames
        victory_right_names = ["victory0r", "victory1r", "victory2r"]
        victory_left_names = ["victory0l", "victory1l", "victory2r"]
        self.victory_right_frames = [pygame.transform.scale(pygame.image.load(f"ryu/victory/{name}.png"), (150, 350)) for name in victory_right_names]
        self.victory_left_frames = [pygame.transform.scale(pygame.image.load(f"ryu/victory/{name}.png"), (150, 350)) for name in victory_left_names]

class ChunLi(Fighter):
    def __init__(self, start_x=100, start_y=300, jump_height=150, direction="right"):
        super().__init__(start_x, start_y, jump_height, direction)
        
        # Load walking frames
        right_image_names = ["walkr", "walk0r", "walk1r", "walk2r","walk3r", "walk4r", "walk5r", "walk6r", "walk7r"]
        self.right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/walk/{name}.png"), (150, 350)) for name in right_image_names]
        
        left_image_names = ["walkl", "walk0l", "walk1l", "walk2l", "walk3l", "walk4l", "walk5l", "walk6l", "walk7l"]
        self.left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/walk/{name}.png"), (150, 350)) for name in left_image_names]
        
        # Jumping
        jump_right_names = ["jump0r", "jump1r", "jump2r", "jump3r"]
        jump_left_names = ["jump0l", "jump1l", "jump2l", "jump3l"]
        self.jump_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/jump/{name}.png"), (150, 350)) for name in jump_right_names]
        self.jump_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/jump/{name}.png"), (150, 350)) for name in jump_left_names]
        
        # Blocking
        self.block0r = pygame.transform.scale(pygame.image.load("chunli/block/block0r.png"), (150, 350))
        self.block0l = pygame.transform.scale(pygame.image.load("chunli/block/block0l.png"), (150, 350))
        self.block1r = pygame.transform.scale(pygame.image.load("chunli/block/block1r.png"), (150, 350))
        self.block1l = pygame.transform.scale(pygame.image.load("chunli/block/block1l.png"), (150, 350))
        
        # Punching
        punch_right_names = ["punch0r", "punch1r", "punch2r"]
        punch_left_names = ["punch0l", "punch1l", "punch2l"]
        self.punch_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/punch/{name}.png"), (150, 350)) for name in punch_right_names]
        self.punch_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/punch/{name}.png"), (150, 350)) for name in punch_left_names]
        
        # Strong punch
        fpunch_right_names = ["fpunch0r", "fpunch1r", "fpunch2r"]
        fpunch_left_names = ["fpunch0l", "fpunch1l", "fpunch2l"]
        self.fpunch_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/fpunch/{name}.png"), (150, 350)) for name in fpunch_right_names]
        self.fpunch_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/fpunch/{name}.png"), (150, 350)) for name in fpunch_left_names]
        
        # Side punch
        punchr_right_names = ["punchr0r", "punchr1r", "punchr2r"]
        punchr_left_names = ["punchr0l", "punchr1l", "punchr2l"]
        self.punchr_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/punchr/{name}.png"), (150, 350)) for name in punchr_right_names]
        self.punchr_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/punchr/{name}.png"), (150, 350)) for name in punchr_left_names]
        
        # Side kick
        legr_right_names = ["legr0r", "legr1r", "legr2r", "legr3r", "legr4r"]
        legr_left_names = ["legr0l", "legr1l", "legr2l", "legr3l","legr4l"]
        self.legr_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/legr/{name}.png"), (150, 350)) for name in legr_right_names]
        self.legr_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/legr/{name}.png"), (150, 350)) for name in legr_left_names]
        
        # Forward kick
        legfor_right_names = ["legfor0r", "legfor1r", "legfor2r", "legfor3r"]
        legfor_left_names = ["legfor0l", "legfor1l", "legfor2l", "legfor3l"]
        self.legfor_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/legfor/{name}.png"), (150, 350)) for name in legfor_right_names]
        self.legfor_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/legfor/{name}.png"), (150, 350)) for name in legfor_left_names]
        
        # Hit frames
        hit_right_names = ["hit0r", "hit1r"]
        hit_left_names = ["hit0l", "hit1l"]
        self.hit_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/hit/{name}.png"), (150, 350)) for name in hit_right_names]
        self.hit_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/hit/{name}.png"), (150, 350)) for name in hit_left_names]
        
        # KO frames
        ko_right_names = ["ko0r", "ko1r", "ko2r"]
        ko_left_names = ["ko0l", "ko1l", "ko2l"]
        self.ko_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/k.o/{name}.png"), (150, 350)) for name in ko_right_names]
        self.ko_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/k.o/{name}.png"), (150, 350)) for name in ko_left_names]
        
        # Timeout frames
        timeout_right_names = ["timeoutr"]
        timeout_left_names = ["timeoutl"]
        self.timeout_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/timeout/{name}.png"), (150, 350)) for name in timeout_right_names]
        self.timeout_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/timeout/{name}.png"), (150, 350)) for name in timeout_left_names]
        
        # Victory frames
        victory_right_names = ["victory0r", "victory1", "victory2"]
        victory_left_names = ["victory0l", "victory1", "victory2"]
        self.victory_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/victory/{name}.png"), (150, 350)) for name in victory_right_names]
        self.victory_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/victory/{name}.png"), (150, 350)) for name in victory_left_names]

class Honda(Fighter):
    def __init__(self, start_x=100, start_y=300, jump_height=150, direction="right"):
        super().__init__(start_x, start_y, jump_height, direction)
        
        # Load walking frames
        right_image_names = [ "walk0r", "walk1r", "walk2r","walk3r"]
        self.right_frames = [pygame.transform.scale(pygame.image.load(f"honda/walk/{name}.png"), (150, 350)) for name in right_image_names]
        
        left_image_names = ["walk0l", "walk1l", "walk2l", "walk3l"]
        self.left_frames = [pygame.transform.scale(pygame.image.load(f"honda/walk/{name}.png"), (150, 350)) for name in left_image_names]
        
        # Jumping
        jump_right_names = ["jump0r", "jump1r", "jump2r", "jump3r"]
        jump_left_names = ["jump0l", "jump1l", "jump2l", "jump3l"]
        self.jump_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/jump/{name}.png"), (150, 350)) for name in jump_right_names]
        self.jump_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/jump/{name}.png"), (150, 350)) for name in jump_left_names]
        
        # Blocking
        self.block0r = pygame.transform.scale(pygame.image.load("honda/block/block0r.png"), (150, 350))
        self.block0l = pygame.transform.scale(pygame.image.load("honda/block/block0l.png"), (150, 350))
        self.block1r = pygame.transform.scale(pygame.image.load("honda/block/block1r.png"), (150, 350))
        self.block1l = pygame.transform.scale(pygame.image.load("honda/block/block1l.png"), (150, 350))
        
        # Punching
        punch_right_names = ["punch0r", "punch1r", "punch2r","punch3r", "punch4r", "punch5r","punch6r"]
        punch_left_names = ["punch0l", "punch1l", "punch2l","punch3l", "punch4l", "punch5l","punch6l"]
        self.punch_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/punch/{name}.png"), (150, 350)) for name in punch_right_names]
        self.punch_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/punch/{name}.png"), (150, 350)) for name in punch_left_names]
        
        # Strong punch
        fpunch_right_names = ["fpunch0r", "fpunch1r", "fpunch2r"]
        fpunch_left_names = ["fpunch0l", "fpunch1l", "fpunch2l"]
        self.fpunch_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/fpunch/{name}.png"), (150, 350)) for name in fpunch_right_names]
        self.fpunch_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/fpunch/{name}.png"), (150, 350)) for name in fpunch_left_names]
        
        # Side punch
        punchr_right_names = ["punchr0r", "punchr1r", "punchr2r"]
        punchr_left_names = ["punchr0l", "punchr1l", "punchr2l"]
        self.punchr_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/punchr/{name}.png"), (150, 350)) for name in punchr_right_names]
        self.punchr_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/punchr/{name}.png"), (150, 350)) for name in punchr_left_names]
        
        # Side kick
        legr_right_names = ["legr0r", "legr1r", "legr2r", "legr3r", "legr4r"]
        legr_left_names = ["legr0l", "legr1l", "legr2l", "legr3l","legr4l"]
        self.legr_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/legr/{name}.png"), (150, 350)) for name in legr_right_names]
        self.legr_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/legr/{name}.png"), (150, 350)) for name in legr_left_names]
        
        # Forward kick
        legfor_right_names = ["legfor0r", "legfor1r", "legfor2r"]
        legfor_left_names = ["legfor0l", "legfor1l", "legfor2l"]
        self.legfor_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/legfor/{name}.png"), (150, 350)) for name in legfor_right_names]
        self.legfor_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/legfor/{name}.png"), (150, 350)) for name in legfor_left_names]
        
        # Hit frames
        hit_right_names = ["hit0r", "hit1r"]
        hit_left_names = ["hit0l", "hit1l"]
        self.hit_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/hit/{name}.png"), (150, 350)) for name in hit_right_names]
        self.hit_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/hit/{name}.png"), (150, 350)) for name in hit_left_names]
        
        # KO frames
        ko_right_names = ["ko0r", "ko1r", "ko2r"]
        ko_left_names = ["ko0l", "ko1l", "ko2l"]
        self.ko_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/k.o/{name}.png"), (150, 350)) for name in ko_right_names]
        self.ko_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/k.o/{name}.png"), (150, 350)) for name in ko_left_names]
        
        # Timeout frames
        timeout_right_names = ["timeoutr"]
        timeout_left_names = ["timeoutl"]
        self.timeout_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/timeout/{name}.png"), (150, 350)) for name in timeout_right_names]
        self.timeout_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/timeout/{name}.png"), (150, 350)) for name in timeout_left_names]
        
        # Victory frames
        victory_right_names = ["victory0r", "victory1r"]
        victory_left_names = ["victory0l", "victory1l"]
        self.victory_right_frames = [pygame.transform.scale(pygame.image.load(f"honda/victory/{name}.png"), (150, 350)) for name in victory_right_names]
        self.victory_left_frames = [pygame.transform.scale(pygame.image.load(f"honda/victory/{name}.png"), (150, 350)) for name in victory_left_names]

class Balrog(Fighter):
    def __init__(self, start_x=100, start_y=300, jump_height=150, direction="right"):
        super().__init__(start_x, start_y, jump_height, direction)
        
        # Load walking frames
        right_image_names = ["walkr", "walk0r", "walk1r", "walk2r","walk3r"]
        self.right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/walk/{name}.png"), (150, 350)) for name in right_image_names]
        
        left_image_names = ["walkl", "walk0l", "walk1l", "walk2l", "walk3l"]
        self.left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/walk/{name}.png"), (150, 350)) for name in left_image_names]
        
        # Jumping
        jump_right_names = ["jump0r", "jump1r", "jump2r", "jump3r", "jump4r"]
        jump_left_names = ["jump0l", "jump1l", "jump2l", "jump3l", "jump4l"]
        self.jump_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/jump/{name}.png"), (150, 350)) for name in jump_right_names]
        self.jump_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/jump/{name}.png"), (150, 350)) for name in jump_left_names]
        
        # Blocking
        self.block0r = pygame.transform.scale(pygame.image.load("balrog/block/block0r.png"), (150, 350))
        self.block0l = pygame.transform.scale(pygame.image.load("balrog/block/block0l.png"), (150, 350))
        self.block1r = pygame.transform.scale(pygame.image.load("balrog/block/block1r.png"), (150, 350))
        self.block1l = pygame.transform.scale(pygame.image.load("balrog/block/block1l.png"), (150, 350))
        
        # Punching
        punch_right_names = ["punch0r", "punch1r", "punch2r", "punch3r", "punch4r"]
        punch_left_names = ["punch0l", "punch1l", "punch2l", "punch3l", "punch4l"]
        self.punch_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/punch/{name}.png"), (150, 350)) for name in punch_right_names]
        self.punch_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/punch/{name}.png"), (150, 350)) for name in punch_left_names]
        
        # Strong punch
        fpunch_right_names = ["fpunch0r", "fpunch1r", "fpunch2r"]
        fpunch_left_names = ["fpunch0l", "fpunch1l", "fpunch2l"]
        self.fpunch_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/fpunch/{name}.png"), (150, 350)) for name in fpunch_right_names]
        self.fpunch_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/fpunch/{name}.png"), (150, 350)) for name in fpunch_left_names]
        
        # Side punch
        punchr_right_names = ["punchr0r", "punchr1r", "punchr2r", "punchr3r", "punchr4r"]
        punchr_left_names = ["punchr0l", "punchr1l", "punchr2l", "punchr3l", "punchr4l"]
        self.punchr_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/punchr/{name}.png"), (150, 350)) for name in punchr_right_names]
        self.punchr_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/punchr/{name}.png"), (150, 350)) for name in punchr_left_names]
        
        # Side kick
        legr_right_names = ["legr0r", "legr1r", "legr2r"]
        legr_left_names = ["legr0l", "legr1l", "legr2l"]
        self.legr_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/legr/{name}.png"), (150, 350)) for name in legr_right_names]
        self.legr_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/legr/{name}.png"), (150, 350)) for name in legr_left_names]
        
        # Forward kick
        legfor_right_names = ["legfor0r", "legfor1r", "legfor2r"]
        legfor_left_names = ["legfor0l", "legfor1l", "legfor2l"]
        self.legfor_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/legfor/{name}.png"), (150, 350)) for name in legfor_right_names]
        self.legfor_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/legfor/{name}.png"), (150, 350)) for name in legfor_left_names]
        
        # Hit frames
        hit_right_names = ["hit0r", "hit1r", "hit2r"]
        hit_left_names = ["hit0l", "hit1l", "hit2l"]
        self.hit_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/hit/{name}.png"), (150, 350)) for name in hit_right_names]
        self.hit_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/hit/{name}.png"), (150, 350)) for name in hit_left_names]
        
        # KO frames
        ko_right_names = ["ko0r", "ko1r", "ko2r"]
        ko_left_names = ["ko0l", "ko1l", "ko2l"]
        self.ko_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/k.o/{name}.png"), (150, 350)) for name in ko_right_names]
        self.ko_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/k.o/{name}.png"), (150, 350)) for name in ko_left_names]
        
        # Timeout frames
        timeout_right_names = ["timeoutr"]
        timeout_left_names = ["timeoutl"]
        self.timeout_right_frames = [pygame.transform.scale(pygame.image.load(f"chunli/timeout/{name}.png"), (150, 350)) for name in timeout_right_names]
        self.timeout_left_frames = [pygame.transform.scale(pygame.image.load(f"chunli/timeout/{name}.png"), (150, 350)) for name in timeout_left_names]
        
        # Victory frames
        victory_right_names = ["victory0", "victory1", "victory2"]
        victory_left_names = ["victory0", "victory1", "victory2"]
        self.victory_right_frames = [pygame.transform.scale(pygame.image.load(f"balrog/victory/{name}.png"), (150, 350)) for name in victory_right_names]
        self.victory_left_frames = [pygame.transform.scale(pygame.image.load(f"balrog/victory/{name}.png"), (150, 350)) for name in victory_left_names]

class Game:
    def __init__(self):
        self.round_time = 90  # 90-second rounds as requested
        self.last_time_update = pygame.time.get_ticks()
        self.player1 = None
        self.player2 = None
        self.game_state = "character_select"
        self.current_opponent = 0
        self.total_opponents = 3
        self.opponents = []
        self.backgrounds = []
        self.victory_count = 0
        self.round_result = None
        self.round_end_time = 0
        self.player_char = None
        
    def start_game(self, player_char):
        # Store selected character
        self.player_char = player_char
        
        # Create random opponents (3 different ones)
        available_chars = [c for c in characters if c["name"] != player_char["name"]]
        self.opponents = random.sample(available_chars, self.total_opponents)
        self.backgrounds = [pygame.image.load(opp["scene"]) for opp in self.opponents]
        
        # Start first round
        self.start_round(player_char, self.opponents[0])
    
    def start_round(self, player1_char, player2_char):
        self.player1 = player1_char["class"](
            start_x=200,
            start_y=player1_char["start_y"],
            jump_height=player1_char["jump_height"],
            direction="right"
        )
        
        self.player2 = player2_char["class"](
            start_x=900,
            start_y=player2_char["start_y"],
            jump_height=player2_char["jump_height"],
            direction="left"
        )
        self.player2.is_cpu = True
        
        self.round_time = 90
        self.last_time_update = pygame.time.get_ticks()
        self.game_state = "fighting"
        self.round_result = None
        
        # Set the appropriate background
        self.current_bg = pygame.image.load(player2_char["scene"])
        self.current_bg = pygame.transform.scale(self.current_bg, (1280, 700))
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        if self.game_state == "fighting":
            # Update round timer
            if current_time - self.last_time_update >= 1000:
                self.round_time -= 1
                self.last_time_update = current_time
                
                if self.round_time <= 0:
                    self.handle_timeout()
            
            # Update players
            keys = pygame.key.get_pressed()
            self.player1.update(keys, current_time, self.player2)
            self.player2.update(None, current_time, self.player1)
            
            # Check for hits
            self.check_hits()
            
            # Check for KO
            if self.player1.health <= 0 or self.player2.health <= 0:
                self.handle_ko()
    
    def check_hits(self):
        # Check player1's attacks against player2
        if (self.player1.is_punching and self.player1.punch_index == 2) or \
           (self.player1.is_fpunching and self.player1.fpunch_index == 2) or \
           (self.player1.is_legforward and self.player1.legfor_index == 2) or \
           (self.player1.is_punchr and self.player1.punchr_index == 2) or \
           (self.player1.is_legr and self.player1.legr_index == 1):
            if self.check_collision(self.player1, self.player2):
                damage = 2 if self.player1.is_punching else 2
                self.player2.take_hit(damage)
        
        # Check player2's attacks against player1
        if (self.player2.is_punching and self.player2.punch_index == 2) or \
           (self.player2.is_fpunching and self.player2.fpunch_index == 1) or \
           (self.player2.is_legforward and self.player2.legfor_index == 1):
            if self.check_collision(self.player2, self.player1):
                damage = 1 if self.player2.is_punching else 1
                self.player1.take_hit(damage)
    
    def check_collision(self, attacker, defender):
        attack_range = 100  # Increased range for better hit detection
        if attacker.direction == "right":
            if (defender.char_x > attacker.char_x and 
                defender.char_x < attacker.char_x + attack_range and
                abs(defender.char_y - attacker.char_y) < 50):
                return True
        else:
            if (defender.char_x < attacker.char_x and 
                defender.char_x > attacker.char_x - attack_range and
                abs(defender.char_y - attacker.char_y) < 50):
                return True
        return False
    
    def handle_ko(self):
         self.game_state = "round_over"
         self.round_end_time = pygame.time.get_ticks()

         if  self.player1.health <= 0:
             self.player2.is_victory = True
             self.player2.victory_index = 0
             self.player2.last_victory_time = pygame.time.get_ticks()
             self.round_result = "lose"
         else:
                self.player1.is_victory = True
                self.player1.victory_index = 0
                self.player1.last_victory_time = pygame.time.get_ticks()
                sounds['victory2'].play()
                self.round_result = "win"
                self.victory_count += 1
        
        # تشغيل صوت النصر فقط عند الفوز النهائي (بعد هزيمة جميع الخصوم)
         #if self.victory_count == self.total_opponents:
            #sounds['victory2'].play()
    
    def handle_timeout(self):
        self.game_state = "round_over"
        self.round_end_time = pygame.time.get_ticks()
    
        self.player1.is_timeout = True
        self.player1.timeout_index = 0
        self.player1.last_timeout_time = pygame.time.get_ticks()
    
        self.player2.is_timeout = True
        self.player2.timeout_index = 0
        self.player2.last_timeout_time = pygame.time.get_ticks()
    
        if  self.player1.health > self.player2.health:
            self.player1.is_victory = True
        self.player1.victory_index = 0
        self.player1.last_victory_time = pygame.time.get_ticks()
        self.round_result = "win"
        self.victory_count += 1
        
        # تشغيل صوت النصر فقط عند الفوز النهائي
        if self.victory_count == self.total_opponents:
            sounds['victory2'].play()
        elif      self.player2.health > self.player1.health:
            self.player2.is_victory = True
            self.player2.victory_index = 0
            self.player2.last_victory_time = pygame.time.get_ticks()
            self.round_result = "lose"
        else:
             self.round_result = "draw"
    
    def next_round(self):
        if self.round_result == "win" and self.victory_count < self.total_opponents:
            self.current_opponent += 1
            # Use stored player character instead of characters[0]
            self.start_round(self.player_char, self.opponents[self.current_opponent])
            return True
        return False
    
    def draw(self, screen):
        screen.blit(self.current_bg, (0, 0))
        
        # Draw timer
        timer_text = timer_font.render(f"Time: {self.round_time}", True, YELLOW)
        screen.blit(timer_text, (580, 20))
        
        # Draw players
        self.player1.draw(screen, self.current_bg)
        self.player2.draw(screen, self.current_bg)
        
        # Draw round result if game is over
        if self.game_state == "round_over":
            if pygame.time.get_ticks() - self.round_end_time > 3000:  # 3 seconds delay
                if self.round_result == "win":
                    if self.victory_count == self.total_opponents:
                        # Player defeated all opponents
                        victory_bg = pygame.image.load("picture/background/imo5.png").convert()
                        screen.blit(victory_bg, (0, 0))
                        ufc_img = pygame.image.load("picture/background/ufc2.png").convert_alpha()
                        screen.blit(ufc_img, (500, 250))
                        big_font = pygame.font.SysFont("arial", 38, bold=True)
                        victory_text = big_font.render("You win", True, YELLOW)
                        screen.blit(victory_text, (530, 450))
                        pygame.display.update()
                        pygame.time.delay(3000)
                    else:
                        # Continue to next opponent
                        next_text = menu_font.render("Press SPACE to continue", True, WHITE)
                        screen.blit(next_text, (450, 600))
                elif self.round_result == "lose":
                    lose_text = big_font.render("YOU LOSE!", True, RED_DARK)
                    screen.blit(lose_text, (450, 300))
                    restart_text = menu_font.render("Press R to restart", True, WHITE)
                    screen.blit(restart_text, (500, 400))
                else:  # draw
                    draw_text = big_font.render("DRAW!", True, WHITE)
                    screen.blit(draw_text, (550, 300))
                    restart_text = menu_font.render("Press R to restart", True, WHITE)
                    screen.blit(restart_text, (500, 400))

# Character list with all attributes
characters = [
    {
        "name": "Ryu", 
        "icon": "picture/icon/r.bmp", 
        "image": "picture/Characters/Ryu.png", 
        "scene": "picture/background/bg2.png",
        "start_x": 100,
        "start_y": 300,
        "jump_height": 150,
        "class": Ryu
    },
    {
        "name": "Chunli", 
        "icon": "picture/icon/c.bmp", 
        "image": "picture/Characters/chunli.png", 
        "scene": "picture/background/bg4.png",
        "start_x": 100,
        "start_y": 280,
        "jump_height": 150,
        "class": ChunLi
    },
    {
        "name": "Honda", 
        "icon": "picture/icon/h.bmp", 
        "image": "picture/Characters/honda.png", 
        "scene": "picture/background/bg0.png",
        "start_x": 100,
        "start_y": 300,
        "jump_height": 150,
        "class": Honda
    },
    {
        "name": "Balrog", 
        "icon": "picture/icon/b.bmp", 
        "image": "picture/Characters/Balrog.png", 
        "scene": "picture/background/bg2.png",
        "start_x": 100,
        "start_y": 300,
        "jump_height": 150,
        "class": Balrog
    }
]

gameplay_levels = ["Easy", "Medium", "Hard"]
sound_levels = [0, 50, 100]
light_levels = [0, 50, 100]

current_gameplay = 0
current_sound = 0
current_light = 0
option_items = ["Game Play", "Sound", "Light"]
option_index = 0

def create_gradient_surface(size):
    width, height = size
    gradient = pygame.Surface((width, height))
    for y in range(height):
        if y < height / 2:
            r = 255
            g = int(165 * (y / (height / 2)))
            b = 0
        else:
            r = 255
            g = 165 + int((255 - 165) * ((y - height / 2) / (height / 2)))
            b = int(255 * ((y - height / 2) / (height / 2)))
        pygame.draw.line(gradient, (r, g, b), (0, y), (width, y))
    return gradient

def adjust_brightness(img, level):
    temp = pygame.Surface(img.get_size()).convert_alpha()
    temp.fill((level, level, level, 0))
    img_copy = img.copy()
    img_copy.blit(temp, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    return img_copy

def show_intro():
    text = "Street Fighter"
    text_surface = big_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(640, 365))
    gradient = create_gradient_surface(text_surface.get_size())
    text_surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_MULT)
    for alpha in range(0, 256, 5):
        screen.fill(BLACK)
        temp = text_surface.copy()
        temp.set_alpha(alpha)
        screen.blit(temp, text_rect)
        pygame.display.flip()
        pygame.time.delay(60)
    start_time = time.time()
    while time.time() - start_time < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def confirm_exit():
    width, height = 680, 200
    rect = pygame.Rect((340, 265, width, height))
    yes_rect = pygame.Rect(370, 390, 100, 50)
    no_rect = pygame.Rect(800, 390, 100, 50)
    while True:
        beige = (101, 67, 33)
        pygame.draw.rect(screen, beige, rect)
        pygame.draw.rect(screen, WHITE, rect, 5)
        msg = menu_font.render("Are you sure you want to go out?", True, WHITE)
        screen.blit(msg, (rect.x + 50, rect.y + 50))
        pygame.draw.rect(screen, (0, 150, 0), yes_rect)
        pygame.draw.rect(screen, (150, 0, 0), no_rect)
        yes_text = menu_font.render("Yes", True, WHITE)
        no_text = menu_font.render("No", True, WHITE)
        screen.blit(yes_text, (yes_rect.x + 10, yes_rect.y - 10))
        screen.blit(no_text, (no_rect.x + 25, no_rect.y - 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif no_rect.collidepoint(event.pos):
                    return

def show_options():
    global current_gameplay, current_sound, current_light, option_index
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    option_index = (option_index + 1) % 3
                elif event.key == pygame.K_UP:
                    option_index = (option_index - 1) % 3
                elif event.key == pygame.K_LEFT:
                    if option_index == 0:
                        current_gameplay = (current_gameplay - 1) % 3
                    elif option_index == 1:
                        current_sound = (current_sound - 1) % 3
                    elif option_index == 2:
                        current_light = (current_light - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    if option_index == 0:
                        current_gameplay = (current_gameplay + 1) % 3
                    elif option_index == 1:
                        current_sound = (current_sound + 1) % 3
                    elif option_index == 2:
                        current_light = (current_light + 1) % 3
                elif event.key == pygame.K_ESCAPE:
                    return
        pygame.mixer.music.set_volume(sound_levels[current_sound] / 100)
        bright_background = adjust_brightness(menu_background, light_levels[current_light])
        screen.blit(bright_background, (0, 0))
        y_positions = [250, 350, 450]
        for i, option in enumerate(option_items):
            title = menu_font.render(option, True, WHITE)
            screen.blit(title, (150, y_positions[i]))
            if i == option_index:
                pygame.draw.polygon(screen, WHITE, [(530, y_positions[i] + 10), (515, y_positions[i] - 10), (515, y_positions[i] + 30)])
        for idx, values in enumerate([gameplay_levels, sound_levels, light_levels]):
            for i, val in enumerate(values):
                color = WHITE if i == [current_gameplay, current_sound, current_light][idx] else (150, 150, 150)
                text = menu_font.render(str(val), True, color)
                screen.blit(text, (550 + i * 150, y_positions[idx]))
        pygame.display.flip()

def show_options1():
    global current_sound, current_light, option_index
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    option_index = (option_index + 1) % 2
                elif event.key == pygame.K_UP:
                    option_index = (option_index - 1) % 2
                elif event.key == pygame.K_LEFT:
                    if option_index == 0:
                        current_sound = (current_sound - 1) % 3
                    elif option_index == 1:
                        current_light = (current_light - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    if option_index == 0:
                        current_sound = (current_sound + 1) % 3
                    elif option_index == 1:
                        current_light = (current_light + 1) % 3
                elif event.key == pygame.K_ESCAPE:
                    return

        pygame.mixer.music.set_volume(sound_levels[current_sound] / 100)
        bright_background = adjust_brightness(menu_background, light_levels[current_light])
        screen.blit(bright_background, (0, 0))

        y_positions = [300, 400]
        for i, option in enumerate(option_items[1:]):
            title = menu_font.render(option, True, WHITE)
            screen.blit(title, (150, y_positions[i]))
            if i == option_index:
                pygame.draw.polygon(screen, WHITE, [(530, y_positions[i] + 10), (515, y_positions[i] - 10), (515, y_positions[i] + 30)])

        for idx, values in enumerate([sound_levels, light_levels]):
            current_value = [current_sound, current_light][idx]
            for i, val in enumerate(values):
                color = WHITE if i == current_value else (150, 150, 150)
                text = menu_font.render(str(val), True, color)
                screen.blit(text, (550 + i * 150, y_positions[idx]))

        pygame.display.flip()

def show_pause_menu():
    pause_items = ["Resume", "Options", "Restart", "Exit", "Quit Game"]
    selected = 0
    while True:
        screen.fill((0, 50, 0))
        for i, item in enumerate(pause_items):
            color = WHITE if i == selected else (100, 255, 100)
            text = menu_font.render(item, True, color)
            screen.blit(text, (500, 200 + i * 70))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(pause_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(pause_items)
                elif event.key == pygame.K_RETURN:
                    return pause_items[selected]
                elif event.key == pygame.K_ESCAPE:
                    return "Resume"

def show_character_select():
    icon_size = 64
    icon_margin = 50
    icons = []
    for i, char in enumerate(characters):
        x = 500 + (i % 2) * (icon_size + icon_margin)
        y = 250 + (i // 2) * (icon_size + icon_margin)
        icon_img = pygame.image.load(char["icon"])
        icons.append({"rect": pygame.Rect(x, y, icon_size, icon_size), "image": icon_img, "data": char})
    
    selected_character = None
    click_count = 0
    
    while True:
        bright_bg = adjust_brightness(game_background, light_levels[current_light])
        screen.blit(bright_bg, (0, 0))
        
        for icon in icons:
            screen.blit(pygame.transform.scale(icon["image"], (icon_size, icon_size)), icon["rect"].topleft)
        
        if selected_character:
            for icon in icons:
                if icon["data"] == selected_character:
                    pygame.draw.rect(screen, BLUE, icon["rect"], 4)
            
            img = pygame.image.load(selected_character["image"])
            img = pygame.transform.scale(img, (200, 300))
            screen.blit(img, (50, 250))
            name_surf = char_font.render(selected_character["name"], True, WHITE)
            name_rect = name_surf.get_rect(center=(150, 220))
            screen.blit(name_surf, name_rect)
            
            if click_count >= 2:
                start_text = menu_font.render("Press SPACE to Start", True, YELLOW)
                screen.blit(start_text, (450, 600))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_SPACE and selected_character and click_count >= 2:
                    game = Game()
                    game.start_game(selected_character)
                    run_game(game)
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for icon in icons:
                    if icon["rect"].collidepoint(event.pos):
                        if selected_character == icon["data"]:
                            click_count += 1
                        else:
                            selected_character = icon["data"]
                            click_count = 1
        
        pygame.display.flip()

def show_loading_screen(duration=3):
    WIDTH, HEIGHT = 1280, 700
    temp_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background = pygame.image.load("picture/background/imo5.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    font = pygame.font.SysFont("arial", 50, bold=True)
    
    start_time = time.time()
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        temp_screen.blit(background, (0, 0))
        loading_text = font.render("LOADING...", True, (255, 255, 255))
        temp_screen.blit(loading_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
        pygame.display.flip()
        pygame.time.delay(30)

def run_game(game):
    clock = pygame.time.Clock()
    running = True
    
    show_loading_screen(duration=3)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = show_pause_menu()
                    if action == "Resume":
                        continue
                    elif action == "Options":
                        show_options1()
                    elif action == "Restart":
                        return "restart"
                    elif action == "Exit":
                        return "exit"
                    elif action == "Quit Game":
                        pygame.quit()
                        sys.exit()
                elif game.game_state == "round_over":
                    if event.key == pygame.K_SPACE and game.round_result == "win":
                        if not game.next_round():
                            return "exit"
                    elif event.key == pygame.K_r:
                        return "restart"
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    return "exit"

def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                start_x = 150
                start_y = 240
                spacing = 90
                for i, text in enumerate(menu_buttons):
                    rect = pygame.Rect(start_x, start_y + i * spacing, 300, 60)
                    if rect.collidepoint(mx, my):
                        if text == "Start Game":
                            show_character_select()
                        elif text == "Options":
                            show_options()
                        elif text == "Exit":
                            confirm_exit()
        screen.blit(menu_background, (0, 0))
        start_x = 150
        start_y = 240
        spacing = 90
        for i, text in enumerate(menu_buttons):
            label = menu_font.render(text, True, RED_DARK)
            screen.blit(label, (start_x, start_y + i * spacing))
        pygame.display.flip()

def main():
    show_intro()
    while True:
        show_menu()

if __name__ == "__main__":
    main()