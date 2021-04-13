import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
import random
import linecache
import requests
from bs4 import BeautifulSoup

d = False

# bot permissions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("chopper"), intents=intents)


def search_digit(msg, aaux):
    ans = ['', '', '']
    for c in msg[5 + aaux:]:
        if c.isdigit():
            ans[0] += c
        else:
            break
    for c in msg[28 + aaux + len(ans[0]):]:
        if c.isdigit() or c == '-':
            ans[1] += c
        else:
            break
    for c in msg[31 + aaux + len(ans[1]) + len(ans[0]):]:
        if c.isdigit() or c == '-':
            ans[2] += c
        else:
            break
    return [int(x) for x in ans]


def check_for_key(f, msg, aaux):
    global d
    for line in f:
        if not line.strip():
            continue
        line = line.strip()
        key, val = line.split(": ")
        if msg.content.lower().replace('?', '').replace(',', '')[aaux:] == key.lower().replace('?', '').replace(',',
                                                                                                                ''):
            return val
    d = True
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


@bot.command()
async def display_avatar(msg):
    await msg.reply(msg.author.avatar_url)


@bot.command()
async def ping(msg):
    await msg.channel.send(f'Pong! Meu ping: {round(bot.latency * 1000)} ms')


@bot.command()
async def chopper_learn(msg, aaux):
    f = open("bot_db.txt", "a")
    f.write(msg.content[9 + aaux:len(msg.content) - 1] + "\n")
    f.close()
    await msg.channel.send("Aprendi.")
    await msg.delete(delay=3)


@bot.command()
async def chopper_choose_user(msg, aaux):
    online_list = [("<@" + str(x.id) + ">") for x in bot.guilds[0].members if
                   x.status != discord.Status.offline and not x.bot]
    aux = 0
    if msg.content[aaux - 1] == ',':
        aux = 1
    chosen_users = random.sample(online_list, int(msg.content[8 + aaux + aux]))

    try:
        await msg.channel.send(chosen_users)
    except:
        await msg.channel.send(
            "Você escreveu errado ou pediu para eu escolher mais do que o número de usuários online no momento.",
            delete_after=3)


@bot.command()
async def chopper_number_generator(msg, aaux):
    try:
        lst = search_digit(
            msg.content[:13 + aaux].replace(',', '') + 's' + msg.content[13 + aaux:23 + aaux] + 's' + msg.content[
                                                                                                      23 + aaux:], aaux)
        output_num = random.randrange(lst[1],
                                      lst[2] + 1)
        await msg.channel.send(output_num)
    except:
        await msg.channel.send(
            "Eu posso até ser uma rena mas só falo português.", delete_after=3)


@bot.command()
async def chopper_numbers_generator(msg, aaux):
    try:
        lst = search_digit(msg.content.replace(',', ''), aaux)
        output_lst = [(random.randrange(lst[1],
                                        lst[2] + 1))
                      for i in range(lst[0])]
        await msg.channel.send(output_lst)
    except:
        await msg.channel.send(
            "Eu posso até ser uma rena mas só falo português.", delete_after=3)


@bot.command()
async def chopper_calculator(msg, aaux):
    try:
        aux = 0
        if msg.content[aaux - 1] == ',':
            aux = 1
        await msg.channel.send(
            eval(msg.content[aaux + aux + 9:].lower().replace(',', '.').replace('?', '').replace('x', '*').replace('^',
                                                                                                                   '**')))
    except:
        await msg.reply(
            "Sei não :confused:", delete_after=3)


@bot.command()
async def chopper_help(msg):
    await msg.channel.send(
        "------------------------------------------------------   :deer:   ------------------------------------------------------\n- Oi! Pra eu te responder sempre digite o meu nome (Chopper) ou me marque antes de qualquer comando!\n\n#  Quanto é (operação matemática) - Resolvo alguma conta aritmética pra você.\n	 - Aí vai alguns dos operadores que você pode utilizar:\n          [* ou x : multiplicação, / : divisão decimal, // : divisão inteira,\n          ^ ou ** : potência, + : soma, - : subtração, % : resto];\n\n#  Escolhe (número) pessoa(s) - Escolho aleatóriamente um número de pessoas online no momento;\n\n#  Gera (quantidade) números aleatórios de (limite inicial) a (limite final) - Gero uma lista de números aleatoriamente selecionados de acordo com o intervalo fechado [limite inicial,limite final];\n\n#  Minha foto de perfil - Mostro a foto de perfil do autor do comando;\n\n#  Ping - Mostro o meu ping;\n\n#  Conta uma piada - Eu mostro uma piada curta aleatória\n\n#  Aprende ((chave: valor)) - Armazeno a chave (obs: não esqueça de coloca-los entre parênteses);\n\n#  (chave) - Respondo com o valor da chave correspondente.\n\n#  Diz/Fala (texto) - Repito o texto pedido;\n\n#  (...) Steam /Sale - Mostro a data da próxima steam sale.\n-------------------------------------------------------------------------------------------------------------------")


@bot.command()
async def check_file(msg, aaux):
    global d
    f = open("bot_db.txt", "r")
    if d:
        await msg.channel.send(check_for_key(f, msg, aaux), delete_after=3)
    else:
        await msg.channel.send(check_for_key(f, msg, aaux))
    d = False


@bot.command()
async def display_random_joke(msg):
    n = random.randrange(1, 380, 3)
    l1 = linecache.getline("jokes.txt", n)
    l2 = linecache.getline("jokes.txt", n + 1)
    await msg.channel.send(l1 + l2)


@bot.command()
async def display_steam_sale(msg):
    sales_months = {
        "January": "Janeiro",
        "February": "Fevereiro",
        "March": "Março",
        "April": "Abril",
        "May": "Maio",
        "June": "Junho",
        "July": "Julho",
        "August": "Agosto",
        "September": "Setembro",
        "October": "Outubro",
        "November": "Novembro",
        "December": "Dezembro"
    }
    url = "https://prepareyourwallet.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    parag = soup.find('div', attrs={'class': 'card-body'}).find_all('p')
    content = str(parag)[37:95]
    sale_name = ''
    year, begins, ends = '', '', ''
    s = content.split()
    bmonth = s[len(s) - 7]
    emonth = s[len(s) - 2]
    aux = False
    for c in content:
        if c.isdigit():
            break
        else:
            sale_name += c
    for c in content:
        if c.isdigit() and len(year) != 4:
            year += c
        elif len(year) == 4 and c.isdigit() and not aux:
            begins += c
        elif len(year) == 4 and len(begins) != 0 and not c.isdigit():
            aux = True
        elif aux and c.isdigit():
            ends += c

    await msg.channel.send(
        f'[ {sale_name}] - começa dia {begins} de {sales_months[bmonth]} e termina dia {ends} de {sales_months[emonth]}  :money_with_wings:')


@bot.command()
async def display_user_msg(msg, aux):
    aux2 = 4
    if msg.content[aux:aux + 5] == "fala ":
        aux2 = 5
    if msg.content[7] == ',':
        aux2 += 1
    try:
        await msg.channel.send(msg.content[aux + aux2:])
    except:
        await msg.channel.send("Tendi não :confused:")


@bot.event
async def on_message(message):
    aux = 0
    if message.content.lower()[:7] == 'chopper':
        aux = 8
    elif message.content.lower()[:22] == '<@!821767506141249558>':
        aux = 23
    if (message.author.bot or aux == 0) and not (
            message.content.lower().endswith("chopper") or message.content.lower().endswith("<@!821767506141249558>")):
        return
    elif message.content.lower().replace(',', '', 1)[aux:].startswith("aprende ("):
        await chopper_learn(message, aux)

    elif message.content.lower().replace(',', '',
                                         1)[aux:].startswith("escolhe "):
        await chopper_choose_user(message, aux)
    elif message.content.lower().replace(',', '',
                                         1)[aux:].startswith("gera 1 "):
        await chopper_number_generator(message, aux)

    elif message.content.lower().replace(',', '',
                                         1)[aux:].startswith("gera "):
        await chopper_numbers_generator(message, aux)
    elif message.content.lower().replace(',', '', 1)[aux:].startswith("quanto é "):
        await chopper_calculator(message, aux)
    elif message.content.lower().replace(',', '', 1)[aux:] == "help":
        await chopper_help(message)
    elif message.content.lower().replace(',', '', 1)[aux:] == "ping":
        await ping(message)
    elif message.content.lower().replace(',', '', 1)[aux:] == "minha foto de perfil":
        await display_avatar(message)
    elif message.content.lower().replace(',', '', 1)[aux:].startswith("conta uma piada") or (
            message.content.lower()[:15] == "conta uma piada" and len(message.content) - 15 == aux):
        await display_random_joke(message)
    elif message.content.lower().replace(',', '', 1).replace('?', '')[aux:].endswith(('steam', 'sale')):
        await display_steam_sale(message)
    elif message.content.lower().replace(',', '', 1)[aux:].startswith(("diz ", "fala ")):
        await display_user_msg(message, aux)
    elif message.content.lower().startswith(
            ("oi chopper", "olá chopper", "salve chopper", "eae chopper",
             "fala chopper")):
        await message.channel.send(
            random.choice(pt_greetings) + random.choice(emojis))
    elif message.content.lower().startswith(
            ("hi chopper", "hello chopper", "hoy chopper")):
        await message.channel.send(random.choice(en_greetings) + random.choice(emojis))
    else:
        await check_file(message, aux)


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(name="Amor Peludo"))


# run continuously
keep_alive()

# get token (There is no Token because discord prevents it to appear in other websites such as GitHub
#bot.run(SECRET TOKEN)