import os
import discord
from logger import logger
import logging
import time
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = '___ ADD BOT TOKEN HERE __'

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
		comradeSheetMain = gSheet.open("DSRR Comradeship System").worksheet("BOT_DATA")
		comradeEventsSheetMain = gSheet.open("DSRR Comradeship System").worksheet("Event Submissions")
		
		logs.log("Loaded gSpread")

	except Exception as error:
		logs.log("ERROR: Couldnt load gSpread [{}]".format(error))

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
logging.basicConfig(level=logging.INFO)
client = commands.Bot(command_prefix = '$')
lastLoginTime = time.time()

# Get Help File
f = open('HELP.info', 'r+')
helpContents = f.read()

if helpContents  == "":
	log("No Help File Found. Created Empty One")

f.close()

logs.log("Loaded help file")

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
	
	for extension in exts :
		
		# load each extension
		try:
			client.load_extension('cogs.' + extension)
			logs.log('Loaded {} cog'.format(extension))
		except Exception as error:
			logs.log("ERROR: Extension {} could not be loaded. [{}]".format(extension, error))
		
		# pass each cog the logger
		try:
			cog = client.get_cog(extension)
			cog.set_refs(logs, gSheet)

			for i in cog.get_commands():
				logs.log(i.name)
		
		except Exception as error:
			logs.log("ERROR: Could not pass the extension {} the logger. [{}]".format(extension, error))
			
	client.run(TOKEN)
	
