# Even-or-odd checker from 1 to 1000


def odd_or_even():
    try:
        number = int(input("Enter number from 1 to 1000: "))
        if 1 <= number <= 1000:
            if number % 2 == 0:
                print("It's even number! Again?")
                print("Enter new number from 1 to 1000 or just hit Enter: ")
                odd_or_even()
            else:
                print("It's odd number! Again?")
                print("Enter new number from 1 to 1000 or just hit Enter: ")
                odd_or_even()
        else:
            print("You've entered wrong number, try again!")
            odd_or_even()
    except ValueError:
        print("Empty or wrong input. Goodbye.")


odd_or_even()