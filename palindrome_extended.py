# User enters five words in a raw, script checks if every of entered word is palindrome or not.
# If one or more words are palindromes, script prints message with quantity of palindromes and 
# palindromes itself, one by one. Otherwise it prints message that no palindromes found.


user_words = input("Enter five words separated by space: ")

palindrome = []
plndr_qntty = 0

for word in user_words.split():
    if word == word[::-1]:
        palindrome.append(word)
        plndr_qntty += 1

if palindrome:
    print(f'We found {plndr_qntty} palindromes: {", ".join(palindrome)}')
else:
    print('We found no palindromes, sorry')
