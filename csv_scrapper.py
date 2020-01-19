import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictWriter

def scrape(data):
    page_quotes = []
    soup = BeautifulSoup(data,"html.parser")
    q = soup.select(".quote")
    if(len(q) == 0):
        return q
    info = []
    for i in range(0,len(q)):
        auth_url = "http://quotes.toscrape.com" + q[i].select("[href]")[0].attrs["href"]
        info.append(dict(text=q[i].contents[1].get_text(),author=q[i].select("small")[0].get_text(),bio_link=auth_url))
    return info

def start_scrapping():
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
    return all_quotes

def write_quotes(quotes):
    with open("quotes.csv","w") as file:
        headers = ["text","author","bio_link"]
        csv_writer = DictWriter(file,fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = start_scrapping()
write_quotes(quotes)