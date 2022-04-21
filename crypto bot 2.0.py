from cv2 import MergeExposures
import discord
import requests
import os
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from binance.spot import Spot 
import finnhub

# client = discord.Client() 
client = commands.Bot(command_prefix = '-') #put your own prefix here

finnhub_client = finnhub.Client(api_key="c99npv2ad3iaj0qos6kg")

# print(finnhub_client.crypto_candles('BINANCE:BTCUSDT', 'D', 1590988249, 1591852249))

def getCryptoChart (crypto):

    URL = "https://finnhub.io/api/v1/crypto/candle?symbol=BINANCE:BTCUSDT&resolution=D&from=1572651390&to=1575243390&token=c99npv2ad3iaj0qos6kg"
    r = requests.get(url=URL)
    data = r.json() 
    # print ("data", data)

getCryptoChart("bitcoin")

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


#TODO add commands 
#TODO add charts to crypto 
#TODO add price alerts 
#TODO add feature to set time for alerts 

@client.command(name= "info")
async def info (context):
    print ("here")
    myEmbed = discord.Embed(title = "this is a title", description="this is a description", color=0x00ff00)
    myEmbed.add_field(name="title: ", value="this is the title", inline=True)
    myEmbed.add_field(name="date released: ", value="apr 10", inline=False)
    myEmbed.set_footer(text="this is a footer")
    myEmbed.set_author(name="alex zhou")

    await context.message.channel.send (embed = myEmbed)



@client.event 
async def on_ready():
  print (f"You have logged in as {client}")

  #called whether there is a message in the chat
  genchat = client.get_channel(958809906859892790)
  await genchat.send("**whomst have awaken the ancient one**")

@client.event
async def on_message(message):
    genchat = client.get_channel(958809906859892790)
    if message.author == client.user:
        return
    if message.content.startswith("ya"):
        myEmbed = discord.Embed(title = "this is a title", description="this is a description", color=0x00ff00)
        myEmbed.add_field(name="title: ", value="this is the title", inline=True)
        myEmbed.add_field(name="date released: ", value="apr 10", inline=False)
        myEmbed.set_footer(text="this is a footer")
        myEmbed.set_author(name="alex zhou")

        await message.channel.send(embed=myEmbed)

    #get crypto 
    if message.content.startswith("!"):
        crypto = getCrypto(message.content[1:])
        myEmbed = discord.Embed(title = "**NAME:**", description=crypto["id"], color=0x00ff00)
        myEmbed.set_thumbnail(url=crypto["image"])
        myEmbed.set_image   (url=crypto["image"])
        myEmbed.add_field(name="Price:", value=crypto["current_price"], inline=False)
        myEmbed.add_field(name="Movement:", value=str(crypto["price_change_percentage_24h"])+"%", inline=False)
        #works with top 100 coins, find price of a coin by using "!" before it 
        await message.channel.send(embed = myEmbed)
        await message.channel.send(crypto)

    await client.process_commands(message)

    # for i in range (0, 10):
    #     if message.content == 
    # if message.content.startswith ("bitcoin"):
    #     await genchat.send(showCryptoInfo("bitcoin"))

    

@client.command()
async def ping(ctx):
    await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"

async def kick(ctx, member : discord.Member):
    try:
        await member.kick(reason=None)
        await ctx.send("kicked "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("bot does not have the kick members permission!")

client.run("OTYxNzAwNTQ5NjcyMTc3Njc0.Yk8zbg.gn7_s-DoHNVhqsamVVcJPEIOc64")
