# FW_RedBot
A Discord Bot for the Flairwars Red Discord Server.

## Setup Info
#### API Credentials
You will need to add a "client_secret.json" file from the google API and a "credentials.json" from the Discord API within teh same directory as the main script inorder for it to work. I advise following a tutorial for the creation of a discord bot with Google Sheets access to see how to set it up.
#### Help Command
The Help command outputs the [Help File](HELP.txt). The file is formatted useing discord formatting and is restricted currently by the discord character limit. if the bot does not find a HELP.txt file in the same directory as it it will create an empty one.
#### Logs
The bot outputs all errors and info to LOGS.txt (not included in this repo), if the bot does not find a LOGS.txt file in the same directory as it it will create an empty one. Each output line has the time and date included in it.
