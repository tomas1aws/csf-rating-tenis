from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import schemas, crud, models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSF Rating Tenis API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "CSF Rating Tenis API funcionando"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jugadores", response_model=schemas.JugadorResponse)
def crear_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    if jugador.email:
        existente = db.query(models.Jugador).filter(models.Jugador.email == jugador.email).first()
        if existente:
            raise HTTPException(status_code=400, detail="Ya existe un jugador con ese email")
    return crud.crear_jugador(db, jugador)


@app.get("/jugadores", response_model=list[schemas.JugadorResponse])
def listar_jugadores(db: Session = Depends(get_db)):
    return crud.listar_jugadores(db)


@app.get("/jugadores/{jugador_id}", response_model=schemas.JugadorResponse)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = crud.obtener_jugador(db, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@app.get("/jugadores/{jugador_id}/historial", response_model=list[schemas.HistorialEloResponse])
def historial_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = crud.obtener_jugador(db, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return crud.obtener_historial_jugador(db, jugador_id)


@app.get("/ranking", response_model=list[schemas.RankingEntry])
def ranking(db: Session = Depends(get_db)):
    return crud.obtener_ranking(db)


@app.post("/partidos", response_model=schemas.PartidoResponse)
def registrar_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    try:
        return crud.registrar_partido(db, partido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/partidos", response_model=list[schemas.PartidoResponse])
def listar_partidos(db: Session = Depends(get_db)):
    return crud.listar_partidos(db)