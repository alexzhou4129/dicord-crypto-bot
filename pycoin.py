from pycoingecko import CoinGeckoAPI
import datetime 
import time 
import seaborn as sns 
import matplotlib.pyplot as plt 

cg = CoinGeckoAPI() 

#functions for handling time 
def unix_time(y, m, d, h, s):
    #takes readable format year:month:day:hour:seconds and converts it to unix time, seconds since 1970 
    date_time = datetime.datetime(y, m, d, h, s)
    return time.mktime(date_time.timetuple())

def human_time(unix_time):
    return datetime.datetime.fromtimestamp(unix_time)

start_time = unix_time(2020, 1, 1, 0, 0)
end_time = unix_time(2022, 6, 1, 0, 0)

btc_result = cg.get_coin_market_chart_range_by_id(
    id="bitcoin",
    vs_currency="usd",
    from_timestamp=start_time,
    to_timestamp=end_time
)

btc = {} 
btc['time'] = [x[0] for x in btc_result['prices']]
btc['price'] = [x[1] for x in btc_result['prices']]

sns.set(rc={'figure.figsize':(13,9)})
sns.set_theme(style="darkgrid")

sns.lineplot(
    x = "time", 
    y = "price", 
    data = btc 
)

plt.savefig("figure.png")
plt.show() 


print(btc['price'])
