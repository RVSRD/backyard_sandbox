# simple variant of game-rock-scissors game

player_1 = input("Player 1: rock, paper or scissors? ")
player_2 = input("Player 2: rock, paper or scissors? ")

control_list = ['rock', 'paper', 'scissors']

#first, simple check if user's choice is correct
if player_1 in control_list and player_2 in control_list:
    if player_1 == 'rock' and player_2 == 'scissors' or \
            player_1 == 'scissors' and player_2 == 'paper' or \
            player_1 == 'paper' and player_2 == 'rock':
        print("Player 1 WINS!")
    elif player_1 == 'rock' and player_2 == 'rock' or \
            player_1 == 'scissors' and player_2 == 'scissors' or \
            player_1 == 'paper' and player_2 == 'paper':
        print("DRAW!")
    else:
        print("Player 2 WINS!")
else:
    print("\nIncorrect choice entered, sorry")