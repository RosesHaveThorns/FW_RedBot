# FW_RedBot
A Discord Bot for the Flairwars Red Discord Server.

## Setup Info
#### API Credentials
You will need to add a "client_secret.json" file from the google API and a "credentials.json" from the Discord API within the same directory as the main script inorder for it to work. I advise following a tutorial for the creation of a discord bot with Google Sheets access to see how to set it up.
#### Help Command
The Help command outputs the [Help File](HELP.info). The file is formatted useing discord formatting and is restricted currently by the discord character limit. if the bot does not find a HELP.info file in the same directory as it it will create an empty one.
#### Logs
The bot outputs all errors and info to .LOG files, named by the date and time it was created (not included in this repo). After the file reaches 500 MB or the bot restarts a new log fiel is created. Each output line has the time and date included in it.
