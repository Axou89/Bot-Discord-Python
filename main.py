import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

def main():
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix = '/', intents = intents)
    load_dotenv()
    token = getenv('TOKEN')
    client.run(token)