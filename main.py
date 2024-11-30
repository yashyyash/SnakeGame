import pygame
import random
import os
from collections import deque

# Initialize pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
FPS = 10
FONT = pygame.font.SysFont(None, 35)

# Directions mapping
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

class SnakeGame:
    def __init__(self):
        self.fullscreen = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game with AI")
        self.clock = pygame.time.Clock()
        self.running = False
        self.reset_game()

    def reset_game(self):
        """Reset the game's state for a new session."""
        self.snake = deque([(5, 5), (4, 5), (3, 5)])
        self.direction = "RIGHT"
        self.food = self.generate_food()
        self.score = 0
        self.high_score = self.load_high_score()
        self.running = True

    def generate_food(self):
        """Generate a new food position not overlapping with the snake."""
        while True:
            x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1)
            y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def move_snake(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.snake[0]
        move_x, move_y = DIRECTIONS[self.direction]
        new_head = (head_x + move_x, head_y + move_y)

        # Check for collisions with walls or itself
        if (
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= SCREEN_WIDTH // CELL_SIZE or
            new_head[1] >= SCREEN_HEIGHT // CELL_SIZE or
            new_head in self.snake
        ):
            return False  # Game over

        self.snake.appendleft(new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()  # Remove tail

        return True

    def draw(self):
        """Draw the game state."""
        self.screen.fill(BLACK)

        # Draw the snake
        for segment in self.snake:
            x, y = segment
            pygame.draw.rect(
                self.screen, GREEN,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

        # Draw the food
        food_x, food_y = self.food
        pygame.draw.rect(
            self.screen, RED,
            (food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

        # Display score and high score
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        high_score_text = FONT.render(f"High Score: {self.high_score}", True, YELLOW)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 50))

        pygame.display.flip()

    def ai_move(self):
        """AI logic for choosing the next move."""
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        # Basic heuristic: move closer to the food
        if food_x > head_x:
            next_move = "RIGHT"
        elif food_x < head_x:
            next_move = "LEFT"
        elif food_y > head_y:
            next_move = "DOWN"
        else:
            next_move = "UP"

        # Check if the move is safe
        move_x, move_y = DIRECTIONS[next_move]
        new_head = (head_x + move_x, head_y + move_y)
        if new_head in self.snake or not (0 <= new_head[0] < SCREEN_WIDTH // CELL_SIZE) or not (0 <= new_head[1] < SCREEN_HEIGHT // CELL_SIZE):
            for direction in DIRECTIONS.keys():
                move_x, move_y = DIRECTIONS[direction]
                new_head = (head_x + move_x, head_y + move_y)
                if new_head not in self.snake and 0 <= new_head[0] < SCREEN_WIDTH // CELL_SIZE and 0 <= new_head[1] < SCREEN_HEIGHT // CELL_SIZE:
                    next_move = direction
                    break

        self.direction = next_move

    def save_high_score(self):
        """Save the high score to a file."""
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def load_high_score(self):
        """Load the high score from a file."""
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        return 0

    def game_over_screen(self):
        """Display the Game Over screen."""
        self.screen.fill(BLACK)
        game_over_text = FONT.render("Game Over!", True, RED)
        score_text = FONT.render(f"Score: {self.score}", True, WHITE)
        play_again_text = FONT.render("Press R to Restart or Q to Quit", True, YELLOW)

        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))
        self.screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, 200))

        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart
                        waiting_for_input = False
                        self.reset_game()
                    elif event.key == pygame.K_q:  # Quit
                        pygame.quit()
                        quit()

    def start_screen(self):
        """Show the start screen."""
        while True:
            self.screen.fill(BLACK)
            title_text = FONT.render("Snake Game with AI", True, GREEN)
            play_text = FONT.render("Press SPACE to Play", True, WHITE)
            quit_text = FONT.render("Press Q to Quit", True, RED)
            fullscreen_text = FONT.render("Press F for Fullscreen Toggle", True, YELLOW)

            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
            self.screen.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, 200))
            self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 250))
            self.screen.blit(fullscreen_text, (SCREEN_WIDTH // 2 - fullscreen_text.get_width() // 2, 300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        """Main game loop."""
        self.start_screen()
        while True:
            self.running = True
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.direction != "DOWN":
                            self.direction = "UP"
                        elif event.key == pygame.K_DOWN and self.direction != "UP":
                            self.direction = "DOWN"
                        elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                            self.direction = "LEFT"
                        elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                            self.direction = "RIGHT"
                        elif event.key == pygame.K_f:
                            self.toggle_fullscreen()

                # AI mode can be enabled here by calling self.ai_move()
                if not self.move_snake():
                    self.running = False  # Exit the inner game loop to show game over

                self.draw()
                self.clock.tick(FPS)

            self.save_high_score()
            self.game_over_screen()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
