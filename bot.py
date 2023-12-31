"""
Discord bot that guide you through the process of creating a story. 
Its based on the game designed by Fer Catz (fercatz.talleres@gmail.com)
"""

import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands

from utils import CARTAS

MENSAJE_DE_BIENVENIDA = """
    ¡Hola! bienvenido, vamos a jugar a escribir un cuento, en menos de 5 minutos...
    Para eso te voy a ir tirando cartas, usalas como disparador y escribí tu texto, así, como surja, no lo pienses mucho.
    Una vez que sientas que la historia ha terminado pone `!fin` y yo te devuelvo lo que escribiste... te vas a sorprender
    >>> AHHH! Me olvidaba. El creador de este juego se llama **Fer Catz**, da talleres de escritura creativa y te ayuda con tu proceso, estés donde estés.
    Podés escribirle un mail: [fercatz.talleres@gmail.com](https://mailto:fercatz.talleres@gmail.com) (o buscarlo en facebook e instagram, eso que usan ustedes los jóvenes) Para agradecerle o sugerirle mejoras... Yo le sugerí que venga a Discord, pero no me hizo caso :(
"""
MENSAJE_PRIMERA_CARTA = """
    Usá el comando `!carta` para pedirme una... carta, obvio. A continuacion indicame de cuál mazo queres que la saque.
    Si no pones nada te devuelvo una al azar
    *psss incluso pódes ponerme la carta especifica que queres*

    Tipo de mazos:
    1) son los recursos basicos de una narracion. podes sacar siempre de acá, no fallan.
    2) son recursos de inmersion y descripcion de la historia
    3) recursos que enriquecen el orden y complejidad del argumento
    4) un condimento fuerte... Usar solo uno por relato... dos como mucho, ojo con abusar! jaj

    **Tip!** para empezar te aconsejo que elijas sacar del mazo (1) que tiene las estructuras básicas.
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
    return f"Podes sacar una carta de los mazos {str(mazos)}"


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
    await ctx.send('Empecemos con la __primera carta!__')
    await ctx.send(tirar_carta('1a'))
    await ctx.send('Ahora poné `!escribir` y a continuacion tu texto para guardar el primer fragmento :)')


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
        if mazo_id > turnos:
            await ctx.send('Ah que picaro que sos eligiendo de otro mazo, muy bien las reglas en la literatura estan PARA ROMPERSE')
        await ctx.send(tirar_carta(mazo_id=str(mazo_id)))


@bot.command(name='escribir', help='Despues de recibir una carta agregale texto a tu cuento!')
async def escribir(ctx, *, texto):
    cuento = buscar_libro(ctx.author.id).get('cuento', '')
    contador_turnos = buscar_libro(ctx.author.id).get('contador_turnos', 0)

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
