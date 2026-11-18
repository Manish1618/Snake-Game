#!/usr/bin/env python3
"""Snake Game with Python (pygame).

Author : Ayush Kumar
Roll No: 251151004038
Course : B.Tech CSE, 2nd Year

Snake chasing an apple. Arrows/WASD to move, P to pause, R to restart, Esc to quit."""
import random
import sys

import pygame

CELL = 24
COLS, ROWS = 25, 20
W, H = COLS * CELL, ROWS * CELL + 40  # 40px HUD
BASE_FPS, MAX_FPS = 8, 20

BG = (18, 18, 24)
GRID = (28, 28, 36)
SNAKE_HEAD = (80, 220, 120)
SNAKE_BODY = (40, 160, 90)
APPLE = (230, 60, 60)
LEAF = (60, 180, 60)
TEXT = (230, 230, 230)

DIRS = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
}


class Game:
    def __init__(self):
        self.high = 0
        self.reset()

    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.dir = (1, 0)
        self.queue = []          # buffered turns so fast key combos aren't lost
        self.score = 0
        self.over = False
        self.paused = False
        self.apple = self.spawn_apple()

    def spawn_apple(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in self.snake]
        return random.choice(free) if free else None

    def turn(self, d):
        last = self.queue[-1] if self.queue else self.dir
        if d != last and d != (-last[0], -last[1]) and len(self.queue) < 3:
            self.queue.append(d)

    def step(self):
        if self.over or self.paused:
            return
        if self.queue:
            self.dir = self.queue.pop(0)
        hx, hy = self.snake[0]
        head = (hx + self.dir[0], hy + self.dir[1])

        hit_wall = not (0 <= head[0] < COLS and 0 <= head[1] < ROWS)
        eating = head == self.apple
        body = self.snake if eating else self.snake[:-1]  # tail moves away unless growing
        if hit_wall or head in body:
            self.over = True
            self.high = max(self.high, self.score)
            return

        self.snake.insert(0, head)
        if eating:
            self.score += 1
            self.apple = self.spawn_apple()
            if self.apple is None:  # filled the board
                self.over = True
                self.high = max(self.high, self.score)
        else:
            self.snake.pop()

    def fps(self):
        return min(MAX_FPS, BASE_FPS + self.score // 3)


def draw(screen, font, big, g):
    screen.fill(BG)
    for x in range(COLS):
        for y in range(ROWS):
            if (x + y) % 2:
                pygame.draw.rect(screen, GRID, (x * CELL, y * CELL + 40, CELL, CELL))

    if g.apple:
        ax, ay = g.apple
        c = (ax * CELL + CELL // 2, ay * CELL + 40 + CELL // 2)
        pygame.draw.circle(screen, APPLE, c, CELL // 2 - 2)
        pygame.draw.ellipse(screen, LEAF, (c[0], c[1] - CELL // 2, 8, 5))

    for i, (x, y) in enumerate(g.snake):
        r = pygame.Rect(x * CELL + 1, y * CELL + 41, CELL - 2, CELL - 2)
        pygame.draw.rect(screen, SNAKE_HEAD if i == 0 else SNAKE_BODY, r, border_radius=6)
    # eyes
    hx, hy = g.snake[0]
    dx, dy = g.dir
    cx, cy = hx * CELL + CELL // 2, hy * CELL + 40 + CELL // 2
    for s in (-1, 1):
        ex = cx + dx * 5 + (-dy) * s * 5
        ey = cy + dy * 5 + dx * s * 5
        pygame.draw.circle(screen, (0, 0, 0), (ex, ey), 3)

    pygame.draw.rect(screen, (10, 10, 14), (0, 0, W, 40))
    screen.blit(font.render(f"Score: {g.score}   High: {g.high}", True, TEXT), (10, 10))

    msg = None
    if g.over:
        msg = "GAME OVER  -  R to restart"
    elif g.paused:
        msg = "PAUSED"
    if msg:
        t = big.render(msg, True, TEXT)
        screen.blit(t, t.get_rect(center=(W // 2, H // 2)))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Snake Game - Ayush Kumar")
    font = pygame.font.SysFont("monospace", 20, bold=True)
    big = pygame.font.SysFont("monospace", 28, bold=True)
    clock = pygame.time.Clock()
    g = Game()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif e.key == pygame.K_r and g.over:
                    g.reset()
                elif e.key == pygame.K_p and not g.over:
                    g.paused = not g.paused
                elif e.key in DIRS:
                    g.turn(DIRS[e.key])
        g.step()
        draw(screen, font, big, g)
        clock.tick(g.fps())


if __name__ == "__main__":
    main()
