#!/usr/bin/python
import pygame
from pygame.locals import KEYDOWN, QUIT, K_LEFT, K_RIGHT
import sys
from breakout_sprites import Ball, Brick, Player

# constants
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
BALL_WIDTH, BALL_HEIGHT = 16, 16
BRICK_WIDTH, BRICK_HEIGHT = 64, 16
PLAYER_WIDTH, PLAYER_HEIGHT = 64, 16
PLAYER_SPEED = 10
BALL_SPEED = 2

# game init
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.key.set_repeat(400, 30)
clock = pygame.time.Clock()
score = 0

# groups
all_sprites_group = pygame.sprite.Group()
player_bricks_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()

# add sprites to their group
ball = Ball('ball.png', BALL_SPEED, -BALL_SPEED)
all_sprites_group.add(ball)

player = Player('player.png')
all_sprites_group.add(player)
player_bricks_group.add(player)

for i in xrange(8):
    for j in xrange(8):
        brick = Brick('brick.png', (i+1)*BRICK_WIDTH + 5, (j+3)*BRICK_HEIGHT + 5)
        all_sprites_group.add(brick)
        bricks_group.add(brick)
        player_bricks_group.add(brick)

# game loop
while True:
    # game over
    if ball.rect.y > WINDOW_HEIGHT:
        print 'Game Over'
        pygame.quit()
        sys.exit()

    # move player horizontally
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if player.rect.x > 0:
                    player.rect = player.rect.move(-PLAYER_SPEED, 0)
            elif event.key == K_RIGHT:
                if player.rect.x < WINDOW_WIDTH:
                    player.rect = player.rect.move(PLAYER_SPEED, 0)

    # collision detection (ball bounce against brick & player)
    hits = pygame.sprite.spritecollide(ball, player_bricks_group, False)
    if hits:
        hit_rect = hits[0].rect
        # bounce the ball (according to side collided)
        if hit_rect.left > ball.rect.left or ball.rect.right < hit_rect.right:
            ball.speed_y *= -1
        else:
            ball.speed_x *= -1

        # collision with blocks
        if pygame.sprite.spritecollide(ball, bricks_group, True):
            score += len(hits)
            print "Score: %s" % score

    # render groups
    window.fill((0, 0, 0))
    all_sprites_group.draw(window)
            
    # refresh screen
    ball.update()
    clock.tick(60)
    pygame.display.flip()