import tkinter as tk
import random

class NeonRhythmGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Rhythm Tapper ⚡")
        self.root.geometry("400x600")
        self.root.configure(bg="#0d0d1a")  

  
        self.score = 0
        self.blocks = []
        self.lanes = {
            'a': {"x": 50, "color": "#00ffcc"},   
            's': {"x": 150, "color": "#ff007f"},  
            'd': {"x": 250, "color": "#9400d3"},  
            'f': {"x": 350, "color": "#00ff00"}   
        }

        self.canvas = tk.Canvas(root, width=400, height=500, bg="#0d0d1a", highlightthickness=0)
        self.canvas.pack()

        self.score_label = tk.Label(root, text="SCORE: 0", font=("Courier", 18, "bold"), fg="#ffffff", bg="#0d0d1a")
        self.score_label.pack(pady=10)

        self.draw_ui()
        
        for key in self.lanes.keys():
            self.root.bind(f"<KeyPress-{key}>", self.check_hit)

        self.spawn_block()
        self.update_game()

    def draw_ui(self):
        for lane in self.lanes.values():
            self.canvas.create_line(lane["x"], 0, lane["x"], 430, fill="#1f1f3d", width=2)
        
        self.canvas.create_rectangle(10, 420, 390, 450, outline="#00ffff", width=2, tags="target")
        self.canvas.create_text(200, 435, text="HIT ZONE [A] [S] [D] [F]", fill="#00ffff", font=("Courier", 10, "bold"))

    def spawn_block(self):
        key = random.choice(list(self.lanes.keys()))
        x = self.lanes[key]["x"]
        color = self.lanes[key]["color"]

        block_id = self.canvas.create_rectangle(x-20, 0, x+20, 30, fill=color, outline="#ffffff", width=1)
        
        self.blocks.append({"id": block_id, "key": key, "y": 0})
        
        
        spawn_delay = max(400, 1000 - (self.score * 20))
        self.root.after(spawn_delay, self.spawn_block)

    def update_game(self):
        blocks_to_remove = []

        for block in self.blocks:
            speed = 5 + (self.score // 5)  
            self.canvas.move(block["id"], 0, speed)
            block["y"] += speed

            
            if block["y"] > 460:
                self.canvas.delete(block["id"])
                blocks_to_remove.append(block)
                self.score = max(0, self.score - 2)
                self.score_label.config(text=f"SCORE: {self.score}")

      
        self.blocks = [b for b in self.blocks if b not in blocks_to_remove]
        
       
        self.root.after(20, self.update_game)

    def check_hit(self, event):
        pressed_key = event.char.lower()
        if pressed_key not in self.lanes:
            return

        for block in self.blocks:
            if block["key"] == pressed_key and 410 <= block["y"] <= 460:
                self.canvas.itemconfig(block["id"], fill="#ffffff")
                self.root.after(50, lambda b=block["id"]: self.canvas.delete(b))
                
                self.blocks.remove(block)
                self.score += 10
                self.score_label.config(text=f"SCORE: {self.score}")
                return

if __name__ == "__main__":
    window = tk.Tk()
    game = NeonRhythmGame(window)
    window.mainloop()
