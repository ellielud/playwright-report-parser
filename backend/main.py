from typing import List
from datetime import datetime

from fastapi import FastAPI, Depends, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from sqlalchemy.orm import Session

from db import get_db
from models import TestRun

app = FastAPI()

# Allow our frontend to talk to our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_playwright_report(report_data: dict) -> List[TestRun]:
    test_runs = []
    
    # Go through each test suite in the report
    for suite in report_data.get('suites', []):
        suite_name = suite['title']
        
        # Go through each test in the suite
        for spec in suite.get('specs', []):
            spec_name = spec['title']
            
            # Go through each test run
            for test in spec.get('tests', []):
                for result in test.get('results', []):
                    # Get the test status (passed, failed, etc.)
                    status = result['status']
                    
                    # Get any error messages if the test failed
                    error_message = None
                    if result.get('errors'):
                        error_message = '\n'.join(error.get('message', '') for error in result['errors'])
                    
                    # Get when the test was run
                    timestamp = datetime.fromisoformat(result['startTime'].replace('Z', '+00:00'))
                    
                    # Create a new test run record
                    test_run = TestRun(
                        test_name=f"{suite_name} - {spec_name}",
                        status=status,
                        error_message=error_message,
                        timestamp=timestamp
                    )
                    test_runs.append(test_run)
    
    return test_runs

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

@app.post("/upload-file/")
async def create_file(file: bytes):
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
