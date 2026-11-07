import datetime as dt

from src.models.workout import DayWorkout, Exercise, Program, WorkoutBlock

# Bloque 2: semana 1 = domingo 8 a sábado 14 de noviembre de 2026.
NOV_BLOCK_START = dt.date(2026, 11, 8)


def ej(name, target, sec=0, desc="Continuo", **kwargs):
    return Exercise(name=name, target=target, rest_seconds=sec, rest_description=desc, **kwargs)


def bl(code, title, subtitle, exercises, rest=None):
    return WorkoutBlock(code=code, title=title, subtitle=subtitle, rest_block_desc=rest, exercises=exercises)


def dia(day_id, day_name, badge, title, tags, blocks):
    return DayWorkout(day_id=day_id, day_name=day_name, date_num="", type_badge=badge,
                      title=title, tags=tags, blocks=blocks)


NOVEMBER_PROGRAM = [
    dia("nov_lun", "Lun", "Empuje + BJJ", "Empuje: press banca, fondos y BJJ 19:30", ["Empuje", "Fuerza", "BJJ"], [
        bl("W", "ACTIVACIÓN", "3 rondas · 60 s entre rondas", [
            ej("Band pull-apart", "10 repeticiones", 0, "Sin pausa"),
            ej("Scapular push-up", "8 repeticiones", 0, "Sin pausa"),
            ej("Dead bug", "6 repeticiones por lado", 60, "60 s entre rondas"),
        ]),
        bl("S", "FUERZA PRINCIPAL", "Carga según la semana del bloque", [
            ej("Barbell Bench Press", "4 series × 5 · pausa de 2 s en el pecho", 150, "2:30 min",
               exercise_key="bench_press", intensity_pct=0.775, target_sets=4, target_reps=5,
               notes="Sin rebote. Deja 2 repeticiones en reserva."),
        ], rest="2:30 min entre series"),
        bl("H", "ACCESORIOS DE EMPUJE", "Progresión controlada", [
            ej("Fondos en paralelas lastrados", "3 × 6–8 · lastre progresivo", 120, "2:00 min",
               target_sets=3, target_reps=6, default_weight=0.0,
               notes="Registra solo el lastre (0 = peso corporal). Sube 2,5 kg si completas las series con 2 repeticiones en reserva y sin molestias en el codo."),
            ej("Press inclinado con mancuernas", "3 × 8–10", 90, "90 s",
               target_sets=3, target_reps=9, default_weight=0.0),
            ej("Elevación lateral en polea a una mano", "3 × 12–15 por lado", 60, "60 s",
               target_sets=3, target_reps=13, default_weight=0.0),
        ], rest="2:00 min en fondos · 60–90 s en el resto"),
        bl("E", "JIU-JITSU · 19:30", "Clase en el tatami", [
            ej("Clase de Jiu-Jitsu", "Técnica y rondas según la clase", 0, "Según la clase"),
        ]),
    ]),

    dia("nov_mar", "Mar", "Series 10 km", "Running: series de calidad", ["Running", "10 km", "Calidad"], [
        bl("W", "CALENTAMIENTO", "Trote suave y preparación", [
            ej("Trote suave", "12 min en zona 1", 0, "Continuo"),
            ej("Movilidad de tobillo y cadera", "5 min", 0, "Continuo"),
            ej("Progresiones de carrera", "4 × 15 s", 45, "45 s"),
        ]),
        bl("R", "SERIES", "Objetivo según la semana del bloque", [
            ej("Series x 1000 m (objetivo por semana)",
               "S1: 5 × 1000 m · S2: 6 × 1000 m · S3: 8 × 600 m · S4: 4 × 1000 m suaves",
               90, "60–90 s de trote suave",
               notes="Ritmo uniforme. En la semana 4 baja 5–10 s/km si lo necesitas."),
            ej("Vuelta a la calma", "10 min en zona 1", 0, "Continuo"),
        ], rest="Trote suave entre repeticiones"),
    ]),

    dia("nov_mie", "Mié", "Sentadilla", "Pierna: sentadilla con pausa y cadena posterior",
        ["Pierna", "Sentadilla", "Cadena posterior"], [
        bl("W", "ACTIVACIÓN", "2 rondas", [
            ej("Puente de glúteo con pausa", "2 × 10 (pausa de 2 s arriba)", 30, "30 s"),
            ej("Sentadilla sin carga con pausa abajo", "2 × 8", 60, "60 s"),
        ]),
        bl("S", "FUERZA PRINCIPAL", "Sentadilla trasera con pausa", [
            ej("Sentadilla trasera con barra", "4 series × 5 · pausa de 2 s abajo", 150, "2:30 min",
               exercise_key="back_squat", intensity_pct=0.775, target_sets=4, target_reps=5,
               notes="Profundidad estable y tronco firme."),
        ], rest="2:30 min entre series"),
        bl("H", "ACCESORIOS DE PIERNA", "Cadena posterior y unilateral", [
            ej("Peso muerto rumano con mancuernas", "3 × 8–10", 90, "90 s",
               target_sets=3, target_reps=9, default_weight=0.0,
               notes="Espalda neutra; siente el estiramiento de isquiotibiales."),
            ej("Rotación unilateral de pierna", "3 × 8 por lado (la variante cambia cada semana)", 75, "75 s",
               target_sets=3, target_reps=8, default_weight=0.0),
            ej("Curl femoral tumbado", "3 × 10–12", 60, "60 s",
               target_sets=3, target_reps=11, default_weight=0.0),
        ], rest="60–90 s entre ejercicios"),
        bl("E", "CORE Y TOBILLO", "Estabilidad lateral y gemelos", [
            ej("Plancha Copenhague", "3 × 20–30 s por lado", 45, "45 s"),
            ej("Elevación de gemelos", "2 × 15 con pausa de 2 s arriba", 45, "45 s"),
        ]),
    ]),

    dia("nov_jue", "Jue", "BJJ 20:30", "Jiu-Jitsu: técnica y sparring (20:30)", ["BJJ", "Grappling"], [
        bl("E", "JIU-JITSU · 20:30", "Clase en el tatami", [
            ej("Clase de Jiu-Jitsu", "Técnica y rondas según la clase", 0, "Según la clase"),
        ]),
    ]),

    dia("nov_vie", "Vie", "Peso muerto", "Peso muerto y tirón", ["Peso muerto", "Tirón", "Agarre"], [
        bl("W", "ACTIVACIÓN", "2 rondas", [
            ej("Band pull-apart", "2 × 15", 30, "30 s"),
            ej("Good morning sin carga", "2 × 10", 60, "60 s"),
        ]),
        bl("S", "FUERZA PRINCIPAL", "Peso muerto con barra hexagonal (trap bar)", [
            ej("Peso muerto con barra hexagonal", "4 series × 5 · empuje desde el suelo", 165, "2:45 min",
               exercise_key="deadlift", intensity_pct=0.80, target_sets=4, target_reps=5,
               notes="Columna neutra. Si la técnica se degrada, para la serie."),
        ], rest="2:45 min entre series"),
        bl("H", "TIRÓN Y ESPALDA ALTA", "Tracción con control", [
            ej("Dominadas", "3 × 6–8", 120, "2:00 min",
               target_sets=3, target_reps=7, default_weight=0.0,
               notes="Registra solo el lastre (0 = peso corporal). Si el codo molesta, cámbialas por jalón al pecho."),
            ej("Remo con pecho apoyado", "3 × 10", 90, "90 s",
               target_sets=3, target_reps=10, default_weight=0.0),
            ej("Rotación deltoides posterior", "3 × 15 (la variante cambia cada semana)", 60, "60 s",
               target_sets=3, target_reps=15, default_weight=0.0),
        ], rest="60–120 s entre ejercicios"),
        bl("E", "AGARRE", "Preparación para el tatami", [
            ej("Farmer carry", "3 × 40 m con mancuernas pesadas", 60, "60 s"),
        ]),
    ]),

    dia("nov_sab", "Sáb", "Rodaje largo", "Running: rodaje largo", ["Running", "Resistencia"], [
        bl("R", "RODAJE", "Objetivo según la semana del bloque", [
            ej("Rodaje largo Z2",
               "S1: 10 km · S2: 12 km · S3: 12 km (últimos 3 km a ritmo 10 km) · S4: sustituir por el test",
               0, "Continuo", notes="Puedes hablar en frases cortas."),
        ]),
        bl("E", "TEST · SOLO SEMANA 4", "Sustituye al rodaje de la semana 4", [
            ej("Test de 5 km", "Calienta 15 min suaves · máximo esfuerzo sostenido", 0, "Anota el tiempo",
               notes="Es tu KPI de running para el siguiente bloque."),
        ]),
    ]),

    dia("nov_dom", "Dom", "Bici Z2", "Bicicleta suave (opcional)", ["Bici", "Zona 2", "Recuperación"], [
        bl("B", "BICI Z2", "Opcional: si estás cargado, descansa", [
            ej("Bici en zona 2", "45–60 min suaves", 0, "Continuo"),
            ej("Movilidad de cadera y torácica", "10 min", 0, "Continuo"),
        ]),
    ]),
]

NOVEMBER_CATALOG = Program(
    id="perform_nov",
    title="BLOQUE 2: Noviembre (Empuje, peso muerto y 10 km)",
    category="Hybrid + BJJ",
    tags=["Press y fondos", "Peso muerto", "Series 10 km", "Sauna"],
    description="Bloque de 4 semanas (8 nov – 5 dic). Mantiene press, sentadilla y peso muerto como principales y cambia accesorios y series de running.",
    is_active=False,
)
