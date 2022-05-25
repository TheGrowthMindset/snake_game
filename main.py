from pdb import line_prefix
import pygame
from pygame.locals import *
import time
import random

SIZE = 7
FOOD = pygame.image.load("resources/apple3.png")

class Apple:
    def __init__(self, parent_screen):
        # self.image = pygame.image.load("resources/apple3.png").convert()
        self.image =pygame.transform.scale(FOOD, (7, 7)).convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit( self.image, (self.x, self.y))
        pygame.display.flip()

    def reset(self):
        self.x = random.randint(0,60) * SIZE
        self.y = random.randint(0,60) * SIZE
        


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
    # loading up our block and giving it a size
        self.block = pygame.image.load("resources/block.png").convert()
        self.direction = "down"

        self.x = [SIZE] * length
        self.y = [SIZE] * length
    
    def increase_length(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)
    
    def move_left(self):
        # self.x -= 10
        # self.draw()
        self.direction = "left"
    def move_right(self):
        # self.x += 10
        # self.draw()
        self.direction = "right"
    def move_up(self):
        # self.y -= 10
        # self.draw()
        self.direction = "up"
    def move_down(self):
        # self.y += 10
        # self.draw()
        self.direction = "down"

    def draw(self):
        self.parent_screen.fill((86,125,70))
    # drawing block 
        for i in range(self.length):
            self.parent_screen.blit( self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(" Classic Snake Game")

        pygame.mixer.init()
        self.play_background_music()
    # setting window / surface
    # setting size of window of game
        self.surface = pygame.display.set_mode( (490, 490) )
    # setting color of background
        # self.surface.fill((225,225,225))
        # initializing Snake
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        # initializing Apple
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collition(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def background_wallpaper(self):
        bg = pygame.image.load("resources/background.png")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.background_wallpaper()
        self.snake.move()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        # Snake colliding apple
        if self.is_collition(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("resources/eat.wav")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.reset()

        # Snake colliding with self
        for i in range(3, self.snake.length):
            if self.is_collition(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/dead.wav")
                pygame.mixer.Sound.play(sound)
                raise "Bit Yourself!"

        # snake colliding with boundry of window
        if not(0 <= self.snake.x[0] <= 490 and 0 <= self.snake.y[0] <= 490):
            sound = pygame.mixer.Sound("resources/dead.wav")
            pygame.mixer.Sound.play(sound)
            raise "Watch where you going!"

    def play_background_music(self):
        pygame.mixer.music.load("resources/background_music.mp3")
        pygame.mixer.music.play()

    def display_score(self):
        font = pygame.font.SysFont( 'calibri', 20)
        score = font.render(f"score:{self.snake.length-1}", True, (225, 225, 225))
        # cordinates to put score
        self.surface.blit(score, (250,10))

    def show_game_over_message(self):
        self.background_wallpaper()
        # self.surface.fill((86,125,70))
        font = pygame.font.SysFont( 'calibri', 20)
        line1 = font.render(f"Game Over! Your score is:{self.snake.length-1}", True, (225, 225, 225))
        self.surface.blit(line1, (50,50))
        line2 = font.render(f"Press Enter to play again! Esc to exit!", True, (225, 225, 225))
        self.surface.blit(line2, (10,70))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def restart_game(self):
        # need to pass snake a length to restart
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


    # LOGIC
    def run(self):
    # while running is true respond according to locals. stop running if event is QUIT/ exited
        running = True
        game_over = False
        while running:
            for event in pygame.event.get() :
                if event.type == KEYDOWN:
                    pass
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.play()
                        game_over = False
                    
                    if not game_over:
                        if event.key == K_LEFT:
                            # block_x -= 10
                            # draw_block()
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            # block_x += 10
                            # draw_block()
                            self.snake.move_right()
                        if event.key == K_UP:
                            # block_y -= 10
                            # draw_block()
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            # block_y += 10
                            # draw_block()
                            self.snake.move_down()

                elif event.type ==  QUIT:
                    running = False
            try:
                if not game_over:
                    self.play()
            except Exception as e:
                self.show_game_over_message()
                game_over = True
                self.restart_game()

            time.sleep(0.1)



if __name__ == "__main__":
    game = Game()
    game.run()
