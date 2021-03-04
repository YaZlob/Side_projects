from urllib.parse import urlsplit

from bs4 import BeautifulSoup as bs
from openpyexcel import Workbook, load_workbook
from selenium import webdriver
url = ""

class Crawler():
    def __init__(self, link):
        self.link = link
        self.site_name = urlsplit(link).netloc
        coin_list = []
        with open("crypt_coin.txt", "r") as f:
            for coin in f.readlines():
                coin_list.append(coin[:-1])
        self.coin_list = list(set(coin_list))

    def find_coin(self):
        soup_Obj = self.JS_rendering().text
        _ = []
        for coin in self.coin_list:
            if coin in soup_Obj:
                _.append(coin)
        return _

    def JS_rendering(self):
        driver = webdriver.Chrome()
        driver.get(self.link)
        html = driver.execute_script("return document.body.innerHTML")
        soup = bs(html, features="html.parser")
        return soup


class Exel_Writing(Workbook):
    def __init__(self):
        super().__init__()
        self.filename = "coin.xlsx"
        try:
            self.wb = load_workbook(filename=self.filename)
            self.current_columns = len(self.wb.active[1]) + 1
        except FileNotFoundError:
            wb = Workbook()
            wb.save(self.filename)
            self.wb = load_workbook(filename=self.filename)
            self.current_columns = 1

    def fill_columns(self, site_name, coin: list):
        sheet = self.wb.active
        # write sitename
        sheet.cell(row=1, column=self.current_columns).value = site_name
        # fill rows
        for i in range(len(coin)):
            current_row = 2 + i
            sheet.cell(row=current_row, column=self.current_columns).value = coin[i]
        self.wb.save(filename=self.filename)


if __name__ == '__main__':
    crawler = Crawler(url)
    site_name = crawler.site_name
    coin_list = crawler.find_coin()
    exel = Exel_Writing()
    exel.fill_columns(site_name, coin_list)
