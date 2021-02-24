from bs4 import BeautifulSoup as bs
from threading import Thread
import requests
import re


"""
На выходе хочу получить фото кольца в директории
проекта, название articul[number]

что нужно сделать
1 - заходим на ссылку каждого кольца на странице сайта;

2 - берем нужную информацию: цена, размер, если да,
сохраняю( в названии артикул), нет, ищу дальше;

3 - так делать каждый раз, пока не встречу ошибку 404-страницы кончились

* Попробовать сделать многопоточную программу *
"""


def information_about_ring(ring_url):
    try:
        ring_info = bs(requests.get(ring_url).content, 'html.parser')
        price = ring_info.find('span', attrs={"class": 'price'})['data-detail-price']
        article = ring_info.find('div', class_='product-article').string.strip().split(' ')[1]
        sizes = ring_info.findAll('button', {'class': 'size'})
        sizes = [float(i['data-size']) for i in sizes]
        image_url = ring_info.find('picture', attrs={'itemprop': 'image'})
        template = re.compile('https://+.*sokolov.*jpg')
        image_url = re.findall(template, str(image_url))[0]
        return price, article, sizes, image_url
    except: pass


def download_img(image_url, filename):
    img = requests.get(image_url)
    with open(r'F:\py_Project\SuddenlyNeeded\rings\ '.rstrip() + '{}.png'.format(filename), 'wb') as f:
        f.write(img.content)


def sort_rings(information_about_ring):
    price = float(information_about_ring[0])
    name = str(information_about_ring[1])
    necessary_size = list(filter(lambda x: x == 15.5, information_about_ring[2]))
    url = information_about_ring[3]
    if price < 3000 and necessary_size:
        download_img(url, name)
        print('All good!')


def informations_from_page(page_url):
    page_info = bs(requests.get(page_url).content, 'html.parser')
    rings = page_info.findAll('meta', attrs={'itemprop': 'sku'})
    rings_article = [ring['content'] for ring in rings]
    return rings_article


#def make_all():


start_ring_url = 'https://sokolov.ru/jewelry-catalog/product/94012455/'

if __name__ == '__main__':
    for i in range(1, 52):
        page_url = 'https://sokolov.ru/jewelry-catalog/rings/silver/?page={}'.format(i)
        rings_article = informations_from_page(page_url)
        for ring in rings_article:
            ring_url = 'https://sokolov.ru/jewelry-catalog/product/{}'.format(ring)
            info = information_about_ring(ring_url)
            sort_rings(info)
    print('Finish!')