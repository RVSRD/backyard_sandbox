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

our_tip = round(our_bill / 100 * wished_tip, 2)
total_bill = round(our_bill + our_tip, 2)
each_part = round(total_bill / visitors, 2)


print(f'Our {wished_tip}% tip is {our_tip} bean$ and total bill is {total_bill} bean$')
print(f'Every of us must pay {each_part} bean$')
