from pydantic import BaseModel, Field
from typing import List, Optional

class Exercise(BaseModel):
    name: str
    target: str  # Ej: "4 x 5 reps (RPE 8)" o "1 min" o "3 x 40m"
    category: str = "accessory"  # warm_up, strength, hypertrophy, prehab, engine, running, cycling
    default_weight: Optional[float] = 0.0
    notes: Optional[str] = None

class WorkoutBlock(BaseModel):
    code: str  # W, S, H, E, R (Running), B (Bike)
    title: str
    subtitle: str
    exercises: List[Exercise]

class DayWorkout(BaseModel):
    day_id: str  # lun, mar, mie, jue, vie, sab, dom
    day_name: str
    date_num: str
    type_badge: str
    title: str
    tags: List[str]
    kpis: List[str] = []
    blocks: List[WorkoutBlock]
    is_rest_day: bool = False

class Program(BaseModel):
    id: str
    title: str
    category: str
    tags: List[str]
    description: str
    is_active: bool = False
