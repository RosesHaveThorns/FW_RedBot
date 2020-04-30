## Moderation Commands for Red Bot

import datetime
import discord
from discord.ext import commands

class Moderation(commands.Cog):
  
  	reportChannelID = 618169388327108639
	muteRoleID = 618186776821104642
	
	def __init__(self, client):
		self.client = client
	
	def set_refs(self, logger, sheets):
		self.logs = logger
		self.gsheet = sheets
		
# COMMAND: $report <reported user> <reasoning>

	@commands.command()
	async def report(self, context):
    
	    self.logs.log("'$report' command called")    

	    dateObj = datetime.datetime.now()
	    dateStr = dateObj.strftime("%a %d %b - %H:%M %Z")

	    msg1 = context.message.author.name + " (" + context.message.author.nick + ")"
	    msg2 = context.message.content.split(" ")[1].strip()
	    msg3temp = context.message.content.split(" ")

	    await context.message.delete()

	    msg3 = ""
	    for i in range(1, len(msg3temp)):
	      msg3 = msg3 + " " + msg3temp[i]

	    reportChnl = client.get_channel(self.reportChannelID)

	    embed = discord.Embed(title="**REPORT**: " + dateStr, color=0x4287f5)
	    embed.add_field(name="User Reported By: ", value=msg1, inline=False)
	    embed.add_field(name="User Reported: ", value=msg2, inline=False)
	    embed.add_field(name="Reason: ", value=msg3, inline=False)

	    await reportChnl.send(embed=embed)

		self.logs.log("Command Succesfull")
		
# COMMAND: $mute <member mention>
		
	@commands.command()
	async def mute(self, context):
		
		self.logs.log("'$mute' command called")
		
		toMute = context.message.mentions[0]
		reasonStr = "Muted by" + context.message.author.display_name
		
		muteRole = context.message.guild.get_role(muteRoleID)
		
		if muteRole == None:
			self.logs.log("ERROR: Mute role not found, check ID is correct")
		else:
			await toMute.add_roles(muteRole, reason=reasonStr)
			self.logs.log("Command Succesfull")
		
def setup(client):
	client.add_cog(Moderation(client))
