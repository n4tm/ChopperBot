import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
import random

# bot permissions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="chopper", intents=intents)


def search_digit(msg):
    ans = ['', '', '']
    for c in msg[13:]:
        if c.isdigit():
            ans[0] += c
        else:
            break
    for c in msg[36 + len(ans[0]):]:
        if c.isdigit() or c == '-':
            ans[1] += c
        else:
            break
    for c in msg[39 + len(ans[1]) + len(ans[0]):]:
        if c.isdigit() or c == '-':
            ans[2] += c
        else:
            break
    return [int(x) for x in ans]


def check_for_key(f, msg):
    for line in f:
        if not line.strip():
            continue
        line = line.strip()
        key, val = line.split(": ")
        if msg.content.lower().replace('?', '').replace(',', '')[8:] == key.lower().replace('?', '').replace(',', ''):
            return val
    return "?"


@bot.event
async def on_ready():
    change_status.start()
    print('CHOPPER IS ALIVE')
    guild = bot.get_guild(711473228442501192)
    print('Guild:', guild.name)


# string variables
en_greetings = ["Hi", "Hello", "Hoy"]
pt_greetings = ["Oi", "Olá", "Eae"]
emojis = [
    "!  :grin:", "!  :blush:", "!  :grinning:", "!  :slight_smile:",
    "!  :upside_down:", "!"
]


@bot.event
async def on_message(message):
    if message.content.lower().replace(',', '', 1).startswith("chopper aprende ("):
        f = open("bot_db.txt", "a")
        f.write(message.content[17:len(message.content) - 1] + "\n")
        f.close()
        await message.channel.send("Aprendi.")
        await message.delete(delay=2)

    elif message.content.lower().replace(',', '', 1).startswith("chopper escolhe "):
        online_list = [
            ("<@" + str(x.id) + ">") for x in bot.guilds[0].members if x.status != discord.Status.offline
            and not x.bot
        ]
        aux = 0
        if message.content[7] == ',':
            aux = 1
        chosen_users = random.sample(online_list, int(message.content[16 + aux]))

        try:
            await message.channel.send(chosen_users)
        except:
            await message.channel.send(
                "Você escreveu errado ou pediu para eu escolher mais do que o número de usuários online no momento."
            )

    elif message.content.lower().replace(',', '', 1).startswith("chopper gera 1 "):
        try:
            lst = search_digit(
                message.content[:21].replace(',', '') + 's' + message.content[21:31] + 's' + message.content[31:]
            )
            output_num = random.randrange(lst[1], lst[2] + 1)
            await message.channel.send(output_num)
        except:
            await message.channel.send("Eu posso até ser uma rena mas só falo português.")

    elif message.content.lower().replace(',', '', 1).startswith("chopper gera "):
        try:
            lst = search_digit(message.content.replace(',', ''))
            output_lst = [(random.randrange(lst[1], lst[2] + 1)) in range(lst[0])]
            await message.channel.send(output_lst)
        except:
            await message.channel.send("Eu posso até ser uma rena mas só falo português.")

    elif message.content.lower().replace(',', '').startswith("chopper quanto é "):
        try:
            aux = 0
            if message.content[7] == ',':
                aux = 1
            await message.channel.send(
                eval(
                    message.content[17 + aux:].lower().replace(',', '.').replace('?', '').replace('x', '*')
                    .replace('^', '**')
                )
            )
        except:
            await message.channel.send("Sei não :confused:")

    elif message.content.lower().replace(',', '') == "chopper help":
        await message.channel.send(
            "------------------------------------------------------   :deer:   ----------------------------------------"
            "--------------\n- Oi! Pra eu te responder sempre digite o meu nome (Chopper) antes de qualquer comando!\n"
            "\n#  Quanto é (operação matemática) - Resolvo alguma conta aritmética pra você.\n"
            "	 - Aí vai alguns dos operadores que você pode utilizar:\n          [* ou x : multiplicação, "
            "/ : divisão decimal, // : divisão inteira,\n          ^ ou ** : potência, + : soma, - : subtração, "
            "% : resto];\n\n#  Escolhe (número) pessoa(s) daqui - Escolho aleatóriamente um número de pessoas online "
            "no momento;\n\n#  Gera (quantidade) números aleatórios de (limite inicial) a (limite final) - Gero uma "
            "lista de números aleatoriamente selecionados de acordo com o intervalo fechado [limite inicial,limite "
            "final];\n\n#  Aprende ((chave: valor)) - Armazeno a chave (obs: não esqueça de coloca-los entre "
            "parênteses);\n\n#  (chave) - Respondo com o valor da chave correspondente.\n------------------------------"
            "-------------------------------------------------------------------------------------"
        )

    elif message.content.lower().replace(',', '', 1).startswith("chopper "):
        f = open("bot_db.txt", "r")
        await message.channel.send(check_for_key(f, message))

    elif message.content.lower().startswith((
            "oi chopper", "olá chopper", "salve chopper", "eae chopper", "fala chopper"
    )):
        await message.channel.send(random.choice(pt_greetings) + random.choice(emojis))

    elif message.content.lower().startswith(("hi chopper", "hello chopper", "hoy chopper")):
        await message.channel.send(random.choice(en_greetings) + random.choice(emojis))


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(name="Amor Peludo"))


# run continuously
keep_alive()

# get token
bot.run("ODIxNzY3NTA2MTQxMjQ5NTU4.YFIgoQ.00Hq69myJF7srWY4Fb_7_cC0jFc")
