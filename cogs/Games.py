## Games and Fun Commands for Red Bot

import discord
from discord.ext import commands
import random

class Games(commands.Cog):
	
	def __init__(self, client):
		self.client = client
	
	def set_refs(self, logger, sheets):
		self.logs = logger
		self.gsheet = sheets
		
# COMMAND: $dice <sides>

	@commands.command()
	async def dice(self, context):
		self.logs.log("'$dice' command called")
		
		msgOut = await context.message.channel.send(content='Rolling the Die, Clickety Clack...')
		failed = 0
		try:
			input = context.message.content.split(" ")[1].strip()
			max = int(input)

		except Exception as error:
			failed = 1
			self.logs.log("FAILED: <sides> Parameter Not an Integer")
			await msgOut.edit(content="<sides> Parameter Must be an Integer [{}]".format(error))

		if failed == 0:
			out = "The " + input + " sided die Landed On a **" + str(random.randint(1, max)) + "**"

			await msgOut.edit(content=out)
			self.logs.log("Command Succesfull, " + out)
		
def setup(client):
	client.add_cog(Games(client))
