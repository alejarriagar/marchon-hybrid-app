from pydantic import BaseModel
from typing import List, Optional

class Exercise(BaseModel):
    name: str
    target: str
    category: str = "accessory"
    exercise_key: Optional[str] = None
    intensity_pct: Optional[float] = None
    target_sets: int = 3
    target_reps: int = 10
    default_weight: Optional[float] = 0.0
    rest_seconds: Optional[int] = 90  # Tiempo de descanso en segundos
    rest_description: Optional[str] = "90s descanso"
    notes: Optional[str] = None

class WorkoutBlock(BaseModel):
    code: str
    title: str
    subtitle: str
    rest_block_desc: Optional[str] = None
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
