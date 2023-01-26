# simple variant of game-rock-scissors game

player_1 = input("Player 1: rock, paper or scissors? ")
player_2 = input("Player 2: rock, paper or scissors? ")

player_1_wins = [(player_1 == 'rock', player_2 == 'scissors'),
                 (player_1 == 'scissors', player_2 == 'paper'),
                 (player_1 == 'paper', player_2 == 'rock')]

player_2_wins = [(player_1 == 'scissors', player_2 == 'rock'),
                 (player_1 == 'paper', player_2 == 'scissors'),
                 (player_1 == 'rock', player_2 == 'paper')]

if (True, True) in player_1_wins:
    print("Player 1 WINS!")
elif (True, True) in player_2_wins:
    print("Player 2 WINS!")
elif player_1 == player_2:
    print("Draw!")
else:
    print("Incorrect input!")
