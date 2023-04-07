import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os import getenv
import random

# Bot client
intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)

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

# Event delete a certain ammount of messages
@tree.command(name = "delete", description = "Delete a certain amount of messages",)
async def DeleteMessage(ctx, amount: int):
    await ctx.channel.purge(limit= amount)

# Event pick random champion
@tree.command(name = "champion", description = "Pick a random champion")
async def RandomChampion(interaction):
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
    await interaction.channel.send(file=discord.File(f"img/Champions/{champion}.png"))
    await interaction.response.send_message(f"Your champion is : {champion}")

# Run bot
def main():
    load_dotenv()
    token = getenv('TOKEN')
    client.run(token)

main()