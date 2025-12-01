## Wordle_C
Command-line Wordle implemented in C with dynamic memory and file-based vocabulary

## Wordle in C

This project is a full command-line version of the Wordle game built in C.  
It reads a vocabulary file containing valid 5-letter words, randomly selects a secret answer, and provides feedback for each user guess using the familiar Wordle logic

## What It Does
- Validates user guesses (length, characters, allowed words)
- Compares guess letters to the secret word and assesses accuracy
- Tracks remaining attempts
- Loads vocabulary from a file into dynamically allocated memory
- Properly frees all memory and passes Valgrind checks with no leaks

## Technical Highlights
- Implemented memory management for storing word lists  
- Employed string processing and letter matching 
- Focused on memory safety, pointer correctness, and clean resource handling 
