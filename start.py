from random import choice
import requests
from bs4 import BeautifulSoup
from csv import DictReader

def read_quotes(filename):
    with open(filename,"r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def get_author_info(author_url):
    auth_html = requests.get(author_url).text
    s = BeautifulSoup(auth_html,"html.parser")
    return f'{s.find(class_="author-born-date").get_text()} {s.find(class_="author-born-location").get_text()}'

def start_game(scrapped_quotes):
    quote = choice(scrapped_quotes)
    remaining_guesses = 4
    print(quote["text"])
    print(quote["author"])
    guess = ''

    while guess.lower() != quote["author"].lower() :
        if remaining_guesses == 3:
            birth_date = get_author_info(quote["bio_link"])
            print(f"Here's a hint: the author was born on {birth_date}")
        elif remaining_guesses == 2:
            print(f"Here's a hint The author first name start with: {quote['author'][0]}")
        elif remaining_guesses == 1:
            print(f"Here's a hint The author first name start with: {quote['author'].split(' ')[1][0]}")
        elif remaining_guesses == 0:
            print(f"Sorry you ran out of guesses. The answer was {quote['author']}")
            break
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} ")
        remaining_guesses -= 1
    if(remaining_guesses>0):
        print("YOU WIN!!!")
    again = ''
    while again.lower() not in ('y','n','yes','no'):
        again = input("Would you like to play again (y/n)")
        if again.lower() in ('yes','y'):
            print("OK YOU PLAY AGAIN!")
            print("-------------------------------------------------------------------------------------------------------")
            return start_game(scrapped_quotes)
        else:
            print("OK, GOODBYE!")
            return;

scrapped_quotes = read_quotes("quotes.csv")
start_game(scrapped_quotes)
