"""Please do NOT abuse my api keys, get your own."""

import asyncio
import concurrent

import discord
import itertools
import numexpr
import os
import random
import re
import requests
import signal
import time
from PIL import Image, ImageOps, ImageDraw, ImageChops
from bs4 import BeautifulSoup
from io import BytesIO
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='$')  # bot prefix for all bot commands
bot.remove_command("help")  # replaces old help command with custom help
BOT_ID = 697040751871262771


"""EVENTS"""


@bot.event  # checks if bot is ready
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="//help"))
	print("Bot is ready!")


@bot.event  # responds to messages
async def on_message(message):
	if message.author == bot.user:
		return

	if message.content == "<@504493647316647936>":
		await message.channel.send("Bot prefix is **//**")
	await bot.process_commands(message)


"""GRAPHICS"""


def crop_to_circle(im):
	data = im.load()
	for x in range(im.size[1]):
		for y in range(im.size[0]):
			if data[x, y][3] == 0:
				data[x, y] = (255, 255, 255, 255)

	bigsize = (im.size[0] * 3, im.size[1] * 3)
	mask = Image.new('L', bigsize, 0)
	ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
	mask = mask.resize(im.size, Image.ANTIALIAS)
	mask = ImageChops.darker(mask, im.split()[-1])
	im.putalpha(mask)


@bot.command()  # Hugs specified user
async def hug(ctx, target: discord.Member, hugger: discord.Member = None):
	choices = [
		["https://i.pinimg.com/originals/09/7b/c0/097bc05f416c3af9c99d85a5563ca44c.png", (185, 80), (300, 60)],
		["https://data.whicdn.com/images/227674492/original.jpg", (30, 80), (135, 50)]
	]

	choice = random.choice(choices)

	base_img = Image.open(BytesIO(requests.get(choice[0]).content))
	hugger_img = Image.open(BytesIO(requests.get(ctx.message.author.avatar_url if hugger == None else hugger.avatar_url).content)).resize((135, 135)).convert("RGBA")
	target_img = Image.open(BytesIO(requests.get(target.avatar_url).content)).resize((135, 135)).convert("RGBA")

	crop_to_circle(hugger_img)
	crop_to_circle(target_img)

	base_img.paste(target_img, choice[1], target_img)
	base_img.paste(hugger_img, choice[2], hugger_img)
	base_img.save("_hug_temp.png")

	file = discord.File("_hug_temp.png", filename="image.png")
	embed = discord.Embed()
	embed.set_image(url="attachment://image.png")
	await ctx.send(file=file, embed=embed)


@hug.error  # error handling for hug command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Invalid `target` parameter.**")
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must give a `target` parameter.**")


@bot.command()
async def nyan(ctx):
	data = requests.get("https://nekos.life")
	soup = BeautifulSoup(data.content)
	tag0 = soup.find("div", attrs={"class":"w3-container w3-card-4 w3-center w3-purple"})
	tag1 = tag0.find("img").attrs["src"]

	embed = discord.Embed()
	embed.set_image(url=tag1)

	await ctx.send(embed=embed)


@bot.command(name="nuke-pic")  # sends picture of a nuke
async def nuke_pic(ctx):
	nukes = (
		"https://nationalinterest.org/sites/default/files/styles/desktop__1486_x_614/public/main_images/atomic_bomb.jpg?itok=cUVH4gSg",
		"https://i.kinja-img.com/gawker-media/image/upload/s--WUTtaPrX--/c_scale,f_auto,fl_progressive,q_80,w_800/jfjo1ikh3pffcavavgiw.jpg",
		"https://i.ytimg.com/vi/-1JFKU9fJfM/hqdefault.jpg",
		"https://www.defencetalk.com/wp-content/uploads/2017/02/poland-wants-us-or-european-nuclear-umbrella-kaczynski-01.jpg",
		"https://c.ndtvimg.com/2018-10/jb1etgrk_nuclear-test-generic-istock_625x300_23_October_18.jpg",
		"https://nationalinterest.org/sites/default/files/styles/resize-1440/public/main_images/Nuclear%20Bomb_0.jpg?itok=_-GjiOrF",
		"https://www.radionz.co.nz/assets/news_crops/42527/eight_col_bravocolor1.jpg?1505707045",
		"http://media2.govtech.com/images/940*630/nuc+%282%292.jpg",
		"https://thumbs-prod.si-cdn.com/sIkNe_eIDylRJqhqZX7gk2KHtYc=/800x600/filters:no_upscale()/https://public-media.si-cdn.com/filer/dd/44/dd44ce31-4cc3-46c0-9378-0ec0da5a13e0/02_10_2014_romeo_nuke.jpg",
		"https://t2.rbxcdn.com/80a408a9af72d79bc34ee4ec0eede71c",
		"https://thenypost.files.wordpress.com/2017/05/051917-nuke-nasa-1.jpg?quality=90&strip=all&w=618&h=410&crop=1",
		"http://c0.thejournal.ie/media/2015/09/mars-nuke-752x501.jpg",
		"https://www.theamericanconservative.com/wp-content/uploads/2016/10/Nuclear2-554x350.jpg",
		"https://nationalpostcom.files.wordpress.com/2016/08/529235836.jpg?quality=80&strip=all&w=780",
		"http://www.52dazhew.com/data/out/173/586952801-nuke-wallpapers.jpg",
		"https://vignette.wikia.nocookie.net/dbz-dokkanbattle/images/2/23/Nuke.gif/revision/latest?cb=20170420230427"
	)

	embed = discord.Embed()
	embed.set_image(url=random.choice(nukes))

	await ctx.send(embed=embed)


@bot.command(name="dog-pic")  # sends picture of a dog
async def dog_pic(ctx):
	dog_data = requests.get("https://dog.ceo/api/breeds/image/random").json()
	embed = discord.Embed()
	embed.set_image(url=dog_data["message"])

	await ctx.send(embed=embed)


@bot.command(name="cat-pic")  # sends picture of a cat
async def cat_pic(ctx):
	api_key = "ca183891-47a4-4ae7-ae2a-c62af21cea04"
	cat_data = requests.get("https://api.thecatapi.com/v1/images/search?format=json&x-api-key=" + api_key).json()
	embed = discord.Embed()
	embed.set_image(url=cat_data[0]["url"])

	await ctx.send(embed=embed)


@bot.command()
async def meme(ctx):
	meme_data = requests.get("http://alpha-meme-maker.herokuapp.com/{}".format(random.randint(1, 11))).json()
	embed = discord.Embed()
	embed.set_image(url=meme_data["data"][random.randint(0, len(meme_data["data"]) - 1)]["image"])

	await ctx.send(embed=embed)


@bot.command(name="st-pic")
async def st_pic(ctx, st_type = None):
	st_text = ("[;]>", "(;)>", "{;}>", "|;|>", r"/;\\>", "[;)>", "£[;]>")
	embed = discord.Embed()

	if st_type is None:
		await ctx.send("**You must enter an** `st_type` **parameter. `type = [text, paint, ink, draw]`.**")
	elif st_type.lower() == "text":
		await ctx.send(random.choice(st_text))
	elif st_type.lower() == "paint":
		await ctx.send(embed=embed.set_image(url="https://i.imgur.com/WM5NVjT.png"))
	elif st_type.lower() == "ink":
		await ctx.send(embed=embed.set_image(url="https://i.imgur.com/q8TSLm9.png"))
	elif st_type.lower() == "draw":
		await ctx.send(embed=embed.set_image(url="https://i.imgur.com/d8GazB7.png"))
	else:
		await ctx.send("**Invalid `st_type` parameter. Type `//st-pic` for more info.**")


"""RANDOM"""


@bot.command()  # checks the bot latency
async def ping(ctx):
	await ctx.send('**Ping in {0}ms**'.format(round(bot.latency * 1000, 1)))


@bot.command(name="pig-latin")  # converts to pig latin
async def pig_latin(ctx, *args):
	await ctx.send(' '.join(re.sub('y*([^aeiou]+)(.*)', r'\2\1ay', 'y' + i) for i in args))


@bot.command()  # repeats the input
async def cat(ctx, *args):
	await ctx.send(" ".join(args))


@bot.command()  # roll a dice
async def roll(ctx, sides = 6):
	await ctx.send("You rolled a {}.".format(random.randint(1, sides)))

@roll.error  # error handling for roll command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**`sides` must be a natural number.**")


@bot.command()  # flip a coin
async def flip(ctx):
	sides = ["heads"] * 10 + ["tails"] * 10 + ["the coin on its side!"]
	await ctx.send("You flipped {}.".format(random.choice(sides)))


@bot.command()  # picks a random card from a deck of cards
async def card(ctx):
	value = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King")
	suit = ("Diamonds", "Clubs", "Hearts", "Spades")
	await ctx.send("Your card is the **{} of {}**.".format(random.choice(value), random.choice(suit)))


@bot.command(name="8ball")  # a magic 8-ball
async def eight_ball(ctx, *args):
	if len(args) == 0:
		return await ctx.send("**Must ask a yes/no question.**")

	question = ""
	for word in args:
		question += word
		question += " "

	responses = ("Signs point to yes.", "Yes.", "Reply hazy.", "Try again.", "Without a doubt.", "My sources say no.",
				 "As I see it, yes.", "You may rely on it.", "Concentrate and ask again.",  "Outlook not so good.",
				 "It is decidedly so.", "Better not tell you now.", "Very doubtful.", "Yes - definitely.",
				 "It is certain.", "Cannot predict now.", "Most likely.", "Ask again later.", "My reply is no.",
				 "Outlook good.", "Don\'t count on it.", "Who cares?", "Never, ever, ever.", "Possibly.",
				 "There is a small chance.")

	await ctx.send(responses[len(str(question)) % 25])


@bot.command(name="f-cookie") # tells a fortune from a cookie
async def fortune_cookie(ctx):
	fortunes = ("Your future will come with riches.", "You open your heart to people you care for.", "Something you have longed for will no longer be a dream.",
				"The fortune you seek is in another cookie.", "A cynic is only a frustrated optimist.", "A foolish man listens to his heart. A wise man listens to cookies",
				"The greatest danger may very well be your stupidity.", "Avoid taking unnecessary gambles. Lucky numbers: 13, 27, 35, 65, 78",
				"This cookie contains 117 calories.", "If a turtle doesn't have a shell, is it naked or homeless?",
				"Don't eat the paper.", "It is a good day to have a good day.", "He who laughs at himself never runs out of things to laugh at.")
	await ctx.send(random.choice(fortunes))


"""INFORMATION"""


@bot.command()  # help command for new users
async def help(ctx, category = None):
	if category == None:
		await ctx.send("`//help <category>`. **Parameters: `Graphics`, `Random`, `Info`, `Config`, `Fun`, `Util`**")
		return

	f = open("help.asc", "r").read().split("\n")
	embed = discord.Embed(colour=discord.Colour.orange())
	embed.set_author(name="Help", icon_url=bot.user.avatar_url)

	try:
		temp = title = ""
		for line in f[f.index("[{}]".format(category.title())):]:
			if line.startswith("["):
				title = line[1:-1]
			elif "---" in line:
				embed.add_field(name=category, value=temp, inline=False)
				break
			else:
				split = line.rstrip().split("|")
				temp += "`{}`\n{}\n\n".format(split[0], split[1])
		await ctx.send(embed=embed)
	except ValueError:
		await ctx.send("**Not a valid category! Type `//help` for more details.**")


@bot.command(name="user-avatar")  # generates picture of user's avatar
async def user_avatar(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author
	await ctx.send(member.avatar_url)


@user_avatar.error  # error handling for user-avatar command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-id")  # shows user's id
async def user_id(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author
	await ctx.send("{0.mention}: {0.id}".format(member))


@user_id.error  # error handling for user-id command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-name")  # shows user's name
async def user_name(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author
	await ctx.send("{0.mention}: {0.name}".format(member))


@user_name.error  # error handling for user-name command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-status")   # shows user's status
async def user_status(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author

	if member.status == discord.Status.online:
		await ctx.send("**{}: Online**".format(member.mention))
	elif member.status == discord.Status.offline:
		await ctx.send("**{}: Offline**".format(member.mention))
	elif member.status == discord.Status.dnd:
		await ctx.send("**{}: Do Not Disturb**".format(member.mention))
	else:
		await ctx.send("**{}: Idle**".format(member.mention))


@user_status.error  # error handling for user-status command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-joined")  # shows when user joined
async def user_joined(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author
	await ctx.send("{0.mention}: {0.joined_at}".format(member))


@user_joined.error  # error handling for user-joined command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-roles")  # shows user's roles
async def user_roles(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author

	roles = member.roles
	del roles[0]

	await ctx.send(member.mention + ':')
	for role in roles:
		await ctx.send(role)


@user_roles.error  # error handling for user-roles command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-toprole")  # shows user's top role
async def user_toprole(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author
	await ctx.send("{0.mention}: {0.top_role}".format(member))


@user_toprole.error  # error handling for user-toprole command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-info")  # shows all user's info
async def user_info(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.author
	embed = discord.Embed(colour=discord.Color.blue())
	embed.add_field(name="Name: ", value=member.name, inline=False)
	embed.add_field(name="ID: ", value=member.id, inline=False)
	embed.add_field(name="Status: ", value=member.status, inline=False)
	embed.add_field(name="Joined: ", value=member.joined_at, inline=False)
	embed.add_field(name="Top Role: ", value=member.top_role, inline=False)
	embed.add_field(name="Avatar URL: ", value=member.avatar_url, inline=False)

	await ctx.send(embed=embed)


@user_info.error  # error handling for user-info command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("**Parameter must be a member.**")


@bot.command(name="user-list")  # shows server's members
async def user_list(ctx):
	embed = discord.Embed(colour=discord.Colour.blue())
	for member in ctx.guild.members:
		embed.add_field(name=member, value=member.top_role, inline=False)
	await ctx.send(embed=embed)


"""CONFIG"""


@bot.command(name="add-reaction")  # adds reaction
async def add_reaction(ctx, ID, emoji, channel = None):
	print(emoji)
	channel_obj = ctx.channel if channel == None else ctx.get_channel(channel)
	msg = await ctx.channel.fetch_message(ID)
	await msg.add_reaction(emoji)
	await ctx.message.delete()


@add_reaction.error  # error handling for add-reaction command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Requires **ID** and **emoji** parameters.")


@bot.command(name="del-reaction")  # deletes reaction
async def del_reaction(ctx, ID, emoji, channel = None):
	channel_obj = ctx.channel if channel == None else ctx.get_channel(channel)
	msg = await ctx.channel.fetch_message(ID)
	await msg.remove_reaction(emoji, bot.user)
	await ctx.message.delete()


@del_reaction.error  # error handling for del-reaction command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Requires **ID** and **emoji** parameters.")


@bot.command()  # clears inputted channel
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 499):
	try:
		if amount in tuple(range(1, 500)):
			await ctx.channel.purge(limit=amount+1)
		else:
			await ctx.send("`amount` **must be an integer between 1 and 500.**")
	except discord.Forbidden:
		await ctx.send("**This bot does not have the permissions to use this command.**")


@clear.error  # error handling for clear command
async def on_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("`amount` **must be an integer between 1 and 500.**")


@bot.command()  # bans specified user
async def ban(ctx, member: discord.Member, reason = None):
	try:
		await bot.ban(member, reason=reason)
		await ctx.send("**{} has been kicked.**".format(member.mention))
	except discord.Forbidden:
		await ctx.send("**This bot does not have the permissions to use this command.**")


@bot.command()  # kicks specified user
async def kick(ctx, member: discord.Member, reason = None):
	try:
		await member.kick(reason=reason)
		await ctx.send("**{} has been kicked.**".format(member.mention))
	except discord.Forbidden:
		await ctx.send("**This bot does not have the permissions to use this command.**")


@bot.command(name="create-role")  # creates a role
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, name):
	try:
		await ctx.guild.create_role(name=name)
	except discord.Forbidden:
		await ctx.send("**This bot does not have the permissions to use this command.**")


@create_role.error  # error handling for create-role command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Requires a `name` parameter.**")


@bot.command(name="give-role")  # gives a role to a specific user
@commands.has_permissions(manage_roles=True)
async def give_role(ctx, _name, member: discord.Member = None):
	if member is None:
		member = ctx.author
	role = discord.utils.get(member.guild.roles, name = _name)
	await member.add_roles(role)


@give_role.error  # error handling for give-role command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Requires a `name` parameter.**")


"""FUN"""


@bot.command()
async def servers(ctx):
	await ctx.send(str(len(bot.guilds)))


@bot.command()
async def wyr(ctx, *option):
	if len(option) == 0:
		embed0 = discord.Embed()
		embed0.add_field(name="`//wyr pick <index>`", value="Plays a round of Would-You-Rather. `<index>` is an integer which denotes the question being asked (0, 1, and 2 are the default questions). A blank `<index>` parameter results in a random question being chosen.")
		embed0.add_field(name="`//wyr erase`", value="Erases all data collected. Only administrators may use this command.")
		embed0.add_field(name="`//wyr create`", value="Creates a custom Would-You-Rather question. Format is `//wyr create option1|option2`.")

		await ctx.send(embed=embed0)
		return

	fn = "_wyr_{}.asc".format(ctx.message.guild.id)
	f = ""
	def_q = [
			"Be the only smart person in the world | Be the only dumb person in the world",
			"Lose both your legs | Lose both your arms",
			"Know the time of your death | Know how you will die"
	]

	try:
		f = open(fn, "r")
	except FileNotFoundError:
		f = open(fn, "w")

		for i in def_q:
			f.write(i + "\n")
			f.write("---\n")
	f.close()

	if option[0] == "pick":
		f = open(fn, "r+")
		parse = [i.split("\n")[:-1] for i in f.read().split("---\n")][:-1]
		f.close()

		pick = 0
		if len(option) > 1:
			try:
				pick = int(option[1])
				if pick < 0 or pick >= len(parse):
					await ctx.send("`pick <index>` parameter is out of bounds.")
					return
			except ValueError:
				await ctx.send("`pick <index>` parameter must be a non-negative integer.")
				return

		if pick is None:
			pick = random.randint(0, len(parse) - 1)
		print(parse)
		question = parse[pick][0].split("|")
		col = random.randint(0, 0xFFFFFF)

		embed0 = discord.Embed(colour=col)
		embed0.add_field(name="Would you rather...", value=":zero: {}\n\n**OR**\n\n:one: {}".format(question[0], question[1]), inline=False)
		embed0.set_footer(text="Text '1' or '0' to submit!")

		msg = await ctx.send(embed=embed0)

		try:
			response = await bot.wait_for("message", timeout=20, check=lambda message: message.author == ctx.author)
			if response.content == "1" or response.content == "0":
				for i in range(1, len(parse[pick])):
					if str(ctx.message.author.id) in parse[pick][i]:
						parse[pick][i] = str(ctx.message.author.id) + " " + response.content
						break
				else:
					parse[pick].append(str(ctx.message.author.id) + " " + response.content)

				cnt0 = cnt1 = 0
				for i in parse[pick][1:]:
					if int(i.split(" ")[0]) != ctx.message.author.id:
						res = int(i.rstrip().split(" ")[1])
						if res == 0:
							cnt0 += 1
						else:
							cnt1 += 1

				embed1 = discord.Embed(colour=col)
				try:
					prob = (cnt1 if response.content == "1" else cnt0) / (cnt0 + cnt1)
					embed1.add_field(name="Results", value="**You agree with {}% of the people in this server!**".format(round(prob * 100, 1)))
				except ZeroDivisionError:
					embed1.add_field(name="Results", value="**You are the first to vote for this question!**")

				embed1.set_footer(text="Total Participants: {}".format(str(len(parse[pick][1:]))))
				await ctx.send(embed=embed1)

				p_to_s = ""
				for p in parse:
					for i in p:
						p_to_s += i + "\n"
					p_to_s += "---\n"
				open(fn, "w").write(p_to_s)
			else:
				await ctx.send("**That is not a valid response. Enter either `1` or `0`.**")
		except asyncio.TimeoutError:
			await ctx.send("**Sorry, you took too long.**")
		f.close()
	elif option[0] == "create":
		choices = " ".join(option[1:]).split("|")
		if len(choices) != 2:
			await ctx.send("**Invalid question format. Try `//wyr` for more info.**")
			return

		f = open(fn, "r+")
		parse = [i.split("\n")[:-1] for i in f.read().split("---\n")][:-1]
		f.close()

		for p in parse:
			if choices == p[0].split(" | "):
				await ctx.send("**This Would-You-Rather question already exists.**")
				return

		f = open(fn, "a")
		f.write("Would you rather {} | {}?\n---\n".format(choices[0], choices[1]))
		f.close()

		await ctx.send("**Successfully created new question!**")

	elif option[0] == "erase":
		if ctx.message.author.permissions_in(ctx.message.channel).administrator:
			os.remove("_wyr_{}.asc".format(ctx.message.guild.id))
			await ctx.send("**Successfully erased all data.**")
		else:
			await ctx.send("**You must have the `administrator` permission to run this command.**")
	else:
		await ctx.send("**Invalid `option` parameter. Type `//wyr` for more info.**")

@bot.command()  # makes bot send custom animated emoji (unlisted)
async def amoji(ctx, ID):
	await ctx.send(f"{bot.get_emoji(int(ID))}")
	await ctx.message.delete()

@bot.command()  # bot says a joke
async def joke(ctx, joke_type):
	if joke_type.lower() == "ym":
		yo_momma = ("fat, I took a picture of her last Christmas and it's still printing.",
					"fat when she got on the scale it said, 'I need your weight not your phone number.'",
					"fat and old when God said, 'Let there be light', he asked your mother to move out of the way.",
					"fat she doesn't need the internet, because she's already world wide.",
					"fat, when she sat on an iPod, she made the iPad!",
					"fat she walked past the TV and I missed 3 episodes.",
					"ugly when she tried to join an ugly contest they said, 'Sorry, no professionals.'",
					"ugly she made One Direction go another direction.",
					"ugly Fix-It Felix said, 'I can\'t fix it.'"
					"stupid when an intruder broke into her house, she ran downstairs, dialed 9-1-1 on the microwave, and couldn't find the 'CALL' button.",
					"stupid she stuck a battery up her ass and said, 'I GOT THE POWER!'",
					"stupid that she sat on the TV to watch the couch.")
		await ctx.send("**Hey {}**, Yo momma so {}".format(ctx.author.name, random.choice(yo_momma)))
	elif joke_type.lower() == "kk":
		await ctx.send("Knock Knock.")

		if ctx.author.bot == bot.user:
			return

		try:
			wt_response = await bot.wait_for("message", timeout=10, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
			if wt_response.content.lower() in ("who's there", "who's there?"):
				kk = [["A little old lady", "All this time, I did not know you could yodel."],
					  ["Cow says", "Cow says mooooo!"],
					  ["Etch", "Bless you, friend."],
					  ["Robin", "Now hand over the cash."],
					  ["Cash", "No thanks, I'll have some peanuts."],
					  ["Mustache", "I mustache you a question, but I'll shave it for later."],
					  ["Tank", "You're welcome."],
					  ["Candice", "Candice door open, or what?"],
					  ["Boo", "No need to cry, it's only a joke."],
					  ["Howl", "Howl you know unless you open this door?"],
					  ["Iran", "Iran all the way here. Let me in already!"]]

				joke_num = random.randint(0, 9)
				chosen_joke = [kk[joke_num][0], kk[joke_num][1]]
				await ctx.send(chosen_joke[0])

				try:
					xwho_response = await bot.wait_for("message", timeout=20, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
					xwho_response = xwho_response.lower()
					if xwho_response.content in ("{} who".format(chosen_joke[0].lower()), "{} who?".format(chosen_joke[0].lower())):
							await ctx.send(chosen_joke[1])
					else:
						await ctx.send("**Must reply with '{0} who or '{0} who?'.**".format(chosen_joke[0].lower()))
				except asyncio.TimeoutError:
					await ctx.send("**Sorry, {}, you took too long.**".format(ctx.author.mention))
			else:
				await ctx.send("**You must answer with** `who\'s there` **or** `who\'s there?`**.**")
		except asyncio.TimeoutError:
			await ctx.send("**Sorry, {}, you took too long.**".format(ctx.author.mention))
	else:
		await ctx.send("**Invalid `type` parameter.** `type = [ym, kk]`")


@joke.error  # error handling for joke command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must give a `type` parameter. `type = [ym, kk]`**")


@bot.command()  # plays rock-paper-scissors
async def rps(ctx):
	await ctx.send("Welcome to Rock, Paper, Scissors. **Please select a weapon: (`rock`, `paper`, `scissors`).**")

	choices = ("rock", "paper", "scissors")

	computer = random.choice(choices)
	try:
		player = await bot.wait_for("message", timeout=10, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
	except asyncio.TimeoutError:
		return await ctx.send("**Sorry, {}, you took too long.**".format(ctx.author.mention))

	if player.content.lower() not in choices:
		return await ctx.send("**That is not a valid choice.**")

	beats = {
		"rock": ["paper"],
		"paper": ["scissors"],
		"scissors": ["rock"]
	}

	if player.content.lower() == computer:
		await ctx.send("**Tie!** You both chose {}.".format(computer))
	elif player.content.lower() in beats[computer]:
		await ctx.send("**You win!** You chose {}, Computer chose {}.".format(player.content, computer))
	else:
		await ctx.send("**You lose!** You chose {}, Computer chose {}.".format(player.content, computer))


@bot.command(name="guess-num")  # plays guess-a-number
async def guess_num(ctx):
	try:
		await ctx.send("Pick an integer between 1 and 100.")
		if ctx.author == bot.user:
			return

		try:
			guess = await bot.wait_for("message", timeout=10.0, check=lambda message: message.author == ctx.author)
		except asyncio.TimeoutError:
			return await ctx.send("**Sorry {}, you took too long.**".format(ctx.author.mention))

		answer = random.randint(1, 100)
		counter = 0
		while True:
			if ctx.author == bot.user:
				return

			counter += 1
			if int(guess.content) not in tuple(range(1, 101)):
				await ctx.send("**Must pick an integer between 1 and 100.**")
				counter -= 1
			elif int(guess.content) > answer:
				await ctx.send("**Your guess is too high. Guess again.**")

				try:
					guess = await bot.wait_for("message", timeout=10.0, check=lambda message: message.author == ctx.author)
				except asyncio.TimeoutError:
					return await ctx.send("**Sorry {}, you took too long.**".format(ctx.author.mention))
			elif int(guess.content) < answer:
				await ctx.send("**Your guess is too low. Guess again.**")

				try:
					guess = await bot.wait_for("message", timeout=10.0, check=lambda message: message.author == ctx.author)
				except asyncio.TimeoutError:
					return await ctx.send("**Sorry, {}, you took too long.**".format(ctx.author.mention))
			else:
				if counter <= 1:
					return await ctx.send("**Congratulations!** You got it on your first attempt.")
				else:
					return await ctx.send("**You are correct!** It took you {} attempts to get it.".format(counter))
	except ValueError:
		await ctx.send("**Not an integer between 1 and 100.**")


@bot.command()  # roasts a given user
async def roast(ctx, member: discord.Member):
	roasts = ("I'd give you a nasty look, but you've already got one.",
			  "I love what you’ve done with your hair. How do you get it to come out of the nostrils like that?",
			  "It looks like your face caught fire and someone tried to put it out with a hammer.",
			  "Just because you have one doesn’t mean you need to act like one.",
			  "I’m sorry, was I meant to be offended? The only thing offending me is your face.",
			  "You are proof that evolution can go in reverse.",
			  "I thought of you today. It reminded me to take the garbage out",
			  "I’d slap you but I don’t want to make your face look any better.",
			  "Were you born on the highway? That is where most accidents happen.",
			  "Shut up, you'll never be the man your mother is.")
	await ctx.send("Hey {}, {}\n🔥🔥🔥😝😝".format(member.mention, random.choice(roasts)))


@roast.error  # error handling for roast command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must give a `member` to roast at.**")
	elif isinstance(error, commands.BadArgument):
		await ctx.send("**Not a valid `member`.**")


@bot.command()  # prints a specified emoji
async def emoji(ctx, type):
	if type == "frozen":
		await ctx.send("The ❄️ 🌟 🔦 ⚪ on the mountain 🌙 🌠. 🙅🏻 a👣 to 🐝 👀. A 🏰 of 😢, and it 👀\n"
					   "like☝️️ the 👑. The 💨 is 🐺 like this 🌀 ❄️ ☔️ 🏠. 🙅🏻 keep it in, ☁️ 💡 ☝️️ tried. 🙅🏻 let\n"
					   "👬👫 in,🙅🏻 let 👬👫 👀. 🐝 the 👍 👧 👇 always have to 🐝. 🙅🏻, don't 👐, 🚫 let 👬\n"
					   "👫💡. Well now 👬👫 💡. 👐 it 🚗,, 👐 it 🚗,,🙅🏻 ✊ it back anymore. 👐 it 🚗,, 👐 it\n"
					   "🚗, turn ✈️ and 🔨 the 🚪. ☝️️ 🚫 care, what 👬👫 going to 👄, let the ☔️ ⚡ ❄️ 😡\n"
					   "on, the ❄️ ⛄️ 🙅🏻 bothered ☝️️ anyway. It's 😜😂 how some ✈️ 🚆 makes everything\n"
					   "😳 🐜. And the 😱 that once 👮 me, 🙅🏻 get to☝️️ at all. It's 🕓 to 👀 what☝️️ can do. To\n"
					   "📝 the 📊 and 🔨 through. 🚫 👍 , 🚫 👎, 🚫 👮 for ☝️️. ☝️️ 🏃. 👐 it 🚗,, 👐 it 🚗., ☝️\n"
					   "am ☝️ with the 🌀 and 🌌. 👐 it 🚗,, 👐 it 🚗..👇 🙅🏻 👀 ☝️️ 😭 . 👉 ☝️️ 🚶, and 👉 ☝️\n"
					   "stay. Let the⚡ ❄️ 😡 on. ☝️️ 💪 ❄️ through the 🌀 into the 🌎.☝️️ 👤 is 🌀 in ❄️ ⛄️\n"
					   "fractals all 🔁. And 1️⃣💡 💎 like an ❄️ 📢. ☝️️ 🙅🏻 🏃 back, the past is in the past. 👐 it\n"
					   "🚗,,👐 it 🚗,. And ☝️️ 🚀 like the 💔 of 🌌. 👐 it 🚗,, 👐 it 🚗.. That 💁 is 🚫. Here\n"
					   "☝️️ 🚶, in the 🔦 of ☀️. Let the ⚡ ❄️ 😡 on, the ❄️ ⛄️ 🙅🏻 bothered ☝️️ anyway.")
	elif type == "up":
		await ctx.send("⁣          🎈🎈  ☁️\n"
					   "         🎈🎈🎈\n"
					   " ☁️   🎈🎈🎈🎈\n"
					   "       🎈🎈🎈🎈\n"
					   "   ☁️   ⁣🎈🎈🎈\n"
					   "             | | |\n"
					   "             🏠   ☁️\n"
					   "   ☁️         ☁️\n"
					   "🌳🌹🏫🌳🏢🏢_🏢🏢🌳🌳")
	elif type == "man":
		if not ctx.channel.is_nsfw():
			return await ctx.send("**You can't use this command here.**")

		await ctx.send("☝️️       👨\n"
					   "🐛💤👔 🐛\n"
					   "             ⛽️     👢\n"
					   "              ⚡️ 8=👊 =D💦\n"
					   "       🎺      🍗                💦\n"
					   "       👢        👢                 🙆🏻")
	elif type == "chess":
		await ctx.send("🏰🏇⛪👸👱⛪🏇🏰\n"
					   "😶😶😶😶😶😶😶😶\n"
					   "🔳🔲🔳🔲🔳🔲🔳🔲\n"
					   "🔳🔲🔳🔲🔳🔲🔳🔲\n"
					   "🔳🔲🔳🔲🔳🔲🔳🔲\n"
					   "🔳🔲🔳🔲🔳🔲🔳🔲\n"
					   "👶👶👶👶👶👶👶👶\n"
					   "🏃🐴👼👰🙇👼🐴🏃")


@emoji.error  # error handling for emoji command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must give a `type` parameter.**")


@bot.command()  # kills a specified user
async def kill(ctx, member: discord.Member, *args):
	verbs = (
		"blended *(in blender)*",
		"stomped on several times",
		"absolutely demolished",
		"drowned, beaten, hammered, stabbed, and poisoned 43 times",
		"bored to death (literally)",
		"ran over",
		"wrapped into a dumpling and then eaten",
		"gruelingly dissected",
		"chopped into tiny, sub-atomic particles",
	)

	if member.id == BOT_ID:
		await ctx.send("You can't make me kill myself!")
	else:
		await ctx.send("{} was {} by {}.".format(member.mention, random.choice(verbs), " ".join(args)))


"""UTILITIES"""


yt_api_key = "AIzaSyBR68aLaWlBarv_g-ND8afn_JnSSjqdU4w"  # youtube api-key


@bot.command(name="sub-count")  # gets sub count of any youtuber
async def sub_count(ctx, username):
	try:
		user_data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + username.lower() + "&key=" + yt_api_key).json()
		user_subs = user_data["items"][0]["statistics"]["subscriberCount"]

		await ctx.send("**{}**: {}".format(username, user_subs))
	except IndexError:
		await ctx.send("**Not a valid username.**")


@sub_count.error  # error handling for sub-count command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must give a `username` parameter.**")


@bot.command(name="view-count")  # gets view count of any youtuber
async def view_count(ctx, username):
	try:
		user_data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + username.lower() + "&key=" + yt_api_key).json()
		user_views = user_data["items"][0]["statistics"]["viewCount"]

		await ctx.send("**{}**: {}".format(username, user_views))
	except IndexError:
		await ctx.send("**Not a valid username.**")


@view_count.error  # error handling for view-count command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must give a `username` parameter.**")


@bot.command(name="video-count")  # gets video count of any youtuber
async def video_count(ctx, username):
	try:
		user_data = requests.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=" + username.lower() + "&key=" + yt_api_key).json()
		user_videos = user_data["items"][0]["statistics"]["videoCount"]

		await ctx.send("**{}**: {}".format(username, user_videos))
	except IndexError:
		await ctx.send("**Not a valid username.**")


@video_count.error  # error handling for video-count command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must give a `username` parameter.**")


@bot.command()  # gets bitcoin value in a currency type
async def bitcoin(ctx, currency="CAD"):
	try:
		bitcoin_data = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
		currency_data = requests.get("https://api.exchangeratesapi.io/latest").json()
		fullname_data = requests.get("https://gist.githubusercontent.com/Fluidbyte/2973986/raw/b0d1722b04b0a737aade2ce6e055263625a0b435/Common-Currency.json").json()
		base_currency = bitcoin_data["bpi"]["EUR"]["rate"].replace(',', '')

		if currency.upper() == "EUR":
			value = float(base_currency)
		else:
			value = float(base_currency) * float(currency_data["rates"][currency.upper()])
		await ctx.send("**{}:** ${}".format(fullname_data[currency.upper()]["name"], round(value, 2)))
	except KeyError:
		await ctx.send("`{}` **is not a valid currency type.**".format(currency))


@bot.command()  # gets the forecast of a specific city
async def forecast(ctx, city, data):
	try:
		forecast_data = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&APPID=8284a846ac560add042f60ab4c7ce7e0".format(city.capitalize())).json()

		if data.lower() == "temp":
			await ctx.send("**Temperature:** {}°C".format(round(float(forecast_data["main"]["temp"]) - 273.15, 1)))
			await ctx.send("**Low:** {}°C".format(round(float(forecast_data["main"]["temp_min"]) - 273.15, 1)))
			await ctx.send("**High:** {}°C".format(round(float(forecast_data["main"]["temp_max"]) - 273.15, 1)))
		elif data.lower() == "weather":
			await ctx.send("**Weather:** {} ({})".format(forecast_data["weather"][0]["main"], forecast_data["weather"][0]["description"]))
		elif data.lower() == "air":
			await ctx.send("**Humidity:** {}%".format(round(float(forecast_data["main"]["humidity"]), 1)))
			await ctx.send("**Wind Speed:** {} km/h".format(round(float(forecast_data["wind"]["speed"]), 1)))
		else:
			await ctx.send("`{}` **is not a valid data. (**`data` **=** `temp`**,** `weather`**,** `air` **|** `city` = **name of city**)".format(data))
	except KeyError:
		await ctx.send("`{}` **is not a city name.**".format(city))


@forecast.error  # error handling for forecast command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must enter** `city` **and** `data` **parameters.**")


@bot.command()  # gets a definition of a word from the urban dictionary
async def urban(ctx, *word):
	if not ctx.channel.is_nsfw():
		return await ctx.send('**Channel must be NSFW to use this command.**')
	
	data = requests.get("http://www.urbandictionary.com/define.php?term={}".format('+'.join(word)))
	soup = BeautifulSoup(data.content)
	definition = soup.find("div", attrs={"class":"meaning"}).text.replace("<br/>", "\n")

	for word in open("banned_words.asc"):
		definition = re.sub(r"(\b{}\b)".format(word.rstrip()), r"||\1||", definition, flags=re.IGNORECASE)

	await ctx.send("**Invalid word**" if not definition else "**Definition:\n** {}".format(definition))


@urban.error  # error handling for urban command
async def on_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Must enter** `word` **parameter.**")


@bot.command()  # sends the link to a Wikipedia article
async def wiki(ctx, *args):
	name = ""
	for word in args:
		name += word + " "
	name = name[:-1].replace(" ", "_")

	if len(args) == 0:
		await ctx.send("**Must enter a Wikipedia article.**")
		return
	elif requests.get("https://en.wikipedia.org/wiki/{}".format(name)).status_code != 200:
		await ctx.send("**Wikipedia article does not exist.**")
		return

	wiki_data = "https://en.wikipedia.org/wiki/{}".format(name.lower())
	await ctx.send(wiki_data)

@bot.command()  # searches for youtube videos
async def yt(ctx, *args):
	search = ""
	for word in args:
		search += word + " "
	search = search.replace(" ", "+")

	yt_url = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&q={}&key={}".format(search, yt_api_key)).json()
	if len(yt_url["items"]) == 0:
		await ctx.send("**No results found.**")

	for vid in range(0, 5):
		await ctx.send("**[{}]:** {}".format(vid + 1, yt_url["items"][vid]["snippet"]["title"]))

	def check(m):
		return m.author == ctx.author and m.channel == ctx.channel

	await ctx.send("\n*Input the number of the video you wish to choose.*")
	num = await bot.wait_for("message", check=check, timeout=10)

	if num is None:
		await ctx.send("**Sorry, you took too long.**")
	elif int(num.content) in (tuple(range(1, 6))):
		await ctx.send("https://www.youtube.com/watch?v={}".format(yt_url["items"][int(num.content) - 1]["id"]["videoId"]))
	else:
		await ctx.send("**You must enter a number between 1 and 5.**")


bot.run("NzQ2ODI0ODIzMTMyNTIwNTE4.X0F80Q.uEGwaOjm6NGpRag4LjtFxrTY37Y"),   # run the bot
