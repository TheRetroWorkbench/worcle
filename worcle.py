from words import answers, allowed
from os import system, name
from datetime import date

ORDINALS = ["1st", "2nd", "3rd", "4th", "5th"]
RESPONSES = ["       Genius", "    Magnificent", "     Impressive", "      Splendid", "       Great", "       Phew"]

# S: space
S = "       "

GREEN = '\033[32m'
YELLOW = '\033[93m'
RED = '\033[31m'
BOLD = '\033[01m'
RESET = '\033[0m'

INTRO = "                           WORCLE\n" +\
		"                      by Michael Heath\n\n" +\
		"                    A command-line-based\n" +\
		"                  Python implementation of\n" +\
		"                           WORDLE\n" +\
		"                       by Josh Wardle\n" +\
		"------------------------------------------------------------\n" +\
		f"Guess the {BOLD}WORCLE{RESET} in six tries.\n\n" +\
		"Each guess must be a valid five-letter word. Hit the enter\n" +\
		"button to submit.\n\n" +\
		"After each guess, the color of the letters will change to\n" +\
		"show how close your guess was to the word.\n" +\
		"------------------------------------------------------------\n" +\
		f"{BOLD}Examples{RESET}\n\n" +\
		f"{GREEN}W{RESET}EARY\n" +\
		f"The letter {BOLD}W{RESET} is in the word and in the correct spot.\n\n" +\
		f"P{YELLOW}I{RESET}LLS\n" +\
		f"The letter {BOLD}I{RESET} is in the word but in the wrong spot.\n\n" +\
		f"VAG{RED}U{RESET}E\n" +\
		f"The letter {BOLD}U{RESET} is not in the word in any spot.\n" +\
		"------------------------------------------------------------\n" +\
		f"{BOLD}A new WORCLE will be available each day!{RESET}\n\n" +\
		"To play in hard mode, type H then press Enter.\n" +\
		"To play in normal mode, simply press Enter."

# kc: key color
kc = [RESET]*26

def clear():
	if name == "nt":
		system("cls")
	else:
		system("clear")

def keyboard():
	kb = f"       {BOLD}WORCLE{RESET}\n\n" +\
		f"{kc[16]}Q {kc[22]}W {kc[4]}E {kc[17]}R {kc[19]}T {kc[24]}Y {kc[20]}U {kc[8]}I {kc[14]}O {kc[15]}P\n" +\
		f" {kc[0]}A {kc[18]}S {kc[3]}D {kc[5]}F {kc[6]}G {kc[7]}H {kc[9]}J {kc[10]}K {kc[11]}L\n" +\
		f"  {kc[25]}Z {kc[23]}X {kc[2]}C {kc[21]}V {kc[1]}B {kc[13]}N {kc[12]}M{RESET}\n\n"
	return kb

def find_greens(word, guess):
	greens = []
	for w, gu in zip(word, guess):
		greens.append(gu == w)
	return greens

def find_yellows(word, guess, greens):
	yellows = []
	guess_counts = [0]*26
	for w, gr in zip(word, greens):
		if gr:
			guess_counts[ord(w) - 65] += 1
	word_counts = [word.count(chr(l)) for l in range(65, 91)]
	for gu, gr in zip(guess, greens):
		l = ord(gu) - 65
		if gu in word and guess_counts[l] < word_counts[l] and not gr:
			yellows.append(True)
			guess_counts[l] += 1
		else:
			yellows.append(False)
	return yellows

def find_hard_greens(guess, greens, hard_greens):
	for idx, (gu, gr) in enumerate(zip(guess, greens)):
		if gr:
			hard_greens[idx] = gu
	return hard_greens

def find_hard_yellows(word, guess, yellows, hard_greens, hard_yellows):
	new_hard_yellows = []
	for gu, y in zip(guess, yellows):
		if y and new_hard_yellows.count(gu) < word.count(gu):
			new_hard_yellows.append(gu)
	for hg in hard_greens:
		if hard_yellows.count(hg) >= hard_greens.count(hg):
			hard_yellows.remove(hg)
		if new_hard_yellows.count(hg) >= hard_greens.count(hg):
			new_hard_yellows.remove(hg)
	for hy in hard_yellows:
		if hy in new_hard_yellows:
			new_hard_yellows.remove(hy)
	hard_yellows += new_hard_yellows
	return hard_yellows

def color_guess(guess, greens, yellows):
	cg = ""
	for gu, gr, y in zip(guess, greens, yellows):
		if gr:
			cg += GREEN
			kc[ord(gu) - 65] = GREEN
		elif y:
			cg += YELLOW
			if kc[ord(gu) - 65] == RESET:
				kc[ord(gu) - 65] = YELLOW
		else:
			cg += RED
			if kc[ord(gu) - 65] == RESET:
				kc[ord(gu) - 65] = RED
		cg += gu
	cg += RESET
	return cg

def get_guess(guesses, hard, hard_greens = None, hard_yellows = None):
	guess_accepted = False
	while not guess_accepted:
		guess = input(S).upper()
		if len(guess) < 5:
			print("Not enough letters")
		elif len(guess) > 5:
			print("Too many letters")
		elif guess not in answers and guess not in allowed:
			print("That is not an allowed guess")
		elif hard and guesses > 0:
			hard_accepted = True
			for idx, (hg, gu) in enumerate(zip(hard_greens, guess)):
				if hg != None and hg != gu:
					print(f"{ORDINALS[idx]} letter must be {hg}")
					hard_accepted = False
			for hy in sorted(hard_yellows):
				if hy not in guess:
					print(f"{hy} must be in guess")
					hard_accepted = False
			guess_accepted = hard_accepted
		else:
			guess_accepted = True
	return guess

def main():
	word = answers[(date.today() - date(2021, 6, 19)).days % len(answers)]
	guesses = 0
	guessed = False
	guessed_words = []

	clear()
	print(INTRO)
	hard = True if input().upper() == 'H' else False
	if hard:
		hard_greens = [None]*5
		hard_yellows = []

	while guesses < 6 and not guessed:
		clear()
		print(keyboard())
		for w in guessed_words:
			print(f"{S}{w}")
		if hard:
			guess = get_guess(guesses, hard, hard_greens, hard_yellows)
		else:
			guess = get_guess(guesses, hard)
		greens = find_greens(word, guess)
		yellows = find_yellows(word, guess, greens)
		if hard:
			hard_greens = find_hard_greens(guess, greens, hard_greens)
			hard_yellows = find_hard_yellows(word, guess, yellows, hard_greens, hard_yellows)
		guessed_words.append(color_guess(guess, greens, yellows))
		guesses += 1
		if False not in greens:
			guessed = True
			
	clear()
	print(keyboard())
	for w in guessed_words:
		print(f"{S}{w}")
	print()
	if guessed:
		print(RESPONSES[guesses - 1])
	else:
		print(f"{S}{word}")

if __name__ == '__main__':
	main()