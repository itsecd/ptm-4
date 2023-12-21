import logging
import random
from time import sleep
import shutil
from simple_colors import *  
from emoji import emojize

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f".log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def intro():
    """
    Function to print the basic introduction about te game
    """
    columns = shutil.get_terminal_size().columns

    print(magenta("SNAKE (🐍) WATER (💧) GUN (🔫)".center(columns))) 

    sleep(1.5)  

    print(cyan("GAME DEVELOPED BY - 👑 AKSHAT DODHIYA 👑".center(columns))) 

    sleep(2)  


intro()  

computer_choice, user_choice = "", "" 
computer_points, user_points, flag, chance = 0, 0, 0, 0  


replay = ""  


def choices():
    """
    This function takes input of user's choice and also takes random input from the computer from list 'options'
    """
    global computer_choice, user_choice 
    options = ["Snake", "Water", "Gun"]  
    computer_choice = random.choice(options)  

    print("Choose:\t\tS for", emojize(":snake:"),
          "\t\tW for", emojize(":droplet:"),
          "\t\tG for", emojize(":pistol:"))  
    user_choice = input().lower()  


def results():
    """
    This function calculates points of both computer and user and
     it also prints whether the user won or lost in that chance and flag value is also handled in this function
    """
    global computer_points, user_points, flag 
    flag = 0  
    if computer_choice == "Snake":
        logger.info("The generated value is Snake")
        if user_choice == "s" or user_choice == "snake":
            print(yellow("AWWW...!!"), emojize(":neutral_face:"), yellow("\nTWO SNAKES HAD BITTEN EACH OTHER :/"))
            logger.info("The user chose snake")

        elif user_choice == "w" or user_choice == "water":
            print(red("NOOO...!!"), emojize(":crying_face:"), red("\nTHE SNAKE DRANK YOUR WATER :("))
            computer_points += 1  
            logger.info("The user chose water")

        elif user_choice == "g" or user_choice == "gun":
            print(green("YEAH...!!"), emojize(":victory_hand:"), green("\nYOU SHOT THE SNAKE BY GUN  :)"))
            user_points += 1  
            logger.info("The user chose gun")

        else:
            print("!!कृपया सही विकल्प चुनें!!") 
            flag = 1  
            logger.warning("The user entered invalid value")

    elif computer_choice == "Water":
        logger.info("The generated value is Water")
        if user_choice == "s" or user_choice == "snake":
            print(green("YEAH...!!"), emojize(":victory_hand:"), green("\nYOUR SNAKE DRANK THE WATER :)"))
            user_points += 1  
            logger.info("The user chose snake")

        elif user_choice == "w" or user_choice == "water":
            print(yellow("AWWW...!!"), emojize(":neutral_face:"), yellow("\nWATER IS INCREASED :/"))
            logger.info("The user chose water")

        elif user_choice == "g" or user_choice == "gun":
            print(red("NOOO...!!"), emojize(":crying_face:"), red("\nYOUR GUN SANK INTO THE WATER :("))
            computer_points += 1  
            logger.info("The user chose gun")

        else:
            print("!!कृपया सही विकल्प चुनें!!") 
            flag = 1  
            logger.warning("The user entered invalid value")

    elif computer_choice == "Gun":
        logger.info("The generated value is Gun")
        if user_choice == "s" or user_choice == "snake":
            print(red("NOOO...!!"), emojize(":crying_face:"), red("\nYOUR SNAKE WAS SHOT BY THE GUN :("))
            computer_points += 1  
            logger.info("The user chose snake")

        elif user_choice == "w" or user_choice == "water":
            print(green("YEAH...!!"), emojize(":victory_hand:"), green("\nYOUR WATER HAD SUNK THE GUN INTO IT :)"))
            user_points += 1  
            logger.info("The user chose water")

        elif user_choice == "g" or user_choice == "gun":
            print(yellow("AWWW...!!"), emojize(":neutral_face:"), yellow("\nTWO GUNS FIRED AT EACH OTHER :/"))
            logger.info("The user chose gun")

        else:
            print("!!कृपया सही विकल्प चुनें!!")  
            flag = 1  
            logger.warning("The user entered invalid value")


def replay_game():
    """
    Function to ask and store the choice of the user for replaying the game
    """
    while 1:  
        print("DO YOU WANT TO PLAY AGAIN ? \nENTER Y FOR YES AND N FOR NO")
        
        global replay  
        replay = input().lower()  

        
        if replay == "y" or replay == "yes":
            logger.info("The user chose to continue the game")
            break 
        elif replay == "n" or replay == "no":
            logger.info("The user chose to finished the game")
            break  
        else:
            print(red("Please enter a valid input only"))
            logger.warning("The user entered invalid value")
            continue  
    logger.info("The game was replayed")


while 1:  
    computer_points, user_points, flag, chance = 0, 0, 0, 0  
    computer_choice, user_choice, replay = "", "", ""  

    try:
        n = int(input("HOW MANY CHANCES DO YOU WANT TO PLAY ?\n"))
        if n < 1:
            print(red('Please enter only natural number', 'bold'))
            logger.warning("The user entered unnatural number")
            continue

    except Exception as e:
        print(red('Please enter only natural number', 'bold'))
        logger.warning("The user entered invalid value")
        continue

    while chance < n:  
        choices()  
        results()  
        if flag == 0:  
            chance += 1
            logger.info("The user entered valid value")
    logger.info("The game has been completed")

    print("\n\t\t\tYOUR SCORE :", user_points)
    print("\n\t\t\tCOMPUTER'S SCORE :", computer_points)

    
    if computer_points > user_points:
        print(red("\n\t\t\tYOU LOST THE GAME !!"), emojize(":loudly_crying_face:"), red("YOU LOST THE GAME"))
        logger.info("The user lost the game")
    elif user_points > computer_points:
        print(green("\n\t\t\tHURRAH !!"), emojize(":smiling_face_with_sunglasses:"), green("YOU WON THE GAME"))
        logger.info("The user won the game")
    else:
        print(yellow("\n\t\t\t!! TIE !!"), emojize(":disappointed_face:"), yellow("!! TRY AGAIN !!"))
        logger.info("")

    replay = ""

    replay_game()

    if replay == "n" or replay == "no":
        print(red("\n\t\t\tSAD TO SEE YOU GO !!", 'bold'), emojize(":disappointed_face:"))
        logger.info("The user has logged out of the game")
        exit()
    if replay == "y" or replay == "yes":
        print(green("\n\t\t\tYO LET'S PLAY AGAIN", 'bold'), emojize(":smiling_face_with_smiling_eyes:"))
        logger.info("The user decided to stay in the game")
        