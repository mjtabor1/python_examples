import random

LOW = 1
HIGH = 10

def get_guess():
  while True:
    player_guess = input(f"Guess a number between {LOW} and {HIGH}: ")
    if not player_guess.isdigit():
      print("Please enter a valid number.")
    elif int(player_guess) < LOW or int(player_guess) > HIGH:
      print(f"Please enter a number between {LOW} and {HIGH}.")
    else:
      return int(player_guess)

def check_guess(player_guess, computers):
  if player_guess == computers:
    return "Congratulations! You guessed the correct number!"
  elif player_guess < computers:
    return "Your guess is too low. Try again."
  else: 
    return "Your guess is too high. Try again."
    
def play_round():
  computers = random.randint(LOW, HIGH)
  attempts = 0

  while True:
    player_choice = get_guess()
    attempts += 1
    print(check_guess(player_choice, computers))
    
    if player_choice == computers:
      print(f"You guessed the number in {attempts} attempts!")
      break


def main():
  print("Welcome to the guessing game!")

  while True:
    play_round()
    run_again = input("Would you like to play again? (yes/no): ").strip().lower()
    if run_again != "yes":
      print("Thanks for playing!")
      break


if __name__ == "__main__":
    main()