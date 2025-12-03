## Wordle — C Implementation

This project is a full command-line version of the Wordle game built in C.  
It reads a vocabulary file containing valid 5-letter words, randomly selects a secret answer, and provides feedback for each user guess using the familiar Wordle  logic.

## What It Does
- Validates user guesses (length, characters, allowed words)
- Compares guess letters to the secret word and assigns feedback
- Tracks remaining attempts
- Loads vocabulary from a file into dynamically allocated memory
- Properly frees all memory and passes Valgrind checks with no leaks

## Technical Highlights
- Implemented dynamic memory management for storing word lists  
- Used modular C design, splitting logic across `.c` and `.h` files  
- Employed string processing and letter matching  
- Demonstrated file I/O for reading dictionary files  
- Focused on memory safety, pointer correctness, and clean resource handling

## Running Code
- You can build the test by running **make** and then wordle_lib_test 
$ make
$ ./wordle_lib_test.c 
- For GUI: run python wordle_gui.py in command prompt
