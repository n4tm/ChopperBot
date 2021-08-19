import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
import random
import linecache
import json

#bot permissions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("chopper"), intents=intents)

def search_digit(msg, aaux):
	ans = ['','','']
	for c in msg[5+aaux:]:
		if c.isdigit():
			ans[0] += c
		else:
			break
	for c in msg[28+aaux+len(ans[0]):]:
		if c.isdigit() or c == '-':
			ans[1] += c
		else:
			break
	for c in msg[31+aaux+ len(ans[1]) + len(ans[0]):]:
		if c.isdigit() or c == '-':
			ans[2] += c
		else:
			break
	return [int(x) for x in ans]
		

def check_for_key(f, msg, aaux):
	data = json.load(f)
	try:
		return data[msg.content.lower().replace('?', '').replace(',','')[aaux:]]
	except KeyError:
		return "?"

@bot.event
async def on_ready():
	change_status.start()
	print('CHOPPER IS ALIVE')
	guilds = bot.guilds
	for guild in guilds:
		print('Guild:', guild.name)

#string variables
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
	await msg.channel.send(f'Pong! Meu ping: {round (bot.latency * 1000)} ms')


@bot.command()
async def chopper_learn(msg, aaux):
	json_file = f'./servers-db/bot_db_{msg.guild.name}.json'
	try:
		f = open(json_file, "a")
	except OSError:
		open(json_file, 'w')
		f = open(json_file, "a")
	key, val = msg.content[9+aaux:len(msg.content)-1].split(": ")
	jsonString = json.dumps({key: val})
	f.write(jsonString)
	f.close()
	await msg.channel.send("Aprendi.")
	await msg.delete(delay=3)

@bot.command()
async def chopper_choose_user(msg, aaux):
	online_list = [("<@" + str(x.id) + ">") for x in msg.guild.members if x.status != discord.Status.offline and not x.bot]
	aux = 0
	if msg.content[aaux-1] == ',':
		aux = 1
	chosen_users = random.sample(online_list, int(msg.content[8+aaux+aux]))
	
	try:
		await msg.channel.send(chosen_users)
	except:
		await msg.channel.send(
			"Você escreveu errado ou pediu para eu escolher mais do que o número de usuários online no momento.", delete_after=3)

@bot.command()
async def chopper_number_generator(msg, aaux):
	try:
		lst = search_digit(msg.content[:13+aaux].replace(',','') + 's' + msg.content[13+aaux:23+aaux] + 's' + msg.content[23+aaux:], aaux)
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
		if msg.content[aaux-1] == ',':
			aux = 1
		await msg.channel.send(
			eval(msg.content[aaux+aux+9:].lower().replace(',', '.').replace('?', '').replace('x', '*').replace('^', '**')))
	except:
		await msg.reply(
			"Sei não :confused:", delete_after=3)

@bot.command()
async def chopper_help(msg):
	await msg.channel.send("------------------------------------------------------   :deer:   ------------------------------------------------------\n- Oi! Pra eu te responder sempre digite o meu nome (Chopper) ou me marque antes de qualquer comando!\n\n#  Quanto é (operação matemática) - Resolvo alguma conta aritmética pra você.\n	 - Aí vai alguns dos operadores que você pode utilizar:\n          [* ou x : multiplicação, / : divisão decimal, // : divisão inteira,\n          ^ ou ** : potência, + : soma, - : subtração, % : resto];\n\n#  Escolhe (número) pessoa(s) - Escolho aleatóriamente um número de pessoas online no momento;\n\n#  Gera (quantidade) números aleatórios de (limite inicial) a (limite final) - Gero uma lista de números aleatoriamente selecionados de acordo com o intervalo fechado [limite inicial,limite final];\n\n#  Minha foto de perfil - Mostro a foto de perfil do autor do comando;\n\n#  Ping - Mostro o meu ping;\n\n#  Conta uma piada - Eu mostro uma piada curta aleatória\n\n#  Aprende ((chave: valor)) - Armazeno a chave (obs: não esqueça de coloca-los entre parênteses);\n\n#  (chave) - Respondo com o valor da chave correspondente.\n\n#  Diz/Fala (texto) - Repito o texto pedido.\n\n-------------------------------------------------------------------------------------------------------------------")

@bot.command()
async def check_file(msg, aaux):
	with open(f'./servers-db/bot_db_{msg.guild.name}.json', "r") as f:
		await msg.channel.send(check_for_key(f, msg, aaux), delete_after=3)

@bot.command()
async def display_random_joke(msg):
	n = random.randrange(1, 380, 3)
	l1 = linecache.getline("./servers-db/jokes.txt", n)
	l2 = linecache.getline("./servers-db/jokes.txt", n+1)
	await msg.channel.send(l1+l2)
	
@bot.command()
async def display_user_msg(msg, aux):
	aux2 = 4
	if msg.content[aux:aux+5] == "fala ":
		aux2 = 5
	if msg.content[7] == ',':
		aux2 += 1
	try:
		await msg.channel.send(msg.content[aux+aux2:])
	except:
		await msg.channel.send("Tendi não :confused:")

@bot.event
async def on_message(message):
	aux = 0
	if message.content.lower()[:7] == 'chopper':
		aux = 8
	elif message.content.lower()[:22] == '<@!821767506141249558>':
		aux = 23
	handledMessage = message.content.lower().replace(',','',1)[aux:]
	if (message.author.bot or aux == 0) and not(message.content.lower().startswith("chopper") or message.content.lower().startswith("<@!821767506141249558>")):
		return
	elif handledMessage.startswith("aprende ("):
		await chopper_learn(message, aux)
	elif handledMessage.startswith("escolhe "):
		await chopper_choose_user(message, aux)
	elif handledMessage.startswith("gera 1 "):
		await chopper_number_generator(message, aux)

	elif handledMessage.startswith("gera "):
		await chopper_numbers_generator(message, aux)
	elif handledMessage.startswith("quanto é "):
		await chopper_calculator(message, aux)
	elif handledMessage == "help":
		await chopper_help(message)
	elif handledMessage == "ping":
		await ping(message)
	elif handledMessage == "minha foto de perfil":
		await display_avatar(message)
	elif handledMessage.startswith("conta uma piada") or (message.content.lower()[:15] == "conta uma piada" and len(message.content)-15 == aux):
		await display_random_joke(message)
	elif handledMessage.startswith(("diz ", "fala ")):
		await display_user_msg(message, aux)
	elif message.content.lower().startswith(
		("oi chopper", "olá chopper", "salve chopper", "eae chopper",
		"fala chopper")):
		await message.channel.send(
			random.choice(pt_greetings) + random.choice(emojis))
	elif message.content.lower().startswith(
		("hi chopper", "hello chopper", "hoy chopper", "hey chopper")):
		await message.channel.send(random.choice(en_greetings) + random.choice(emojis))
	else:
		await check_file(message, aux)


@tasks.loop(seconds=10)
async def change_status():
	await bot.change_presence(activity=discord.Game(name="Wano Kuni"))


#run continuously
keep_alive()

#get token
bot.run("bot token here")