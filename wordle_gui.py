#!/usr/bin/env python3
"""
Wordle GUI - A graphical version of the popular word guessing game
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import os

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle")
        self.root.geometry("600x800")
        self.root.resizable(False, False)

        # Game state
        self.secret_word = ""
        self.current_guess = ""
        self.guesses = []
        self.current_row = 0
        self.game_over = False
        self.max_guesses = 6
        self.word_length = 5

        # Letter states for keyboard coloring
        self.letter_states = {}  # letter -> 'correct', 'wrong_pos', 'wrong'

        # Load vocabulary
        self.vocabulary = self.load_vocabulary("vocabulary.txt")

        # Colors
        self.colors = {
            'empty': '#ffffff',
            'wrong': '#787c7e',
            'wrong_pos': '#c9b458',
            'correct': '#6aaa64',
            'border': '#d3d6da',
            'keyboard_default': '#d3d6da',
            'keyboard_wrong': '#787c7e',
            'keyboard_wrong_pos': '#c9b458',
            'keyboard_correct': '#6aaa64'
        }

        self.setup_ui()
        self.new_game()

    def load_vocabulary(self, filename):
        """Load vocabulary from file"""
        vocabulary = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    word = line.strip().lower()
                    if len(word) == 5 and word.isalpha():
                        vocabulary.append(word)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Could not find {filename}")
            return []
        return vocabulary

    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="WORDLE", font=('Arial', 36, 'bold'), bg='white')
        title_label.pack(pady=(0, 20))

        # Game grid (6 rows, 5 columns)
        self.grid_frame = tk.Frame(main_frame, bg='white')
        self.grid_frame.pack(pady=(0, 20))

        self.letter_labels = []
        for row in range(self.max_guesses):
            row_labels = []
            for col in range(self.word_length):
                frame = tk.Frame(self.grid_frame, width=60, height=60, bg='white',
                               highlightbackground=self.colors['border'],
                               highlightthickness=2)
                frame.pack_propagate(False)
                frame.grid(row=row, column=col, padx=2, pady=2)

                label = tk.Label(frame, text="", font=('Arial', 24, 'bold'),
                               bg=self.colors['empty'], fg='black')
                label.pack(fill=tk.BOTH, expand=True)
                row_labels.append(label)
            self.letter_labels.append(row_labels)

        # Input frame
        input_frame = tk.Frame(main_frame, bg='white')
        input_frame.pack(pady=(0, 20))

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var,
                                  font=('Arial', 18), width=10, justify='center')
        self.input_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.input_entry.bind('<Return>', lambda e: self.make_guess())

        self.guess_button = tk.Button(input_frame, text="Guess", font=('Arial', 14),
                                    command=self.make_guess, bg='#4CAF50', fg='white')
        self.guess_button.pack(side=tk.LEFT)

        # Keyboard
        keyboard_frame = tk.Frame(main_frame, bg='white')
        keyboard_frame.pack(pady=(0, 20))

        # Create keyboard rows
        keyboard_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]

        self.keyboard_buttons = {}
        for row_idx, row in enumerate(keyboard_layout):
            row_frame = tk.Frame(keyboard_frame, bg='white')
            row_frame.pack(pady=2)

            for letter in row:
                button = tk.Button(row_frame, text=letter, font=('Arial', 12, 'bold'),
                                 width=4, height=2, bg=self.colors['keyboard_default'],
                                 command=lambda l=letter: self.keyboard_press(l))
                button.pack(side=tk.LEFT, padx=1)
                self.keyboard_buttons[letter] = button

        # New game button
        self.new_game_button = tk.Button(main_frame, text="New Game", font=('Arial', 14),
                                       command=self.new_game, bg='#2196F3', fg='white')
        self.new_game_button.pack(pady=(10, 0))

    def new_game(self):
        """Start a new game"""
        if not self.vocabulary:
            messagebox.showerror("Error", "No vocabulary loaded!")
            return

        self.secret_word = random.choice(self.vocabulary)
        self.current_guess = ""
        self.guesses = []
        self.current_row = 0
        self.game_over = False
        self.letter_states = {}

        # Reset grid
        for row in self.letter_labels:
            for label in row:
                label.config(text="", bg=self.colors['empty'])

        # Reset keyboard colors
        for button in self.keyboard_buttons.values():
            button.config(bg=self.colors['keyboard_default'])

        # Reset input
        self.input_var.set("")
        self.input_entry.focus()

        print(f"Secret word: {self.secret_word}")  # For debugging

    def keyboard_press(self, letter):
        """Handle keyboard button press"""
        if self.game_over:
            return

        if len(self.current_guess) < self.word_length:
            self.current_guess += letter.lower()
            self.input_var.set(self.current_guess.upper())

    def make_guess(self):
        """Process a guess"""
        if self.game_over:
            return

        guess = self.input_var.get().strip().lower()

        if len(guess) != self.word_length:
            messagebox.showwarning("Invalid Guess", f"Please enter a {self.word_length}-letter word")
            return

        if not guess.isalpha():
            messagebox.showwarning("Invalid Guess", "Please enter only letters")
            return

        if guess not in self.vocabulary:
            messagebox.showwarning("Invalid Guess", "Word not in vocabulary")
            return

        # Score the guess
        result = self.score_guess(guess)

        # Update grid display
        self.update_grid_display(guess, result)

        # Update keyboard colors
        self.update_keyboard_colors(guess, result)

        # Add to guesses and increment row
        self.guesses.append(guess)
        self.current_row += 1

        # Check win condition
        if all(r == 'g' for r in result):
            self.game_over = True
            messagebox.showinfo("Congratulations!", f"You won in {len(self.guesses)} guesses!")
            return

        # Check lose condition
        if self.current_row >= self.max_guesses:
            self.game_over = True
            messagebox.showinfo("Game Over", f"The word was: {self.secret_word.upper()}")
            return

        # Clear input for next guess
        self.input_var.set("")
        self.current_guess = ""

    def score_guess(self, guess):
        """Score a guess using Wordle rules"""
        result = ['x'] * self.word_length
        secret_letters = list(self.secret_word)
        guess_letters = list(guess)

        # First pass: mark correct positions
        for i in range(self.word_length):
            if guess_letters[i] == secret_letters[i]:
                result[i] = 'g'
                secret_letters[i] = None  # Mark as used

        # Second pass: mark wrong position letters
        for i in range(self.word_length):
            if result[i] == 'x' and guess_letters[i] in secret_letters:
                result[i] = 'y'
                # Remove one instance of this letter
                secret_letters[secret_letters.index(guess_letters[i])] = None

        return result

    def update_grid_display(self, guess, result):
        """Update the grid display with the guess and colors"""
        for col in range(self.word_length):
            label = self.letter_labels[self.current_row][col]
            label.config(text=guess[col].upper())

            if result[col] == 'g':
                label.config(bg=self.colors['correct'])
            elif result[col] == 'y':
                label.config(bg=self.colors['wrong_pos'])
            else:
                label.config(bg=self.colors['wrong'])

    def update_keyboard_colors(self, guess, result):
        """Update keyboard button colors based on guess results"""
        for i, letter in enumerate(guess):
            letter_upper = letter.upper()

            # Determine the best state for this letter
            if result[i] == 'g':
                new_state = 'correct'
            elif result[i] == 'y':
                new_state = 'wrong_pos'
            else:
                new_state = 'wrong'

            # Only upgrade states, never downgrade
            current_state = self.letter_states.get(letter, 'none')
            if (current_state == 'none' or
                (current_state == 'wrong' and new_state in ['wrong_pos', 'correct']) or
                (current_state == 'wrong_pos' and new_state == 'correct')):
                self.letter_states[letter] = new_state

                # Update button color
                if new_state == 'correct':
                    self.keyboard_buttons[letter_upper].config(bg=self.colors['keyboard_correct'])
                elif new_state == 'wrong_pos':
                    self.keyboard_buttons[letter_upper].config(bg=self.colors['keyboard_wrong_pos'])
                else:
                    self.keyboard_buttons[letter_upper].config(bg=self.colors['keyboard_wrong'])

def main():
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
