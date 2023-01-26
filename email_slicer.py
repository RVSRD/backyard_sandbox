"""
Script asks user for e-mail. It's supposed e-mail is valid one.
After script print greeting message with user registered name took from e-mail and e-mail domain.
If user's domain is in the list of popular ones, script prints approving message.
If it is not, script prints message that user's domain is rare.
"""

# importing regular expressions support
import re

# Making dictionary with two popular domain as a demonstrator of "list"
popular_domains = {'Mail.ru': 'mail.ru', 'Google mail': 'gmail.com'}

user_email = input("Enter your e-mail: ").strip()

# Short regular expression to exctract user's name
user_name = re.findall('(\\w+)', user_email)[0].title()
# Exctracting domain name after "@"
user_domain = user_email.split('@')[-1]

# Check if domain name presents in the list of popular ones and print according message
if user_domain in popular_domains.values():
    print(f'\nHello {user_name}! We are happy with your popular "{user_domain}" email domain!')
else:
    print(f'\nHello {user_name}! How rare your "{user_domain}" email domain is!')

