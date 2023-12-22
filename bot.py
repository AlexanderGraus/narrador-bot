import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} estas conectado al servidor:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'miembros:\n - {members}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'quiero escribir!':
        await message.channel.send(
            "Hola bienvenido al bot para crear historias!"
        )

client.run(TOKEN)
