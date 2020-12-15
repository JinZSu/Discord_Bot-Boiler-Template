from discord.ext import commands

#IEX API and commands into Discord

class IEX(commands.Cog):
	def __init__(self,bot):
		self.bot=bot

def setup(bot):
	bot.add_cog(IEX(bot))