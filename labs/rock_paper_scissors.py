import random

CHOICES = ["rock", "paper", "scissors"]

WINS_AGAINST = {
  "rock": "scissors",
  "paper": "rock",
  "scissors": "paper"
}

def get_player_choice():
  while True:
    choice = input("Enter your choice (rock, paper, scissors): ").strip().lower()
    if choice in CHOICES:
      return choice
    print("Invalid choice. Please try again.")

def get_computer_choice():
  return random.choice(CHOICES)

def determine_winner(player_choice, computer_choice):
  if player_choice == computer_choice:
    return "tie"
  elif WINS_AGAINST[player_choice] == computer_choice:
    return "player"
  else:
    return "computer"

def play_game():
  print("Welcome to Rock, Paper, Scissors!")

  while True:

    player_choice = get_player_choice()
    computer_choice = get_computer_choice()

    if computer_choice == None:
      print("Computer did not make a choice. Please try again.")
      continue

    winner = determine_winner(player_choice, computer_choice)

    none_value = None

    print(f"You chose {player_choice}, computer chose {computer_choice}. {none_value}")
    print(f"The winner is the {winner}!")

    again = input("Do you want to play again? (y/n): ").strip().lower()
    if again != "y":
      print("Thanks for playing!")
      break

if __name__ == "__main__":
  play_game()