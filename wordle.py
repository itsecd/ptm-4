import random
import logging
from collections import Counter
from rich.prompt import Prompt
from rich import print
from words import words

logger2 = logging.getLogger("wordle")
logger2.setLevel(logging.INFO)
handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
handler2.setFormatter(formatter2)
logger2.addHandler(handler2)


class Wordle:

    def __init__(self):
        self.words: list = words.get('five_letter')
        self.valid_words: list = words.get("valid_word")
        self.chosen_word: str = self._select_word()
        self.max_words = 5
        self.user_guess: str = ""
        logger2.info("Wordle initialized with chosen word: %s",
                     self.chosen_word)

    def get_user_guess(self, remaining: int = None):
        self.user_guess = Prompt.ask(
            f"\n\n[gray]Guess your word ({remaining} guess left) [/gray]").strip()
        if len(self.user_guess) != self.max_words:
            print(
                '\n [red]--- Wait a minute.... That ain\'t a five letter word !!!! --- \n')
            logger2.warning("Invalid guess length: %s", len(self.user_guess))
            self.get_user_guess(remaining=remaining)
        elif self.user_guess not in self.words and self.user_guess not in self.valid_words:
            print('\n [red]--- Oops! Not a valid word!!!! --- \n')
            logger2.warning("Invalid guess: %s", self.user_guess)
            self.get_user_guess(remaining=remaining)

    def _select_word(self):
        random_index = int(
            random.random() * len(self.words)
        )
        chosen_word = self.words[random_index].lower()
        logger2.info("Selected word: %s", chosen_word)
        return chosen_word

    def is_correct_guess(self):
        return self.chosen_word.lower() == self.user_guess.lower()

    def check_word(self):
        user_guess_validated = []

        # Strings converted to lists
        user_guess = list(self.user_guess)
        system_word = list(self.chosen_word)

        # Count of each word in the list
        guess_count = dict(Counter(user_guess))
        correct_count = dict(Counter(system_word))

        # Check for exact match
        for idx, ltr in enumerate(user_guess):
            temp = {'letter': ltr, 'index': idx}
            if ltr == system_word[idx]:
                print(idx, ltr, "matches")
                correct_count[ltr] -= 1
                temp['color'] = 'spring_green2'
                user_guess_validated.append(temp)
            else:
                temp['color'] = 'grey84'
                user_guess_validated.append(temp)

        # Sort the Validated result with index key
        user_guess_validated = sorted(
            user_guess_validated, key=lambda x: x['index'])

        # Check for letter presence in the correct word
        for idx, ltr in enumerate(user_guess):
            if ltr in system_word:
                # Execute only when there is a remaining letter on the correct word
                if correct_count[ltr] != 0:
                    # If it's already found to be an exact match, ignore it else, change it to orange1
                    if user_guess_validated[idx]['color'] != "spring_green2":
                        user_guess_validated[idx]['color'] = 'orange1'
                        # Once Changed reduce the count
                        correct_count[ltr] -= 1
                    # If the count is negative, automatically assume the letter is not present.
                    elif correct_count[ltr] < 1:
                        user_guess_validated[idx]['color'] = 'grey84'

        # Check if the word is correct directly
        if self.is_correct_guess():
            logger2.info("User successfully guessed the word.")
            return True, user_guess_validated
        logger2.info("User's guess did not match the chosen word.")
        return False, user_guess_validated
