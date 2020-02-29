import requests
from bs4 import BeautifulSoup
import csv


def main():
    url = 'https://coinmarketcap.com/'
    get_page_data(get_html(url))


def get_html(url):
    r = requests.get(url)
    return r.text


def normal_price(price: str) -> float:
    clean_str = price.lstrip('$').replace(',', '')
    price = float(clean_str)
    return price


def write_csv(data):
    with open('cmc.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['name'],
                         data['url'],
                         data['price']])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        name = tds[1].find('a', class_='cmc-link').text
        url = 'https://coinmarketcap.com' + tds[1].find('a').get('href')
        price = tds[3].find('a').text.replace(',', '')
        norm_price = normal_price(price)

        data = {'name': name,
                'url': url,
                'price': norm_price}
        write_csv(data)


if __name__ == '__main__':
    main()
