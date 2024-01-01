"""
Discord bot that guide you through the process of creating a story.
Its based on the game designed by Fer Catz (fercatz.talleres@gmail.com)
"""

import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands

from utils import (
    MENSAJE_DE_BIENVENIDA,
    MENSAJE_PRIMERA_CARTA,
    CREDITO_FER_CATZ,
    mezclar_mazos,
    tirar_carta,
    escribir_libro,
    buscar_libro,
    mazos_disponibles,
)


load_dotenv()
# ----------- Variables -----------------------------

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
mazos_mezclados = mezclar_mazos()
libros = {
    'author_id': {
        'contador_turnos': 0,
        'cuento': ''
    }
}


# ----------- Commands -----------------------------
@bot.command(name='empezar', help='Comienza el proceso de crear una historia!')
async def crear_historia(ctx):
    await ctx.send(MENSAJE_DE_BIENVENIDA)
    escribir_libro(libros, ctx.author.id)
    await ctx.send('Empecemos con la __primera carta!__')
    await ctx.send(tirar_carta(carta_id='1a'))
    await ctx.send('Ahora poné `!escribir` y a continuacion tu texto para guardar el primer fragmento :)')


@bot.command(name='carta', help='Tirar una carta nueva, indicando de cuál mazo queres sacar. En caso de no elegir ninguno saca una al azar de cualquier mazo')
async def carta(ctx, mazo_id):
    if int(mazo_id) > 4:
        raise Exception('Perdon, tengo hasta 4 mazos, por ahora...')
    turnos = buscar_libro(libros, ctx.author.id).get('contador_turnos', 0)
    if int(mazo_id) > turnos:
        await ctx.send('Ah que picaro que sos eligiendo de otro mazo, muy bien las reglas en la literatura estan PARA ROMPERSE')
    await ctx.send(tirar_carta(mazo_id))


@bot.command(name='escribir', help='Despues de recibir una carta agregale texto a tu cuento!')
async def escribir(ctx, *, texto):
    libro =  buscar_libro(libros, ctx.author.id)
    cuento = libro.get('cuento', '')
    contador_turnos = libro.get('contador_turnos', 0)

    contador_turnos += 1
    cuento += texto + '. '
    escribir_libro(ctx.author.id, contador_turnos, cuento)
    if contador_turnos == 1:
        await ctx.send(MENSAJE_PRIMERA_CARTA)
    await ctx.send(mazos_disponibles(contador_turnos))


@bot.command(name='fin', help='Cerra tu historia y mira el cuento terminado!')
async def cerrar_historia(ctx):
    await ctx.send(
        f"Muy bien, excelente historia! Así quedó tu cuento: \n`{buscar_libro(ctx.author.id).get('cuento', '')}`"
    )
    await ctx.send(CREDITO_FER_CATZ)
    escribir_libro(ctx.author.id)


# ------------------ Error Handler -------------------------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Ups, aca hay un problema de permisos, fijate de tener la jerarquia necesaria!.')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Hmm no conozco ese comando, proba con !help para que te tire la lista de ordenes disponibles')
    else:
        await ctx.send(error.original)

bot.run(TOKEN)
