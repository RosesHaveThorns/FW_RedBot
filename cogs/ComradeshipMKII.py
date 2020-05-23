## Comradeship Commands for Red Bot

import datetime
import discord
from discord.ext import commands
from discord.ext.commands import has_role

class ComradeshipMKII(commands.Cog):

	requestChnlID = 586886560360693761

	def __init__(self, client):
		self.client = client
# TODO: MAKE POINTS BASED ON DATA IN SHEET RATHER THAN SEMI-HARDCODED
		self.cmrd_events = {"wall":[5, "a"], "raidloss":[15, "a"], "raidwin":[20, "a"], "raiddraw":[18, "a"], "raidmatfound":[5, "i"], "raidmatmade":[10, "i"], "lore":[15, "i"], "drawpile":[5, "i"]}

	def set_refs(self, logger, sheets):
		self.logger = logger
		self.gsheet = sheets

		self.cmrd_data = self.gsheet.open("Comradeship 2.0").worksheet("User Data")
		self.cmrd_bot_data = self.gsheet.open("Comradeship 2.0").worksheet("Sheet Data")
		self.cmrd_event_log = self.gsheet.open("Comradeship 2.0").worksheet("Event Log")

	def get_next_empty_log_row(self):
			str_list = list(filter(None, self.cmrd_event_log.col_values(1)))
			return str(len(str_list)+1)

	def get_next_empty_user_row(self):
			str_list = list(filter(None, self.cmrd_data.col_values(1)))
			return str(len(str_list)+1)

# COMMAND: $comradeshiplevel <username>

	@commands.command()
	async def comradeshiplevel(self, context):
		self.logger.log("'$comradeshiplevel2' command called")

		msg = context.message

		msg_out = await msg.channel.send('Give me a second, looking you up...')

		# Get Username
		username = msg.content.split(" ")[1].lower().strip()

		usernames = self.cmrd_data.col_values(1)

		user_found = False

		for i in range(len(usernames)):
			if usernames[i].lower().strip() == username:
				await msg_out.edit(content='Found you in the spreadsheet, almost there...')
				user_row = i+1
				user_found = True
				break
		if username == "Username" or username == "":
			user_found = False

		if not user_found:
			await msg_out.edit(content="**I couldn't find you!**\nYou're not on my spreadsheet (if this is the case, you need to register for comradeship) or you got your username wrong!")
			self.logger.log("Command failed, couldn't find username")

		if user_found:
			## GET CELL VALUES (indices start at 1)

			aud_points = self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(3, 2).value).value
			inv_points = self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(5, 2).value).value
			total_points = self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(7, 2).value).value
			total_rank = self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(8, 2).value).value
			aud_rank = self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(4, 2).value).value
			inv_rank = self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(6, 2).value).value

			## SETUP EMBED
			embed = discord.Embed(title="**Comradeship Data**: " + username, color=0x8c0808)
			embed.add_field(name="Audaciousness", value="Points: " + aud_points + "\nRank: " + aud_rank, inline=False)
			embed.add_field(name="Inventiveness", value="Points: " + inv_points + "\nRank: " + inv_rank, inline=False)
			embed.add_field(name="Overall", value="Total Points: " + total_points + "\n**Comrade Rank: " + total_rank + "**", inline=False)

			## SEND MESSAGE
			await msg_out.edit(content='', embed=embed)
			self.logger.log("Command Succesfull")

# COMMAND: $comradeship_request <description>

	@commands.command()
	async def comradeship_request(self, context):

		self.logger.log("'$comradeship_request' command called")

		dateObj = datetime.datetime.now()
		dateStr = dateObj.strftime("%a %d %b - %H:%M ") + "GMT"

		msg1 = context.message.author.name + " | Nickname: " + context.message.author.display_name
		msg2temp = context.message.content.split(" ")

		msg2 = ""
		for i in range(1, len(msg2temp)):
			msg2 = msg2 + " " + msg2temp[i]

		requestChnl = self.client.get_channel(self.requestChnlID)

		embed = discord.Embed(title="**COMRADESHIP REQUEST**: " + dateStr, color=0x4287f5)
		embed.add_field(name="User: ", value=msg1, inline=False)
		embed.add_field(name="Request: ", value=msg2, inline=False)

		await requestChnl.send(embed=embed)
		await context.message.channel.send('Sent the request, a Premier will get you updated ASAP')

		self.logger.log("Command Succesfull")


# COMMAND: $comradeshipevent <username> <description> <evidence>

	@has_role("Premier")
	@commands.command()
	async def comradeshipevent(self, context):
		self.logger.log("'$comradeshipevent2' command called")

		msg = context.message

		msg_out = await msg.channel.send('Give me a second, sending the data by Crimson Courier...')

		# Get Command Data
		username = msg.content.split(" ")[1].lower().strip()
		event = msg.content.split(" ")[2].lower().strip()
		evidence = msg.content.split(" ")[3].strip()
		date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)

		# Get user's row in Spreadsheet
		user_found = False
		usernames = self.cmrd_data.col_values(1)

		for i in range(len(usernames)):
			if usernames[i].lower().strip() == username:
				user_row = i+1
				user_found = True
				break
		if username == "Username":
			user_found = False

		if not user_found:
			await msg_out.edit(content="**I couldn't find you!**\nYou're not on my spreadsheet (if this is the case, you need to register for comradeship) or you got your username wrong!")
			self.logger.log("Command failed, couldnt find username")

		chk_event = False
		for i in self.cmrd_events:
			if event == i:
				chk_event = True
				break

		if not chk_event:
			await msg_out.edit(content="**I don't think that is an event!**\nThat event was unexpected, did you get the spelling right?")
			self.logger.log("Command failed, unexpected event")


		if user_found and chk_event:
			## UPDATE POINTS

			new_points = self.cmrd_events[event][0]

			success = False
			if self.cmrd_events[event][1] == "a":
				aud_points = int(self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(3, 2).value).value.strip())
				self.cmrd_data.update_cell(user_row, self.cmrd_bot_data.cell(3, 2).value, str(aud_points+new_points))
				success = True

			elif self.cmrd_events[event][1] == "i":
				inv_points = int(self.cmrd_data.cell(user_row, self.cmrd_bot_data.cell(5, 2).value).value.strip())
				self.cmrd_data.update_cell(user_row, self.cmrd_bot_data.cell(5, 2).value, str(inv_points+new_points))
				success = True

			else:
				await msg_out.edit(content="**Something didn't work!!!**\n Go ree at Miner not me!")
				self.logger.log("Command failed, issue while adding points")

			if success:
				# ADD LOG
				row = self.get_next_empty_log_row()
				self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(11, 2).value, username)
				self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(12, 2).value, date)
				self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(13, 2).value, event)
				self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(14, 2).value, evidence)

				## SEND CONFIRMATION
				await msg_out.edit(content="**Your submission has been recieved**\n Your points have been updated!")

				self.logger.log("Command Succesfull")

# COMMAND: $comradeshipevent <username> <description> <evidence>

	@has_role("Premier")
	@commands.command()
	async def comradeshipregister(self, context):
		self.logger.log("'$comradeshipregister2' command called")

		msg = context.message

		msg_out = await msg.channel.send('Give me a second, sending the data by Crimson Courier...')

		username = msg.content.split(" ")[1].lower().strip()
		date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)

		self.cmrd_data.update_cell(self.get_next_empty_user_row(), 1, username)

		row = self.get_next_empty_log_row()
		self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(11, 2).value, username)
		self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(12, 2).value, date)
		self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(13, 2).value, "Registered")
		self.cmrd_event_log.update_cell(row, self.cmrd_bot_data.cell(14, 2).value, "Red Bot")

		await msg_out.edit(content='**Comradeship Registration Complete**\nWelcome in!')


def setup(client):
	client.add_cog(ComradeshipMKII(client))
