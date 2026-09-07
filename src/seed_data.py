from src.models.workout import DayWorkout, WorkoutBlock, Exercise, Program

SEPTEMBER_PROGRAM = [
    DayWorkout(
        day_id="lun",
        day_name="Lun",
        date_num="7",
        type_badge="Upper Fuerza",
        title="Upper Body: Push & Pull (Fuerza & Armadura)",
        tags=["Hybrid", "Strength & Power"],
        kpis=["Barbell Bench Press", "Weighted Pull-up"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP", subtitle="2 Rondas continuas por calidad",
                exercises=[
                    Exercise(name="SkiErg / Rower", target="1 min a ritmo constante"),
                    Exercise(name="Band Pull-aparts + Scapular Push-ups", target="15 + 10 reps"),
                    Exercise(name="Deadbugs con control pélvico", target="10 e/s")
                ]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH", subtitle="Velocidad y control • RPE 8",
                exercises=[
                    Exercise(name="Barbell Bench Press (o Floor Press)", target="4 x 5 reps (RPE 8)", default_weight=90.0),
                    Exercise(name="Weighted Pull-ups (o Chin-ups)", target="4 x 5-6 reps (RPE 8)", default_weight=15.0)
                ]
            ),
            WorkoutBlock(
                code="H", title="FUNCTIONAL HYPERTROPHY", subtitle="Triserie • RIR 2 • 3 Rondas",
                exercises=[
                    Exercise(name="Incline Dumbbell Press (Agarre Neutro)", target="3 x 8-10 reps"),
                    Exercise(name="Chest-Supported Dumbbell Row (Pausa 1s)", target="3 x 10-12 reps"),
                    Exercise(name="Face Pulls en polea + Rotadores externos", target="3 x 15 reps")
                ]
            ),
            WorkoutBlock(
                code="E", title="PREHAB & ENGINE", subtitle="Fuerza de agarre y core anti-rotacional",
                exercises=[
                    Exercise(name="Farmer's Walks pesados con mancuernas", target="3 x 40 metros"),
                    Exercise(name="Pallof Press con banda / polea", target="3 x 12 e/s")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mar",
        day_name="Mar",
        date_num="8",
        type_badge="Run 10k Calidad",
        title="Running: Series San Silvestre 10k (Ritmo Umbral)",
        tags=["Running", "Threshold", "San Silvestre"],
        kpis=["Ritmo 1000m (Umbral de lactato)"],
        blocks=[
            WorkoutBlock(
                code="W", title="CALENTAMIENTO & TÉCNICA", subtitle="Preparación tendinosa y movilidad",
                exercises=[
                    Exercise(name="Trote muy suave Z1", target="10 minutos"),
                    Exercise(name="Drills de técnica de carrera (Skips, talones, zancada reactiva)", target="5 minutos"),
                    Exercise(name="Progresiones en recta (70m al 85%)", target="3 rectas")
                ]
            ),
            WorkoutBlock(
                code="R", title="BLOQUE PRINCIPAL 10K", subtitle="Ritmo objetivo San Silvestre (RPE 8.5)",
                exercises=[
                    Exercise(name="6 x 1000 metros al ritmo objetivo 10k", target="6 series • Rec: 90s trote suave", notes="Mantener ritmo uniforme en cada serie"),
                    Exercise(name="Trote de vuelta a la calma (Enfriamiento)", target="10 minutos Z1")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mie",
        day_name="Mié",
        date_num="9",
        type_badge="Lower Squat",
        title="Lower Body: Potencia, Sentadilla & Rodilla Blindada",
        tags=["Hybrid", "Legs", "Durability"],
        kpis=["Barbell Back Squat", "Trap Bar Deadlift"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP & PREHAB", subtitle="Movilidad de cadera y tobillos para carrera",
                exercises=[
                    Exercise(name="90/90 Hip Switches + Spiderman Lunges", target="2 x 8 e/s"),
                    Exercise(name="Calf / Soleus raises con pausa de 2s", target="2 x 15 reps")
                ]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH", subtitle="Fuerza máxima y reclutamiento",
                exercises=[
                    Exercise(name="Barbell Back Squat (o Safety Bar Squat)", target="4 x 5 reps (RPE 8)", default_weight=110.0),
                    Exercise(name="Trap Bar Deadlift", target="3 x 5 reps (RPE 8)", default_weight=130.0)
                ]
            ),
            WorkoutBlock(
                code="H", title="UNILATERAL & POSTERIOR", subtitle="Prevención de desbalances y periostitis",
                exercises=[
                    Exercise(name="Bulgarian Split Squat con mancuernas", target="3 x 8 e/s"),
                    Exercise(name="Dumbbell Romanian Deadlift (RDL)", target="3 x 10 reps"),
                    Exercise(name="Tibialis Raises (en pared o máquina)", target="2 x 20 reps")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="jue",
        day_name="Jue",
        date_num="10",
        type_badge="Upper Hipertrofia",
        title="Upper Body: Estructura, Hombros & Espalda Alta",
        tags=["Physique", "Volume", "Upper"],
        kpis=["Standing Barbell Overhead Press"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP", subtitle="Movilidad escapular y manguito",
                exercises=[
                    Exercise(name="Kettlebell Halos", target="2 x 8 por sentido"),
                    Exercise(name="Rotaciones torácicas con pica/goma", target="2 x 10 reps")
                ]
            ),
            WorkoutBlock(
                code="S", title="STRENGTH & DENSITY", subtitle="Fuerza vertical de empuje y tracción",
                exercises=[
                    Exercise(name="Standing Barbell Overhead Press (OHP)", target="4 x 6 reps", default_weight=55.0),
                    Exercise(name="Barbell Pendlay Row (desde el suelo)", target="4 x 6-8 reps", default_weight=75.0)
                ]
            ),
            WorkoutBlock(
                code="H", title="VOLUME & PUMP", subtitle="Hipertrofia funcional",
                exercises=[
                    Exercise(name="Neutral Grip DB Floor Press", target="3 x 10-12 reps"),
                    Exercise(name="Single-Arm Cable Row (Dorsal focus)", target="3 x 10 e/s"),
                    Exercise(name="Biceps Barbell Curl + Triceps Rope Extension", target="3 x 12 reps")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="vie",
        day_name="Vie",
        date_num="11",
        type_badge="Descanso",
        title="Recuperación Total & Aclimatación Térmica",
        tags=["Recovery", "Sauna", "Longevity"],
        is_rest_day=True,
        blocks=[]
    ),
    DayWorkout(
        day_id="sab",
        day_name="Sáb",
        date_num="12",
        type_badge="Run 10k Tirada",
        title="Running: Tirada Continua Progresiva (8-10 km)",
        tags=["Running", "Aerobic Base", "San Silvestre"],
        kpis=["Tiempo 10 km"],
        blocks=[
            WorkoutBlock(
                code="R", title="TIRADA AERÓBICA", subtitle="Base cardiovascular para la San Silvestre",
                exercises=[
                    Exercise(name="Primeros 6 km a ritmo conversacional (Zona 2)", target="6 km Z2"),
                    Exercise(name="Últimos 2-3 km en progresión hacia ritmo de carrera", target="2-3 km progresivos")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="dom",
        day_name="Dom",
        date_num="13",
        type_badge="Bici Zona 2",
        title="Ciclismo: Capacidad Aeróbica de Bajo Impacto",
        tags=["Cycling", "Zone 2", "Cardio"],
        kpis=[],
        blocks=[
            WorkoutBlock(
                code="B", title="FONDO EN BICI", subtitle="Recuperación activa y desarrollo mitocondrial",
                exercises=[
                    Exercise(name="Salida en bicicleta de carretera / gravel", target="60-90 minutos continuos en Zona 2", notes="Mantener cadencia fluida (85-95 rpm)")
                ]
            )
        ]
    )
]

PROGRAMS_CATALOG = [
    Program(
        id="perform",
        title="PERFORM (Hybrid Athlete)",
        category="Hybrid",
        tags=["Strength", "Conditioning", "Engine"],
        description="Construye fuerza máxima, potencia atlética y masa muscular mientras mantienes una resistencia de élite.",
        is_active=True
    ),
    Program(
        id="san_silvestre",
        title="SAN SILVESTRE 10K (Running Prep)",
        category="Aerobic Capacity",
        tags=["10k Race", "Intervals", "Pacing"],
        description="Especialización de carrera de 10k con trabajo de umbral de lactato y fortalecimiento de tibiales/sóleo.",
        is_active=False
    ),
    Program(
        id="bjj_armor",
        title="BJJ ARMOR (Grappling Prehab)",
        category="Functional Fitness",
        tags=["BJJ", "Grip Strength", "Anti-Rotation"],
        description="Programa de blindaje articular para hombros, cuello, agarre y caderas enfocado en practicantes de Jiu-Jitsu.",
        is_active=False
    )
]
