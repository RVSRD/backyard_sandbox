"""
Guess the number game. User enters number between 1 and 50. If entered number is less or bigger
then this predefined range, script prints warning message and restarts.
If user missed the predefined number, script prints was user's number too big or too small and
then offers to continue or to exit.
Also script counts all attempts user made and shows counter on exit with no reference
to result of guessing.
"""

predefined_number = 42

# More fancy variant
# import random
# predefined_number = random.randint(1, 50)

attempts = 0


def num_guess_game():
    global attempts
    attempts += 1
    user_guessed = int(input("Enter number from 0 to 50: "))
    if user_guessed in range(1, 51):
        if user_guessed == predefined_number:
            print("Congrats! You WON!")
            print(f"You've tried for {attempts} times!")
        else:
            if user_guessed > predefined_number:
                print(f"Your number {user_guessed} is too big!")
            elif user_guessed < predefined_number:
                print(f"Your number {user_guessed} is too small!")
            user_choice = input("Would you like to take one more attempt? Y/N? ").title()
            if user_choice == 'Y':
                num_guess_game()
            else:
                print("So goodbye!")
                print(f"You've tried for {attempts} times!")
                exit()
    else:
        print("Your number is out of range! Try again!")
        num_guess_game()


num_guess_game()
