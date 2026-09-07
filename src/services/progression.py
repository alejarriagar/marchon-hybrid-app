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

def calculate_training_load(sets_data: list) -> float:
    total_volume = 0.0
    for s in sets_data:
        total_volume += s.get("weight", 0.0) * s.get("reps", 0)
    return round(total_volume, 1)
