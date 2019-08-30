## HonRed Commands for Red Bot

import datetime
import discord
from discord.ext import commands

class HonRed(commands.Cog):
	
	def __init__(self, client):
		self.client = client
	
	def set_refs(self, logger, sheets):
		self.logs = logger
		self.gsheet = sheets
		
		self.honSheetMain = self.gsheet.open("Honarary Red Tracking").worksheet("BOT_DATA")
		self.honRegisterSheetMain = self.gsheet.open("Honarary Red Tracking").worksheet("Registration")
		self.honSubmissionSheetMain = self.gsheet.open("Honarary Red Tracking").worksheet("Submissions")
		
# COMMAND: $honstatus <username>

	@commands.command(pass_context = True)
	async def honstatus(self, context):
		self.logs.log("'$honstatus' command called")

		msg = context.message

		msgOut = await msg.channel.send(content='Give me a second, looking you up...')

		# Get Username
		username = msg.content.split(" ")[1].strip()

		sheetUsernames = self.honSheetMain.col_values(1)

		found = False

		for i in range(len(sheetUsernames)):
			if sheetUsernames[i].strip() == username:
				await msgOut.edit(content='Found you in the spreadsheet, almost there...')
				userRow = i
				found = True
				break
		if username == "Username":
			found = False

		if not found:
			await msgOut.edit(content="I couldn't find you! You're not on my spreadsheet (if this is the case, contact a premier) or you got your username wrong!")
			self.logs.log("Command failed, couldnt find user")	
			
		if found:
			## GET CELL VALUES (indices start at 1)
			Lore = self.honSheetMain.cell(userRow+1, 2).value
			RedOC = self.honSheetMain.cell(userRow+1, 3).value
			Voteing = self.honSheetMain.cell(userRow+1, 5).value
			Test = self.honSheetMain.cell(userRow+1, 6).value

			self.logs.log("Collected Cell Values")

			## FORMAT MESSAGE

			# Lore Contribution
			if Lore == "1":
				msg1 = "Completed"
			else:
				msg1 = "Not Yet Submitted"

			# Amount of Red OC
			msg2 = RedOC

			# Voting on Posts
			if Voteing == "1":
				msg3 = "Completed"
			else:
				msg3 = "Evidence Not Yet Submitted"

			# The Test
			if Test == "1":
				msg4 = "Completed"
			else:
				msg4 = "Not Yet Passed"

			## SETUP EMBED
			embed = discord.Embed(title="**Honarary Red Progression**: " + username, color=0x8c0808)
			embed.add_field(name="Lore Contribution", value=msg1, inline=False)
			embed.add_field(name="Amount of Red OC Created", value=msg2, inline=False)
			embed.add_field(name="Voting on Requested Posts", value=msg3, inline=False)
			embed.add_field(name="The *TEST*", value=msg4, inline=False)

			## SEND MESSAGE
			await msgOut.edit(content='',embed=embed)
			self.logs.log("Command Succesfull")

# COMMAND: $honupdate <username> <requirement>

	@commands.command(pass_context = True)
	async def honupdate(self, context):

		msg = context.message
		
		if msg.channel.name == "honorary-red-logging":
			self.logs.log("'$honupdate' command called")	
			
			msgOut = await msg.channel.send('Adding to update list...')
				
			# Get Username
			username = msg.content.split(" ")[1].strip()
			date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)
			premier = msg.author.nick
			requirement = msg.content.split(" ")[2].strip()

			sheetUsernames = self.honSubmissionSheetMain.col_values(1)
			
			# Get Gap in Spreadsheet
			found = False

			for i in range(len(sheetUsernames)):
				if sheetUsernames[i] == "-":
					userRow = i
					found = True
					break
			if username == "Username":
				found = False

			if not found:
				await msgOut.edit(content="**I couldn't find a gap in the spreadsheet**, please let the Minister for Personell know about this!")
 				self.logs.log("Command failed, couldnt find user")	
	  
			if found:
				## SET CELLS
				self.honSubmissionSheetMain.update_cell(userRow+1, 1, username)
				self.honSubmissionSheetMain.update_cell(userRow+1, 2, premier)
				self.honSubmissionSheetMain.update_cell(userRow+1, 3, requirement)
				self.honSubmissionSheetMain.update_cell(userRow+1, 4, date)

				## SEND CONFIRMATION
				await msgOut.edit(content="**The update request has been recieved**, the Minister for Personell will update the spreadhseet soon!")
				self.logs.log("Command Succesfull")
				
# COMMAND: $honregister <username>

	@commands.command(pass_context = True)
	async def honupdate(self, context):
		
		self.logs.log("'$honregister' command called")	

		msg = context.message
		
		msgOut = await msg.channel.send('Informing the premiers, a crimson courier has been dispatched...')

		# Get Username
		username = msg.content.split(" ")[1].strip()
		date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)

		sheetUsernames = self.honRegisterSheetMain.col_values(1)

		# Get Gap in Spreadsheet
		found = False

		for i in range(len(sheetUsernames)):
			if sheetUsernames[i] == "-":
				userRow = i
				found = True
				break
		if username == "Username":
			found = False

		if not found:
			await msgOut.edit(content="**I couldn't find a gap in the spreadsheet**, please let the Minister for Personell know about this!")
			self.logs.log("Command failed, couldnt find user")	
			
		if found:
			## SET CELLS
			self.honRegisterSheetMain.update_cell(userRow+1, 1, username)
			self.honRegisterSheetMain.update_cell(userRow+1, 2, date)

			## SEND CONFIRMATION
			await msgOut.edit(content="**Your registration request has been recieved**, the Minsister for Personell will add you to the spreadsheet soon!")
			self.logs.log("Command Succesfull")
			
def setup(client):
    client.add_cog(HonRed(client))
