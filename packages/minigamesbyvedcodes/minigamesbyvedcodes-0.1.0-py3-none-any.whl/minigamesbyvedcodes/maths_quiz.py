import random
from .users import get_players

def play():
    player = get_players(1)[0]
    score = 0

    print("\n Maths Quiz Started...")

    for i in range(5):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        answer = a + b

        try:
            user_answer = int(input(f"Q{i+1}: {a} + {b} = "))
            if user_answer == answer:
                print(" Correct...")
                score += 1
            else:
                print(f" Wrong... correct answer is {answer}")
        except ValueError:
            print(" Invalid input...")

    print(f"\n {player}, your final score is {score}/5")

    
