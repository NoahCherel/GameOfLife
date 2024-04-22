import pygame
import numpy as np

class GameOfLife:
    def __init__(self, width, height, cell_size=30):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.grid = np.zeros((self.rows, self.cols), dtype=np.uint8)
        self.running = False  # Flag to indicate whether the simulation is running
        self.viewport = pygame.Rect(0, 0, width, height)  # Initialize viewport to cover the entire grid

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

        # Define colors for cell states
        self.colors = {
            0: (0, 0, 0),  # Dead cells
            1: (255, 255, 255)   # Alive cells
        }

    def draw_grid(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.rows):
            for x in range(self.cols):
                cell_rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if cell_rect.colliderect(self.viewport):
                    color = self.colors[self.grid[y, x]]
                    adjusted_rect = cell_rect.move(-self.viewport.left, -self.viewport.top)
                    pygame.draw.rect(self.screen, color, adjusted_rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), adjusted_rect, 1)  # Add borders

    def count_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (0 <= y + i < self.rows) and (0 <= x + j < self.cols):
                    count += self.grid[y + i, x + j]
        return count

    def update_grid(self):
        new_grid = np.copy(self.grid)
        for y in range(self.rows):
            for x in range(self.cols):
                neighbors = self.count_neighbors(x, y)
                if self.grid[y, x] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y, x] = 0
                else:
                    if neighbors == 3:
                        new_grid[y, x] = 1
        self.grid = new_grid

    def toggle_cell(self, x, y):
        # Adjust coordinates to match the new grid dimensions
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        # Calculate the new cell position in the grid based on relative position and new cell size
        new_cell_x = cell_x * (self.width / (self.cols * self.cell_size))
        new_cell_y = cell_y * (self.height / (self.rows * self.cell_size))
        # Check if the new cell position is within the grid bounds
        if 0 <= new_cell_y < self.rows and 0 <= new_cell_x < self.cols:
            self.grid[int(new_cell_y), int(new_cell_x)] = 1 - self.grid[int(new_cell_y), int(new_cell_x)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.toggle_cell(*event.pos)
                elif event.button in (4, 5):  # Scroll up or down
                    old_rows = self.rows
                    old_cols = self.cols
                    self.cell_size += 5 if event.button == 5 else -5
                    self.cell_size = max(5, self.cell_size)
                    self.rows = self.height // self.cell_size
                    self.cols = self.width // self.cell_size
                      
                    # Resize the grid without clearing its contents
                    new_grid = np.zeros((self.rows, self.cols), dtype=np.uint8)
                    new_grid[:min(old_rows, self.rows), :min(old_cols, self.cols)] = self.grid[:min(old_rows, self.rows), :min(old_cols, self.cols)]
                    self.grid = new_grid

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = not self.running

    def run(self):
        while True:
            self.handle_events()

            if self.running:
                self.update_grid()

            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(10)  # Adjust the speed here

            if not self.running:
                continue

# Example usage:
if __name__ == "__main__":
    game = GameOfLife(900, 600)
    game.run()
