import requests
from bs4 import BeautifulSoup
import csv
from random import choice


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:15]
    proxies = []
    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)

    return choice(proxies)


def get_html(url):
    p = get_proxy()
    proxy = {p['schema']: p['address']}
    r = requests.get(url, proxies=proxy, timeout=5)
    r.encoding = 'utf-8'
    if r.ok:
        print(r.status_code)
        return r.text
    print(r.status_code)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='product_info')
    for div in divs:
        try:
            name = div.find('span', class_='item_name').text
        except:
            name = ''
        try:
            url = 'pleer.ru/' + div.find('a').get('href')
        except:
            url = ''
        try:
            text = div.find('div', class_='product_desc').text.strip()
        except:
            text = ''
        try:
            price = div.find('div', class_='price')
        except:
            price = ''
        print(price)


def write_csv(data):
    with open('pleer.csv', 'a') as f:
        writer = csv.writer(f)
        pass


def main():
    url = 'https://www.pleer.ru/list_mikrovolnovye-pechi.html'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()
