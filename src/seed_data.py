from src.models.workout import DayWorkout, WorkoutBlock, Exercise, Program

# FASE 1: SEPTIEMBRE (4 DÍAS GYM + 2 RUNNING 10K + BICI + SAUNA)
SEPTEMBER_PROGRAM = [
    DayWorkout(
        day_id="lun_sep", day_name="Lun", date_num="7", type_badge="Gym 1: Torso A",
        title="Upper Body A: Push & Pull (Fuerza & Cuidado de Brazo)",
        tags=["Gym", "Fuerza", "Bench Press"], kpis=["Barbell Bench Press"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP", subtitle="2 Rondas continuas por calidad",
                rest_block_desc="Sin descanso entre ejercicios",
                exercises=[
                    Exercise(name="SkiErg / Rower suave", target="1 min a ritmo constante", rest_seconds=0, rest_description="Fluido"),
                    Exercise(name="Band Pull-aparts + Scapular Push-ups", target="15 + 10 reps", rest_seconds=0, rest_description="Fluido"),
                    Exercise(name="Deadbugs con control pélvico", target="10 e/s", rest_seconds=30, rest_description="30s descanso")
                ]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="Semana 1: Onda 72.5% - 80% 1RM • RPE 8",
                rest_block_desc="Descanso estricto: 2:30 min entre series",
                exercises=[
                    Exercise(
                        name="Barbell Bench Press",
                        exercise_key="bench_press",
                        intensity_pct=0.775,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 72.5% - 80% 1RM (RPE 8)",
                        rest_seconds=150,
                        rest_description="2:30 min descanso",
                        notes="Pausa de 1 segundo en el pecho. Agarre firme sin hiperextender muñecas."
                    ),
                    Exercise(
                        name="Chest-Supported T-Bar / DB Row (Protección de brazo)",
                        default_weight=32.5,
                        target_sets=4,
                        target_reps=6,
                        target="4 x 6 reps pesadas (RPE 8)",
                        rest_seconds=120,
                        rest_description="2:00 min descanso",
                        notes="Apoyo en banco para eliminar tensión lumbar y usar agarre neutro que no fuerce el brazo."
                    )
                ]
            ),
            WorkoutBlock(
                code="H", title="FUNCTIONAL HYPERTROPHY", subtitle="Triserie • RIR 2 • 3 Rondas",
                rest_block_desc="90 segundos de descanso tras completar la triserie",
                exercises=[
                    Exercise(name="Incline Dumbbell Press (Agarre Neutro 45°)", target="3 x 8-10 reps", rest_seconds=0, rest_description="Sin descanso -> H2"),
                    Exercise(name="Neutral Grip Lat Pulldown (Jalón neutro en polea)", target="3 x 10-12 reps", rest_seconds=0, rest_description="Sin descanso -> H3"),
                    Exercise(name="Face Pulls en polea + Rotadores externos", target="3 x 15 reps", rest_seconds=90, rest_description="90s descanso al finalizar")
                ]
            ),
            WorkoutBlock(
                code="E", title="PREHAB & CORE", subtitle="Anti-rotación y transporte",
                rest_block_desc="60 segundos de descanso entre rondas",
                exercises=[
                    Exercise(name="Farmer's Walks con mancuernas (peso moderado)", target="3 x 40 metros", rest_seconds=45, rest_description="45s descanso"),
                    Exercise(name="Pallof Press con banda / polea", target="3 x 12 e/s", rest_seconds=60, rest_description="60s descanso")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mar_sep", day_name="Mar", date_num="8", type_badge="Run 10k Series",
        title="Running: Series San Silvestre 10k (Ritmo Umbral)",
        tags=["Running", "Threshold", "San Silvestre"], kpis=["Ritmo 1000m (Umbral)"],
        blocks=[
            WorkoutBlock(
                code="W", title="CALENTAMIENTO & DRILLES", subtitle="Preparación tendinosa",
                exercises=[
                    Exercise(name="Trote suave Z1", target="10 minutos", rest_seconds=60, rest_description="1 min"),
                    Exercise(name="Drills de técnica + Progresiones", target="3 rectas de 70m", rest_seconds=90, rest_description="90s")
                ]
            ),
            WorkoutBlock(
                code="R", title="BLOQUE PRINCIPAL 10K", subtitle="Ritmo objetivo San Silvestre",
                rest_block_desc="Recuperación: 90s trote muy suave Z1 entre series de 1000m",
                exercises=[
                    Exercise(name="6 x 1000m a ritmo objetivo 10k", target="6 series", rest_seconds=90, rest_description="90s trote suave Z1", notes="Mantener ritmo uniforme en todas las repeticiones"),
                    Exercise(name="Enfriamiento suave Z1", target="10 minutos", rest_seconds=0, rest_description="Fin de sesión")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mie_sep", day_name="Mié", date_num="9", type_badge="Gym 2: Pierna A",
        title="Lower Body A: Sentadilla, Cuádriceps & RDL",
        tags=["Gym", "Fuerza", "Squat", "RDL"], kpis=["Barbell Back Squat"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP & PREHAB", subtitle="Cadera y tobillos para carrera",
                exercises=[
                    Exercise(name="90/90 Hip Switches + Spiderman Lunges", target="2 x 8 e/s", rest_seconds=0, rest_description="Fluido"),
                    Exercise(name="Calf / Soleus raises con pausa de 2s", target="2 x 15 reps", rest_seconds=45, rest_description="45s descanso")
                ]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="Semana 1: Onda 75% - 80% 1RM",
                rest_block_desc="2:30 min de descanso entre series pesadas",
                exercises=[
                    Exercise(
                        name="Barbell Back Squat",
                        exercise_key="back_squat",
                        intensity_pct=0.775,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 75% - 80% 1RM (RPE 8)",
                        rest_seconds=150,
                        rest_description="2:30 min descanso",
                        notes="Profundidad paralela, tronco firme."
                    )
                ]
            ),
            WorkoutBlock(
                code="H", title="POSTERIOR & UNILATERAL", subtitle="Cadena posterior y prevención",
                rest_block_desc="75 segundos de descanso",
                exercises=[
                    Exercise(name="Dumbbell Romanian Deadlift (RDL)", target="3 x 10 reps (RIR 2)", default_weight=30.0, rest_seconds=90, rest_description="90s descanso", notes="Bisagra pura de cadera estirando isquios"),
                    Exercise(name="Bulgarian Split Squat con mancuernas", target="3 x 8 e/s", rest_seconds=60, rest_description="60s entre piernas"),
                    Exercise(name="Tibialis Raises en pared (Anti-periostitis)", target="2 x 20 reps", rest_seconds=45, rest_description="45s descanso")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="jue_sep", day_name="Jue", date_num="10", type_badge="Gym 3: Torso B",
        title="Upper Body B: Estructura, Hombros & Remos",
        tags=["Gym", "Physique", "Overhead Press"], kpis=["Overhead Press"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP", subtitle="Movilidad escapular y manguito",
                exercises=[Exercise(name="Kettlebell Halos + Rotaciones torácicas", target="2 x 8 e/s", rest_seconds=30, rest_description="30s descanso")]
            ),
            WorkoutBlock(
                code="S", title="STRENGTH & DENSITY", subtitle="Semana 1: 72.5% - 77.5% 1RM",
                rest_block_desc="2:00 min de descanso entre series",
                exercises=[
                    Exercise(
                        name="Standing Barbell Overhead Press (OHP)",
                        exercise_key="ohp",
                        intensity_pct=0.75,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 72.5% - 77.5% 1RM (RPE 8)",
                        rest_seconds=120,
                        rest_description="2:00 min descanso",
                        notes="Glúteos y core compactados."
                    ),
                    Exercise(name="Barbell Pendlay Row (o Remo en Polea Neutro)", target="4 x 6-8 reps", default_weight=70.0, rest_seconds=90, rest_description="90s descanso")
                ]
            ),
            WorkoutBlock(
                code="H", title="VOLUME & ARM SAFE", subtitle="Hipertrofia sin estrés articular",
                rest_block_desc="60 a 75 segundos de descanso",
                exercises=[
                    Exercise(name="Neutral Grip DB Floor Press", target="3 x 10-12 reps", rest_seconds=75, rest_description="75s descanso", notes="El suelo limita el rango protegiendo hombro y codo"),
                    Exercise(name="Single-Arm Cable Row (Enfoque Dorsal)", target="3 x 10 e/s", rest_seconds=60, rest_description="60s descanso"),
                    Exercise(name="Dumbbell Lateral Raises (Elevaciones laterales)", target="3 x 15 reps", rest_seconds=60, rest_description="60s descanso")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="vie_sep", day_name="Vie", date_num="11", type_badge="Gym 4: Pierna B",
        title="Lower Body B: Deadlift Focus, Cadena Posterior & Glúteo",
        tags=["Gym", "Fuerza", "Deadlift", "Cadena Posterior"], kpis=["Trap Bar Deadlift"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP & HINGE PREP", subtitle="Activación de glúteos e isquios",
                exercises=[
                    Exercise(name="Glute Bridges con banda", target="2 x 15 reps", rest_seconds=0, rest_description="Fluido"),
                    Exercise(name="Good Mornings con Kettlebell/Banda", target="2 x 10 reps", rest_seconds=30, rest_description="30s descanso")
                ]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="Semana 1: Onda 75% - 82.5% 1RM",
                rest_block_desc="Descanso estricto: 2:30 min entre series de Peso Muerto",
                exercises=[
                    Exercise(
                        name="Trap Bar Deadlift (o Peso Muerto Convencional)",
                        exercise_key="deadlift",
                        intensity_pct=0.80,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 77.5% - 82.5% 1RM (RPE 8)",
                        rest_seconds=150,
                        rest_description="2:30 min descanso",
                        notes="Empuje explosivo desde el suelo manteniendo columna neutra."
                    )
                ]
            ),
            WorkoutBlock(
                code="H", title="POSTERIOR CHAIN POWER", subtitle="Glúteo, isquios y estabilidad",
                rest_block_desc="75 segundos de descanso",
                exercises=[
                    Exercise(name="Barbell / DB Hip Thrust", target="3 x 10-12 reps", default_weight=90.0, rest_seconds=75, rest_description="75s descanso"),
                    Exercise(name="Walking Lunges con mancuernas", target="3 x 10 pasos e/s", rest_seconds=60, rest_description="60s descanso"),
                    Exercise(name="Hanging Knee / Leg Raises", target="3 x 12-15 reps", rest_seconds=60, rest_description="60s descanso")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="sab_sep", day_name="Sáb", date_num="12", type_badge="Run 10k Tirada",
        title="Running: Tirada Continua Progresiva (8-10 km)",
        tags=["Running", "Aerobic Base", "San Silvestre"], kpis=["Tiempo 10 km"],
        blocks=[
            WorkoutBlock(
                code="R", title="TIRADA AERÓBICA", subtitle="Base cardiovascular para la San Silvestre",
                rest_block_desc="Carrera continua",
                exercises=[
                    Exercise(name="Primeros 6 km en Zona 2 conversacional", target="6 km Z2", rest_seconds=0, rest_description="Continuo"),
                    Exercise(name="Últimos 3 km a ritmo objetivo 10k", target="3 km ritmo carrera", rest_seconds=0, rest_description="Continuo")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="dom_sep", day_name="Dom", date_num="13", type_badge="Bici Z2 + Sauna",
        title="Ciclismo: Fondo Aeróbico & Sauna de Regeneración",
        tags=["Cycling", "Zone 2", "Sauna"], kpis=[],
        blocks=[
            WorkoutBlock(
                code="B", title="FONDO EN BICI & SAUNA", subtitle="Recuperación activa y desarrollo mitocondrial",
                rest_block_desc="Pedaleo continuo + Sauna post-sesión",
                exercises=[
                    Exercise(name="Salida en bicicleta de carretera / gravel", target="60-90 min Zona 2", rest_seconds=0, rest_description="Continuo"),
                    Exercise(name="Sauna Seca + Rehidratación con electrolitos", target="25-30 min", rest_seconds=0, rest_description="Regeneración total")
                ]
            )
        ]
    )
]

# FASE 2: OCTUBRE CON BJJ (3 DÍAS GYM + 2 DÍAS BJJ + 2 RUNNING + BICI)
OCTOBER_BJJ_PROGRAM = [
    DayWorkout(
        day_id="lun_oct", day_name="Lun", date_num="5", type_badge="Gym + BJJ 19:30",
        title="Upper Body Strength (Mañana) + Jiu-Jitsu (19:30)",
        tags=["Hybrid", "BJJ", "Strength"], kpis=["Barbell Bench Press"],
        blocks=[
            WorkoutBlock(
                code="W", title="WARM UP & PREHAB", subtitle="Activación sin fatiga para la noche",
                exercises=[Exercise(name="Band Pull-aparts + Deadbugs", target="2 x 15 reps", rest_seconds=30, rest_description="30s")]
            ),
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="75% - 80% 1RM • RPE 8",
                rest_block_desc="2:30 min descanso entre series pesadas",
                exercises=[
                    Exercise(
                        name="Barbell Bench Press",
                        exercise_key="bench_press",
                        intensity_pct=0.775,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 75% - 80% 1RM (RPE 8)",
                        rest_seconds=150,
                        rest_description="2:30 min descanso"
                    ),
                    Exercise(
                        name="Chest-Supported Row Pesado",
                        default_weight=35.0,
                        target_sets=4,
                        target_reps=6,
                        target="4 x 6 reps (RPE 8)",
                        rest_seconds=120,
                        rest_description="2:00 min descanso"
                    )
                ]
            ),
            WorkoutBlock(
                code="H", title="BJJ ARMOR & GRIP", subtitle="Blindaje para el tatami",
                rest_block_desc="60 segundos de descanso",
                exercises=[
                    Exercise(name="Farmer's Walks pesados (Agarre)", target="3 x 40m", rest_seconds=60, rest_description="60s descanso"),
                    Exercise(name="Face Pulls en polea", target="3 x 15 reps", rest_seconds=45, rest_description="45s descanso")
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
                rest_block_desc="2 minutos de trote suave de recuperación entre series de 2000m",
                exercises=[
                    Exercise(name="3 x 2000m a ritmo 10k", target="3 x 2000m", rest_seconds=120, rest_description="2 min trote suave Z1"),
                    Exercise(name="Trote de vuelta a la calma", target="10 min Z1", rest_seconds=0, rest_description="Fin de sesión")
                ]
            )
        ]
    ),
    DayWorkout(
        day_id="mie_oct", day_name="Mié", date_num="7", type_badge="Lower Power",
        title="Lower Body: Peso Muerto & Potencia Isquios",
        tags=["Hybrid", "Legs", "Deadlift", "BJJ Prehab"], kpis=["Trap Bar Deadlift"],
        blocks=[
            WorkoutBlock(
                code="S", title="PRIMARY STRENGTH (% 1RM WAVE)", subtitle="77.5% - 82.5% 1RM",
                rest_block_desc="2:30 min descanso entre series",
                exercises=[
                    Exercise(
                        name="Trap Bar Deadlift",
                        exercise_key="deadlift",
                        intensity_pct=0.80,
                        target_sets=4,
                        target_reps=5,
                        target="4 x 5 @ 77.5% - 82.5% 1RM (RPE 8)",
                        rest_seconds=150,
                        rest_description="2:30 min descanso"
                    ),
                    Exercise(name="Bulgarian Split Squat", target="3 x 8 e/s", default_weight=24.0, rest_seconds=60, rest_description="60s entre piernas")
                ]
            ),
            WorkoutBlock(
                code="H", title="TENDON HEALTH & RDL", subtitle="Protección de rodillas y tobillos",
                rest_block_desc="75 segundos de descanso",
                exercises=[
                    Exercise(name="Dumbbell Romanian Deadlift (RDL)", target="3 x 8-10 reps", rest_seconds=90, rest_description="90s descanso"),
                    Exercise(name="Tibialis & Soleus raises", target="2 x 15 reps", rest_seconds=45, rest_description="45s descanso")
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
                rest_block_desc="1 minuto de descanso entre asaltos de sparring",
                exercises=[
                    Exercise(name="Calentamiento y Drills de paso de guardia", target="20 min", rest_seconds=60, rest_description="1 min agua"),
                    Exercise(name="Técnica específica de sumisiones y control", target="30 min", rest_seconds=60, rest_description="1 min"),
                    Exercise(name="Rondas de sparring libre", target="5 x 5 min", rest_seconds=60, rest_description="1 min descanso entre rondas")
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
                rest_block_desc="90 segundos de descanso",
                exercises=[
                    Exercise(name="Standing Dumbbell Push Press", target="4 x 6 reps", default_weight=26.0, rest_seconds=90, rest_description="90s descanso"),
                    Exercise(name="Chest-Supported Row", target="3 x 10 reps", default_weight=30.0, rest_seconds=90, rest_description="90s descanso")
                ]
            ),
            WorkoutBlock(
                code="H", title="CORE ANTI-ROTACIÓN", subtitle="Defensa de pasadas en BJJ",
                rest_block_desc="60 segundos de descanso",
                exercises=[
                    Exercise(name="Pallof Press con banda", target="3 x 12 e/s", rest_seconds=45, rest_description="45s e/s"),
                    Exercise(name="Hanging Knee Raises", target="3 x 12 reps", rest_seconds=60, rest_description="60s descanso")
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
                rest_block_desc="Carrera continua",
                exercises=[Exercise(name="10 km continuos con desniveles", target="Ritmo cómodo + 2 km fuertes al final", rest_seconds=0, rest_description="Continuo")]
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
                rest_block_desc="Continuo + Sauna",
                exercises=[
                    Exercise(name="Salida suave en bicicleta", target="60 min Zona 2", rest_seconds=0, rest_description="Continuo"),
                    Exercise(name="Sauna Seca + Rehidratación con electrolitos", target="25 min", rest_seconds=0, rest_description="Fin de sesión")
                ]
            )
        ]
    )
]

PROGRAMS_CATALOG = [
    Program(
        id="perform_sep",
        title="FASE 1: Septiembre (Cimentación Híbrida - 4 Días Gym)",
        category="Hybrid (4 Días Gym)",
        tags=["4 Días Gym", "Running 10k", "Deadlift Focus", "Sauna"],
        description="Fase de 4 días de fuerza (Torso/Pierna), blindaje articular sin dominadas lastradas y peso muerto pesado.",
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
