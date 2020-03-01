import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url, timeout=5)
    r.encoding = 'utf-8'
    if r.ok:
        print(r.status_code)
        return r.text
    print(r.status_code)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='product_center_block')
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
            price = div.find('div', class_='price').text.split('.')[1]
        except:
            price = ''

        data = {'name': name,
                'url': url,
                'text': text,
                'price': price}
        write_csv(data)


def write_csv(data):
    with open('pleer.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['name'],
                         data['url'],
                         data['text'],
                         data['price']])


def main():
    patten = 'https://www.pleer.ru/list_mikrovolnovye-pechi_1-0,2-0,5-0,8-0,6-8_page{}.html'
    for i in range(1, 4):
        url = patten.format(str(i))
        get_page_data(get_html(url))


if __name__ == '__main__':
    main()
