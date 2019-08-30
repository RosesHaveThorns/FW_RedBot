import discord
from discord.ext import commands

TOKEN = '__PUT DISCORD BOT TOKEN HERE__'

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
	
