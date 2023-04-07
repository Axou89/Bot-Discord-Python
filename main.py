import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os import getenv
import random
from Node import list_chained
from Node import Node

# Bot client
intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

AllCmd = list_chained(None)

# Event sync commands
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

# Event on message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("hello"):
        await message.channel.send("Hello")

# Add command to list_chained
def AddCmd(name):
    AllCmd.append(name)

# Event delete a certain ammount of messages
@tree.command(name = "delete", description = "Delete a certain amount of messages",)
async def DeleteMessage(interaction, amount: int):
    await interaction.channel.purge(limit= amount)
    AddCmd("delete")

# Event last command of a user
@tree.command(name = "lastcmd", description = "Last command of a user")
async def LastCmd(interaction):
    await interaction.response.send_message(f"Last command is : {AllCmd.last_node.data}")

# Event Ultimate Bravery
@tree.command(name = "bravery", description = "Ultimate Bravery")
async def UltimateBravery(interaction, role : str = ""):
    # Champion
    champions = ["Aatrox","Ahri","Akali","Akshan","Alistar","Amumu","Anivia","Annie","Aphelios","Ashe",
                 "Aurelion Sol","Azir","Bard","Bel'Veth","Blitzcrank","Brand","Braum","Caitlyn","Cassiopeia","Cho'Gath","Corki",
                    "Darius","Diana","Dr. Mundo","Draven","Ekko","Elise","Evelynn","Ezreal","Fiddlesticks","Fiora",
                    "Fizz","Galio","Gangplank","Garen","Gnar","Gragas","Graves","Gwen","Hecarim","Heimerdinger","Illaoi",
                    "Irelia","Ivern","Janna","Jarvan IV","Jax","Jayce","Jhin","Jinx","K'Sante","Kai'sa","Kalista","Karma",
                    "Karthus","Kassadin","Katarina","Kayle","Kayn","Kennen","Kha'Zix","Kindred","Kled","Kog'Maw",
                    "LeBlanc","Lee Sin","Leona","Lillia","Lissandra","Lucian","Lulu","Lux","Malphite","Malzahar","Maokai",
                    "Master Yi","Milio","Miss Fortune","Mordekaiser","Morgana","Nami","Nasus","Nautilus","Neeko","Nidalee",
                    "Nilah","Nocturne","Nunu & Willump","Olaf","Orianna","Ornn","Pantheon","Poppy","Pyke","Qiyana","Quinn",
                    "Rakan","Rammus","Rek'Sai","Rell","Renata","Renekton","Rengar","Riven","Rumble","Ryze","Samira",
                    "Sejuani","Senna","Seraphine","Sett","Shaco","Shen","Shyvana","Singed","Sion","Sivir","Skarner","Sona",
                    "Soraka","Swain","Sylas","Syndra","Tahm Kench","Taliyah","Talon","Taric","Teemo","Thresh","Tristana",
                    "Trundle","Tryndamere","Twisted Fate","Twitch","Udyr","Urgot","Varus","Vayne","Veigar","Vel'Koz","Vex",
                    "Vi","Viego","Viktor","Vladimir","Volibear","Warwick","Wukong","Xayah","Xerath","Xin Zhao","Yasuo",
                    "Yone","Yorick","Yuumi","Zac","Zed","Zeri","Ziggs","Zilean","Zoe","Zyra"]
    champion = random.choice(champions)
    await interaction.response.send_message(f"Your champion is : {champion}")
    await interaction.channel.send(file=discord.File(f"img/Champions/{champion}.png"))

    # Role
    role = role.lower()
    roles = ["top","jungle","mid","bot","support"]
    if role == "" or role not in roles:
        role = random.choice(roles)
    await interaction.channel.send(file=discord.File(f"img/Roles/{role}.png"))

    # Spell
    spells = ["Q","W","E"]
    spell = random.choice(spells)
    await interaction.channel.send(f"Your Spell to max is : {spell}")
    #await interaction.channel.send(file=discord.File(f"img/Spells/{champion+spell}.png"))
    
    # Historic
    AddCmd("bravery")

# Run bot
def main():
    load_dotenv()
    token = getenv('TOKEN')
    client.run(token)

main()