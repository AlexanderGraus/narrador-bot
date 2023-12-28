import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands

from utils import CARTAS

MENSAJE_DE_BIENVENIDA = """
    Las cartas de narración son un disparador para construir historias.
    explicacion de comandos + dinamicas
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
        carta_id = random.choice(mazo) if mazo else None
    carta = CARTAS.get(carta_id, {})
    if not carta:
        return "Esa carta no exite, pa, si queres mas cartas... Inventalas"
    return f"{carta_id}: **{carta['titulo']}** \n{carta['descripcion']}"


def mazos_disponibles(turnos):
    mazos = []
    for i in range(1, turnos+1):
        mazos.append(i)
        if i == 4:
            break
    return f"Tenes disponibles los mazos {str(mazos)}"


def escribir_libro(autor_id, contador_turnos=0, cuento=''):
    libros.update(
        {
            autor_id:  {
                'contador_turnos': contador_turnos,
                'cuento': cuento,
            }
        }
    )


def buscar_libro(autor_id):
    return libros.get(autor_id, {})


# ----------- Commands -----------------------------
@bot.command(name='empezar', help='Comienza el proceso de crear una historia!')
async def crear_historia(ctx):
    await ctx.send(MENSAJE_DE_BIENVENIDA)
    escribir_libro(ctx.author.id)
    await ctx.send(tirar_carta('1a'))


@bot.command(name='carta', help='Tirar una carta nueva, indicando de cuál mazo queres sacar. En caso de no elegir ninguno saca una al azar de cualquier mazo')
async def carta(ctx, id=None):
    if not id:
        await ctx.send(tirar_carta())
        return
    if len(id) > 1:
        carta_id = id
        await ctx.send(tirar_carta(carta_id=carta_id))
    else:
        mazo_id = int(id)
        if mazo_id > 4:
            raise Exception("Para viejo, yo tengo hasta 4 mazos, si queres mas cartas inventalas")
        turnos = buscar_libro(ctx.author.id).get('contador_turnos', 0)
        if int(mazo_id) > turnos:
            await ctx.send('Ah que picaro que sos eligiendo de otro mazo, muy bien las reglas en la literatura estan PARA ROMPERSE')
        await ctx.send(tirar_carta(mazo_id=mazo_id))


@bot.command(name='escribir', help='Despues de recibir una carta agregale texto a tu cuento!')
async def escribir(ctx, *, texto):
    cuento = buscar_libro(ctx.author.id).get('cuento', '')
    contador_turnos = buscar_libro(ctx.author.id).get('contador_turnos', 0)

    contador_turnos += 1
    cuento += texto + '. '
    escribir_libro(ctx.author.id, contador_turnos, cuento)

    await ctx.send(mazos_disponibles(contador_turnos))


@bot.command(name='fin', help='Cerra tu historia y mira el cuento terminado!')
async def cerrar_historia(ctx):
    await ctx.send(
        f"Muy bien, excelente historia! Así quedó tu cuento: \n>>>{buscar_libro(ctx.author.id).get('cuento', '')}"
    )
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
