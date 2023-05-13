import discord
from discord import app_commands
from dotenv import load_dotenv
from os import getenv
import random
import os
import Node
from Hashtable import Hashtable
import Tree
from requests import get
from PIL import Image
from json import load

# Bot client
intents = discord.Intents.all()
client = discord.Client(intents = intents)
bot = app_commands.CommandTree(client)

MyConversation = Hashtable([("User", ["Content"])])

# Event sync commands
@client.event
async def on_ready():
    await bot.sync()
    LoadHistorical()
    print("Ready!")

# Event on message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = MyConversation.get_value(str(message.author.id))
    if content != None:
        content.append(message.content)
        MyConversation.update_bucket([(str(message.author.id), content)])
    else:
        MyConversation._assign_buckets([(str(message.author.id), [message.content])])


# Event User Conversation
@bot.command(name = "conversation", description = "User Conversation")
async def UserConversation(interaction):
    await interaction.response.send_message(MyConversation.get_value(str(interaction.user.id)), ephemeral = True)

# Add command to list_chained
def AddCmd(name, author):
    Node.AllCmd.append(name, author)

# Event on interaction
@client.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.application_command:
        AddCmd(f"{interaction.data['name']}", f"{interaction.user.id}")

# Event to disconnect the bot
@bot.command(name = "disconnect", description = "Disconnect the bot")
async def Disconnect(interaction):
    Node.AllCmd.save_to_json()
    await interaction.response.send_message("Disconnecting...", ephemeral = True)
    await client.close()

# Event delete a certain ammount of messages
@bot.command(name = "delete", description = "Delete a certain amount of messages")
async def DeleteMessage(interaction, amount: int):
    await interaction.response.send_message(f"{amount} messages deleted", ephemeral = True)
    await interaction.channel.purge(limit= amount)

# Event last command of a user
@bot.command(name = "lastcmd", description = "Last command of a user")
async def LastCmd(interaction):
    await interaction.response.send_message(f"Last command is : {Node.AllCmd.last_node.data}")

# Event all commands of a user
@bot.command(name = "allcmd", description = "All commands of a user")
async def AllCmds(interaction, user : discord.User = None):
    if user == None:
        user = interaction.user
    current_node = Node.AllCmd.first_node
    embed = discord.Embed(title = f"All commands of {user.name}", color = 0x00ff00)
    while current_node != None:
        if current_node.author == str(user.id):
            embed.add_field(name="Command", value=f"{current_node.data}", inline=False)
        current_node = current_node.next_node
    await interaction.response.send_message(embed = embed)

# Event clear commands historic
@bot.command(name = "clearcmd", description = "Clear commands historic")
async def ClearCmd(interaction):
    Node.AllCmd.clear()
    await interaction.response.send_message("Historic cleared", ephemeral = True)

# Event move in historic
@bot.command(name = "travelcmd", description = "Move in historic")
async def TravelCmd(interaction, index : int):
    if index > Node.AllCmd.size()-1 or index < 0:
        index = Node.AllCmd.size()
    current_node = Node.AllCmd.first_node
    i = 1
    while i < index:
        current_node = current_node.next_node
        i += 1
    embed = discord.Embed(title = f"Command at index {index}", description=current_node.data, color = 0x00ff00)
    await interaction.response.send_message(embed=embed)
    ##### TODO: ADD BUTTON TO TRAVEL IN HISTORIC

# Event to show all available commands
@bot.command(name = "helpcmd", description = "Show all available commands")
async def HelpCmd(interaction):
    embed = discord.Embed(title = "All available commands", color = 0x00ff00)
    embed.add_field(name="allcmd", value="Show all commands made by an user", inline=False)
    embed.add_field(name="lastcmd", value="Show last command used", inline=False)
    embed.add_field(name="travelcmd", value="Move in historic", inline=False)
    embed.add_field(name="clearcmd", value="Clear historic", inline=False)
    embed.add_field(name="delete", value="Delete a certain amount of messages", inline=False)
    embed.add_field(name="disconnect", value="Disconnect the bot", inline=False)
    embed.add_field(name="conversation", value="Show conversation with the bot", inline=False)
    embed.add_field(name="bravery", value="Do a random Ultimate Bravery", inline=False)
    embed.add_field(name="help", value="Talk with the bot", inline=False)
    embed.add_field(name="speakbout", value="Ask the bot if he talks about a subject", inline=False)
    await interaction.response.send_message(embed = embed)

# Event Chat bot
@bot.command(name = "help", description = "Chat bot")
async def ChatBot(interaction):
    await interaction.response.send_message(Tree.Chatbot.first_question())
    over = False
    content = ""
    while over == False :
        message = await client.wait_for("message", check = lambda message: message.author == interaction.user)
        if message.content == "reset":
            await interaction.channel.send("Chatbot reset")
            await interaction.channel.send(Tree.Chatbot.first_question())
            continue
        if message.content == "soloq" or message.content == "flex" or message.content == "level":
            content = message.content
        tempo = Tree.Chatbot.send_answer(message.content)
        await interaction.channel.send(tempo)
        if tempo == "Give a summoner name :":
            over = True
    message = await client.wait_for("message", check = lambda message: message.author == interaction.user)

    user = get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + message.content + "?api_key=" + getenv('RIOT_KEY'))
    userJson = user.json()
    if content == "level":
        await interaction.channel.send(f"Account Level : {userJson['summonerLevel']}")
    else:
        result = get("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + userJson["id"] + "?api_key=" + getenv('RIOT_KEY'))
        resultJson = result.json()
        noRank = True
        for elem in resultJson:
            if elem["queueType"] == "RANKED_SOLO_5x5" and content == "soloq":
                await interaction.channel.send(f"Rank SoloQ : {elem['tier']} {elem['rank']} {elem['leaguePoints']} LP")
                noRank = False
                break
            elif elem["queueType"] == "RANKED_FLEX_SR" and content == "flex":
                await interaction.channel.send(f"Rank Flex : {elem['tier']} {elem['rank']} {elem['leaguePoints']} LP")
                noRank = False
                break
        if noRank:
            await interaction.channel.send("The summoner is not ranked in this queue")

# Event Speak about Chatbot
@bot.command(name = "speakabout", description = "Speak about Chatbot")
async def SpeakAbout(interaction, subject : str):
    Tree.Chatbot.first_question()
    if Tree.Chatbot.send_answer(subject) == "Write which command you want to use : level / rank" :
        await interaction.response.send_message(f"Chatbot isn't able to speak about {subject}", ephemeral = True)
    else:
        await interaction.response.send_message(f"Chatbot is able to speak about {subject}", ephemeral = True)

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

    # Role
    if gamemode != "aram":
        role = role.lower()
        roles = ["top","jungle","mid","bot","support"]
        if role == "" or role not in roles:
            role = random.choice(roles)

    # Spell
    spell = random.choice(os.listdir(f"img/Spells/{champion}/"))

    # Summoner Spell
    Summoner1, Summoner2 = ChooseSummonerSpell(role, gamemode.lower())

    # Mix Champion Role Spell SummonerSpell
    imageChampion = Image.open(f"img/Champions/{champion}.png")
    imageSpell = Image.open(f"img/Spells/{champion}/{spell}")
    imageSummoner1 = Image.open(f"img/SummonerSpells/{Summoner1}")
    imageSummoner2 = Image.open(f"img/SummonerSpells/{Summoner2}")

    if gamemode == "aram":
        imageMix = Image.new("RGBA", (imageChampion.width + imageSpell.width + imageSummoner1.width + imageSummoner2.width, imageChampion.height))
        imageMix.paste(imageChampion, (0, 0))
        imageMix.paste(imageSpell, (imageChampion.width, 0))
        imageMix.paste(imageSummoner1, (imageChampion.width + imageSpell.width, 0))
        imageMix.paste(imageSummoner2, (imageChampion.width + imageSpell.width + imageSummoner1.width, 0))
        imageMix.save("img/tempo/mix.png")
    else:
        imageRole = Image.open(f"img/Roles/{role}.png")
        imageMix = Image.new("RGBA", (imageChampion.width + imageRole.width + imageSpell.width + imageSummoner1.width + imageSummoner2.width, imageChampion.height))
        imageMix.paste(imageChampion, (0, 0))
        imageMix.paste(imageRole, (imageChampion.width, 0))
        imageMix.paste(imageSpell, (imageChampion.width + imageRole.width, 0))
        imageMix.paste(imageSummoner1, (imageChampion.width + imageRole.width + imageSpell.width, 0))
        imageMix.paste(imageSummoner2, (imageChampion.width + imageRole.width + imageSpell.width + imageSummoner1.width, 0))
        imageMix.save("img/tempo/mix.png")

    EmbedMix = discord.Embed(title = "Champion", color = 0x00ff00)
    EmbedMix.set_image(url="attachment://mix.png")
    FileMix = discord.File("img/tempo/mix.png")

    # Items
    Boots = random.choice(os.listdir("img/Items/Boots/"))
    ItemMythic = random.choice(os.listdir("img/Items/Mythic/"))
    ItemsLegendary = random.sample(os.listdir("img/Items/Legendary/"), 4)

    imageBoots = Image.open(f"img/Items/Boots/{Boots}")
    imageMythic = Image.open(f"img/Items/Mythic/{ItemMythic}")
    image1 = Image.open(f"img/Items/Legendary/{ItemsLegendary[0]}")
    image2 = Image.open(f"img/Items/Legendary/{ItemsLegendary[1]}")
    image3 = Image.open(f"img/Items/Legendary/{ItemsLegendary[2]}")
    image4 = Image.open(f"img/Items/Legendary/{ItemsLegendary[3]}")

    if role == "support" or role == "jungle":
        role.capitalize()
        ItemStarter = random.choice(os.listdir(f"img/Items/{role}/"))

        new_image = Image.new('RGB', (image1.width*7, image1.height))
        imageStarter = Image.open(f"img/Items/{role}/{ItemStarter}")
        new_image.paste(imageStarter, (0,0))
        new_image.paste(imageBoots, (image1.width*1,0))
        new_image.paste(imageMythic, (image1.width*2,0))
        new_image.paste(image1, (image1.width*3,0))
        new_image.paste(image2, (image1.width*4,0))
        new_image.paste(image3, (image1.width*5,0))
        new_image.paste(image4, (image1.width*6,0))
    else :
        new_image = Image.new('RGB', (image1.width*6, image1.height))
        new_image.paste(imageBoots, (0,0))
        new_image.paste(imageMythic, (image1.width*1,0))
        new_image.paste(image1, (image1.width*2,0))
        new_image.paste(image2, (image1.width*3,0))
        new_image.paste(image3, (image1.width*4,0))
        new_image.paste(image4, (image1.width*5,0))
    
    new_image.save(f"img/tempo/legendary.png")
    EmbedItems = discord.Embed(title = "Items", color = 0x00ff00)
    EmbedItems.set_image(url="attachment://legendary.png")
    FileItems = discord.File(f"img/tempo/legendary.png")

    # Runes
    Runes = ["Precision","Domination","Sorcery","Resolve","Inspiration"]

    rune = random.sample(Runes, 2)
    PrimaryRune = rune[0]
    MajorRune = random.choice(os.listdir(f"img/Runes/{PrimaryRune}/Major/"))
    Rune1 = random.choice(os.listdir(f"img/Runes/{PrimaryRune}/Rune1/"))
    Rune2 = random.choice(os.listdir(f"img/Runes/{PrimaryRune}/Rune2/"))
    Rune3 = random.choice(os.listdir(f"img/Runes/{PrimaryRune}/Rune3/"))

    MinorRune = rune[1]
    SecondRune = random.sample(["Rune1","Rune2","Rune3"], 2)
    Rune4 = random.choice(os.listdir(f"img/Runes/{MinorRune}/{SecondRune[0]}/"))
    Rune5 = random.choice(os.listdir(f"img/Runes/{MinorRune}/{SecondRune[1]}/"))

    Adap1 = random.choice(os.listdir("img/Runes/Adaptive/Adap1/"))
    Adap2 = random.choice(os.listdir("img/Runes/Adaptive/Adap2/"))
    Adap3 = random.choice(os.listdir("img/Runes/Adaptive/Adap3/"))

    imageMajorRune = Image.open(f"img/Runes/{PrimaryRune}/Major/{MajorRune}")
    imageRune1 = Image.open(f"img/Runes/{PrimaryRune}/Rune1/{Rune1}")
    imageRune2 = Image.open(f"img/Runes/{PrimaryRune}/Rune2/{Rune2}")
    imageRune3 = Image.open(f"img/Runes/{PrimaryRune}/Rune3/{Rune3}")
    imageRune4 = Image.open(f"img/Runes/{MinorRune}/{SecondRune[0]}/{Rune4}")
    imageRune5 = Image.open(f"img/Runes/{MinorRune}/{SecondRune[1]}/{Rune5}")
    imageAdap1 = Image.open(f"img/Runes/Adaptive/Adap1/{Adap1}")
    imageAdap2 = Image.open(f"img/Runes/Adaptive/Adap2/{Adap2}")
    imageAdap3 = Image.open(f"img/Runes/Adaptive/Adap3/{Adap3}")

    imageRune = Image.new("RGBA", (imageMajorRune.width + imageRune1.width + imageRune4.width + imageAdap1.width, imageMajorRune.height))
    imageRune.paste(imageMajorRune, (0,0))
    imageRune.paste(imageRune1, (imageMajorRune.width,0))
    imageRune.paste(imageRune2, (imageMajorRune.width, imageRune1.height))
    imageRune.paste(imageRune3, (imageMajorRune.width, imageRune1.height + imageRune2.height))
    imageRune.paste(imageRune4, (imageMajorRune.width + imageRune1.width, 0))
    imageRune.paste(imageRune5, (imageMajorRune.width + imageRune1.width, imageRune4.width))
    imageRune.paste(imageAdap1, (imageMajorRune.width + imageRune1.width + imageRune4.width, 0))
    imageRune.paste(imageAdap2, (imageMajorRune.width + imageRune1.width + imageRune4.width, imageAdap1.height))
    imageRune.paste(imageAdap3, (imageMajorRune.width + imageRune1.width + imageRune4.width, imageAdap1.height*2))

    imageRune.save(f"img/tempo/rune.png")

    EmbedRunes = discord.Embed(title = "Runes", color = 0x00ff00)
    EmbedRunes.set_image(url="attachment://rune.png")
    FileRunes = discord.File(f"img/tempo/rune.png")

    await interaction.response.send_message("Your Ultimate Bravery :")
    await interaction.channel.send(embeds = [EmbedMix, EmbedItems, EmbedRunes], files= [FileMix, FileItems, FileRunes])

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

# Load historical data on start
def LoadHistorical():
    with open("historical.json", 'r') as file:
        data = load(file)
        for elem in data:
            Node.AllCmd.append(elem["data"], elem["author"])

# Run bot
def main():
    load_dotenv()
    token = getenv('TOKEN')
    client.run(token)

main()