
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from .database import SessionLocal, engine
from . import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blip Bloup API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/ping")
def create_ping(request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    ping = models.Ping(
        ip=ip,
        created_at=datetime.utcnow()
    )
    db.add(ping)
    db.commit()
    db.refresh(ping)

    return {"message": "Blip enregistré", "ip": ip}


@app.get("/pings")
def get_pings(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    pings = db.query(models.Ping)\
        .order_by(models.Ping.created_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    total = db.query(models.Ping).count()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": pings
    }