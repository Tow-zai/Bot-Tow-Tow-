import discord
import os
import asyncio
import requests
import json
import random
import time
from datetime import datetime
import pytz
import aiohttp
import io
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from staying_alive import staying_alive
from variable_s import *
from react_commands import *
from aiohttp import request
from discord import File
from PIL import Image, ImageDraw, ImageFont


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("tt"),case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
	print('{0.user} is in! '.format(bot))
	await bot.change_presence(activity=discord.Game('EPIC RPG'))

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(830593281817182208)
    channel = bot.get_channel(830593281817182212)
    emb = discord.Embed(title='歡迎新成員既加入', description=f'{member.mention} 你終於來咗啦? 想睇咩都講聲啊!唔洗怕羞既尼度!', colour=0xFF99FF)
    fields = [("歡迎來到",f'{guild.name}', True),("Server現有成員", f'{len(guild.members)}', True),]
    for name, value, inline in fields:
        emb.add_field(name=name, value=value, inline=inline)
    emb.set_author(name='New Member', icon_url=f'{member.avatar_url}')
    emb.set_footer(text="多d宣傳suck友入來一齊睇片啦~ →_→")
    emb.set_thumbnail(url=f'{member.avatar_url}')
    # emb.set_image(url=f'{member.avatar_url}')
    msg = await channel.send(embed=emb)


@bot.event
async def on_voice_state_update(member, before, after):
    if not member.bot:
        if after.channel.id == 827272740817076235:  #VC
            if not before.channel or before.channel.id != 827272740817076235:
                channel = bot.get_channel(827278669494878278)   #文字chan            
                await channel.send(f'{member.name} = Here')
        if after.channel.id == 837057086339809360:  #VC
            if not before.channel or before.channel.id != 837057086339809360:
                channel = bot.get_channel(837057315365715969)   #文字chan
                if member.id != 809795855988555787:
                    if member.nick is None:
                        await channel.send(f'{member.name}入咗來,條友仲未改名 >_>')
                    else:
                        await channel.send(f'{member.nick}來咗啦!你今日忍咗未?')

@bot.command(name='ser')
async def fetchServerInfo(ctx):
    guild = ctx.guild
    emb = discord.Embed(title="Server 資料", description=f"哩個ser我暫時俾{random.randint(6,10)}分!", colour=0xFF0000)
    fields = [("Server Size", f'{len(guild.members)}', True),("Server Owner", f'{guild.owner.display_name}', True),('Server "起源地"', f'{guild.region}', False)]
    for name, value, inline in fields:
        emb.add_field(name=name, value=value, inline=inline)
    emb.set_author(name=f'{guild.name}', icon_url=ctx.guild.icon_url)
    emb.set_footer(text="つづく")
    emb.set_thumbnail(url=ctx.guild.icon_url)
    emb.set_image(url=ctx.guild.icon_url)
    msg = await ctx.channel.send(embed=emb)

#R&M API random character generator
@bot.command(name="RnM")
async def rick_morty(ctx):
    character_num = random.randint(1,671)
    endpoint = f"https://rickandmortyapi.com/api/character/{character_num}"
    response = requests.get(endpoint).json()
    emb = discord.Embed(title=f'角色:{response["name"]}', description=f"```狀態:{response['status']}```", colour=0x33ffff)
    fields = [("人物ID",f"{response['id']}", True),("性別", f"{response['gender']}", True),("種族", f"{response['species']}", True),("起源", f"{response['type']}",True),("Origin", f"{response['origin']['name']}",False),("位置", f"{response['location']['name']}",False)]
    for name, value, inline in fields:
        emb.add_field(name=name, value=value, inline=inline)
    emb.set_author(name='Rick & Morty 人物卡')#, icon_url=ctx.guild.icon_url)
    emb.set_footer(text=f"出現集數:{len(response['episode'])}")
    emb.set_thumbnail(url=f'{response["image"]}')
    emb.set_image(url=f'{response["image"]}')
    msg = await ctx.channel.send(embed=emb)

@bot.command()
async def nick(ctx, *, user: discord.Member):
    if user.nick == None:
        await ctx.send(f"條友仔無d創意,個個ser既名都係: {user.display_name}")
    else:
        await ctx.send(f"佢係尼個ser既名係: {user.nick}")


@bot.command()
async def pl(ctx, url : str):
    channel = ctx.author.voice.channel

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
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


@bot.command(name='hurt')
async def canvas(ctx,*,txt):
    image = Image.open(f'./Pic/dog.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("SansTC.ttf", 18)
    text_width, text_height = draw.textsize(txt, font=font)
    x = 120
    y = 280
    draw.text( (x, y), txt, fill=(128,128,130), font=font)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')    
    buffer.seek(0) 
    await ctx.send(file=File(buffer, 'myimage.png'))


@bot.command(name = "whowin")
async def whowin(ctx,*,member: discord.Member = None):
    image = Image.open(f'./Pic/whowin.png')
    print('size:', image.size)
    IMAGE_WIDTH, IMAGE_HEIGHT = image.size
    draw = ImageDraw.Draw(image)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')    
    buffer.seek(0) 
    
    AVATAR_SIZE = 128
    avatar_asset = ctx.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)
    buffer_avatar = io.BytesIO()
    await avatar_asset.save(buffer_avatar)
    buffer_avatar.seek(0)
    avatar_image = Image.open(buffer_avatar)
    avatar_image = avatar_image.resize((AVATAR_SIZE + 110, AVATAR_SIZE + 110))
    x = 10
    y = (IMAGE_HEIGHT-AVATAR_SIZE)//2
    image.paste(avatar_image, (x, y))

    avatar_asset2 = member.avatar_url_as(format='jpg', size=AVATAR_SIZE)
    buffer_avatar2 = io.BytesIO()
    await avatar_asset2.save(buffer_avatar2)
    buffer_avatar2.seek(0)
    avatar_image2 = Image.open(buffer_avatar2)
    avatar_image2 = avatar_image2.resize((AVATAR_SIZE + 110, AVATAR_SIZE + 110))
    x = 270
    y = (IMAGE_HEIGHT-AVATAR_SIZE)//2
    image.paste(avatar_image2, (x, y))

    buffer_output = io.BytesIO()
    image.save(buffer_output, format='PNG')    
    buffer_output.seek(0) 
    msg = await ctx.send(file=File(buffer_output, 'myimage.png'))
    await msg.add_reaction("👈")
    await msg.add_reaction("👉")

@bot.command(name = "mstake")
async def whowin(ctx,*,member: discord.Member = None):
    image = Image.open(f'./Pic/mstake.png')
    print('size:', image.size)
    IMAGE_WIDTH, IMAGE_HEIGHT = image.size
    draw = ImageDraw.Draw(image)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')    
    buffer.seek(0) 
    
    AVATAR_SIZE = 128
    avatar_asset = member.avatar_url_as(format='jpg', size=AVATAR_SIZE)
    buffer_avatar = io.BytesIO()
    await avatar_asset.save(buffer_avatar)
    buffer_avatar.seek(0)
    avatar_image = Image.open(buffer_avatar)
    avatar_image = avatar_image.resize((AVATAR_SIZE + 350, AVATAR_SIZE + 350))
    x = 480
    y = ((IMAGE_HEIGHT-AVATAR_SIZE)//2)+80
    image.paste(avatar_image, (x, y))

    buffer_output = io.BytesIO()
    image.save(buffer_output, format='PNG')    
    buffer_output.seek(0) 
    await ctx.send(file=File(buffer_output, 'myimage.png'))

@bot.command(name = "shake")
async def whowin(ctx,*,member: discord.Member = None):
    image = Image.open(f'./Pic/shake.png')
    IMAGE_WIDTH, IMAGE_HEIGHT = image.size
    print('size:', image.size)
    draw = ImageDraw.Draw(image)
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')    
    buffer.seek(0) 
    
    AVATAR_SIZE = 128
    avatar_asset = ctx.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)
    buffer_avatar = io.BytesIO(await avatar_asset.read())
    avatar_image = Image.open(buffer_avatar)
    avatar_image = avatar_image.resize((AVATAR_SIZE - 30 , AVATAR_SIZE - 30))

    circle_image = Image.new('L', (AVATAR_SIZE - 30, AVATAR_SIZE - 30))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, AVATAR_SIZE - 30, AVATAR_SIZE - 30), fill=255)
    x = 1
    y = 110
    image.paste(avatar_image, (x, y), circle_image)

    avatar_asset2 = member.avatar_url_as(format='jpg', size=AVATAR_SIZE)
    buffer_avatar2 = io.BytesIO(await avatar_asset2.read())
    avatar_image2 = Image.open(buffer_avatar2)
    avatar_image2 = avatar_image2.resize((AVATAR_SIZE - 30 , AVATAR_SIZE - 30))
    circle_image2 = Image.new('L', (AVATAR_SIZE - 30, AVATAR_SIZE - 30))
    circle_draw2 = ImageDraw.Draw(circle_image2)
    circle_draw2.ellipse((0, 0, AVATAR_SIZE - 30, AVATAR_SIZE - 30), fill=255)
    x = 450
    y = 120
    image.paste(avatar_image2, (x, y), circle_image2)

    buffer_output = io.BytesIO()
    image.save(buffer_output, format='PNG')    
    buffer_output.seek(0) 
    await ctx.send(file=File(buffer_output, 'myimage.png'))

    
@bot.command(name="fact")
async def animal_fact(ctx, *, animal: str):
    if animal.lower() in ("dog", "cat", "panda", "fox", "bird", "koala"):
        endpoint = f"https://some-random-api.ml/facts/{animal.lower()}"
        response = requests.get(endpoint).json()
        await ctx.channel.send(response["fact"])
    else:
        await ctx.channel.send("自己Google啦!")

@bot.command(name="do")
async def expre_ss(ctx, *, action: str):
    if action.lower() in ("wink", "pat", "hug", "face-palm"):
        url = f'https://some-random-api.ml/animu/{action.lower()}'
        response = requests.get(url, headers={"Accept": "application/json"}).json()
        await ctx.channel.send(response["link"])
    else:
        await ctx.channel.send("https://tenor.com/view/what-do-you-wanna-do-edward-asner-abe-rifkin-dead-to-me-what-should-we-do-gif-17803589")

@bot.command(name="img")
async def img(ctx, *, img: str):
    if img.lower() in ("dog", "cat", "panda", "fox", "red_panda", "koala", "birb", "racoon", "kangaroo", "whale", "pikachu"):
        url = f'https://some-random-api.ml/img/{img.lower()}'
        response = requests.get(url, headers={"Accept": "application/json"}).json()
        await ctx.channel.send(response["link"])
    else:
        await ctx.channel.send("Google Image幫到你!")

@bot.command(name="jokea")
async def ichdj(ctx):
    url = 'https://icanhazdadjoke.com/'
    response = requests.get(url, headers={"Accept": "application/json"}).json()
    await ctx.channel.send(response["joke"])

@bot.command(name="jokeb")
async def SRF_joke(ctx):
    endpoint = "https://some-random-api.ml/joke"
    response = requests.get(endpoint).json()
    await ctx.channel.send(response["joke"])

@bot.command(name="meme")
async def SRF_meme(ctx):
    endpoint = "https://some-random-api.ml/meme"
    response = requests.get(endpoint).json()
    await ctx.channel.send(response["image"])

@bot.command()
async def yn(ctx, *, message):
    emb = discord.Embed(title=f'投票:{message}',description=f'我覺得係{random.choice(ynchoice)}')
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@bot.command(pass_context = True)
@commands.has_permissions(administrator=True, manage_messages=True)
async def clr(ctx, number):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in ctx.channel.history(limit = number):
        mgs.append(x)
    await ctx.message.channel.delete_messages(mgs)
    await ctx.channel.send('還我河蟹社會!')

@bot.command()
async def rate(ctx):
    emb = discord.Embed(title="你會俾幾分?",description=f'我唔係逼你,但如果係frd既就比{random.randrange(10)}分!')
    msg = await ctx.channel.send(embed=emb)
    number_of_responses = 10
    emoji_numbers = ['1️⃣', "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", '🔟']
    for i in range(number_of_responses):
        await msg.add_reaction(emoji_numbers[i])

async def react(message):
    await message.add_reaction('🫂')  #841102889510371419
    await message.add_reaction('<:LOVEU2:831585270398189600>')
    await message.channel.send(random.choice(starter_encouragements))


@bot.command(name= 'lgbtq')
async def exp_res(ctx, member: discord.Member=None):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png")}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'gay.png'))
    
@bot.command(name= 'wasted')
async def exp_res(ctx, member: discord.Member=None):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format="png")}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'wasted.png'))


@bot.command (name= 'rps')
async def rps(ctx):
    choice = ("🍞", "✂️", "👊")
    pc = random.choice(choice)
    msg = await ctx.channel.send("清侵,無教,叉燒包!")
    await msg.add_reaction("🍞")
    await msg.add_reaction("✂️")
    await msg.add_reaction("👊")

    try:
        def check1(reaction, user):
            return user != bot.user 
        reaction, user = await bot.wait_for("reaction_add", timeout=5.0, check=check1)
        
        await asyncio.sleep(1)

        if str(reaction.emoji) == pc:
            await ctx.channel.send('打和!SUPER!')
        elif str(reaction.emoji) == "🍞":
            if pc == "👊":
                await ctx.channel.send('哎呀~衰鬼~我居然比你包住咗~ <3')
            elif pc == "✂️":
                await ctx.channel.send("哼!你個廢柴!果然輸比我個奪命鉸剪腳呢")
        elif str(reaction.emoji) == "✂️":
            if pc == "🍞":
                await ctx.channel.send('哎呀~我個法國麵包啊~~~剪細力啦好心你~ <3')
            elif pc == "👊":
                await ctx.channel.send("超!你個軟腳蟹!睇就知唔夠我硬啦!")
        elif str(reaction.emoji) == "👊":
            if pc == "✂️":
                await ctx.channel.send('哼~比你難得贏翻一次甘多多啦!')
            elif pc == "🍞":
                await ctx.channel.send("垃圾!我求其出個小籠包都贏你啊!")
    except asyncio.TimeoutError:
        why = ["你唔好聽日先出?","我寧願你彈弓手好過咯!","你以為bot就無生活可以等你成世?"]
        await ctx.channel.send(f"諗甘耐做咩?{random.choice(why)}")


@bot.command(name= 'passed')
async def exp_res(ctx, member: discord.Member=None):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/passed?avatar={member.avatar_url_as(format="png")}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'passed.png'))

@bot.command(name= 'jail')
async def exp_res(ctx, member: discord.Member=None):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/jail?avatar={member.avatar_url_as(format="png")}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'jail.png'))

@bot.command(name= 'communism')
async def exp_res(ctx, member: discord.Member=None):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/comrade?avatar={member.avatar_url_as(format="png")}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'comrade.png'))

@bot.command(name= 'pixel')
async def exp_res(ctx, member: discord.Member=None):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format="png")}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'pixelate.png'))

@bot.command(name= 'cm')
async def exp_res(ctx, member: discord.Member=None,*, message):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/youtube-comment?avatar={member.avatar_url_as(format="png")}&comment={message}&username={member.display_name}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'youtube-comment.png'))

@bot.command(name= 'dog')
async def exp_res(ctx, member: discord.Member=None, *, msg):
    if not member:
        member = ctx.author
    my_url = f'https://some-random-api.ml/canvas/its-so-stupid?avatar={member.avatar_url_as(format="png")}&dog={msg}' 
    async with aiohttp.ClientSession() as session:
        async with session.get(my_url) as resp:
            if resp.status != 200:
                return await ctx.channel.send('網絡唔穩定,你遲d再整過')
            data = io.BytesIO(await resp.read())
            await ctx.channel.send(file=discord.File(data, 'its-so-stupid.png'))

@bot.command(name='CAtime')
async def CAtime(context):
    tz_CA = pytz.timezone('America/Toronto')
    CA_T = datetime.now(tz_CA)
    await context.channel.send(CA_T.strftime("%a %d %b,%y %I:%M:%S %p"))

@bot.command(name='UKtime')
async def UK_T(message):
    tz_UK = pytz.timezone('Europe/London')
    UK_T = datetime.now(tz_UK)
    await message.channel.send(UK_T.strftime("%a %d %b,%y %I:%M:%S %p"))

@bot.command(name='HKtime')
async def HK_T(message):
    tz_HK = pytz.timezone('Asia/Hong_Kong')
    HK_T = datetime.now(tz_HK)
    await message.channel.send(HK_T.strftime("%a %d %b,%y %I:%M:%S %p"))


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user or message.author.bot == True:
        return
    username = str(message.author).split('#')[0]
    msg = message.content.lower()
    
    if msg.endswith(".gif") or msg.startswith("http"): 
        return

    if any(word in msg for word in sad_words):
        await react(message)
    
    if msg.startswith('ping'):
        await message.channel.send(f'{bot.latency*1000}(毫秒)')

    if any(word in msg for word in stel_la):
        tmpmsg = await message.channel.send('你講緊Stella?')
        time.sleep(3)
        await tmpmsg.delete()

    if ('比幾分' in msg):
        await message.channel.send(f'我比較公道,會比{random.randrange(10)}分!')

    if msg.startswith('bling'):
        await bling(message)

    if any(map(msg.startswith, greet_ings)):
        await message.add_reaction('<:LOVEU2:831585270398189600>')

    if ('雞湯' in msg):
        await message.channel.send(random.choice(poison_soup))

    if msg.startswith('挽'):
        await message.channel.send('https://tenor.com/view/holding-hands-dog-cars-gif-13660273')

    if msg.startswith('say'):
        tmp = message.content.split(" ", 1)
        if len(tmp) == 1:
            await message.channel.send('https://tenor.com/view/wow-what-say-what-gif-16598538')
        else:
            await message.delete()
            temp_mg = await message.channel.send(tmp[1])
            time.sleep(5)
            await temp_mg.delete()

    if ('joker' in msg):
        await message.channel.send('https://tenor.com/view/batman-joker-heath-ledger-clap-clapping-gif-11060757')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.channel.send("遺失參數")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.channel.send("無尼個cmd啊!係咪打錯字啊?")
    else:
        await ctx.channel.send({error})

staying_alive()
bot.run(os.getenv('TOKEN'))