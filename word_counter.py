# user inputs arbitrary phrase, script counting words


user_mind = []
user_input = input("What are you thinking about? Enter here: ")

for word in user_input.split():
    user_mind.append(word)

print(f"Your minds consist of {len(user_mind)} words!")