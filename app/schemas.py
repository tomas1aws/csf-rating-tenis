from typing import Optional
from pydantic import BaseModel, EmailStr


class JugadorCreate(BaseModel):
    nombre: str
    email: Optional[EmailStr] = None
    elo_inicial: int = 800


class JugadorResponse(BaseModel):
    id: int
    nombre: str
    email: Optional[EmailStr] = None
    elo_actual: int
    partidos_jugados: int
    victorias: int
    derrotas: int
    activo: int

    class Config:
        from_attributes = True


class PartidoCreate(BaseModel):
    jugador_1_id: int
    jugador_2_id: int
    ganador_id: int


class PartidoResponse(BaseModel):
    id: int
    jugador_1_id: int
    jugador_2_id: int
    ganador_id: int
    elo_jugador_1_antes: int
    elo_jugador_2_antes: int
    elo_jugador_1_despues: int
    elo_jugador_2_despues: int

    class Config:
        from_attributes = True


class HistorialEloResponse(BaseModel):
    id: int
    jugador_id: int
    partido_id: int
    elo_anterior: int
    elo_nuevo: int
    variacion: int

    class Config:
        from_attributes = True


class RankingEntry(BaseModel):
    posicion: int
    id: int
    nombre: str
    elo_actual: int
    partidos_jugados: int
    victorias: int
    derrotas: int