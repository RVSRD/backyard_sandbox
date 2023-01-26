"""
Function accepts low and high values of integers series and sum the series.

If such conditions are followed:

- low value is less than high, other way warning message arises and function restarts;
-  both (low and high) values are bigger than 0, other way warning message arises and function restarts;
- user entered INTEGERS, other way warning message arises and function restarts
"""


def add_it_up():
    try:
        left_limit = int(input("PLZ, enter low integer: "))
        right_limit = int(input("PLZ, enter high integer: "))
        if left_limit < right_limit:
            if left_limit > 0 and right_limit > 0:
                list_of_integers = [num for num in range(left_limit, right_limit+1)]
                print(sum(list_of_integers))
            else:
                print("Entered integers must be greater than 0, try again!")
                add_it_up()
        else:
            print("Low integer must be less than high, try again!")
            add_it_up()
    except ValueError:
        print("Nope, it must be an integer, try again!")
        add_it_up()


add_it_up()
