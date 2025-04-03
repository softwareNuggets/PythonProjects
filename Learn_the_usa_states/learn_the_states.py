## written by Scott Johnson | @SoftwareNuggets
## Date written: 2/24/2025
## Python: U.S. State Quiz Game
## YouTube : https://youtube.com/c/softwareNuggets
## GitHub  : https://github.com/softwareNuggets/Python_Shorts/tree/main/CreateImageMapCoordinates


import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk, ImageDraw
from usa_states import *
from state_boundaries import state_boundaries
import random


class StateQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("U.S. States Quiz Game")

        # Load the U.S. map image
        try:
            self.original_map_image = Image.open("usa_v1.png")
            self.map_image = self.original_map_image.copy()
        except FileNotFoundError:
            messagebox.showerror("Error", "Map image not found!")
            self.root.quit()
            return
        
        self.map_photo = ImageTk.PhotoImage(self.map_image)

        # Create a canvas to display the map
        self.canvas = tk.Canvas(root, width=self.map_image.width, height=self.map_image.height)
        self.canvas.pack()
        self.map_image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)

        # Create a frame for the buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=12)

        # Create a large font for buttons
        self.button_font = font.Font(size=14, weight='bold')
        
        # Initialize game variables
        self.current_state = None
        self.current_state_index = 0
        self.buttons = []
        self.randomized_list = []
        
        # Add a score display
        self.score = 0
        self.total_questions = 0
        self.score_label = tk.Label(root, text="Score: 0/0", font=self.button_font)
        self.score_label.pack(pady=5)
        
        # Initialize the game
        self.reset_game()
        
        # Add a reset button
        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset_game, font=self.button_font)
        self.reset_button.pack(pady=5)
    
    def randomize_states(self):
        # Create a copy to avoid modifying the original list
        self.randomized_list = usa_states.copy()
        # Shuffle the list in-place
        random.shuffle(self.randomized_list)
        self.number_of_states = len(self.randomized_list)
        
    def reset_game(self):
        # Reset the map image
        self.map_image = self.original_map_image.copy()
        self.map_photo = ImageTk.PhotoImage(self.map_image)
        self.canvas.itemconfig(self.map_image_on_canvas, image=self.map_photo)
        
        # Reset game variables
        self.randomized_list = []
        self.randomize_states()
        self.current_state_index = 0
        self.score = 0
        self.total_questions = 0
        self.update_score_display()
        self.number_of_states = len(self.randomized_list)
        #print(f"self.number_of_states: {self.number_of_states}")
        
        # Clear previous buttons
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        
        # Start the first question
        self.next_question()
    
    def update_score_display(self):
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
    
    def next_question(self):
        # Check if we've gone through all states
        if self.current_state_index == len(self.randomized_list):
            messagebox.showinfo("Game Over", f"Quiz completed! Final score: {self.score}/{self.total_questions}")
            self.reset_game()
            return
            
        # Get the next state
        self.current_state = self.randomized_list[self.current_state_index]
        self.current_state_index += 1
        
        # Highlight the selected state's boundary
        self.highlight_state(self.current_state, "yellow")
        
        # Generate 4 buttons: 3 random states and 1 correct state
        self.generate_buttons()

    def highlight_state(self, state, color):
        """Highlight the boundary of the given state with the specified color."""
        if state in state_boundaries:
            boundary = state_boundaries[state]
            draw = ImageDraw.Draw(self.map_image)
            draw.polygon(boundary, outline="black", fill=color)
            self.map_photo = ImageTk.PhotoImage(self.map_image)
            self.canvas.itemconfig(self.map_image_on_canvas, image=self.map_photo)

    def generate_buttons(self):
        """Generate 4 buttons: 3 random states and 1 correct state."""
        # Clear previous buttons
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()

        # Select 3 random states (excluding the correct state)
        random_states = random.sample([s for s in usa_states if s != self.current_state], 3)
        options = random_states + [self.current_state]
        random.shuffle(options)  # Shuffle the options

        # Create buttons for each option
        for option in options:
            button = tk.Button(
                self.button_frame, 
                text=option, 
                command=lambda opt=option: self.check_answer(opt),
                width=15,
                font=self.button_font,
                padx=5, 
                pady=5
            )
            button.pack(side=tk.LEFT, padx=5)
            self.buttons.append(button)

    def check_answer(self, selected_state):
        """Check if the selected state is correct and update the map accordingly."""
        self.total_questions += 1
        
        if selected_state == self.current_state:
            self.score += 1
            self.highlight_state(self.current_state, "green")
        else:
            self.highlight_state(self.current_state, "pink")
            #messagebox.showinfo("Incorrect", f"Wrong! The correct state is {self.current_state}.")
        
        self.update_score_display()
        
        # Wait a short moment before moving to the next question
        self.root.after(100, self.next_question)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x700")
    app = StateQuizApp(root)
    root.mainloop()
