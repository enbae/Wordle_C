#include "wordle_lib.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

bool score_guess(char *secret, char *guess, char *result) {
	int secret_word[26] = {0};
	int guess_word[26] = {0};
	bool word_match = true;
	//for exact match
	for (int i = 0; i < 5; i++) {
		if (guess[i] == secret[i]) {
			result[i] = 'g';
		} else {
			result[i] = 'x';
			secret_word[secret[i] - 'a'] += 1;
			guess_word[guess[i] - 'a'] += 1;
			word_match = false;
		}
	}
	//for some matches
	for (int i = 0; i < 5; i++) {
		bool guess_secret = (secret_word[guess[i] - 'a'] > 0);
		bool guess_count = (guess_word[guess[i] - 'a'] > 0);
		bool no_match = (result[i] == 'x');
		if (no_match) {
			if (guess_secret) {
				if (guess_count) {
					result[i] = 'y';
					secret_word[guess[i] - 'a'] -= 1;
				}
			}
		}
	}
	result[5] = '\0';
	return word_match;
}

// Returns true if the specified guess is one of the strings in the vocabulary,

bool valid_guess(char *guess, char **vocabulary, size_t num_words) {
	size_t i_guess = 0;
	while (i_guess < num_words) {
		if (strcmp(guess, vocabulary[i_guess]) == 0) {
			return true;
		}
		i_guess++;
	}
	return false;
	
}

// Returns an array of strings (so, char **), where each string contains a word
// from the specified file. The file is assumed to contain 5-letter words, one
// per line.
// Also, this function sets the value pointed at by *num_words to be the number
// of words read.

// This will need to allocate enough memory to hold all of the char* pointers --
// so you will keep track of the size of your char** array and then use realloc
// to make the array larger over time, so that you have enough space for the
// dynamically-growing array of char *.
// Use fopen to open the input file for reading,
// strdup (or strndup) to make copies of each word read from that file, and
// fclose to close the file when you are done reading from it.
// Each element of the array should be a single five-letter word,
// null-terminated.
char **load_vocabulary(char *filename, size_t *num_words) {
	FILE *file = fopen(filename, "r");
	size_t cap_size = 10;
	char **vocabulary = malloc(cap_size * sizeof(char *));
	if (!vocabulary) {
		fclose(file);
		return NULL;
	}
	char word[6];
	*num_words = 0;
	
	while (fscanf(file, "%5s", word) == 1) {
		char *c_word = strdup(word);
		if (*num_words >= cap_size) {
			cap_size *= 2;
			char **store_t = realloc(vocabulary, cap_size * sizeof(char *));
			vocabulary = store_t;
		}
		vocabulary[*num_words] = c_word;
		(*num_words)++;
	}	
	fclose(file);
	return vocabulary;
}

// Free each of the strings in the vocabulary, as well as the pointer vocabulary

void free_vocabulary(char **vocabulary, size_t num_words) {
	size_t idx = 0;
	while (idx < num_words) {
		if (vocabulary[idx] != NULL) {
			free(vocabulary[idx]);
			vocabulary[idx] = NULL;
		}
		idx++;
	}
	free(vocabulary);
	vocabulary = NULL;
}
