import discord
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
import random

#get client object
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged as {0.user}'.format(client))


#string variables
en_greetings = ["Hi", "Hello", "Hoy"]
pt_greetings = ["Oi", "Olá", "Eae"]
emojis = ["!  :grin:", "!  :blush:", "!  :grinning:", "!  :slight_smile:", "!  :upside_down:", "!"]


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith((
            "oi chopper", "olá chopper", "salve chopper", "eae chopper", "fala chopper", "chopper"
    )):
        await message.channel.send(random.choice(pt_greetings) + random.choice(emojis))
    elif message.content.lower().startswith(("hi chopper", "hello chopper", "hoy chopper", "chopper")):
        await message.channel.send(random.choice(en_greetings) + "! :grin:")


#run continuously
keep_alive()

#get token
load_dotenv('.env')
client.run(os.getenv('TOKEN'))
