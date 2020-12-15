# bot.py
import os
from os import listdir
from os.path import isfile, join

import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
KEYWORDS = ["options","short","calls","puts","fuck","retard"]
TENDIEs_msg = ["This literally cannot go tits up.","Tomorrow is a bear market","SPY puts 3 months out","Retard bulls will be dominant for the foreseeable future","Why aren't you doing SPY calls fucking autist?","That's a good DD. I'm in.","Beautiful write up fag, i’m in.","Who the fuck are you playing tic tac toe with?"]
cogs_dir = "cogs"
description = 'AlphaWold is a Stock Tracker'

AW = commands.Bot(command_prefix='!', description=description)

@AW.event
async def on_ready():
	print('------')
	await AW.change_presence(activity=discord.Game("STOCK MARKET!"))
	print(f'{AW.user.name,AW.user.id} has connected to Discord!')
	print('------')
	

@AW.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: {args[0]}\n')
		else:
			raise

# @AW.command(name='reddit')
# async def search(ctx, *args):
#     await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
#     for i in range(len(args)):
#     	rAPI.sub(args[i])

@AW.event
async def on_message(message):
	print(message.content)
	if message.author == AW.user:
		return

	if AW.user.mentioned_in(message):
		await message.channel.send(random.choice(TENDIEs_msg))
	elif any(word in message.content.lower() for word in KEYWORDS):
		await message.channel.send(random.choice(TENDIEs_msg))
	elif "shutdown" in message.content.lower():
		print("Attempt to shutdown")
		await message.channel.send("SHOOTING FOR THE MOON :STONKS:")
		await AW.close()
	elif message.content == 'raise-exception':
		raise discord.DiscordException
	await AW.process_commands(message)

@AW.command()
async def unload(ctx,extension_name : str):
	"""
	For Testing Purpose: Unloading Extentions
	"""
	try:
		AW.unload_extension(extension_name)
		await ctx.send("{} unloaded.".format(extension_name))
	except (AttributeError, ImportError) as e:
		await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
		return
@AW.command()
async def load(ctx,extension_name: str):
	"""
	For Testing Purpose: Loading Extentions
	"""
	try:
		AW.load_extension(extension_name.split(".")[0])
		await ctx.send("{} loaded.".format(extension_name))
	except Exception as e:
		await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
		return
		
if __name__=="__main__":
	for file in listdir(cogs_dir):
		if isfile(join(cogs_dir,file)):
			file=file.split(".")
			if(file[1]=='py'):
				try:
					AW.load_extension(cogs_dir + "." + file[0])
				except Exception as extension:
					print(f'Failed to load extension {extension}.')

AW.run(TOKEN,bot=True, reconnect=True)
