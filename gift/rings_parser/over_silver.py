from bs4 import BeautifulSoup as bs
import requests
import re, time, random

from scripts.rings_parse import download_img


# template = re.compile('https://+.*sokolov.*jpg')

def info_about_jewellery(url):
    # только для подвесок и
    jewellery_info = bs(requests.get(url).content, 'html.parser')
    find_all_jewellery_price_and_articul = jewellery_info.findAll('button',
                                                                  attrs=
                                                                  {'class': 'favorite js-favorite'})
    template = re.compile('data-product.*">')

    check = re.findall(template, str(find_all_jewellery_price_and_articul))
    articul_template = re.compile('\d{8}')
    price_template = re.compile('[0-9]+\.[0-9]+')

    articul = [re.search(articul_template, i).group() for i in check]
    price = [re.search(price_template, i).group() for i in check]

    return list(zip(articul, price))


def sort_jewellery(jewellery_list: list):
    necessary = [(int(item[0])) for item in jewellery_list
                 if float(item[1]) < 2500. and float(item[1]) > 1200]
    return necessary


def img_url(article):
    base = 'https://sokolov.ru/jewelry-catalog/product/{}'.format(article)
    inf = bs(requests.get(url=base).content, 'html.parser')
    template = re.compile('https://+.*sokolov.*jpg')
    img = inf.find('img', attrs={'itemprop': 'contentUrl'})
    img = re.search(template,str(img)).group()
    return str(img)


def main_loop(url):
    for i in range(1, 92):
        url += str(i)
        info = sort_jewellery(info_about_jewellery(url))
        for item in info:
                # перехожу на украшение, забираю картинку
            print('All Good')
            download_img(img_url(item), str(item))
            time.sleep(0.5)



main_loop('https://sokolov.ru/jewelry-catalog/pendants/silver/?page=')
""" 
inf = bs(requests.get(url='https://sokolov.ru/jewelry-catalog/product/83030023/').content, 'html.parser')
img = inf.find('img', attrs={'itemprop': 'contentUrl'})
print(img)
"""