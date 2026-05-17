import random

def play():
    options = ["rock", "paper", "scissors"]
    user = input("Choose rock, paper, or scissors: ").lower() 
    comp = random.choice(options)
    
    print(f"Computer chose: {comp}")

    if user == comp:
        print("It's a tie!")
    elif (user == "rock" and comp == "scissors") or \
         (user == "paper" and comp == "rock") or \
         (user == "scissors" and comp == "paper"):
        print("You win! 🏆")
    else:
        print("You lose! 💀")

play()
    
