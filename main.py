import discord
from discord.ext import commands
import asyncio  # Import to use asyncio.sleep, for me it's easir then use time
from bs4 import BeautifulSoup # BS is for the scraping of HTML file

# Perms and starting the bot
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
bot = commands.Bot(command_prefix="TL!", intents=permissoes)

# Global VAR used, in the first attempt, I tried to manipulate the HTML online, but had no permissions to access tierlist, so it's local for now
URL = None
tempo = 30  # Time used to users to vote

# This function is to check if user is an admin
def isLT():
    async def predicate(ctx):
        cargo = discord.utils.get(ctx.author.roles, name="Allies LT") #Here you put your admin role in name
        if cargo is None:
            await ctx.reply("Você não possui permissão para isso.")
            return False
        return True
    return commands.check(predicate)

# function to check if user is registered in Participantes.txt file
def is_registered(user_id):
    with open("Participantes.txt", "r") as file:
        participantes = file.read().splitlines()
    return str(user_id) in participantes

# Command: tierlist start the update of Options.txt with tierlist options in html file
@bot.command()
@isLT()
async def tierlist(ctx):

    # read tierlist.html content
    with open("tierlist.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # this is for the HTML parsing
    soup = BeautifulSoup(html_content, "html.parser")
    carousel_div = soup.find("div", id="create-image-carousel")

    if carousel_div is None:
        await ctx.reply("Não foi possível encontrar a div com id 'create-image-carousel'. Verifique o arquivo HTML.")
        return

    # find itens from class 'character' and extract URL from images
    items = carousel_div.find_all("div", class_="character")

    if not items:
        await ctx.reply("Não foram encontrados itens com a classe 'character' no arquivo HTML.")
        return

    # clear the Options.txt and add new images URL
    with open("Options.txt", "w") as file:
        for item in items:
            # Extract the image url from style attribute
            style = item.get("style", "")
            if "background-image" in style:
                start = style.find('url("') + len('url("')
                end = style.find('")', start)
                image_url = style[start:end]
                file.write(image_url + "\n")

    await ctx.reply("Items atualizados com sucesso no Options.txt.")

# Command: add + @user
@bot.command()
@isLT()
async def add(ctx, member: discord.Member):
    with open("Participantes.txt", "a") as file:
        file.write(f"{member.id}\n")
    await ctx.reply(f"{member.display_name} foi adicionado aos participantes.")

# Command: ZerarParticipantes is to clear the Participantes.txt user list
@bot.command()
@isLT()
async def ZerarParticipantes(ctx):
    with open("Participantes.txt", "w") as file:
        file.truncate(0)
    await ctx.reply("A lista de participantes foi limpa.")

# Command: Start it's for start
@bot.command()
@isLT()
async def Start(ctx):
    with open("Options.txt", "r") as file:
        options = file.readlines()

    if not options:
        await ctx.reply("Não há itens para votar.")
        return

    option = options[0].strip()

    # check if string contains 'url("'
    if 'url("' in option:
        try:
            # Extract URL from image
            image_url = option.split('url("')[1].split('")')[0]
            image_url = "https://tiermaker.com" + image_url  # Adjust to fix the full URL
        except IndexError:
            await ctx.reply("Erro ao processar a URL da imagem.")
            return
    else:
        await ctx.reply("Formato inválido encontrado no arquivo Options.txt.")
        return

    message = await ctx.send(image_url)
    emojis = ["❤", "🧡", "💛", "💚", "💙"]
    for emoji in emojis:
        await message.add_reaction(emoji)

    # Wait for the 30 seconds
    await asyncio.sleep(30)

    # Calculate the average of votes
    message = await ctx.channel.fetch_message(message.id)
    reactions = message.reactions
    total_votes = sum([r.count for r in reactions])
    total_score = sum([r.count * (5 - i) for i, r in enumerate(reactions)])  # Emojis in order from 5 to 1
    media = (total_score - 15) / (total_votes - 5) if total_votes > 5 else 0

    # Final check
    if media > 4.4:
        resultado = "❤"
    elif media > 3.4:
        resultado = "🧡"
    elif media > 2.4:
        resultado = "💛"
    elif media > 1.4:
        resultado = "💚"
    else:
        resultado = "💙"

    await ctx.reply(f"Resultado final: {resultado}")

# Function to check if user is in Participantes file.
def is_registered(user_id):
    with open("Participantes.txt", "r") as file:
        participantes = file.read().splitlines()
    return str(user_id) in participantes

# Event that read reactions added in image
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return  # Ignora bots reactions

    # Check if user is registered in "participantes" file
    if not is_registered(user.id):
        # Remove all users roles (If you want just comment this for loop so it can be more soft)
        for role in user.roles[1:]:  # Ignore @everyone role
            await user.remove_roles(role)

        # Remove reaction added by user
        await reaction.message.remove_reaction(reaction.emoji, user)

        # Send a warning message in channel informing that user was remvoed
        await reaction.message.channel.send(f"{user.display_name} não está registrado e teve os cargos e reações removidos.")
        
# Command: next
@bot.command()
@isLT()
async def next(ctx):
    with open("Options.txt", "r") as file:
        options = file.readlines()

    if len(options) <= 1:
        await ctx.reply("Não há mais itens para votar.")
        return

    with open("Options.txt", "w") as file:
        file.writelines(options[1:])  # Remove the firs item

    await Start(ctx)
    
bot.run("KEY")