import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep 
from random import choice
from csv import DictWriter


BASE_URL = "http://quotes.toscrape.com"

def get_quote():
    all_quotes = []
    page_url = "/page/1/"
    while page_url:    

        res  = requests.get(f"{BASE_URL}{page_url}")
        print(f"Scrapping {BASE_URL}{page_url} ")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes =  soup.find_all(class_ = "quote")
        for quote in quotes:
            all_quotes.append({
                "text":quote.find(class_ = "text").get_text(), 
                "author":quote.find(class_ = "author").get_text(), 
                "bio-link":quote.find("a")["href"]
            })
        next_btn = soup.find(class_="next")
        page_url = next_btn.find("a")["href"] if next_btn else None
        sleep(2)
    return all_quotes

def write_quotes(quotes):
    # writes quotes to csv files
    with open("quotes.csv", "w") as file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = get_quote()
write_quotes(quotes)