def calculate_estimated_1rm(weight: float, reps: int) -> float:
    """Calcula el 1RM estimado usando la fórmula de Epley"""
    if reps <= 0 or weight <= 0:
        return 0.0
    if reps == 1:
        return weight
    return round(weight * (1 + reps / 30.0), 1)

def calculate_training_load(sets_data: list) -> float:
    """Calcula el volumen total de carga (kg x reps)"""
    total_volume = 0.0
    for s in sets_data:
        total_volume += s.get("weight", 0.0) * s.get("reps", 0)
    return round(total_volume, 1)
