"""
Scripts asks for:

- cafe's bill
- fixed percent of tip visitors want to leave
- how much visitors

And prints:

- percent of tip visitors chose
- total tip sum
- total bill, now including tip sum
- how much every of visitors have to pay
"""


our_bill = float(input("Our total bill is: "))
wished_tip = int(input('Enter wished tip: 18, 20 or 25%: '))
visitors = int(input("How much of us: "))


def calc_tip():
    return our_bill / 100 * wished_tip


def total_bill():
    return our_bill + calc_tip()


print(f'\nOur {wished_tip}% tip is {round(calc_tip(), 2)} bean$ '
      f'and total bill is {round(total_bill(), 2)} bean$')
print(f'Every of us must pay {round(total_bill()/visitors, 2)} bean$')

