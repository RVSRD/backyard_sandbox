# User enters arbitrary name of organization (more than one word) and script prints acronym

user_input = input("Enter the organizatioan full name: ")

for word in user_input.split():
    print(word[:1].capitalize(), end='')

