import praw
import time
import os

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv(verbose=True)
class redditAPI(commands.Cog):

	def __init__(self,bot):
		self.user_agent = os.getenv('USER_AGENT')
		self.client_id = os.getenv('CLIENT_ID')
		self.client_secret = os.getenv('CLIENT_SECRET')
		self.username = os.getenv('USERNAME1')
		self.password = os.getenv('PASSWORD')
		self.reddit = praw.Reddit(client_id=self.client_id,client_secret=self.client_secret,password=self.password,user_agent=self.user_agent,username=self.username)
		self.print_creds();
		self.TINKER = set()
		self.TINKER1 = set()
		self.bot = bot


	def print_creds(self):
		# print(self.user_agent)
		# print(self.client_id)
		# print(self.client_secret)
		# print(self.username)
		# print(self.password)
		print("Checking Reddit Status",self.reddit.user.me())

	def sub(self,subreddit_name):
		print(subreddit_name)
		for submission in self.reddit.subreddit(subreddit_name).rising(limit=15):
			print("="*20)
			print("num_comments",submission.num_comments)
			print("upvote_ratio",submission.upvote_ratio)
			print("url",submission.url)
			print("title",submission.title)
			self.tinker(submission.title)
			print("selftext",submission.selftext)
			self.tinker(submission.selftext)
			submission.comments.replace_more(limit=5)
			for comment in submission.comments.list():
				print(comment.body)
				self.tinker1(submission.selftext)
			print("="*20)

		print("KEYWORDS title",self.TINKER)
		print("KEYWORDS comments",self.TINKER1)
		return self.TINKER

	def tinker(self,text):
		for sentence in text.split("."):
			for words in sentence.split(" "):
				if(words.isupper() and words.find("AM") and words.find("\n") and len(words)>1):
					self.TINKER.add(words)

	def tinker1(self,text):
		for sentence in text.split("."):
			for words in sentence.split(" "):
				if(words.isupper() and words.find("AM") and words.find("\n") and len(words)>1):
					self.TINKER1.add(words)

	@commands.command(name='reddit',pass_context=True)
	# @commands.has_role("Mod")
	async def acommand(self, ctx, args):
		await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
		for arg in args.split(" "):
			await ctx.send(str(self.sub(arg)));

	async def on_message(self, message):
		print(message.content)

def setup(bot):
	bot.add_cog(redditAPI(bot))


# reddit = redditAPI()
# print(reddit.print_creds())
# print(reddit.sub("wallstreetbets"))