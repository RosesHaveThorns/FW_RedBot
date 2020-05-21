## Comradeship Commands for Red Bot

import datetime
import discord
from discord.ext import commands

class Comradeship(commands.Cog):

	def __init__(self, client):
		self.client = client

	def set_refs(self, logger, sheets):
		self.logs = logger
		self.gsheet = sheets

		self.comradeSheetMain = self.gsheet.open("DSRR Comradeship System").worksheet("BOT_DATA")
		self.comradeEventsSheetMain = self.gsheet.open("DSRR Comradeship System").worksheet("Event Submissions")

# COMMAND: $comradeshiplevel <username>

	@commands.command()
	async def comradeshiplevel(self, context):
		self.logs.log("'$comradeshiplevel' command called")

		msg = context.message

		msgOut = await msg.channel.send('Give me a second, looking you up...')

		# Get Username
		username = msg.content.split(" ")[1].strip()

		sheetUsernames = self.comradeSheetMain.col_values(1)

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
			await msgOut.edit(content="**I couldn't find you!**\nYou're not on my spreadsheet (if this is the case, you need to register for comradeship) or you got your username wrong!")
			self.logs.log("Command failed, couldnt find username")

		if found:
			## GET CELL VALUES (indices start at 1)
			audPoints = self.comradeSheetMain.cell(userRow+1, 2).value
			invPoints = self.comradeSheetMain.cell(userRow+1, 3).value
			totalPoints = self.comradeSheetMain.cell(userRow+1, 4).value
			totalRank = self.comradeSheetMain.cell(userRow+1, 5).value
			audRank = self.comradeSheetMain.cell(userRow+1, 6).value
			invRank = self.comradeSheetMain.cell(userRow+1, 7).value

			## SETUP EMBED
			embed = discord.Embed(title="**Comradeship Data**: " + username, color=0x8c0808)
			embed.add_field(name="Audaciousness", value="Points: " + audPoints + "\nRank: " + audRank, inline=False)
			embed.add_field(name="Inventiveness", value="Points: " + invPoints + "\nRank: " + invRank, inline=False)
			embed.add_field(name="Overall", value="Total Points: " + totalPoints + "\n**Comrade Rank: " + totalRank + "**", inline=False)

			## SEND MESSAGE
			await msgOut.edit(content='', embed=embed)
			self.logs.log("Command Succesfull")

# COMMAND: $comradeshipevent <username> <description> <evidence>

	@commands.command()
	async def comradeshipevent(self, context):
		self.logs.log("'$comradeshipevent' command called")

		msg = context.message

		msgOut = await msg.channel.send('Give me a second, sending the data by Crimson Courier...')

		# Get Command Data
		username = msg.content.split(" ")[1].strip()
		description = msg.content.split(" ")[2].strip()
		evidence = msg.content.split(" ")[3].strip()
		date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)

		sheetUsernames = self.comradeEventsSheetMain.col_values(8)

		# Get empty space in Spreadsheet
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
			self.logs.log("Command failed, couldnt find username")

		if found:
			## SET CELLS
			self.comradeEventsSheetMain.update_cell(userRow+1, 8, username)
			self.comradeEventsSheetMain.update_cell(userRow+1, 9, date)
			self.comradeEventsSheetMain.update_cell(userRow+1, 10, description)
			self.comradeEventsSheetMain.update_cell(userRow+1, 11, evidence)

			## SEND CONFIRMATION
			await msgOut.edit(content="**Your submission has been recieved**, the Minsister for Personell will update you points soon!")

			self.logs.log("Command Succesfull")

def setup(client):
	client.add_cog(Comradeship(client))
