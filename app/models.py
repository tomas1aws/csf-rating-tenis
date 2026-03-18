from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    email = Column(String, nullable=True, unique=True)
    elo_actual = Column(Integer, nullable=False, default=800)
    partidos_jugados = Column(Integer, nullable=False, default=0)
    victorias = Column(Integer, nullable=False, default=0)
    derrotas = Column(Integer, nullable=False, default=0)
    activo = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    partidos_como_jugador_1 = relationship(
        "Partido", foreign_keys="Partido.jugador_1_id", back_populates="jugador_1"
    )
    partidos_como_jugador_2 = relationship(
        "Partido", foreign_keys="Partido.jugador_2_id", back_populates="jugador_2"
    )


class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    jugador_1_id = Column(Integer, ForeignKey("jugadores.id"), nullable=False)
    jugador_2_id = Column(Integer, ForeignKey("jugadores.id"), nullable=False)
    ganador_id = Column(Integer, ForeignKey("jugadores.id"), nullable=False)

    elo_jugador_1_antes = Column(Integer, nullable=False)
    elo_jugador_2_antes = Column(Integer, nullable=False)
    elo_jugador_1_despues = Column(Integer, nullable=False)
    elo_jugador_2_despues = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    jugador_1 = relationship("Jugador", foreign_keys=[jugador_1_id], back_populates="partidos_como_jugador_1")
    jugador_2 = relationship("Jugador", foreign_keys=[jugador_2_id], back_populates="partidos_como_jugador_2")


class HistorialElo(Base):
    __tablename__ = "historial_elo"

    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"), nullable=False)
    partido_id = Column(Integer, ForeignKey("partidos.id"), nullable=False)
    elo_anterior = Column(Integer, nullable=False)
    elo_nuevo = Column(Integer, nullable=False)
    variacion = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())