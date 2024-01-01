import random


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
        'descripcion': '`Un Personaje Hace", al mismo tiempo, en otro lugar `',
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
    mazos_mezclados = {}
    mazos = armar_mazos()
    for mazo in mazos:
        cartas = mazos[mazo]
        random.shuffle(cartas)
        mazos_mezclados[mazo] = cartas
    return mazos_mezclados


def borrar_carta_del_mazo(mazo, carta_id):
    mazo_id = carta_id[0]
    cartas_del_mazo = mazo[mazo_id]
    cartas_del_mazo.pop(0)
    print(cartas_del_mazo)
    if len(cartas_del_mazo) == 0:
        nuevo_mazo = armar_mazos()[mazo_id]
        random.shuffle(nuevo_mazo)
        mazo.update({mazo_id: nuevo_mazo})


def tirar_carta(mazo, mazo_id=None, carta_id=None):
    if mazo_id:
        carta_id = mazo[mazo_id][0]
    carta = CARTAS.get(carta_id, {})
    if not carta:
        raise Exception("Esa carta no exite, pa, si queres mas cartas... Inventalas")
    borrar_carta_del_mazo(mazo, carta_id)
    return f"{carta_id}: **{carta['titulo']}** \n{carta['descripcion']}"


def mazos_disponibles(turnos):
    mazos = []
    for i in range(1, turnos+1):
        mazos.append(i)
        if i == 4:
            break
    return f"Podes sacar una carta de los mazos {str(mazos)}"


def escribir_libro(libros, autor_id, contador_turnos=0, cuento=''):
    libros.update(
        {
            autor_id:  {
                'contador_turnos': contador_turnos,
                'cuento': cuento,
            }
        }
    )


def buscar_libro(libros, autor_id):
    return libros.get(autor_id, {})
