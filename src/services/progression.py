def calculate_estimated_1rm(weight: float, reps: int) -> float:
    """Calcula el 1RM estimado usando la fórmula de Epley"""
    if reps <= 0 or weight <= 0:
        return 0.0
    if reps == 1:
        return weight
    return round(weight * (1 + reps / 30.0), 1)

def calculate_target_weight(one_rep_max: float, pct: float, rounding: float = 2.5) -> float:
    """Calcula el peso exacto según el % 1RM y lo redondea a discos de 2.5kg"""
    if not one_rep_max or not pct:
        return 0.0
    raw_weight = one_rep_max * pct
    return round(raw_weight / rounding) * rounding

def get_week_periodization_wave(week_num: int) -> dict:
    """Retorna la configuración de la onda de carga según la semana de periodización de Ollie Marchon"""
    if week_num == 1:
        return {
            "name": "Semana 1: Acumulación",
            "pct_wave": [72.5, 75.0, 77.5, 80.0],
            "sets": 4,
            "reps": 5,
            "rpe": 8.0,
            "desc": "Establecimiento de volumen y velocidad de barra"
        }
    elif week_num == 2:
        return {
            "name": "Semana 2: Sobrecarga Progresiva",
            "pct_wave": [75.0, 77.5, 80.0, 82.5],
            "sets": 4,
            "reps": 5,
            "rpe": 8.5,
            "desc": "Incremento de intensidad manteniendo volumen"
        }
    elif week_num == 3:
        return {
            "name": "Semana 3: Pico de Intensidad",
            "pct_wave": [80.0, 82.5, 85.0, 87.5],
            "sets": 4,
            "reps": 3,
            "rpe": 9.0,
            "desc": "Fuerza máxima y reclutamiento neuromuscular"
        }
    else:  # Semana 4
        return {
            "name": "Semana 4: Descarga (Deload)",
            "pct_wave": [60.0, 65.0],
            "sets": 2,
            "reps": 5,
            "rpe": 6.5,
            "desc": "Asimilación biológica y regeneración articular"
        }

def calculate_running_10k_paces(target_time_min: float) -> dict:
    """Calcula ritmos específicos de entrenamiento para la San Silvestre 10k"""
    race_pace_sec = (target_time_min * 60) / 10.0
    intervals_pace_sec = race_pace_sec - 8  # 8 seg más rápido que ritmo de carrera
    easy_z2_pace_sec = race_pace_sec * 1.25  # Ritmo aeróbico suave

    def sec_to_min_sec(s):
        m = int(s // 60)
        sec = int(s % 60)
        return f"{m}:{sec:02d} min/km"

    return {
        "race_pace": sec_to_min_sec(race_pace_sec),
        "intervals_1000m": sec_to_min_sec(intervals_pace_sec),
        "tempo_pace": sec_to_min_sec(race_pace_sec + 5),
        "z2_easy": sec_to_min_sec(easy_z2_pace_sec)
    }
