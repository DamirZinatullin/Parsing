import requests
from bs4 import BeautifulSoup
import csv
import re


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def write_csv(data):
    with open('cmc.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['url'], data['price']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', class_='cmc-table--sort-by__rank').find_all(
        'div', class_='cmc-table__table-wrapper-outer')[2]
    trs = table.find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        try:
            name = tds[1].find('a', class_='cmc-link').text.strip()
        except:
            name = ''
        try:
            url = 'https://coinmarketcap.com' + tds[1].find('a',
                                                            class_='cmc-link').get(
                'href')
        except:
            url = ''
        try:
            price = tds[3].find('a').text.strip()
        except:
            price = ''

        data = {'name': name,
                'url': url,
                'price': price}
        write_csv(data)


def main():
    url = 'https://coinmarketcap.com/'
    # soup = BeautifulSoup(get_html(url), 'lxml')
    # pattern = 'Next'
    # a = soup.find_all('a', class_='wn9odt-0 bzWQIF cmc-link',
    #                   text=re.compile(pattern))
    # for i in a:
    #     print(i)
    while True:
        get_page_data(get_html(url))
        soup = BeautifulSoup(get_html(url), 'lxml')
        try:
            pattern = 'Next'
            url = ('https://coinmarketcap.com' +
                   soup.find('a', class_='wn9odt-0 bzWQIF cmc-link',
                             text=re.compile(pattern)).get('href'))
            print(url)
        except:
            break


if __name__ == '__main__':
    main()
