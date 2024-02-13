Python
import random

def play_rps():
  user_choice = input("Choose rock (r), paper (p), or scissors (s): ")
  computer_choice = random.choice(['r', 'p', 's'])

  if user_choice == computer_choice:
    print("It's a tie!")
  elif user_choice == 'r' and computer_choice == 's':
    print("You win!")
  elif user_choice == 'p' and computer_choice == 'r':
    print("You win!")
  elif user_choice == 's' and computer_choice == 'p':
    print("You win!")
  else:
    print("You lose!")

play_rps()