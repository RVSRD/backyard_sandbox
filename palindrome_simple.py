# User enters five words in a raw and script checks if every of entered
# word is palindrome or not.


user_words = input("Enter five words separated by space: ")

for word in user_words.split():
    if word == word[::-1]:
        print(f'{word} is palindrome!')
    else:
        print(f'{word} is not palindrome!')
