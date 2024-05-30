import requests
from bs4 import BeautifulSoup
import pandas as pd
from Utils.paths import INVESTING_URL

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'}

urls = [
    INVESTING_URL + "ibm"
]

all = []
for url in urls:
    page = requests.get(url, headers=headers)
    try:
        soup = BeautifulSoup(page.text, 'html.parser')
        company = soup.find('h1', {
            'class': 'mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr'}).text
        price = soup.find('div', {
            'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]'}).text
        change = soup.find('div', {
            'class': 'flex items-center gap-2 text-base/6 font-bold md:text-xl/7 rtl:force-ltr text-negative-main'}).text.split(
            '(')
        stock_information = {company:
                                 {'Price': price,
                                  'Price change': change[0],
                                  'Percent Change': change[1][:-1]}
                             }
        all.append(stock_information)

    except AttributeError:
        print("Change the Element id")
print(all)
