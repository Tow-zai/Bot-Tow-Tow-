import discord
import os
import asyncio
import requests
import json
import random
import youtube_dl
import time
from datetime import datetime
import pytz
from discord.ext import commands
from staying_alive import staying_alive
from variable_s import *
from react_commands import *
from aiohttp import request

intents = discord.Intents(messages=True,guilds=True,members=True,typing=False,presences=False,reactions=True)
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
	print('{0.user} is in! '.format(client))
	await client.change_presence(activity=discord.Game('EPIC RPG'))


@client.command(name='server')
async def fetchServerInfo(context):
	guild = context.guild
	emb = discord.Embed(title="Server 資料",
	                    description=f"哩個ser我暫時俾{random.randrange(10)}分!",
	                    colour=0xFF0000)
	fields = [("Server Size", f'{len(guild.members)}', True),
	          ("Server Owner", f'{guild.owner.display_name}', True),
	          ("Server 起源地", f'{guild.region}', False)]
	for name, value, inline in fields:
		emb.add_field(name=name, value=value, inline=inline)
	emb.set_author(name=f'{guild.name}', icon_url=context.guild.icon_url)
	emb.set_footer(text="つづく")
	emb.set_thumbnail(url=context.guild.icon_url)
	emb.set_image(url=context.guild.icon_url)
	msg = await context.channel.send(embed=emb)


@client.command(name="fact")
async def animal_fact(ctx, animal: str):
	if animal.lower() in ("dog", "cat", "panda", "fox", "bird", "koala"):
		endpoint = f"https://some-random-api.ml/facts/{animal.lower()}"
		response = requests.get(endpoint).json()
		await ctx.channel.send(response["fact"])
	else:
		await ctx.channel.send("自己Google啦!")


@client.command(name="do")
async def ichdj(ctx, action: str):
	if action.lower() in ("wink", "pat", "hug", "face-palm"):
		url = f'https://some-random-api.ml/animu/{action.lower()}'
		response = requests.get(url, headers={
		    "Accept": "application/json"
		}).json()
		await ctx.channel.send(response["link"])
	else:
		await ctx.channel.send(
		    "吓? https://tenor.com/view/what-do-you-wanna-do-edward-asner-abe-rifkin-dead-to-me-what-should-we-do-gif-17803589"
		)


@client.command(name="img")
async def img(ctx, img: str):
	if img.lower() in ("dog", "cat", "panda", "fox", "red_panda", "koala",
	                   "birb", "racoon", "kangaroo", "whale", "pikachu"):
		url = f'https://some-random-api.ml/img/{img.lower()}'
		response = requests.get(url, headers={
		    "Accept": "application/json"
		}).json()
		await ctx.channel.send(response["link"])
	else:
		await ctx.channel.send("Google Image幫到你!")


#@client.command()
#async def study_up():
#    if


@client.command(name="jokea")
async def ichdj(ctx):
	url = 'https://icanhazdadjoke.com/'
	response = requests.get(url, headers={"Accept": "application/json"}).json()
	await ctx.channel.send(response["joke"])


@client.command(name="jokeb")
async def SRF_joke(ctx):
	endpoint = "https://some-random-api.ml/joke"
	response = requests.get(endpoint).json()
	await ctx.channel.send(response["joke"])


@client.command(name="pl")
async def pl(ctx, url: str):
	channel = ctx.author.voice.channel
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice and not voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		voice.play(discord.FFmpegPCMAudio(f"./MP3/{url}.mp3"))
		while voice.is_playing():
			await asyncio.sleep(1)
		else:
			await asyncio.sleep(1)
			while voice.is_playing():
				break
			else:
				await voice.disconnect()


@client.command(name="leave")
async def leave(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_connected():
		await voice.disconnect()
	else:
		await ctx.send("not connected")


@client.command()
async def yn(ctx, *, message):
	emb = discord.Embed(title=f'投票:{message}',description=f'我覺得係{random.choice(ynchoice)}')
	msg = await ctx.channel.send(embed=emb)
	await msg.add_reaction('👍')
	await msg.add_reaction('👎')


@client.command()
async def rate(ctx):
	emb = discord.Embed(title="你會俾幾分?",
	                    description=f'我唔知你,但係我會比{random.randrange(10)}分!')
	msg = await ctx.channel.send(embed=emb)
	number_of_responses = 10
	emoji_numbers = [
	    '1️⃣', "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", '🔟'
	]
	for i in range(number_of_responses):
		await msg.add_reaction(emoji_numbers[i])


@client.command()
async def hel_lo(message):
	await message.add_reaction('<:LOVEU2:831585270398189600>')
	await message.channel.send(random.choice(hi_gif))


async def react(message):
	await message.add_reaction('🫂')  #841102889510371419
	await message.add_reaction('<:LOVEU2:831585270398189600>')
	await message.channel.send(random.choice(starter_encouragements))


async def pman(message):
	await message.delete()
	await message.channel.send(
	    " <:Support:833905650140053544> <:3Dpigman:831527282816188456> ")


@client.command(name='CAtime')
async def CA_T(context):
	tz_CA = pytz.timezone('America/Toronto')
	CA_T = datetime.now(tz_CA)
	await context.channel.send(CA_T.strftime("%a %d %b,%y %I:%M:%S %p"))


@client.command(name='UKtime')
async def UK_T(message):
	tz_UK = pytz.timezone('Europe/London')
	UK_T = datetime.now(tz_UK)
	await message.channel.send(UK_T.strftime("%a %d %b,%y %I:%M:%S %p"))


@client.command(name='HKtime')
async def HK_T(message):
	tz_HK = pytz.timezone('Asia/Hong_Kong')
	HK_T = datetime.now(tz_HK)
	await message.channel.send(HK_T.strftime("%a %d %b,%y %I:%M:%S %p"))


@client.event
async def on_message(message):
	await client.process_commands(message)
	if message.author == client.user:
		return

	username = str(message.author).split('#')[0]
	msg = message.content.lower()

	if any(word in msg for word in sad_words):
		await react(message)

	if ('熱狗' in msg):
		tmpmsg = await message.channel.send('你講緊Stella?')
		time.sleep(3)
		await tmpmsg.delete()

	if ('比幾分' in msg):
		await message.channel.send(f'我比較公道,會比{random.randrange(10)}分!')

	if message.content.startswith('pigman'):
		await pman(message)

	if message.content.startswith('bbling'):
		await bling(message)

	if any(map(message.content.lower().startswith, greet_ings)):
		await hel_lo(message)

	if ('雞湯' in msg):
		await message.channel.send(random.choice(poison_soup))

	if message.content.startswith('挽'):
		await message.channel.send(
		    'https://tenor.com/view/holding-hands-dog-cars-gif-13660273')

	if message.content.startswith('say'):
		tmp = message.content.split(" ", 1)
		if len(tmp) == 1:
			await message.channel.send(
			    'https://tenor.com/view/wow-what-say-what-gif-16598538')
		else:
			await message.channel.send(tmp[1])

	if ('joker' in msg):
		await message.channel.send(
		    'https://tenor.com/view/batman-joker-heath-ledger-clap-clapping-gif-11060757'
		)


#    if message.content.startswith('幾點'):
#        await timezon(message)

staying_alive()
client.run(os.getenv('TOKEN'))
