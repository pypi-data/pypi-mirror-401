import random
from .users import get_players

def play():
    player = get_players(1)[0]
    choices = ["rock","paper","scissor"]

    user = input("Choose rock/paper/scissors: ").lower()
    computer = random.choice(choices)

    print(f"Computer chooses: {computer}")

    if user == computer:
        print("Draw....!")
    
    elif (user,computer) in [("rock","scissors"), ("paper","rock"), ("scissors","paper")]:
        print(f"{player} WINS....... :)")

    else:
        print("Computer wins..... :)")