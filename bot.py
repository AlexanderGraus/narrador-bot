import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

MENSAJE_DE_BIENVENIDA = """
    Las cartas de narración son un disparador para construir historias.
"""

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
libros = {}


def tirar_carta():
    return random.choice(('1a', '1b', '1c'))


@bot.command(name='empezar', help='Comienza el proceso de crear una historia!')
async def crear_historia(ctx):
    await ctx.send(MENSAJE_DE_BIENVENIDA)
    libros.update({ctx.author.id: {'cuento': ''}})
    await ctx.send("Personaje hace: un personaje cualquiera realiza una acción que modifica la situación o cambia lugar o tiempo")


@bot.command(name='escribir', help='Despues de recibir una carta agregale texto a tu cuento!')
async def escribir(ctx, *, texto):
    cuento = libros.get(ctx.author.id, {}).get('cuento', '')
    cuento += texto + '. '
    libros.update({ctx.author.id: {'cuento': cuento}})
    await ctx.send(cuento+'\n'+tirar_carta())


@bot.command(name='fin', help='Cerra tu historia y mira el cuento terminado!')
async def cerrar_historia(ctx):
    await ctx.send('Muy bien, excelente historia! Así quedó tu cuento: \n' + libros.get(ctx.author.id).get('cuento'))
    libros.update({ctx.author.id: {'cuento': ''}})


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Ups, aca hay un problema de permisos, fijate de tener la jerarquia necesaria!.')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Hmm no conozco ese comando, proba con !help para que te tire la lista de ordenes disponibles')
    else:
        await ctx.send(error.args[0])

bot.run(TOKEN)
