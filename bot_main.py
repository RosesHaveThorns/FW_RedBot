import os
import discord
from logging import logger
from discord.ext import commands

TOKEN = '__PUT DISCORD BOT TOKEN HERE__'

logs = logger()
logs.log("---------------------- Starting Up ----------------------")

# Gspread variables
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

# Non-Discord Functions

def setup_gSpread():
	try:
		global gSheet
		global honSheetMain
		global comradeSheetMain
		global comradeEventsSheetMain
		global honRegisterSheetMain
		global honSubmissionSheetMain

		gSheet = gspread.authorize(credentials)

		# Get required worksheets
		honSheetMain = gSheet.open("Honarary Red Tracking").worksheet("BOT_DATA")
		honRegisterSheetMain = gSheet.open("Honarary Red Tracking").worksheet("Registration")
		honSubmissionSheetMain = gSheet.open("Honarary Red Tracking").worksheet("Submissions")

		comradeSheetMain = gSheet.open("DSRR Comradeship System").worksheet("BOT_DATA")
		comradeEventsSheetMain = gSheet.open("DSRR Comradeship System").worksheet("Event Submissions")
	except Exception as error:
		logs.log("ERROR: Couldnt load gSpread [{error}]")

def find_extensions(folder):
	cogs = []
	
	extensionFiles = os.listdir("./{}".format(folder))
	
	for file in extensionFiles:
		pyPos = file.find(".py")
		if pyPos != -1:
			cogs.append(file[:pyPos])
	
	return cogs

## Setup
setup_gSpread()

# Discord setup
client = commands.Bot(command_prefix = '$')
lastLoginTime = time.time()

# Get Help File
f = open('HELP.txt', 'r+')
helpContents = f.read()

if readMe_contents == "":
	log("No Help File Found. Created Empty One")

f.close()

# Discord functions:

@client.event
async def on_ready():
	logs.log('We have logged in as {0.user}, setup complete'.format(client))

@client.event
async def on_message(msg):
	global lastLoginTime
	
	## Check if gSpread has been logged in for more than 20 minutes, if so reload
	if time.time() - lastLoginTime >= (20*30):
		logs.log("Time since last gsheets login is " + str((time.time() - lastLoginTime)/60) + " minutes")
		logs.log("Avoiding timeout; Logging back in to gsheets")
		setup_gSpread()
		lastLoginTime = time.time()
	
	await client.process_commands(msg)
	
if __name__ == '__main__':
	exts = find_extensions("./cogs")
	
	for extension in extensions:
		
		# load each extension
		try:
			client.load_extension('cogs.' + extension)
			logs.log('DEBUG: Loaded {extension} cog.')
		except Exception as error:
			logs.log("ERROR: Extension {extension} could not be loaded. [{error}]")
		
		# give each cog the logger
		try:
			client.get_cog(extension).set_logger(logs)
		except Exception as error:
			logs.log("ERROR: Could not give the extension {extension} the logger. [{error}]")
			
	client.run(TOKEN)
	
