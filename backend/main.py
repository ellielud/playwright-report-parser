from typing import Annotated, List, Optional

from fastapi import FastAPI, Depends, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel

from db import get_db
from models import TestRun

app = FastAPI()

# Pydantic model for updating test runs
class TestRunUpdate(BaseModel):
    test_name: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None

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
        test_name="login_test",
        status="failed",
        error_message="Element not found on first try"
    )
    db.add(new_run)
    db.commit()

@app.get("/goodbye")
async def goodbye():
    return {"message": "Goodbye World"}

@app.post("/upload-file/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.get("/get-flaky-tests")
def get_flaky_tests(db: Session = Depends(get_db)):
    flaky_tests = db.query(TestRun).filter(
        TestRun.status == "flaky"
    ).order_by(desc(TestRun.timestamp)).all()
    
    return [
        {
            "id": test.id,
            "test_name": test.test_name,
            "error_message": test.error_message,
            "timestamp": test.timestamp.isoformat()
        }
        for test in flaky_tests
    ]

@app.get("/get-failed-tests")
def get_failed_tests(db: Session = Depends(get_db)):
    failed_tests = db.query(TestRun).filter(
        TestRun.status == "failed"
    ).order_by(desc(TestRun.timestamp)).all()
    
    return [
        {
            "id": test.id,
            "test_name": test.test_name,
            "error_message": test.error_message,
            "timestamp": test.timestamp.isoformat()
        }
        for test in failed_tests
    ]

@app.delete("/test-run/{test_run_id}")
def delete_test_run(test_run_id: int, db: Session = Depends(get_db)):
    test_run = db.query(TestRun).filter(TestRun.id == test_run_id).first()
    if not test_run:
        raise HTTPException(status_code=404, detail="Test run not found")
    
    db.delete(test_run)
    db.commit()
    return {"message": f"Test run {test_run_id} deleted successfully"}

@app.patch("/test-run/{test_run_id}")
def update_test_run(test_run_id: int, update_data: TestRunUpdate, db: Session = Depends(get_db)):
    test_run = db.query(TestRun).filter(TestRun.id == test_run_id).first()
    if not test_run:
        raise HTTPException(status_code=404, detail="Test run not found")
    
    # Update only the fields that are provided
    if update_data.test_name is not None:
        test_run.test_name = update_data.test_name
    if update_data.status is not None:
        test_run.status = update_data.status
    if update_data.error_message is not None:
        test_run.error_message = update_data.error_message
    
    db.commit()
    db.refresh(test_run)
    
    return {
        "id": test_run.id,
        "test_name": test_run.test_name,
        "status": test_run.status,
        "error_message": test_run.error_message,
        "timestamp": test_run.timestamp.isoformat()
    }