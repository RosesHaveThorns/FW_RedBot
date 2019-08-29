##	---------------------------------------------------------------------------------------------------------------------------------
##	Discord Bot For Reading a Spreadsheet
##	Created by Cowminer27
##
##	Uses gspread: https://gspread.readthedocs.io/en/latest/user-guide.html#getting-a-cell-value
##
##      Licensed under the GNU General Public License v3.0
##	---------------------------------------------------------------------------------------------------------------------------------

import discord
import logging
import gspread
import datetime
import time
from oauth2client.service_account import ServiceAccountCredentials
import signal
import random

# Log File Setup
def log(txt):
	updateText = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " >>> " + txt + "\n"
	print(updateText)
	
	f_Log = open('LOGS.txt', 'a+')
	f_Log.write(updateText)
	f_Log.close()
try:
	log("---------------------- Starting Up ----------------------")

	# Gspread setup
	scope = ['https://spreadsheets.google.com/feeds',
			 'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

	# global variables
	gsheet = ""
	honSheetMain = ""
	comradeSheetMain = ""
	comradeEventsSheetMain = ""
	honRegisterSheetMain = ""
	honSubmissionSheetMain = ""
	
	emojiLetters = [
		"\N{REGIONAL INDICATOR SYMBOL LETTER A}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER B}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER C}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER D}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
		"\N{REGIONAL INDICATOR SYMBOL LETTER F}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER G}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER H}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER I}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER J}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER K}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER L}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER M}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER N}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER O}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER P}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER R}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER S}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER T}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER U}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER V}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER W}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER X}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
		"\N{REGIONAL INDICATOR SYMBOL LETTER Z}"]

	def setup_gSpread():
		global gSheet
		global honSheetMain
		global comradeSheetMain
		global comradeEventsSheetMain
		global honRegisterSheetMain
		global honSubmissionSheetMain
		
		gSheet = gspread.authorize(credentials)

		honSheetMain = gSheet.open("Honarary Red Tracking").worksheet("BOT_DATA")
		honRegisterSheetMain = gSheet.open("Honarary Red Tracking").worksheet("Registration")
		honSubmissionSheetMain = gSheet.open("Honarary Red Tracking").worksheet("Submissions")
			
		comradeSheetMain = gSheet.open("DSRR Comradeship System").worksheet("BOT_DATA")
		comradeEventsSheetMain = gSheet.open("DSRR Comradeship System").worksheet("Event Submissions")

	setup_gSpread()

	# Discord setup
	logging.basicConfig(level=logging.INFO)

	client = discord.Client()

	startSymbol = "$"

	# Time stuff
	lastLoginTime = time.time()

	# Get ReadMe File
	f = open('HELP.txt', 'r+')
	helpContents = f.read()

	if readMe_contents == "":
		log("No Help File Found. Created Empty One")
		
	f.close()

	# Discord Functions
	@client.event
	async def on_ready():
		log('We have logged in as {0.user}, setup complete'.format(client))

		userList = client.users
		

	@client.event
	async def on_message(message):
		
		global lastLoginTime
		sentBy = message.author.name
		
		## Check if gSpread has been logged in for more than 59 minutes, if so reload
		if time.time() - lastLoginTime > (60*30):
			log("Time since last gsheets login is " + str((time.time() - lastLoginTime)/60) + " minutes")
			log("Avoiding timeout; Logging back in to gsheets")
			setup_gSpread()
			lastLoginTime = time.time()

		# Check if message is from this client
		if message.author == client.user:
			return

	## ------------------------------------------------------------------------------------------------

		# COMMAND: $Help
		
		if message.content.lower().startswith(startSymbol + 'help'):
			log(sentBy + ": '$help' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")

			await message.channel.send(helpContents)
			log("Command Succesfull")

	## ------------------------------------------------------------------------------------------------

		# COMMAND: $Dice <sides>
		
		if message.content.lower().startswith(startSymbol + 'dice '):
			log(sentBy + ": '$dice' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")
			
			msgOut = await message.channel.send(content='Rolling the Die, Clickety Clack...')
			failed = 0
			try:
				input = message.content.split(" ")[1].strip()
				max = int(input)

			except:
				failed = 1
				log("<sides> Parameter Not an Integer")
				await message.channel.send("<sides> Parameter Must be an Integer")

			if failed == 0:
				out = "The " + input + " sided die Landed On a **" + str(random.randint(1, max)) + "**"

				await msgOut.edit(content=out)
				log("Command Succesfull, " + out)

	## ------------------------------------------------------------------------------------------------
	
	# COMMAND: $Poll <question> OR $Poll {<question>} [<itemA>] [<itemB>] [<itemC>] ...


		if message.content.lower().startswith(startSymbol + "poll"):
			log(sentBy + ": '$poll' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")
			messageContent = message.clean_content
			if messageContent.find("{") == -1:
				await message.add_reaction(u"\U0001F44D")
				await message.add_reaction(u"\U0001F44E")
				await message.add_reaction(u"\U0001F937")
			else:
				first = messageContent.find("{") + 1
				second = messageContent.find("}")
				title = messageContent[first:second]

				# gets the # of options and assigns them to an array
				newMessage = messageContent[second:]
				loopTime = 0

				option = []
				for options in messageContent:
					# get from } [option 1]
					stillOptions = newMessage.find("[")
					if stillOptions != -1:
						if loopTime == 0:
							first = newMessage.find("[") + 1
							second = newMessage.find("]")
							second1 = second + 1
							option.append(newMessage[first:second])
							loopTime += 1
						else:
							newMessage = newMessage[second1:]
							first = newMessage.find("[") + 1
							second = newMessage.find("]")
							second1 = second + 1
							option.append(newMessage[first:second])
							loopTime += 1

				try:
					pollMessage = ""
					i = 0
					for choice in option:
						if not option[i] == "":
							if len(option) > 20:
								await message.channel.send("Maximum of 20 options")
								log("Command Failed, Too many Options")
								return
							elif not i == len(option) - 1:
								pollMessage = pollMessage + "\n\n" + emojiLetters[i] + " " + choice
						i += 1

					e = discord.Embed(title="**" + title + "**",
							description=pollMessage,
									  colour=0x83bae3)
					pollMessage = await message.channel.send(embed=e)
					i = 0
					final_options = []	# There is a better way to do this for sure, but it also works that way
					for choice in option:
						if not i == len(option) - 1 and not option[i] == "":
							final_options.append(choice)
							await pollMessage.add_reaction(emojiLetters[i])
						i += 1
					log("Command Succesfull")
				except KeyError:
					log("Command Failed, Incorrect Format")
					return "Please make sure you are using the format '$poll {<question>} [<itemA>] [<itemB>] [<itemC>]'"


	## ------------------------------------------------------------------------------------------------


		# COMMAND: $HonStatus <username>
		
		if message.content.lower().startswith(startSymbol + 'honstatus '):
			log(sentBy + ": '$honstatus' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")
			
			msgOut = await message.channel.send(content='Give me a second, looking you up...')

			#Get server
			for server in client.guilds:
				if server.name == "TestBot":
					thisServer = server
					break
				
			# Get Username
			username = message.content.split(" ")[1].strip()

			sheetUsernames = honSheetMain.col_values(1)

			found = False
			
			for i in range(len(sheetUsernames)):
				if sheetUsernames[i].strip() == username:
					await msgOut.edit(content='Found you in the spreadsheet, almost there...')
					userRow = i
					found = True
					break
			if username == "Username":
				found = False
	 
			log("Found Username")

			if not found:
				await msgOut.edit(content="I couldn't find you! You're not on my spreadsheet (if this is the case, contact a premier) or you got your username wrong!")
			
			if found:
				## GET CELL VALUES (indices start at 1)
				Lore = honSheetMain.cell(userRow+1, 2).value
				RedOC = honSheetMain.cell(userRow+1, 3).value
				Bridge = honSheetMain.cell(userRow+1, 4).value
				Voteing = honSheetMain.cell(userRow+1, 5).value
				Test = honSheetMain.cell(userRow+1, 6).value

				log("Collected Cell Values")

				## FORMAT MESSAGE
				
				# Lore Contribution
				if Lore == "1":
					msg1 = "Completed"
				else:
					msg1 = "Not Yet Submitted"
					
				# Amount of Red OC
				msg2 = RedOC

				# Bridge Between Colours
				if Bridge == "1":
					msg3 = "Completed"
				else:
					msg3 = "Not Yet Submitted"

				# Voting on Posts
				if Voteing == "1":
					msg4 = "Completed"
				else:
					msg4 = "Evidence Not Yet Submitted"

				# The Test
				if Test == "1":
					msg5 = "Completed"
				else:
					msg5 = "Not Yet Passed"
					
				## SETUP EMBED
				embed = discord.Embed(title="**Honarary Red Progression**: " + username, color=0x8c0808)
				embed.add_field(name="Lore Contribution", value=msg1, inline=False)
				embed.add_field(name="Amount of Red OC Created", value=msg2, inline=False)
				embed.add_field(name="Proof of Bridging Between Colors", value=msg3, inline=False)
				embed.add_field(name="Voting on Requested Posts", value=msg4, inline=False)
				embed.add_field(name="The *TEST*", value=msg5, inline=False)

				## SEND MESSAGE
				await msgOut.edit(content='',embed=embed)
				log("Command Succesfull")

	## ------------------------------------------------------------------------------------------------

		# COMMAND: $HonUpdate <username> <requirement>
		
		if message.content.lower().startswith(startSymbol + 'honupdate ') and message.channel.name == "honorary-red-logging":
			log(sentBy + ": '$honupdate' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")
			
			msgOut = await message.channel.send('Adding to update list...')

			#Get server
			for server in client.guilds:
				if server.name == "TestBot":
					thisServer = server
					break
				
			# Get Username
			username = message.content.split(" ")[1].strip()
			date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)
			premier = sentBy
			requirement = message.content.split(" ")[2].strip()

			sheetUsernames = honSubmissionSheetMain.col_values(1)
			
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
 
			log("Found username")
	  
			if found:
				## SET CELLS
				honSubmissionSheetMain.update_cell(userRow+1, 1, username)
				honSubmissionSheetMain.update_cell(userRow+1, 2, premier)
				honSubmissionSheetMain.update_cell(userRow+1, 3, requirement)
				honSubmissionSheetMain.update_cell(userRow+1, 4, date)

				## SEND CONFIRMATION
				await msgOut.edit(content="**The update request has been recieved**, the Minsister for Personell will update the spreadhseet soon!")
				log("Command Succesfull")

	## ------------------------------------------------------------------------------------------------

		# COMMAND: $HonRegister <username>

		if message.content.lower().startswith(startSymbol + 'honregister '):
			log(sentBy + ": '$honregister' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")
			
			msgOut = await message.channel.send('Informing the premiers, a crimson courier has been dispatched...')
			
			# Get Username
			username = message.content.split(" ")[1].strip()
			date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)

			sheetUsernames = honRegisterSheetMain.col_values(1)

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

			if found:
				## SET CELLS
				honRegisterSheetMain.update_cell(userRow+1, 1, username)
				honRegisterSheetMain.update_cell(userRow+1, 2, date)

				## SEND CONFIRMATION
				await msgOut.edit(content="**Your registration request has been recieved**, the Minsister for Personell will add you to the spreadsheet soon!")
				log("Command Succesfull")

	## ---------------------------------------------------------------------------------------------------------
				
		# COMMAND: $ComradeshipLevel <username>
		
		if message.content.lower().startswith(startSymbol + 'comradeshiplevel '):
			log(sentBy + ": '$comradeshiplevel' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")
			
			msgOut = await message.channel.send('Give me a second, looking you up...')
				
			# Get Username
			username = message.content.split(" ")[1].strip()

			sheetUsernames = comradeSheetMain.col_values(1)

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
			
			if found:
				## GET CELL VALUES (indices start at 1)
				audPoints = comradeSheetMain.cell(userRow+1, 2).value
				invPoints = comradeSheetMain.cell(userRow+1, 3).value
				totalPoints = comradeSheetMain.cell(userRow+1, 4).value
				totalRank = comradeSheetMain.cell(userRow+1, 5).value
				audRank = comradeSheetMain.cell(userRow+1, 6).value
				invRank = comradeSheetMain.cell(userRow+1, 7).value
					
				## SETUP EMBED
				embed = discord.Embed(title="**Comradeship Data**: " + username, color=0x8c0808)
				embed.add_field(name="Audaciousness", value="Points: " + audPoints + "\nRank: " + audRank, inline=False)
				embed.add_field(name="Inventiveness", value="Points: " + invPoints + "\nRank: " + invRank, inline=False)
				embed.add_field(name="Overall", value="Total Points: " + totalPoints + "\n**Comrade Rank: " + totalRank + "**", inline=False)

				## SEND MESSAGE
				await msgOut.edit(content='', embed=embed)
				log("Command Succesfull")

	## --------------------------------------------------------------------------------------------------------

		# COMMAND: $ComradeshipEvent <username> <description> <evidence>
		
		if message.content.lower().startswith(startSymbol + 'comradeshipevent '):
			log(sentBy + ": '$comradeshipevent' command called " + str((time.time() - lastLoginTime)/60) + " minutes after last gsheets login")
			
			msgOut = await message.channel.send('Give me a second, sending the data by Crimson Courier...')
				
			# Get Command Data
			username = message.content.split(" ")[1].strip()
			description = message.content.split(" ")[2].strip()
			evidence = message.content.split(" ")[3].strip()
			date = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day)
			
			log("Command Data Collected")

			sheetUsernames = comradeEventsSheetMain.col_values(8)

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
			log("Found username, updating spreadsheet")
			if found:
				## SET CELLS
				comradeEventsSheetMain.update_cell(userRow+1, 8, username)
				comradeEventsSheetMain.update_cell(userRow+1, 9, date)
				comradeEventsSheetMain.update_cell(userRow+1, 10, description)
				comradeEventsSheetMain.update_cell(userRow+1, 11, evidence)
				
				## SEND CONFIRMATION
				await msgOut.edit(content="**Your submission has been recieved**, the Minsister for Personell will update you points soon!")
			log("Command Succesfull")

	## ---------------------------------------------------------------------------------------------------------

	# Start as Discord Bot
	client.run('NTY2MTY1MTg4OTg3MDYwMjQ0.XLBbzg.ZwaBplOaVqBqwEidaV6DJRv4uTw')

except Exception as e:
	log("ERROR - EXCEPTION CAUGHT:" + e)

