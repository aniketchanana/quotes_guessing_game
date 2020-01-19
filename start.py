import requests
from bs4 import BeautifulSoup
from random import choice

def get_author_info(author_url):
    auth_html = requests.get(author_url).text
    s = BeautifulSoup(auth_html,"html.parser")
    return f'{s.find(class_="author-born-date").get_text()} {s.find(class_="author-born-location").get_text()}'

def scrape(data):
    page_quotes = []
    soup = BeautifulSoup(html,"html.parser")
    q = soup.select(".quote")
    if(len(q) == 0):
        return q
    info = []
    for i in range(0,len(q)):
        auth_url = "http://quotes.toscrape.com" + q[i].select("[href]")[0].attrs["href"]
        # author_info = get_author_info(auth_url)
        info.append(dict(text=q[i].contents[1].get_text(),author=q[i].select("small")[0].get_text(),bio_link=auth_url))
    return info

url = "http://quotes.toscrape.com/page/"

count = 1

all_quotes = []

while True:
    html = requests.get(url+str(count)+"/").text
    res = scrape(html)
    if(len(res) == 0):
        break
    else:
        all_quotes.extend(res)
    count+=1

quote = choice(all_quotes)
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