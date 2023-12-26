import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands

from utils import CARTAS

MENSAJE_DE_BIENVENIDA = """
    Las cartas de narración son un disparador para construir historias.
"""

load_dotenv()
# ----------- Variables -----------------------------

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
libros = {
    'author_id': {
        'contador_turnos': 0,
        'cuento': ''
    }
}


# ----------- Utils -----------------------------
def tirar_carta(carta_id=None, mazo_id=None):
    if not carta_id:
        if mazo_id:
            mazo = [carta_id for carta_id in CARTAS.keys() if carta_id[0] == mazo_id]
        else:
            mazo = list(CARTAS.keys())
        carta_id = random.choice(mazo)
    carta = CARTAS.get(carta_id)
    carta_formatted = f"{carta_id}: **{carta['titulo']}** \n{carta['descripcion']}"
    return carta_formatted


def escribir_cuento(autor_id, cuento):
    libros.update({autor_id: {'cuento': cuento}})


def buscar_cuento(autor_id):
    return libros.get(autor_id, {}).get('cuento', '')


# ----------- Commands -----------------------------
@bot.command(name='empezar', help='Comienza el proceso de crear una historia!')
async def crear_historia(ctx):
    await ctx.send(MENSAJE_DE_BIENVENIDA)
    escribir_cuento(ctx.author.id, '')
    await ctx.send(tirar_carta('1a'))


@bot.command(name='escribir', help='Despues de recibir una carta agregale texto a tu cuento!')
async def escribir(ctx, *, texto):
    cuento = buscar_cuento(ctx.author.id)
    cuento += texto + '. '
    escribir_cuento(ctx.author.id, cuento)
    await ctx.send('Nueva carta!\n'+tirar_carta())


@bot.command(name='fin', help='Cerra tu historia y mira el cuento terminado!')
async def cerrar_historia(ctx):
    await ctx.send(
        f"Muy bien, excelente historia! Así quedó tu cuento: \n`{buscar_cuento(ctx.author.id)}`"
    )
    escribir_cuento(ctx.author.id, '')


# ------------------ Error Handler -------------------------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Ups, aca hay un problema de permisos, fijate de tener la jerarquia necesaria!.')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Hmm no conozco ese comando, proba con !help para que te tire la lista de ordenes disponibles')
    else:
        await ctx.send(error.args[0])

bot.run(TOKEN)
