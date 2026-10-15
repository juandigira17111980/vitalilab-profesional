"""General, adaptable activities. Not clinically validated prescriptions."""

ROUTINES = (
    {
        "slug": "fortalece-tu-centro",
        "name": "Fortalece tu centro",
        "category": "Movimiento",
        "seconds": 90,
        "icon": "focus",
        "habit_code": "gentle-movement",
        "description": (
            "Haz una pausa para reconocer tu postura y activar suavemente "
            "tu zona media, sin buscar cambiar tu cuerpo."
        ),
        "steps": (
            "Siéntate con apoyo o elige una postura cómoda y estable.",
            (
                "Alarga suavemente tu espalda y activa el abdomen sin contener el aire; "
                "suelta después de unos segundos."
            ),
            (
                "Descansa y repite solo si te resulta cómodo. "
                "No necesitas hacer una plancha ni soportar dolor."
            ),
        ),
    },
    {
        "slug": "despierta-tu-energia",
        "name": "Despierta tu energía",
        "category": "Movimiento",
        "seconds": 120,
        "icon": "sun",
        "habit_code": "gentle-movement",
        "description": (
            "Un momento de movimiento adaptable para retomar tu día con atención y vitalidad."
        ),
        "steps": (
            "Despeja el espacio y elige moverte sentado o de pie con apoyo.",
            (
                "Alterna movimientos suaves de brazos y piernas a tu ritmo, "
                "sin forzar las articulaciones."
            ),
            (
                "Intercala pausas cuando lo necesites. El objetivo es participar con comodidad, "
                "no completar un número de repeticiones."
            ),
        ),
    },
    {
        "slug": "construye-tu-fuerza",
        "name": "Construye tu fuerza",
        "category": "Movimiento",
        "seconds": 120,
        "icon": "move",
        "habit_code": "gentle-movement",
        "description": (
            "Explora una activación suave y progresiva, "
            "con espacio para adaptar o detener la actividad."
        ),
        "steps": (
            "Busca una postura estable, sentado o de pie, y relaja los hombros.",
            (
                "Junta las palmas frente al pecho y haz una presión suave durante unos segundos, "
                "respirando con normalidad."
            ),
            (
                "Descansa antes de repetir. Si aparece dolor, mareo o incomodidad, detente; "
                "en clase, pide una alternativa al docente."
            ),
        ),
    },
    {
        "slug": "pausa-consciente",
        "name": "Un minuto para volver a ti",
        "category": "Calma",
        "seconds": 60,
        "icon": "calm",
        "habit_code": "mindful-minute",
        "description": "Suelta la pantalla y observa tu respiración, sin forzarla.",
        "steps": (
            "Busca una posición cómoda y mira un punto tranquilo.",
            "Observa cómo entra y sale el aire a tu ritmo natural.",
            "Al terminar, elige una sola acción para continuar tu día.",
        ),
    },
    {
        "slug": "pausa-activa",
        "name": "Cambia de postura",
        "category": "Movimiento",
        "seconds": 180,
        "icon": "move",
        "habit_code": "active-break",
        "description": "Una pausa para moverte suavemente después de estar sentado.",
        "steps": (
            "Despeja el espacio y acomódate según tus posibilidades.",
            "Cambia de postura y mueve hombros y manos suavemente, sin dolor.",
            "Si te resulta cómodo, da unos pasos; también puedes realizar la pausa sentado.",
        ),
    },
    {
        "slug": "ritual-de-descanso",
        "name": "Cierra el día con calma",
        "category": "Descanso",
        "seconds": 120,
        "icon": "moon",
        "habit_code": "sleep",
        "description": "Deja listo un pequeño ritual para tu próxima hora de descanso.",
        "steps": (
            "Elige una hora realista para empezar a desconectarte.",
            "Reduce las distracciones y deja preparado lo que necesitarás mañana.",
            "Identifica una actividad tranquila que te ayude a cerrar el día.",
        ),
    },
    {
        "slug": "foco-en-una-cosa",
        "name": "Una cosa a la vez",
        "category": "Enfoque",
        "seconds": 300,
        "icon": "focus",
        "habit_code": "daily-intention",
        "description": "Dedica cinco minutos a comenzar una tarea concreta.",
        "steps": (
            "Elige una tarea pequeña que puedas empezar ahora.",
            "Silencia distracciones opcionales y prepara solo lo necesario.",
            "Trabaja hasta que termine el reloj; después decide si continuar o pausar.",
        ),
    },
    {
        "slug": "pausa-de-pantallas",
        "name": "Mira más allá de la pantalla",
        "category": "Enfoque",
        "seconds": 90,
        "icon": "sun",
        "habit_code": "screen-break",
        "description": "Interrumpe el desplazamiento automático y cambia de actividad.",
        "steps": (
            "Deja el dispositivo en una posición segura.",
            "Mira tu entorno o conversa brevemente sin otra pantalla.",
            "Decide con intención para qué quieres volver al dispositivo.",
        ),
    },
    {
        "slug": "momento-de-hidratacion",
        "name": "Una pausa para hidratarte",
        "category": "Calma",
        "seconds": 60,
        "icon": "water",
        "habit_code": "hydration",
        "description": "Prepara una pausa de agua acorde con tus necesidades personales.",
        "steps": (
            "Ten agua disponible si forma parte de tus indicaciones personales.",
            "Haz una pausa breve y bebe con tranquilidad si lo necesitas.",
            "Relaciona esa pausa con un momento habitual de tu día para recordarla.",
        ),
    },
)

ROUTINES += (
    {
        "slug": "postura-sentada",
        "name": "Encuentra tu postura",
        "category": "Movimiento",
        "seconds": 90,
        "icon": "focus",
        "habit_code": "gentle-movement",
        "description": "Una pausa sentada para reconocer el apoyo y alargar suavemente la espalda.",
        "steps": (
            "Elige una silla estable, sin ruedas, con los pies apoyados.",
            "Relaja los hombros y alarga la espalda sin arquearla ni contener el aire.",
            "Vuelve a una posición cómoda. Repite solo si te resulta agradable "
            "y descansa cuando quieras.",
        ),
    },
    {
        "slug": "hombros-libres",
        "name": "Dale espacio a tus hombros",
        "category": "Movimiento",
        "seconds": 120,
        "icon": "move",
        "habit_code": "gentle-movement",
        "description": "Explora movimientos pequeños de hombros, sentado o de pie con apoyo.",
        "steps": (
            "Busca una posición estable y deja los brazos relajados.",
            "Eleva un poco los hombros y vuelve a soltarlos, sin acercarte al dolor.",
            "Haz pausas y reduce el recorrido si lo necesitas. No fuerces el cuello.",
        ),
    },
    {
        "slug": "brazos-en-movimiento",
        "name": "Activa tus brazos",
        "category": "Movimiento",
        "seconds": 120,
        "icon": "sun",
        "habit_code": "gentle-movement",
        "description": "Alterna movimientos de brazos a un ritmo cómodo; puedes hacerlo sentado.",
        "steps": (
            "Elige una postura sentada o de pie que puedas mantener con estabilidad.",
            "Mueve un brazo hacia delante y vuelve; alterna con el otro sin impulsos.",
            "Mantén una respiración natural y descansa antes de cansarte. El ritmo lo eliges tú.",
        ),
    },
    {
        "slug": "pasos-a-tu-ritmo",
        "name": "Unos pasos para volver",
        "category": "Movimiento",
        "seconds": 180,
        "icon": "move",
        "habit_code": "gentle-movement",
        "description": "Interrumpe un rato sentado con una caminata corta en un espacio despejado.",
        "steps": (
            "Comprueba que el suelo esté libre de obstáculos. Usa apoyo si lo necesitas.",
            "Camina despacio dentro de tu espacio, sin perseguir una distancia ni un ritmo.",
            "Para y descansa cuando quieras. Si caminar no te resulta adecuado, "
            "elige Activa tus brazos.",
        ),
    },
    {
        "slug": "fuerza-con-palmas",
        "name": "Fuerza suave con tus manos",
        "category": "Movimiento",
        "seconds": 90,
        "icon": "focus",
        "habit_code": "gentle-movement",
        "description": "Una activación suave con las palmas juntas, sin cargas externas.",
        "steps": (
            "Siéntate con apoyo y mantén los hombros relajados.",
            "Junta las palmas y presiónalas suavemente mientras respiras con normalidad.",
            "Suelta la presión y descansa. No mantengas el esfuerzo si te incomoda.",
        ),
    },
    {
        "slug": "apoyo-en-pared",
        "name": "Explora el apoyo en pared",
        "category": "Movimiento",
        "seconds": 120,
        "icon": "move",
        "habit_code": "gentle-movement",
        "description": "Una alternativa con apoyo estable y un esfuerzo que puedas controlar.",
        "steps": (
            "Solo si puedes estar de pie con estabilidad: apoya ambas manos "
            "en una pared firme a una altura cómoda.",
            "Con los pies cerca de la pared, flexiona un poco los codos y vuelve suavemente; "
            "no bloquees la respiración.",
            "Descansa sin forzar. Si no te resulta adecuado, elige Fuerza suave con tus manos. "
            "En menores, consulta al adulto responsable.",
        ),
    },
)

VISUALS = {
    "posture": "Postura sentada: pies apoyados, espalda alargada y hombros relajados.",
    "march": "Brazos alternos: una posición de reposo y otra con un brazo hacia delante.",
    "palms": "Manos separadas y palmas juntas frente al pecho, sin elevar los hombros.",
    "shoulders": "Hombros relajados y elevación pequeña, sin forzar el cuello.",
    "wall": "Apoyo de manos en pared y pequeña flexión de codos con los pies estables.",
    "walk": "Pasos suaves: alterna las piernas al caminar en un espacio despejado.",
    "breathing": "Pausa sentada: observa la respiración manteniendo una postura cómoda.",
    "custom": "Rutina propia: revisa las instrucciones que guardaste para cada ejercicio.",
}
_DETAILS = {
    "fortalece-tu-centro": ("center", "posture", ("seated", "supported", "standing")),
    "despierta-tu-energia": ("energy", "march", ("seated", "supported", "standing")),
    "construye-tu-fuerza": ("strength", "palms", ("seated", "supported", "standing")),
    "postura-sentada": ("center", "posture", ("seated", "supported")),
    "hombros-libres": ("center", "shoulders", ("seated", "supported", "standing")),
    "brazos-en-movimiento": ("energy", "march", ("seated", "supported", "standing")),
    "pasos-a-tu-ritmo": ("energy", "walk", ("standing",)),
    "fuerza-con-palmas": ("strength", "palms", ("seated", "supported", "standing")),
    "apoyo-en-pared": ("strength", "wall", ("supported", "standing")),
}
ROUTINES = tuple(
    {
        **routine,
        "goal": _DETAILS.get(routine["slug"], (None,))[0],
        "visual": _DETAILS.get(routine["slug"], (None, "breathing"))[1],
        "preferences": _DETAILS.get(
            routine["slug"], (None, None, ("seated", "supported", "standing"))
        )[2],
    }
    for routine in ROUTINES
)
