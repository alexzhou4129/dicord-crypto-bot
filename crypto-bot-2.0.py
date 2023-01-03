import discord
import requests
import os
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import fetchinfo
from discord import app_commands

class client(discord.Client):
    async def startup(self):
        await self.wait_until_ready() 
        # await tree.sync(guild=discord.Object(id = 958809906323009607))

# client = discord.Client(intents=intents) 
client = commands.Bot(command_prefix = "-", intents=discord.Intents.all() ) #put your own prefix here
# tree = app_commands.CommandTree(client)

#TODO push it all onto glitch.com (download all the dependencies) (opencv is not working)
#TODO add reddit and twitter sentiment (greed/fear)
#TODO daily news with fear greed index and today's crypto headlines 
#TODO add trading charts to crypto 
#TODO add price alerts 
#TODO add feature to set time for alerts 

# @client.command(name= "info")
# async def info (context):
#     print ("here")
#     myEmbed = discord.Embed(title = "this is a title", description="this is a description", color=0x00ff00)
#     myEmbed.add_field(name="title: ", value="this is the title", inline=True)
#     myEmbed.add_field(name="date released: ", value="apr 10", inline=False)
#     myEmbed.set_footer(text="this is a footer")
#     myEmbed.set_author(name="alex zhou")

#     await context.message.channel.send (embed = myEmbed)

# @client.command(name = "list") #list all coins 
# async def coins(context):
#     list = fetchinfo.listAllCoin() 
#     myEmbed = discord.Embed(title = "All coins supported", description=list[0::], color=0x00ff00)
#     await context.message.channel.send (embed = myEmbed)

@client.tree.command(name = "hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"this is a slash command!")


@client.event 
async def on_ready():
  print (f"You have logged in as {client}")

  #called whether there is a message in the chat
  botchat = client.get_channel(962506194457608302)
  await botchat.send("**Coin Sage Online**")

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
        crypto = fetchinfo.getCrypto(message.content[1:])
        myEmbed = discord.Embed(title = "**NAME:**", description=crypto["id"], color=0x00ff00)
        myEmbed.set_thumbnail(url=crypto["image"])
        myEmbed.set_image("figure.png")
        myEmbed.add_field(name="Price:", value=str(crypto["current_price"])+" USDT", inline=False)
        myEmbed.add_field(name="Movement:", value=str(crypto["price_change_percentage_24h"])+"%", inline=False)
        #works with top 100 coins, find price of a coin by using "!" before it 
        await message.channel.send(embed = myEmbed)
        # await message.channel.send(crypto)

    await client.process_commands(message)

    # for i in range (0, 10):
    #     if message.content == 
    # if message.content.startswith ("bitcoin"):
    #     await genchat.send(showCryptoInfo("bitcoin"))

    

# @client.command()
# async def ping(ctx):
#     await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"

# async def kick(ctx, member : discord.Member):
#     try:
#         await member.kick(reason=None)
#         await ctx.send("kicked "+member.mention) #simple kick command to demonstrate how to get and use member mentions
#     except:
#         await ctx.send("bot does not have the kick members permission!")

client.run(os.getenv("DISCORD_BOT_ID"))
