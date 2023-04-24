import discord
from discord import app_commands
from dotenv import load_dotenv
from os import getenv
import random
import os
from Node import list_chained
from Tree import Tree
from requests import get

# Bot client
intents = discord.Intents.all()
client = discord.Client(intents = intents)
bot = app_commands.CommandTree(client)

AllCmd = list_chained("Start of commands", "Bot")

# Create the tree
def DefineTree():
    global Chatbot
    Chatbot = Tree("Command to use")
    Chatbot.append_question("level", ["Write the name of the summoner"], "Command to use")

# Event sync commands
@client.event
async def on_ready():
    await bot.sync()
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
@bot.command(name = "delete", description = "Delete a certain amount of messages")
async def DeleteMessage(interaction, amount: int):
    await interaction.response.send_message(f"{amount} messages deleted", ephemeral = True)
    await interaction.channel.purge(limit= amount)

# Event last command of a user
@bot.command(name = "lastcmd", description = "Last command of a user")
async def LastCmd(interaction):
    await interaction.response.send_message(f"Last command is : {AllCmd.last_node.data}")

# Event all commands of a user
@bot.command(name = "allcmd", description = "All commands of a user")
async def AllCmds(interaction, user : discord.User = None):
    current_node = AllCmd.first_node
    embed = discord.Embed(title = f"All commands of {user.name}", color = 0x00ff00)
    while current_node != None:
        if current_node.author == str(user.id):
            embed.add_field(name="Command", value=f"{current_node.data}", inline=False)
        current_node = current_node.next_node
    await interaction.response.send_message(embed = embed)

# Event clear commands historic
@bot.command(name = "clearcmd", description = "Clear commands historic")
async def ClearCmd(interaction):
    AllCmd.clear()
    await interaction.response.send_message("Historic cleared", ephemeral = True)

# Event move in historic
@bot.command(name = "travelcmd", description = "Move in historic")
async def TravelCmd(interaction, index : int):
    if index > AllCmd.size()-1 or index < 0:
        index = AllCmd.size()
    current_node = AllCmd.first_node
    i = 1
    while i < index:
        current_node = current_node.next_node
        i += 1
    embed = discord.Embed(title = f"Command at index {index}", description=current_node.data, color = 0x00ff00)
    await interaction.response.send_message(embed=embed)
    ##### TODO: ADD BUTTON TO TRAVEL IN HISTORIC

# Event Chat bot
@bot.command(name = "help", description = "Chat bot")
async def ChatBot(interaction):
    embed = discord.Embed(title = "Write which command you want to use", description = "level / soloq / flex", color = 0x00ff00)
    await interaction.response.send_message(embed = embed)
    message = await client.wait_for("message", check = lambda message: message.author == interaction.user)
    if Chatbot.get_question() != None:
        print()
        await interaction.channel.send("Write")

    #result = get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/BDS%20Snake?api_key=" + getenv('RIOT_KEY'))
    #resultJson = result.json()
    #print(resultJson["summonerLevel"])

# Event Ultimate Bravery
@bot.command(name = "bravery", description = "Ultimate Bravery")
async def UltimateBravery(interaction, role : str = "", gamemode : str = ""):
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
    embedChampion = discord.Embed(title = "Champion", description=f"{champion}", color = 0x00ff00)
    embedChampion.set_image(url=f"attachment://{champion}.png")
    fileChampion = discord.File(f"img/Champions/{champion}.png")

    # Role
    if gamemode != "aram":
        role = role.lower()
        roles = ["top","jungle","mid","bot","support"]
        if role == "" or role not in roles:
            role = random.choice(roles)
        embedRole = discord.Embed(title = "Role", description=f"{role}", color = 0x00ff00)
        embedRole.set_image(url=f"attachment://{role}.png")
        fileRole = discord.File(f"img/Roles/{role}.png")

    # Spell
    spell = random.choice(os.listdir(f"img/Spells/{champion}/"))
    embedSpell = discord.Embed(title = "Spell", color = 0x00ff00)
    embedSpell.set_image(url=f"attachment://{spell}")
    fileSpell = discord.File(f"img/Spells/{champion}/{spell}")

    # Summoner Spell
    Summoner1, Summoner2 = ChooseSummonerSpell(role, gamemode.lower())
    embedSummoner1 = discord.Embed(title = "Summoner Spell 1", color = 0x00ff00)
    embedSummoner1.set_image(url=f"attachment://{Summoner1}")
    fileSummoner1 = discord.File(f"img/SummonerSpells/{Summoner1}")
    embedSummoner2 = discord.Embed(title = "Summoner Spell 2", color = 0x00ff00)
    embedSummoner2.set_image(url=f"attachment://{Summoner2}")
    fileSummoner2 = discord.File(f"img/SummonerSpells/{Summoner2}")

    # Items
    if role == "support":
        ItemSupp = random.choice(os.listdir("img/Items/Support/"))
        embedStarter = discord.Embed(title = "Starter", color = 0x00ff00)
        embedStarter.set_image(url=f"attachment://{ItemSupp}")
        fileStarter = discord.File(f"img/Items/Support/{ItemSupp}")
    elif role == "jungle":
        ItemJgl = random.choice(os.listdir("img/Items/Jungle/"))
        embedStarter = discord.Embed(title = "Starter", color = 0x00ff00)
        embedStarter.set_image(url=f"attachment://{ItemJgl}")
        fileStarter = discord.File(f"img/Items/Jungle/{ItemJgl}")
    
    Boots = random.choice(os.listdir("img/Items/Boots/"))
    embedBoots = discord.Embed(title = "Boots", color = 0x00ff00)
    embedBoots.set_image(url=f"attachment://{Boots}")
    fileBoots = discord.File(f"img/Items/Boots/{Boots}")

    ItemMythic = random.choice(os.listdir("img/Items/Mythic/"))
    embedMythic = discord.Embed(title = "Mythic", color = 0x00ff00)
    embedMythic.set_image(url=f"attachment://{ItemMythic}")
    fileMythic = discord.File(f"img/Items/Mythic/{ItemMythic}")

    ItemsLegendary = random.sample(os.listdir("img/Items/Legendary/"), 4)
    EmbedItem1 = discord.Embed(title = "Legendary", color = 0x00ff00, url="https://example.org/")
    EmbedItem1.set_image(url=f"attachment://{ItemsLegendary[0]}")
    FileItem1 = discord.File(f"img/Items/Legendary/{ItemsLegendary[0]}")
    EmbedItem2 = discord.Embed(title = "Legendary", color = 0x00ff00, url="https://example.org/")
    EmbedItem2.set_image(url=f"attachment://{ItemsLegendary[1]}")
    FileItem2 = discord.File(f"img/Items/Legendary/{ItemsLegendary[1]}")
    EmbedItem3 = discord.Embed(title = "Legendary", color = 0x00ff00, url="https://example.org/")
    EmbedItem3.set_image(url=f"attachment://{ItemsLegendary[2]}")
    FileItem3 = discord.File(f"img/Items/Legendary/{ItemsLegendary[2]}")
    EmbedItem4 = discord.Embed(title = "Legendary", color = 0x00ff00, url="https://example.org/")
    EmbedItem4.set_image(url=f"attachment://{ItemsLegendary[3]}")
    FileItem4 = discord.File(f"img/Items/Legendary/{ItemsLegendary[3]}")

    await interaction.response.send_message("Your Ultimate Bravery :")
    await interaction.channel.send(
            embeds = [embedChampion, embedRole, embedSpell, embedSummoner1, embedSummoner2], 
            files = [fileChampion, fileRole, fileSpell, fileSummoner1, fileSummoner2])
    if role == "support" or role == "jungle":
        await interaction.channel.send(
            embeds = [embedStarter, embedBoots, embedMythic, EmbedItem1, EmbedItem2, EmbedItem3, EmbedItem4], 
            files = [fileStarter, fileBoots, fileMythic, FileItem1, FileItem2, FileItem3, FileItem4])
    else:
        await interaction.channel.send(
            embeds = [embedBoots, embedMythic, EmbedItem1, EmbedItem2, EmbedItem3, EmbedItem4], 
            files = [fileBoots, fileMythic, FileItem1, FileItem2, FileItem3, FileItem4])

# Choose random summoner spell
def ChooseSummonerSpell(role, gamemode):
    lst = os.listdir("img/SummonerSpells/")
    if gamemode == "aram":
        for elem in lst:
            if elem == "SummonerSmite.png" or elem == "SummonerTeleport.png":
                lst.remove(elem)
        SummonerSpell1 = random.choice(lst)
        SummonerSpell2 = random.choice(lst)
        while SummonerSpell1 == SummonerSpell2:
            SummonerSpell2 = random.choice(lst)
        return SummonerSpell1, SummonerSpell2
    else:
        for elem in lst:
            if elem == "SummonerMana.png" or elem == "SummonerSnowball.png" or elem == "SummonerSmite.png":
                lst.remove(elem)
        if role == "jungle":
            SummonerSpell1 = "SummonerSmite.png"
        else:
            SummonerSpell1 = random.choice(lst)
        SummonerSpell2 = random.choice(lst)
        while SummonerSpell1 == SummonerSpell2:
            SummonerSpell2 = random.choice(lst)
        return SummonerSpell1, SummonerSpell2

# Run bot
def main():
    load_dotenv()
    token = getenv('TOKEN')
    DefineTree()
    client.run(token)

main()