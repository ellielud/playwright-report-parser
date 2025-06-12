from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import get_db
from models import TestRun

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # match your frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_test_runs(db: Session = Depends(get_db)):
    return db.query(TestRun).all()

@app.get("/add-row")
def add_row(db: Session = Depends(get_db)):
    new_run = TestRun(
        test_name="search_test",
        status="flaky",
        error_message="Element not found on first try"
    )
    db.add(new_run)
    db.commit()

@app.get("/goodbye")
async def goodbye():
    return {"message": "Goodbye World"}
