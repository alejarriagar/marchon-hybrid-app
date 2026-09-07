from pydantic import BaseModel, Field
from typing import List, Optional

class Exercise(BaseModel):
    name: str
    target: str
    category: str = "accessory"
    exercise_key: Optional[str] = None  # bench_press, back_squat, deadlift, ohp, pull_up
    intensity_pct: Optional[float] = None  # Ej: 0.775 (77.5% 1RM)
    target_sets: int = 3
    target_reps: int = 10
    default_weight: Optional[float] = 0.0
    notes: Optional[str] = None

class WorkoutBlock(BaseModel):
    code: str
    title: str
    subtitle: str
    exercises: List[Exercise]

class DayWorkout(BaseModel):
    day_id: str
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
