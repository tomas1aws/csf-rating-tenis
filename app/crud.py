from sqlalchemy.orm import Session
from . import models, schemas
from .rating import calculate_new_ratings


def crear_jugador(db: Session, jugador: schemas.JugadorCreate):
    nuevo = models.Jugador(
        nombre=jugador.nombre,
        email=jugador.email,
        elo_actual=jugador.elo_inicial,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_jugadores(db: Session):
    return db.query(models.Jugador).order_by(models.Jugador.nombre.asc()).all()


def obtener_jugador(db: Session, jugador_id: int):
    return db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()


def obtener_historial_jugador(db: Session, jugador_id: int):
    return (
        db.query(models.HistorialElo)
        .filter(models.HistorialElo.jugador_id == jugador_id)
        .order_by(models.HistorialElo.id.desc())
        .all()
    )


def obtener_ranking(db: Session):
    jugadores = (
        db.query(models.Jugador)
        .filter(models.Jugador.activo == 1)
        .order_by(models.Jugador.elo_actual.desc(), models.Jugador.nombre.asc())
        .all()
    )

    ranking = []
    for i, jugador in enumerate(jugadores, start=1):
        ranking.append(
            {
                "posicion": i,
                "id": jugador.id,
                "nombre": jugador.nombre,
                "elo_actual": jugador.elo_actual,
                "partidos_jugados": jugador.partidos_jugados,
                "victorias": jugador.victorias,
                "derrotas": jugador.derrotas,
            }
        )
    return ranking


def registrar_partido(db: Session, partido: schemas.PartidoCreate):
    if partido.jugador_1_id == partido.jugador_2_id:
        raise ValueError("Un jugador no puede jugar contra sí mismo")

    jugador_1 = obtener_jugador(db, partido.jugador_1_id)
    jugador_2 = obtener_jugador(db, partido.jugador_2_id)

    if not jugador_1 or not jugador_2:
        raise ValueError("Uno o ambos jugadores no existen")

    if partido.ganador_id not in [jugador_1.id, jugador_2.id]:
        raise ValueError("El ganador debe ser uno de los dos jugadores del partido")

    elo_1_antes = jugador_1.elo_actual
    elo_2_antes = jugador_2.elo_actual

    jugador_1_gana = partido.ganador_id == jugador_1.id
    elo_1_despues, elo_2_despues = calculate_new_ratings(
        elo_1_antes,
        elo_2_antes,
        a_wins=jugador_1_gana,
        k=32,
    )

    nuevo_partido = models.Partido(
        jugador_1_id=jugador_1.id,
        jugador_2_id=jugador_2.id,
        ganador_id=partido.ganador_id,
        elo_jugador_1_antes=elo_1_antes,
        elo_jugador_2_antes=elo_2_antes,
        elo_jugador_1_despues=elo_1_despues,
        elo_jugador_2_despues=elo_2_despues,
    )
    db.add(nuevo_partido)

    jugador_1.elo_actual = elo_1_despues
    jugador_2.elo_actual = elo_2_despues

    jugador_1.partidos_jugados += 1
    jugador_2.partidos_jugados += 1

    if jugador_1_gana:
        jugador_1.victorias += 1
        jugador_2.derrotas += 1
    else:
        jugador_2.victorias += 1
        jugador_1.derrotas += 1

    db.flush()

    historial_1 = models.HistorialElo(
        jugador_id=jugador_1.id,
        partido_id=nuevo_partido.id,
        elo_anterior=elo_1_antes,
        elo_nuevo=elo_1_despues,
        variacion=elo_1_despues - elo_1_antes,
    )
    historial_2 = models.HistorialElo(
        jugador_id=jugador_2.id,
        partido_id=nuevo_partido.id,
        elo_anterior=elo_2_antes,
        elo_nuevo=elo_2_despues,
        variacion=elo_2_despues - elo_2_antes,
    )

    db.add(historial_1)
    db.add(historial_2)

    db.commit()
    db.refresh(nuevo_partido)
    return nuevo_partido


def listar_partidos(db: Session):
    return db.query(models.Partido).order_by(models.Partido.id.desc()).all()