import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

MENSAJE_DE_BIENVENIDA = """
    Las cartas de narración son un disparador para construir historias.
"""

load_dotenv()
# ----------- Variables -----------------------------

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
libros = {}

CARTAS = {
    "1a": {
        'titulo': 'Personaje Hace',
        'descripcion': '`Un personaje cualquiera realiza una acción que modifica la situación o cambia lugar o tiempo`',
    },
    "1b": {
        'titulo': 'Entonces',
        'descripcion': '`Un personaje cualquiera realiza una accion que continua el sentido en que se desarrolla la historia`',
    },
    "1c": {
        'titulo': 'Pero',
        'descripcion': '`Un personaje o situacion cualquiera rompe, interrumpe o cambia el sentido en que se desarrolla la historia`',
    },
    "2a": {
        'titulo': 'Sensacion',
        'descripcion': '`Algo que se puede percibir con alguno/s de los cinco sentidos`',
    },
    "2b": {
        'titulo': 'Pensamiento',
        'descripcion': '`Lo que pasa por la cabeza de un personaje, con su punto de vista, emociones o contradicciones`',
    },
    "2c": {
        'titulo': 'Detalle',
        'descripcion': '`Una característica de la situacióno una acción nos transmite un ambiente o sentimiento. Detenerse en lo único, usar metáfora o comparación`',
    },
    "2d": {
        'titulo': 'Sentimiento',
        'descripcion': '`La emoción de un personaje, expresada como sensación el cuerpo, metáfora o comparación`',
    },
    "2e": {
        'titulo': 'Contexto',
        'descripcion': '`Sugerimos en qué lugar y momento sucede la acción, sin necesidad de decirlo explícitamente`',
    },
    "2f": {
        'titulo': 'Caracteristica de personaje',
        'descripcion': '`Una característica física, psicológica o social que es propia del personaje. Detenerse en lo único, usar metáfora o comparación`',
    },
    "3a": {
        'titulo': 'Porque antes',
        'descripcion': '`Algo que no sabíamos de un personaje o acción, que explica o nos hace cambiar lo que opinábamos o esperábamos`',
    },
    "3b": {
        'titulo': 'Mientras tanto',
        'descripcion': '`"Un Personaje Hace", al mismo tiempo, en otro lugar `',
    },
    "3c": {
        'titulo': 'Elemento repetido',
        'descripcion': '`Alguna información, objeto, sentimiento, símbolo que apareció antes, reaparace y nos muestra la continuidad o diferencias`',
    },
    "3d": {
        'titulo': 'Personaje quiere otra cosa',
        'descripcion': '`Uno de los personajes intenta hacer algo opuesto al deseo de otro`',
    },
    "3e": {
        'titulo': 'Diálogo',
        'descripcion': '`Dos personajes hablan (o callan), cada uno quiere llevar la conversación a un resultado o tema diferente`',
    },
    "3f": {
        'titulo': 'Personaje cambia',
        'descripcion': '`Un personaje hace algo contrario a lo que esperábamos`',
    },
    "4a": {
        'titulo': 'Parodia o cita',
        'descripcion': '`Reproducimos una manera de hablar, un género o una escena de una historia conocida`',
    },
    "4b": {
        'titulo': 'Síntesis',
        'descripcion': '`Una frase de 3 a 5 palabras`',
    },
    "4c": {
        'titulo': 'Amontonamiento',
        'descripcion': '`Una frase larga, que describe mucho, enumera acciones, sensaciones, objetos u otros elementos de manera acelerada`',
    },
    "4d": {
        'titulo': 'Reflexión',
        'descripcion': '`Una frase filosófica, poética, una conclusión de la vida, un descrubrimiento`',
    },
    "4e": {
        'titulo': 'Sorpresa',
        'descripcion': '`Un personaje, elemento o acción que no tenga nada que ver con lo que está pasando`',
    },
    "4f": {
        'titulo': 'Lo inconprensible',
        'descripcion': '`No todo tiene que ser claro. Puede haber misterio. Algo inasible, un secreto que no se revela, una frase inaccesible`',
    },
}


# ----------- Utils -----------------------------
def tirar_carta(id=None):
    if not id:
        id = random.choice(('1a', '1b', '1c'))
    carta = CARTAS.get(id)
    carta_formatted = f"{id}: **{carta['titulo']}** \n{carta['descripcion']}"
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
