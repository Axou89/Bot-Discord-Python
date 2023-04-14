import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os import getenv
import random
import os
from Node import list_chained
from Node import Node

# Bot client
intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

AllCmd = list_chained("Start of commands", "Bot")

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
    if message.content.startswith("RivenOTP"):
        await message.channel.send("Hello")

# Add command to list_chained
def AddCmd(name, author):
    AllCmd.append(name, author)

# Event on interaction
@client.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.application_command:
        AddCmd(f"{interaction.data['name']}", f"{interaction.user.id}")

# Event delete a certain ammount of messages
@tree.command(name = "delete", description = "Delete a certain amount of messages")
async def DeleteMessage(interaction, amount: int):
    await interaction.response.send_message(f"{amount} messages deleted", ephemeral = True)
    await interaction.channel.purge(limit= amount)

# Event last command of a user
@tree.command(name = "lastcmd", description = "Last command of a user")
async def LastCmd(interaction):
    await interaction.response.send_message(f"Last command is : {AllCmd.last_node.data}")

# Event all commands of a user
@tree.command(name = "allcmd", description = "All commands of a user")
async def AllCmds(interaction, user : discord.User = None):
    current_node = AllCmd.first_node
    embed = discord.Embed(title = f"All commands of {user.name}", color = 0x00ff00)
    while current_node != None:
        if current_node.author == str(user.id):
            embed.add_field(name="Command", value=f"{current_node.data}", inline=False)
        current_node = current_node.next_node
    await interaction.response.send_message(embed = embed)

# Event clear commands historic
@tree.command(name = "clearcmd", description = "Clear commands historic")
async def ClearCmd(interaction):
    AllCmd.clear()
    await interaction.response.send_message("Historic cleared", ephemeral = True)

# Event Ultimate Bravery
@tree.command(name = "bravery", description = "Ultimate Bravery")
async def UltimateBravery(interaction, role : str = ""):
    embeds = []
    files = []

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
    embed = discord.Embed(title = "Champion", description=f"{champion}", color = 0x00ff00)
    embed.set_image(url=f"attachment://{champion}.png")
    files.append(discord.File(f"img/Champions/{champion}.png"))
    embeds.append(embed)

    # Role
    role = role.lower()
    roles = ["top","jungle","mid","bot","support"]
    if role == "" or role not in roles:
        role = random.choice(roles)
    embed = discord.Embed(title = "Role", description=f"{role}", color = 0x00ff00)
    embed.set_image(url=f"attachment://{role}.png")
    embeds.append(embed)
    files.append(discord.File(f"img/Roles/{role}.png"))

    # Spell
    spell = random.choice(os.listdir(f"img/Spells/{champion}/"))
    embed = discord.Embed(title = "Spell", color = 0x00ff00)
    embed.set_image(url=f"attachment://{spell}")
    embeds.append(embed)
    files.append(discord.File(f"img/Spells/{champion}/{spell}"))

    await interaction.response.send_message("Your Ultimate Bravery :")
    for embed in embeds:
        await interaction.channel.send(embed = embed, file=files[embeds.index(embed)])

# Run bot
def main():
    load_dotenv()
    token = getenv('TOKEN')
    client.run(token)

main()