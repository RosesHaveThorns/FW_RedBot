import os
import discord
from logger import logger
import logging
import time
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

logs = logger()
logs.log("---------------------- Starting Up ----------------------")

# Load Discord Bot Token
try:
	tokenf = open("token.txt","r")
	TOKEN = tokenf.read()
	tokenf.close()

except Exception as error:
	logs.log("ERROR: Couldn't load Token [{}]".format(error))

logs.log("Loaded Discord Token: [{}]".format(TOKEN))


# Gspread variables
scope = ['https://spreadsheets.google.com/feeds',
			 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

# global variables
gsheet = ""

# Non-Discord Functions

def setup_gSpread():
	try:
		global gSheet
		global comradeSheetMain
		global comradeEventsSheetMain

		gSheet = gspread.authorize(credentials)
		
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

# Discord functions

@client.event
async def on_ready():
	logs.log('We have logged in as {0.user}, setup complete'.format(client))

@client.event
async def on_message(msg):
	global lastLoginTime
	
	## Check if gSpread token has expired, reload
	if credentials.access_token_expired:
		logs.log("GSheets Token expired. Last login at {}".format(lastLoginTime ))
		gSheet.login()
		lastLoginTime = time.time()

	await client.process_commands(msg)
	
	
if __name__ == '__main__':
	global gSheets
	
	client.remove_command("help")
	
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
				logs.log("Created Command " + i.name)
		
		except Exception as error:
			logs.log("ERROR: Could not pass the extension {} the logger. [{}]".format(extension, error))
			
	client.run(TOKEN)