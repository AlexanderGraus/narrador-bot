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
"""
MENSAJE_PRIMERA_CARTA = """
    Usá el comando `!carta` para pedirme una... carta, obvio. A continuacion indicame de cuál mazo queres que la saque.

    Tipo de mazos (asi sabes que elegir):
    1) son los recursos basicos de una narracion. podes sacar siempre de acá, no fallan.
    2) son recursos de inmersion y descripcion de la historia
    3) recursos que enriquecen el orden y complejidad del argumento
    4) un condimento fuerte... Usar solo uno por relato... dos como mucho, ojo con abusar! jaj

    **Tip!** para empezar te aconsejo que elijas sacar del mazo (1) que tiene las estructuras básicas.
"""
CREDITO_FER_CATZ = """
    \n>>> AHHH! Me olvidaba. El creador de este juego se llama **Fer Catz**, da talleres de escritura creativa y te ayuda con tu proceso, estés donde estés.
    Podés escribirle un mail: [fercatz.talleres@gmail.com](https://mailto:fercatz.talleres@gmail.com) (o buscarlo en facebook e instagram, eso que usan ustedes los jóvenes) Para agradecerle o sugerirle mejoras... Yo le sugerí que venga a Discord, pero no me hizo caso :(
"""
load_dotenv()
# ----------- Variables -----------------------------

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
mazos_mezclados = {}
libros = {
    'author_id': {
        'contador_turnos': 0,
        'cuento': ''
    }
}


# ----------- Utils -----------------------------
def armar_mazos():
    mazos = {}
    cartas_repetidas_por_mazo = {'1': 4, '2': 2, '3': 1, '4': 1}
    for carta_id in CARTAS.keys():
        mazo_id = carta_id[0]
        if mazo_id not in mazos:
            mazos[mazo_id] = []
        mazos[mazo_id].extend([carta_id]*cartas_repetidas_por_mazo[mazo_id])
    return mazos


def mezclar_mazos():
    mazos = armar_mazos()
    for mazo in mazos:
        cartas = mazos[mazo]
        random.shuffle(cartas)
        mazos_mezclados[mazo] = cartas

def borrar_carta_del_mazo(carta_id):
    mazo_id = carta_id[0]
    cartas_del_mazo = mazos_mezclados[mazo_id]
    cartas_del_mazo.pop(0)
    if len(cartas_del_mazo) == 0:
        nuevo_mazo = armar_mazos()[mazo_id]
        random.shuffle(nuevo_mazo)
        mazos_mezclados.update({mazo_id: nuevo_mazo})


def tirar_carta(mazo_id=None, carta_id=None):
    if mazo_id:
        carta_id = mazos_mezclados[mazo_id][0]
    carta = CARTAS.get(carta_id, {})
    if not carta:
        raise Exception("Esa carta no exite, pa, si queres mas cartas... Inventalas")
    borrar_carta_del_mazo(carta_id)
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
    mezclar_mazos()
    await ctx.send(MENSAJE_DE_BIENVENIDA)
    escribir_libro(ctx.author.id)
    await ctx.send('Empecemos con la __primera carta!__')
    await ctx.send(tirar_carta(carta_id='1a'))
    await ctx.send('Ahora poné `!escribir` y a continuacion tu texto para guardar el primer fragmento :)')


@bot.command(name='carta', help='Tirar una carta nueva, indicando de cuál mazo queres sacar. En caso de no elegir ninguno saca una al azar de cualquier mazo')
async def carta(ctx, mazo_id):
    if int(mazo_id) > 4:
        raise Exception('Perdon, tengo hasta 4 mazos, por ahora...')
    turnos = buscar_libro(ctx.author.id).get('contador_turnos', 0)
    if int(mazo_id) > turnos:
        await ctx.send('Ah que picaro que sos eligiendo de otro mazo, muy bien las reglas en la literatura estan PARA ROMPERSE')
    await ctx.send(tirar_carta(mazo_id))


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
