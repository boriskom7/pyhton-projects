import json
from art import logo

with open("morse-english.json") as file:
    dictionary = json.load(file)

print(logo)

# get user input
user_input = input("Enter statement to translate to Morse code...")

# translate to morse letter by letter
morse = ''
for letter in user_input:
    morse += dictionary[letter.lower()] + ' '

# print morse translation
print(morse)