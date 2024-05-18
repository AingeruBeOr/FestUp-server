from datetime import date, timedelta
from dbClasses import Evento
from database import SessionLocal
import os

# Get today date + 2 hours (to match the timezone of Madrid, Spain)
today = date.today() + timedelta(hours=2)

conn = SessionLocal()

eventos_query = conn.query(Evento).filter(Evento.fecha < today)
eventos = eventos_query.all()
query = eventos_query.delete()
conn.commit()

# Delete event images
deleted_images = 0
for evento in eventos:
    try:
        os.remove(f"/app/eventoImages/{evento.id}.png")
        deleted_images += 1
    except FileNotFoundError:
        pass

print(f"{query} past events deleted, {deleted_images} images deleted")