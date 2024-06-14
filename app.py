from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import databases
import sqlalchemy

DATABASE_URL = "postgresql://users_data_gjpa_user:lPRq94fX7KBrUbRFg1SqK97goEWAh8Oh@dpg-cpm2nqqj1k6c739vt06g-a.oregon-postgres.render.com:5432/users_data_gjpa"

# Initialize the database connection
database = databases.Database(DATABASE_URL)

# SQLAlchemy metadata
metadata = sqlalchemy.MetaData()

# Define the table
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("quiz_start", sqlalchemy.Integer),
    sqlalchemy.Column("quiz_end", sqlalchemy.Integer),
    sqlalchemy.Column("quiz_result", sqlalchemy.Integer),
)

# Create the database engine
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

class UserData(BaseModel):
    user_id: int
    full_name: str
    quiz_start: int
    quiz_end: int
    quiz_result: int

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Hello There!"}

@app.post("/api/user_data")
async def video_watched(user_data: UserData):
    query = users.insert().values(
        id=user_data.user_id,
        full_name=user_data.full_name,
        quiz_start=user_data.quiz_start,
        quiz_end=user_data.quiz_end,
        quiz_result=user_data.quiz_result,
    )
    try:
        await database.execute(query)
        return {"message": "Data added."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api")
async def video_watcheds():
    query = users.select()
    try:
        all_users = await database.fetch_all(query)
        return {"message": f"hello update {all_users}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
