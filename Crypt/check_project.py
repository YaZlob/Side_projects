from crawler import Crawler,Exel_Writing

markets = []
with open("markets.txt", "r") as f:
    for site in f.readlines():
        markets.append(site[:-1])

for item in markets:
    crawler = Crawler(item)
    site_name = crawler.site_name
    coin_list = crawler.find_coin()
    exel = Exel_Writing()
    exel.fill_columns(site_name, coin_list)