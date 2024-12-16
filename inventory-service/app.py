from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

DB_CONFIG = {
    "dbname": "inventory_service",
    "user": "postgres",
    "password": "password",
    "host": "postgres",
    "port": "5432"
}

class Room(BaseModel):
    room_number: int
    room_type: str
    status: str

@app.post("/rooms")
def create_room(room: Room):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO rooms (room_number, room_type, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (room.room_number, room.room_type, room.status))
        conn.commit()
        return {"message": "Room created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
