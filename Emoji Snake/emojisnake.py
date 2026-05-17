import tkinter as tk
import random

class NeonEmojiSnake:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Emoji Snake 🔥")
        self.root.geometry("600x600")
        self.root.configure(bg="#3a0ca3")  # Cyberpunk Purple

        self.game_started = False
        self.grid_size = 20
        self.base_delay = 110  
        
        # Snake setup (Starts safely in the center)
        self.snake = [(300, 300), (280, 300), (260, 300)]
        self.direction = "Right"
        self.score = 0
        
        self.food_emojis = ["🍓", "🍌", "🍋", "🍏", "🍊", "🍕", "🍦", "🍩"]
        self.current_food_emoji = random.choice(self.food_emojis)
        self.obstacles = []  
        
        self.canvas = tk.Canvas(root, width=600, height=530, bg="#3a0ca3", highlightthickness=0)
        self.canvas.pack()

        self.score_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), fg="#ffffff", bg="#3a0ca3")
        self.score_label.pack(pady=10)

        # Generate elements safely away from starting position
        self.food_pos = self.get_random_valid_pos()
        self.spawn_obstacle()

        # Render menu screen
        self.show_intro_screen()

        # Controls
        self.root.bind("<space>", self.start_game)
        self.root.bind("<KeyPress-Up>", lambda e: self.change_direction("Up"))
        self.root.bind("<KeyPress-Down>", lambda e: self.change_direction("Down"))
        self.root.bind("<KeyPress-Left>", lambda e: self.change_direction("Left"))
        self.root.bind("<KeyPress-Right>", lambda e: self.change_direction("Right"))

    def show_intro_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(300, 90, text="🐍 NEON EMOJI SNAKE 🐍", font=("Helvetica", 24, "bold"), fill="#00f5d4")
        self.canvas.create_text(300, 130, text="Hardcore Mode", font=("Helvetica", 14, "italic"), fill="#ff007f")
        
        # FIXED: Box adjusted to fit text perfectly
        self.canvas.create_rectangle(60, 180, 540, 420, fill="#240046", outline="#ffffff", width=2)
        
        # FIXED: Narrower text margins so it never leaks out of the borders
        instructions = (
            "🎮 HOW TO PLAY:\n\n"
            "• Use ARROW KEYS to steer your snake.\n"
            "• Eat bright fruits & snacks for +10 pts.\n"
            "• Avoid crashing into walls or your own tail!\n"
            "• WARNING: A hot pink mine drops every time\n"
            "  you eat a piece of food!"
        )
        self.canvas.create_text(80, 200, text=instructions, font=("Helvetica", 12), fill="#ffffff", anchor="nw", justify="left")
        self.canvas.create_text(300, 470, text="🔥 PRESS [SPACEBAR] TO START 🔥", font=("Helvetica", 16, "bold"), fill="#ffffff")

    def start_game(self, event=None):
        if not self.game_started:
            self.game_started = True
            self.score_label.config(text=f"💥 SCORE: 0  |  🔥 OBSTACLES: {len(self.obstacles)}")
            self.update_game()

    def get_random_valid_pos(self):
        while True:
            x = random.randint(1, 28) * self.grid_size
            y = random.randint(1, 25) * self.grid_size
            # FIXED: Do not let items spawn near the middle start zone on frame one
            if (x, y) not in self.snake and (x, y) not in self.obstacles and x != 320:
                return (x, y)

    def spawn_obstacle(self):
        new_obs = self.get_random_valid_pos()
        self.obstacles.append(new_obs)

    def change_direction(self, new_dir):
        if not self.game_started:
            return
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_dir != opposites.get(self.direction):
            self.direction = new_dir

    def update_game(self):
        self.canvas.delete("all")

        head_x, head_y = self.snake[0]
        
        if self.direction == "Up": head_y -= self.grid_size
        elif self.direction == "Down": head_y += self.grid_size
        elif self.direction == "Left": head_x -= self.grid_size
        elif self.direction == "Right": head_x += self.grid_size

        new_head = (head_x, head_y)

        # Border and asset collision validation
        if (head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 530 or 
            new_head in self.snake or new_head in self.obstacles):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Check if eating food
        if new_head == self.food_pos:
            self.score += 10
            self.spawn_obstacle()
            self.score_label.config(text=f"💥 SCORE: {self.score}  |  🔥 OBSTACLES: {len(self.obstacles)}")
            self.current_food_emoji = random.choice(self.food_emojis)
            self.food_pos = self.get_random_valid_pos()
        else:
            self.snake.pop()

        # Render food emoji
        fx, fy = self.food_pos
        self.canvas.create_text(fx + 10, fy + 10, text=self.current_food_emoji, font=("Arial", 16))

        # Render active hot pink obstacles
        for (ox, oy) in self.obstacles:
            self.canvas.create_rectangle(ox + 1, oy + 1, ox + self.grid_size - 1, oy + self.grid_size - 1, fill="#ff007f", outline="#ffffff", width=1)

        # Render custom glowing neon snake body elements
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                self.canvas.create_oval(x, y, x + self.grid_size, y + self.grid_size, fill="#ffffff", outline="")
            else:
                self.canvas.create_oval(x + 2, y + 2, x + self.grid_size - 2, y + self.grid_size - 2, fill="#00f5d4", outline="")

        current_delay = max(40, self.base_delay - (self.score // 5))
        self.root.after(current_delay, self.update_game)

    def game_over(self):
        self.canvas.create_text(300, 230, text="💥 CRASHED! 💥", font=("Helvetica", 32, "bold"), fill="#ff007f")
        self.canvas.create_text(300, 290, text=f"Final Score: {self.score}", font=("Helvetica", 18), fill="#ffffff")

if __name__ == "__main__":
    window = tk.Tk()
    game = NeonEmojiSnake(window)
    window.mainloop()
