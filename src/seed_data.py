from src.models.workout import DayWorkout, WorkoutBlock, Exercise, Program

SEPTEMBER_PROGRAM = [
    DayWorkout(
        day_id="lun_sep", day_name="Lun", date_num="7", type_badge="Upper Fuerza",
        title="Upper Body: Push & Pull (Fuerza & Armadura)",
        tags=["Hybrid", "Strength & Power"], kpis=["Barbell Bench Press", "Weighted Pull-up"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP", subtitle="2 Rondas por calidad",
                exercises=[
                    Exercise(name="SkiErg / Rower", target="1 min a ritmo constante"),
                    Exercise(name="Band Pull-aparts + Scapular Push-ups", target="15 + 10 reps"),
                    Exercise(name="Deadbugs con control pélvico", target="10 e/s")
                ]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="Semana 1: Onda 72.5% - 80% 1RM • RPE 8",
                exercises=[
                    Exercise(
                        name="Barbell Bench Press",
                        exercise_key="bench_press",
                        intensity_pct=0.775,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 72.5% - 80% 1RM (RPE 8)",
                        notes="Pausa de 1 segundo en el pecho. Velocidad concéntrica máxima."
                    ),
                    Exercise(
                        name="Weighted Pull-ups (o Chin-ups)",
                        exercise_key="pull_up",
                        intensity_pct=0.75,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 70% - 77.5% 1RM",
                        notes="Extensión completa abajo y barbilla claramente sobre la barra."
                    )
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
                code="E", title="PREHAB & ENGINE", subtitle="Fuerza de agarre y core",
                exercises=[
                    Exercise(name="Farmer's Walks pesados con mancuernas", target="3 x 40 metros"),
                    Exercise(name="Pallof Press con banda / polea", target="3 x 12 e/s")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mar_sep", day_name="Mar", date_num="8", type_badge="Run 10k Calidad",
        title="Running: Series San Silvestre 10k (Ritmo Umbral)",
        tags=["Running", "Threshold", "San Silvestre"], kpis=["Ritmo 1000m (Umbral)"],
        blocks=[
            WorkoutBlock(
                code="W", title="CALENTAMIENTO & DRILLES", subtitle="Preparación tendinosa",
                exercises=[
                    Exercise(name="Trote suave Z1", target="10 minutos"),
                    Exercise(name="Drills de técnica + Progresiones", target="3 rectas de 70m")
                ]
            ),
            WorkoutBlock(
                code="R", title="BLOQUE PRINCIPAL 10K", subtitle="Ritmo objetivo San Silvestre",
                exercises=[
                    Exercise(name="6 x 1000m a ritmo 10k (Rec: 90s trote)", target="6 series"),
                    Exercise(name="Enfriamiento suave Z1", target="10 minutos")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mie_sep", day_name="Mié", date_num="9", type_badge="Lower Squat",
        title="Lower Body: Sentadilla & Rodilla Blindada",
        tags=["Hybrid", "Legs", "Durability"], kpis=["Barbell Back Squat", "Trap Bar Deadlift"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP & PREHAB", subtitle="Cadera y tobillos para carrera",
                exercises=[
                    Exercise(name="90/90 Hip Switches + Spiderman Lunges", target="2 x 8 e/s"),
                    Exercise(name="Calf / Soleus raises con pausa de 2s", target="2 x 15 reps")
                ]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="Semana 1: Onda 75% - 82.5% 1RM",
                exercises=[
                    Exercise(
                        name="Barbell Back Squat",
                        exercise_key="back_squat",
                        intensity_pct=0.775,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 75% - 80% 1RM (RPE 8)",
                        notes="Profundidad paralela, tronco firme."
                    ),
                    Exercise(
                        name="Trap Bar Deadlift",
                        exercise_key="deadlift",
                        intensity_pct=0.80,
                        target_sets=3,
                        target_reps=5,
                        target="3 x 5 @ 77.5% - 82.5% 1RM (RPE 8)",
                        notes="Empuje potente desde el suelo."
                    )
                ]
            ),
            WorkoutBlock(
                code="H", title="UNILATERAL & TIBIALES", subtitle="Prevención de periostitis",
                exercises=[
                    Exercise(name="Bulgarian Split Squat con mancuernas", target="3 x 8 e/s"),
                    Exercise(name="Dumbbell Romanian Deadlift (RDL)", target="3 x 10 reps"),
                    Exercise(name="Tibialis Raises en pared", target="2 x 20 reps")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="jue_sep", day_name="Jue", date_num="10", type_badge="Upper Hipertrofia",
        title="Upper Body: Estructura, Hombros & Espalda Alta",
        tags=["Physique", "Volume", "Upper"], kpis=["Overhead Press"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP", subtitle="Movilidad escapular",
                exercises=[Exercise(name="Kettlebell Halos + Rotaciones torácicas", target="2 x 8 e/s")]
            ),
            WorkoutBlock(
                code="S", title="STRENGTH & DENSITY", subtitle="Semana 1: 72.5% - 77.5% 1RM",
                exercises=[
                    Exercise(
                        name="Standing Barbell Overhead Press (OHP)",
                        exercise_key="ohp",
                        intensity_pct=0.75,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 72.5% - 77.5% 1RM (RPE 8)",
                        notes="Glúteos y core compactados."
                    ),
                    Exercise(name="Barbell Pendlay Row", target="4 x 6-8 reps", default_weight=75.0)
                ]
            ),
            WorkoutBlock(
                code="H", title="VOLUME & ARMS", subtitle="Hipertrofia funcional",
                exercises=[
                    Exercise(name="Neutral Grip DB Floor Press", target="3 x 10-12 reps"),
                    Exercise(name="Single-Arm Cable Row", target="3 x 10 e/s"),
                    Exercise(name="Biceps Barbell Curl + Triceps Rope", target="3 x 12 reps")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="vie_sep", day_name="Vie", date_num="11", type_badge="Descanso",
        title="Recuperación Total & Sauna",
        tags=["Recovery", "Sauna", "Longevity"], is_rest_day=True, blocks=[]
    ),
    DayWorkout(
        day_id="sab_sep", day_name="Sáb", date_num="12", type_badge="Run 10k Tirada",
        title="Running: Tirada Continua Progresiva (8-10 km)",
        tags=["Running", "Aerobic Base", "San Silvestre"], kpis=["Tiempo 10 km"],
        blocks=[
            WorkoutBlock(
                code="R", title="TIRADA AERÓBICA", subtitle="Base cardiovascular para la San Silvestre",
                exercises=[
                    Exercise(name="Primeros 6 km en Zona 2 conversacional", target="6 km Z2"),
                    Exercise(name="Últimos 3 km a ritmo objetivo 10k", target="3 km ritmo carrera")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="dom_sep", day_name="Dom", date_num="13", type_badge="Bici Zona 2",
        title="Ciclismo: Capacidad Aeróbica de Bajo Impacto",
        tags=["Cycling", "Zone 2", "Cardio"], kpis=[],
        blocks=[
            WorkoutBlock(
                code="B", title="FONDO EN BICI", subtitle="Recuperación activa y desarrollo mitocondrial",
                exercises=[Exercise(name="Salida en bicicleta de carretera / gravel", target="60-90 min Zona 2")]
            )
        ]
    )
]

OCTOBER_BJJ_PROGRAM = [
    DayWorkout(
        day_id="lun_oct", day_name="Lun", date_num="5", type_badge="Gym + BJJ 19:30",
        title="Upper Body Strength (Mañana) + Jiu-Jitsu (19:30)",
        tags=["Hybrid", "BJJ", "Strength"], kpis=["Barbell Bench Press"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP & PREHAB", subtitle="Activación sin fatiga para la noche",
                exercises=[Exercise(name="Band Pull-aparts + Deadbugs", target="2 x 15 reps")]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="75% - 80% 1RM • RPE 8",
                exercises=[
                    Exercise(
                        name="Barbell Bench Press",
                        exercise_key="bench_press",
                        intensity_pct=0.775,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 75% - 80% 1RM (RPE 8)"
                    ),
                    Exercise(
                        name="Weighted Chin-ups",
                        exercise_key="pull_up",
                        intensity_pct=0.75,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 72.5% - 77.5% 1RM"
                    )
                ]
            ),
            WorkoutBlock(
                code="H", title="BJJ ARMOR & GRIP", subtitle="Blindaje para el tatami",
                exercises=[
                    Exercise(name="Farmer's Walks pesados (Agarre)", target="3 x 40m"),
                    Exercise(name="Face Pulls en polea", target="3 x 15 reps")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mar_oct", day_name="Mar", date_num="6", type_badge="Run 10k Calidad",
        title="Running: Series de Ritmo San Silvestre (1000m / 2000m)",
        tags=["Running", "Threshold", "San Silvestre"], kpis=["Ritmo 10k"],
        blocks=[
            WorkoutBlock(
                code="R", title="SERIES ESPECÍFICAS 10K", subtitle="Calidad de zancada y umbral",
                exercises=[
                    Exercise(name="3 x 2000m a ritmo 10k (Rec: 2 min trote)", target="3 x 2000m"),
                    Exercise(name="Trote de vuelta a la calma", target="10 min Z1")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mie_oct", day_name="Mié", date_num="7", type_badge="Lower Power",
        title="Lower Body: Potencia & Resistencia Isquios (Anti-lesión)",
        tags=["Hybrid", "Legs", "BJJ Prehab"], kpis=["Trap Bar Deadlift", "Back Squat"],
        blocks=[
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="77.5% - 82.5% 1RM",
                exercises=[
                    Exercise(
                        name="Trap Bar Deadlift",
                        exercise_key="deadlift",
                        intensity_pct=0.80,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 77.5% - 82.5% 1RM (RPE 8)"
                    ),
                    Exercise(name="Bulgarian Split Squat", target="3 x 8 e/s", default_weight=24.0)
                ]
            ),
            WorkoutBlock(
                code="H", title="TENDON HEALTH", subtitle="Protección de rodillas y tobillos",
                exercises=[
                    Exercise(name="Nordic Curls o RDL con mancuernas", target="3 x 8-10 reps"),
                    Exercise(name="Tibialis & Soleus raises", target="2 x 15 reps")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="jue_oct", day_name="Jue", date_num="8", type_badge="BJJ 20:30",
        title="Jiu-Jitsu: Clase Técnica & Sparring (20:30)",
        tags=["BJJ", "Martial Arts", "Grappling"], kpis=[],
        blocks=[
            WorkoutBlock(
                code="E", title="TATAMI SESSION", subtitle="Clase de BJJ + Rondas de Sparring",
                exercises=[
                    Exercise(name="Calentamiento y Drills de paso de guardia", target="20 min"),
                    Exercise(name="Técnica específica de sumisiones y control", target="30 min"),
                    Exercise(name="Rondas de sparring libre", target="5 x 5 min")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="vie_oct", day_name="Vie", date_num="9", type_badge="Full Body Gym",
        title="Full Body Athletic & Hipertrofia Funcional",
        tags=["Physique", "Perform", "Full Body"], kpis=["Overhead Press"],
        blocks=[
            WorkoutBlock(
                code="S", title="STRENGTH & POWER", subtitle="Empuje vertical y core",
                exercises=[
                    Exercise(name="Standing Dumbbell Push Press", target="4 x 6 reps", default_weight=26.0),
                    Exercise(name="Chest-Supported Row", target="3 x 10 reps", default_weight=30.0)
                ]
            ),
            WorkoutBlock(
                code="H", title="CORE ANTI-ROTACIÓN", subtitle="Defensa de pasadas en BJJ",
                exercises=[
                    Exercise(name="Pallof Press con banda", target="3 x 12 e/s"),
                    Exercise(name="Hanging Knee Raises", target="3 x 12 reps")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="sab_oct", day_name="Sáb", date_num="10", type_badge="Run 10k Tirada",
        title="Running: Tirada Larga San Silvestre (10-12 km)",
        tags=["Running", "Endurance", "San Silvestre"], kpis=["Tiempo 10 km"],
        blocks=[
            WorkoutBlock(
                code="R", title="TIRADA LARGA", subtitle="Simulación de ritmo de carrera",
                exercises=[Exercise(name="10 km continuos con desniveles", target="Ritmo cómodo + 2 km fuertes al final")]
            )
        ]
    ),
    DayWorkout(
        day_id="dom_oct", day_name="Dom", date_num="11", type_badge="Bici Z2 + Sauna",
        title="Ciclismo Z2 & Protocolo Sauna de Regeneración",
        tags=["Cycling", "Sauna", "Recovery"], is_rest_day=False,
        blocks=[
            WorkoutBlock(
                code="B", title="RECOVERY RIDE & SAUNA", subtitle="Vascularización y reseteo del SNC",
                exercises=[
                    Exercise(name="Salida suave en bicicleta", target="60 min Zona 2"),
                    Exercise(name="Sauna Seca + Rehidratación con electrolitos", target="25 min")
                ]
            )
        ]
    )
]

PROGRAMS_CATALOG = [
    Program(
        id="perform_sep",
        title="FASE 1: Septiembre (Cimentación Híbrida)",
        category="Hybrid",
        tags=["4 Días Gym", "Running 10k", "Bici Z2", "Sauna"],
        description="Fase de construcción de masa muscular, blindaje articular y base de velocidad para la 10k sin fatiga de BJJ.",
        is_active=True
    ),
    Program(
        id="perform_oct_bjj",
        title="FASE 2: Octubre (Híbrido con Jiu-Jitsu)",
        category="Hybrid + BJJ",
        tags=["3 Días Gym", "2 Días BJJ (Lun/Jue)", "Running 10k", "Bici Z2"],
        description="Integración de Jiu-Jitsu con entrenamiento de fuerza adaptado para proteger hombros, cuello y agarre.",
        is_active=False
    ),
    Program(
        id="san_silvestre",
        title="ESPECIAL: San Silvestre Vallecana 10k",
        category="Aerobic Capacity",
        tags=["Ritmo 10k", "Umbral Lactato", "Tibiales"],
        description="Foco prioritario en optimizar tu tiempo de 10k para el 31 de diciembre con trabajo de economía de carrera.",
        is_active=False
    )
]
