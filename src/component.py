from dataclasses import dataclass, field
from pigframe import *

@dataclass
class Velocity(Component):
    x: int = 0
    y: int = 0
    speed: int = 1
    default_speed: int = 1

@dataclass
class Position(Component):
    x: int = 0
    y: int = 0

@dataclass
class Controlable(Component):
    up: int
    down: int
    left: int
    right: int

@dataclass
class Collidable(Component):
    pass

@dataclass
class Hockey(Component):
    id: int = None
    color: int = 2
    radius: int = 20

@dataclass
class Puck(Component):
    id: int = None
    radius: int = 10
    
@dataclass
class Field(Component):
    width: int = 580
    height: int = 380
    goal_width: int = 80
    
@dataclass
class Score(Component):
    score: int = 0
    
@dataclass
class Result(Component):
    winner: str = None
    scores: dict = field(default_factory= lambda: {
        0: 0,
        1: 0
    })
    names: dict = field(default_factory= lambda: {
        0: "ひだり",
        1: "みぎ"
    })