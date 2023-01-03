from typing import Optional
import os 
import discord
from discord import app_commands
import fetchinfo
import imgur


MY_GUILD = discord.Object(id=958809906323009607)  # replace with your guild id

#TODO add a message command to sync commands 
#TODO add a wake up message (optional)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.

    async def setup_hook(self):
        print ("synced")
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    """
    NOTE this is client.someMethod, not MyClient.someMethod since MyCLient is a class
    whereas client is an instance of the MyClient Class, you can't call the method on the class,
    you call it on an instance of the class. (you live in the house, not its blueprint)
    """
    await client.get_channel(962506194457608302).send("**Coin Sage Online**")

#this command was added at 5:11pm, it might take up to an hour for this shit to load
@client.tree.command() 
async def coin(interaction: discord.Interaction,  name: str):
    """Check the price of a cryptocurrency"""
    coin = fetchinfo.getCrypto(name)
    if coin != None: 
        myEmbed = discord.Embed(title = "**NAME:**", description=coin["id"], color=0x00ff00)
        myEmbed.set_thumbnail(url=coin["image"])
        myEmbed.set_image(url="https://i.imgur.com/0oc6H3J.png")
        myEmbed.add_field(name="Price:", value=str(coin["current_price"])+" USDT", inline=False)
        myEmbed.add_field(name="24H Movement:", value=str(coin["price_change_percentage_24h"])+"%", inline=False)
    else: 
        myEmbed = discord.Embed(
            title = "oops, something went wrong", 
            description= "that didn't work, check your spelling maybe?",
            color=0x00ff00
        )
    await interaction.response.send_message(embed = myEmbed)

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

##an attempt to have a command to sync globally
# @client.tree.command()
# async def sync(interaction: discord.Interaction, self):
#     if interaction.user.id == 430457620609105930:
#         await 
#         print('Command tree synced.')
#     else:
#         await interaction.response.send_message('You must be the owner to use this command!')


@client.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command()
# @app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
    """Sends the text into the current channel."""
    await interaction.response.send_message(text_to_send)


# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


# This context menu command only works on messages
@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(962506194457608302)  # replace with your channel id

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)


client.run(os.getenv("DISCORD_BOT_ID"))