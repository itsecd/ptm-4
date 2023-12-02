import logging
import random
import shutil
from time import sleep

from emoji import emojize
from simple_colors import *


logging.basicConfig(level=logging.INFO)

def intro(): 
    """ 
    Function to print the basic introduction about the game 
    """ 
    columns = shutil.get_terminal_size().columns 
 
    logging.info("SNAKE () WATER () GUN ()".center(columns))  # Printing the name of the game 
 
    sleep(1.5)  # Making program to sleep to print next statement after sometime 
 
    logging.info("GAME DEVELOPED BY -  AKSHAT DODHIYA ".center(columns))  # Printing the name of the developer 
 
    sleep(2)  # Making program to sleep to execute next part of the program after sometime
    logger.info("the beginning of the game: success")

intro()  # Calling the function intro() to introduce the game


computer_choice, user_choice = "", ""  # Declaring variables to store choices
computer_points, user_points, flag, chance = 0, 0, 0, 0  # Variables :
# store points, flag = to repeat loop once again for invalid input,
# chance = use in while loop for calculating the chances of the user
replay = ""  # Declaring empty string to store user's choice for replay


def choices():
    """
    This function takes input of user's choice and also takes random input from the computer from list 'options'
    """
    global computer_choice, user_choice  # Declaring variables as global to use in function
    options = ["Snake", "Water", "Gun"]  # List of options for computer to choose randomly
    computer_choice = random.choice(options)  # function to store random choice from list 'options'

    logging.info("Choose:\t\tS for 🐍\t\tW for 💧\t\tG for 🔫")  # Logging the options for user to select
    user_choice = input().lower()  # Storing input of the user in lower case


def results():
    """
    This function calculates points of both computer and user and
     it also prints whether the user won or lost in that chance and flag value is also handled in this function
    """
    global computer_points, user_points, flag
    flag = 0
    index = 0
    if computer_choice == roles[index]:
        if user_choice == roles[index][index] or user_choice == roles[index]:
            print(yellow("AWWW...!!"), emojize(":neutral_face:"),
                  yellow("\nTWO SNAKES HAD BITTEN EACH OTHER :/"))
            logger.info(
                "the user chose " + f'{roles[index]}'
                + " the computer chose " + f'{roles[index]}')
        elif user_choice == roles[index + 1][index] or user_choice == roles[index + 1]:
            print(red("NOOO...!!"), emojize(":crying_face:"),
                  red("\nTHE SNAKE DRANK YOUR WATER :("))
            logger.info(
                "the user chose " + f'{roles[index + 1]}'
                + " the computer chose " + f'{roles[index]}')
            computer_points += 1
        elif user_choice == roles[index + 2][index] or user_choice == roles[index + 2]:
            print(green("YEAH...!!"), emojize(":victory_hand:"),
                  green("\nYOU SHOT THE SNAKE BY GUN  :)"))
            logger.info(
                "the user chose " + f'{roles[index + 2]}'
                + " the computer chose " + f'{roles[index]}')
            user_points += 1
        else:
            print("!!कृपया सही विकल्प चुनें!!")
            logger.warning("the user entered the selected item incorrectly")
            flag = 1
    elif computer_choice == roles[index + 1]:
        if user_choice == roles[index][index] or user_choice == roles[index]:
            print(green("YEAH...!!"), emojize(":victory_hand:"),
                  green("\nYOUR SNAKE DRANK THE WATER :)"))
            logger.info(
                "the user chose " + f'{roles[index]}'
                + " the computer chose " + f'{roles[index + 1]}')
            user_points += 1
        elif user_choice == roles[index + 1][index] or user_choice == roles[index + 1]:
            print(yellow("AWWW...!!"), emojize(":neutral_face:"),
                  yellow("\nWATER IS INCREASED :/"))
            logger.info(
                "the user chose " + f'{roles[index + 1]}'
                + " the computer chose " + f'{roles[index + 1]}')
        elif user_choice == roles[index + 2][index] or user_choice == roles[index + 2]:
            print(red("NOOO...!!"), emojize(":crying_face:"),
                  red("\nYOUR GUN SANK INTO THE WATER :("))
            logger.info(
                "the user chose " + f'{roles[index + 2]}'
                + " the computer chose " + f'{roles[index + 1]}')
            computer_points += 1
        else:
            print("!!कृपया सही विकल्प चुनें!!")
            logger.warning("the user entered the selected item incorrectly")
            flag = 1
    elif computer_choice == roles[index + 2]:
        if user_choice == roles[index][index] or user_choice == roles[index]:
            print(red("NOOO...!!"), emojize(":crying_face:"),
                  red("\nYOUR SNAKE WAS SHOT BY THE GUN :("))
            logger.info(
                "the user chose " + f'{roles[index]}'
                + " the computer chose " + f'{roles[index + 2]}')
            computer_points += 1
        elif user_choice == roles[index + 1][index] or user_choice == roles[index + 1]:
            print(green("YEAH...!!"), emojize(":victory_hand:"),
                  green("\nYOUR WATER HAD SUNK THE GUN INTO IT :)"))
            logger.info(
                "the user chose " + f'{roles[index + 1]}'
                + " the computer chose " + f'{roles[index + 2]}')
            user_points += 1
        elif user_choice == roles[index + 2][index] or user_choice == roles[index + 2]:
            print(yellow("AWWW...!!"), emojize(":neutral_face:"),
                  yellow("\nTWO GUNS FIRED AT EACH OTHER :/"))
            logger.info(
                "the user chose " + f'{roles[index + 2]}'
                + " the computer chose " + f'{roles[index + 2]}')
        else:
            print("!!कृपया सही विकल्प चुनें!!")
            logger.warning("the user entered the selected item incorrectly")
            flag = 1


def replay_game():
    """
    Function to ask and store the choice of the user for replaying the game
    """
    while 1:  # infinite loop till the user enters a valid choice
        logging.info("DO YOU WANT TO PLAY AGAIN ? \nENTER Y FOR YES AND N FOR NO")
        # Giving choice to the user for replaying the game
        global replay  # Globalising the variable to edit value of main variable
        replay = input().lower()  # Taking input in lower case string

        # if else condition to check whether the user has entered the valid input or not
        if replay == "y" or replay == "yes":
            break  # breaking infinite loop after getting valid input
        elif replay == "n" or replay == "no":
            break  # breaking infinite loop after getting valid input
        else:
            logger.warning(
                f"invalid value has been entered for the repetition of the games")
            print(red("Please enter a valid input only"))
            continue  # executing the loop again due to invalid input given by the user


while 1:  # Infinite loop to play the game as many times as the user wants
    computer_points, user_points, flag, chance = 0, 0, 0, 0  # Initialising values to zero at the beginning of the game
    computer_choice, user_choice, replay = "", "", ""  # Emptying strings at the beginning of the game

    try:
        logging.info(f"User input for number of chances: {n}")
        if n < 1:
            logging.error("Please enter only natural number", "bold")
            continue

    except Exception as e:
        logging.error("Please enter only natural number", "bold")
        continue

    while chance < n:  # Iterating loop 'n' times for playing 'n' number of chances
        choices()  # Calling function to take choice of the user as input
        results()  # Calling function to calculate result of a particular chance
        if flag == 0:  # Incrementing flag's value only if the input given by the user will be valid
            chance += 1

    # Displaying points of both computer and user
    print("\n\t\t\tYOUR SCORE :", user_points)
    print("\n\t\t\tCOMPUTER'S SCORE :", computer_points)         
    
    if computer_points > user_points:
        print(red("\n\t\t\tYOU LOST THE GAME !!"),
                emojize(":loudly_crying_face:"), red("YOU LOST THE GAME"))
        logger.info("output of results: computer won")
    elif user_points > computer_points:
        print(green("\n\t\t\tHURRAH !!"),
                  emojize(":smiling_face_with_sunglasses:"),
                  green("YOU WON THE GAME"))
        logger.info("output of results: user won")
    else:
        print(yellow("\n\t\t\t!! TIE !!"),
                emojize(":disappointed_face:"),
                yellow("!! TRY AGAIN !!"))
        logger.info("output of results: tie")
    replay = ""
    replay_game()
    if replay == "n" or replay == "no":
        print(red("\n\t\t\tSAD TO SEE YOU GO !!", 'bold'),
                emojize(":disappointed_face:"))
        logger.info("the decision to continue the game: the game is over")
        exit()
    if replay == "y" or replay == "yes":
        print(green("\n\t\t\tYO LET'S PLAY AGAIN", 'bold'),
                emojize(":smiling_face_with_smiling_eyes:"))
        logger.info(
            "the decision to continue the game: continuation of the game")