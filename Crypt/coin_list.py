from bs4 import BeautifulSoup as bs
# from "https://www.okex.com/markets/coin-list"

with open("parse.html") as f:
    soup = bs(f)

crypt_names = soup.find_all("div",{"class":"token-names"})
sep = "\n"

with open("crypt_coin.txt","w") as file:
    for coin in crypt_names:
        names = coin.find_all("div")
        full_name,short_name = names
        full_name = full_name.string
        short_name = short_name.string
        file.write(full_name+sep)
        file.write(short_name+sep)



