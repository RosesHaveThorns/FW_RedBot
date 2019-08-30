## Help adn Info Commands for Red Bot

import discord
from discord.ext import commands

class Help(commands.Cog):
	
	def __init__(self, client):
		self.client = client
    
		# Get help File
		f = open('HELP.info', 'r+')
		self.helpContents = f.read()

		if readMe_contents == "":
			log("No Help File Found. Created Empty One")
		
		f.close()
	
	def set_refs(self, logger, sheets):
		self.logs = logger
		self.gsheet = sheets
		
# COMMAND: $help

	@commands.command()
	async def help(self):
		self.logs.log("'$help' command called")
		
		await message.channel.send(self.helpContents)
		
		log("Command Succesfull")
		
def setup(client):
	client.add_cog(Help(client))
