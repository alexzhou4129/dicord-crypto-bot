import requests
# import coingecko_api

#TODO convert all this shit to use coingeckoAPI() 

#getting crypto info stuff 
def getCrypto (crypto):
    URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    r = requests.get(url=URL)
    data = r.json()
    #data is a list of dictionaries 

    for i in range (0, 100):
        coin = data[i]
        #coin is a dictionary, indexed with strings 
        if coin["id"]== crypto:
            # print (crypto, "price is", coin["current_price"])
            return coin 
    return None 

def showCryptoInfo (crypto, channel):
    coin = getCrypto(crypto)
    coinInfo = [coin["id"], coin["current_price"], coin["price_change_percentage_24h"], coin["image"]]
    return coinInfo

def listAllCoin():
    URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    r = requests.get(url=URL)
    data = r.json()
    list = [] 

    for i in range (0,100):
        coin = data[i]
        list.append(coin["id"])
    
    return list

listAllCoin() 