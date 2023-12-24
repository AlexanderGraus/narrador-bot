import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.command(name='on', help='Comienza el proceso de crear una historia!')
async def crear_historia(ctx):
    await ctx.send('me alegro bro! empecemos a escribir \n elige tus opciones: 1,2,3')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
bot.run(TOKEN)
