---
title: The Swap Engage - The Story
description: The story of development of my earliest large project
slug: the_swap_engage_story_en
date: 2025-10-17
image: posts/the_swap_engage/cover.jpg
coverHeight: l1
categories:
    - Programming
    - Russian
tags:
    - Programming
    - Unity
    - Russian
seealso:
     - https://youtu.be/TTxDh-AFe1Y?si=2WTuKmUO55Slflls | Watch on Youtube (ru) | brand-youtube | showInList
     - https://ananasikdev.github.io/TheSwapEngageWeb/ | Visit website | brand-github | showInList
draft: true
---

# The Swap: Engage

## Before I knew

### Dread Forest

It was year 2019

```python
class Obj:  # Player/mob class
    def __init__(self, x, y, width, height, image_file, back_color=[255, 255, 255], colorkey=[255, 255, 255],
                 sight_speed=0, up_speed=0, jump_speed=0, jump_speed_memory=0, up_plank=0, down_plank=0, speed_update=0,
                 img_num=None, matrix_x=0, matrix_y=0, mx=0, my=0):  # color_key=[255,255,255]
        self.x = x  # cords
        self.y = y  # cords
        self.image_file = image_file  # name of image
        self.sight_speed = sight_speed  # speed to go to right/left
        self.up_speed = up_speed  # to move up/down
        self.width = width
        self.height = height
        self.jump_speed = jump_speed  # jump speed
        self.jump_speed_memory = jump_speed_memory  # obj's jump_speed written in memory
        self.up_plank = up_plank  # height of jump
        self.down_plank = down_plank  # the lowest point of obj's y
        self.speed_update = speed_update  # changing of obj speed in process
        self.back_color = back_color  # color uses to fill field near the obj
        self.colorkey = colorkey  # color uses to ignor for moveing obj
        self.img_num = img_num  # uses to fastly changing os skins :D
        self.matrix_x = matrix_x
        self.matrix_y = matrix_y
        self.mx = mx
        self.my = my
        self.image = pygame.image.load(self.image_file).convert()
        self.image.set_colorkey(self.colorkey)
        # pygame.transform.scale(self.image,[self.width, self.height])

    def update(self):  # Flip screen to another page
        pygame.display.flip()

    def draw(self):  # Draw obj on screen
        screen.blit(self.image, [self.x, self.y])

    # ----Refilling functions----
    # for fill _color_ near obj  (Also all there funcs are costructions you may use to eraser field you need)

    def rub_circle(self, x=0, y=0, radius=0,
                   edge=0):  # Use it to refill screen around obj (often uses for circle objects)
        radius = self.width
        pygame.draw.circle(screen, self.back_color,
                           [round(self.x + (self.width // 2)) + x, round(self.y + (self.height // 2)) + y], radius,
                           edge)

    def rub_rect_sight(self, x_up=0, y_up=0, wid_up=0, hei_up=0, edge=0):
        if self.sight_speed == abs(self.sight_speed):
            pygame.draw.rect(screen, self.back_color,
                             [self.x - abs(self.sight_speed) + x_up, self.y, 3 + abs(self.sight_speed) + wid_up,
                              self.height + hei_up], edge)
        elif self.sight_speed != abs(self.sight_speed):
            pygame.draw.rect(screen, self.back_color,
                             [self.x + self.width, self.y, 3 + abs(self.sight_speed), self.height], edge)

    def rub_rect_up(self, x_up=0, y_up=0, wid_up=0, hei_up=0,
                    edge=0):  # You can change size or cords of obj's rubber just for that
        if self.jump_speed != abs(self.jump_speed):
            pygame.draw.rect(screen, self.back_color,
                             [self.x + x_up, self.y - (self.height - y_up), self.width + wid_up, self.height + hei_up],
                             edge)
        elif self.jump_speed == abs(self.jump_speed):
            pygame.draw.rect(screen, self.back_color,
                             [self.x + x_up, self.y + (self.height + hei_up), self.width + wid_up,
                              self.height + hei_up], edge)

    def rub(self, x_up=0, y_up=0, wid_up=0, hei_up=0, edge=0):  # The simpliest constructor of rubber funcs
        pygame.draw.rect(screen, self.back_color,
                         [self.x + x_up, self.y + y_up, self.width + wid_up, self.height + hei_up], edge)

    # ----Moving functions----

    def jump(self):  # quite real jump
        self.y -= self.jump_speed
        self.jump_speed -= self.speed_update

    def simple_jump(self):  # jump without phisics
        pass

    def spontan_move(self, x_move, y_move):  # Move x and y as far as you need
        self.x += x_move
        self.y += y_move

    def bounce(self, ceil=True, floor=True, wall_left=True, wall_right=True, hei_up=0,
               wid_up=0):  # Ceil,floor - True/False (If you need to bounce from ceil/floor), wall_ left/right - True/False (If you need to bounce from walls)
        if ceil:
            if self.y <= 0:
                self.up_speed = -self.up_speed
        if floor:
            if self.y >= screen_height - hei_up:
                self.up_speed = - self.up_speed
        if wall_left:
            if self.x <= 0:
                self.sight_speed = -self.sight_speed
        if wall_right:
            if self.x >= screen_width - wid_up:
                self.sight_speed = -self.sight_speed

    def spawn(self, randomize_x=False, randomize_y=False, x=0, y=0, min_x=0, max_x=0, min_y=0,
              max_y=0):  # To respawn mobs in random/noted places you need
        if randomize_x:
            self.x = random.randint(min_x, max_x)  # Don't forget to note min_ and max_ x to use it)
        else:
            self.x = x
        if randomize_y:
            self.y = random.randint(min_y,
                                    max_y)  # Pleeease, don't forget to note min_ and max_ y to use it!!) I'm not kidding you!
        else:
            self.y = y
```