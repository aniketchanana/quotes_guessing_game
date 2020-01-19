import requests
from bs4 import BeautifulSoup
from random import randint

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
        info.append(dict(quote=q[i].contents[1].get_text(),author=q[i].select("small")[0].get_text(),birth=auth_url))
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

for quote in all_quotes:
    print(quote)
    print("-----------------------")