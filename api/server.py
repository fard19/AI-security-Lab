from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import uuid
import asyncio
import logging
import json
import re
from pathlib import Path

from attack_engine.adversarial_runner import AdversarialRobustnessTest


# ================================================
# CONFIGURATION
# ================================================

class Config:
    PRIMARY_GOAL = "Secure the company's network infrastructure."
    MAX_ROUNDS = 10
    MIN_ROUNDS = 1
    DEFAULT_ROUNDS = 3


# ================================================
# LOGGING
# ================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ================================================
# MODELS
# ================================================

class TestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TestRequest(BaseModel):
    objective: str = Field(..., min_length=10, max_length=500)
    rounds: int = Field(default=3, ge=1, le=10)

    @validator("objective")
    def validate_objective(cls, v):
        if not v.strip():
            raise ValueError("Objective cannot be empty")
        if len(v.split()) < 3:
            raise ValueError("Objective must contain at least 3 words")
        return v.strip()


class TestResponse(BaseModel):
    test_id: str
    status: TestStatus
    objective: str
    rounds: int
    created_at: str


class TestResultDetail(BaseModel):
    test_id: str
    status: TestStatus
    objective: str
    rounds: int
    created_at: str
    completed_at: Optional[str] = None
    execution_time: Optional[float] = None
    round_results: List[Dict[str, Any]] = []
    pressure: Optional[Dict[str, Any]] = None
    deviation: Optional[Dict[str, Any]] = None
    performance: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ================================================
# STORAGE
# ================================================

class TestStorage:

    def __init__(self):
        self._tests: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def create_test(self, test_id: str, objective: str, rounds: int):

        async with self._lock:
            test_data = {
                "test_id": test_id,
                "status": TestStatus.PENDING,
                "objective": objective,
                "rounds": rounds,
                "created_at": datetime.utcnow().isoformat(),
                "completed_at": None,
                "execution_time": None,
                "results": None,
                "error": None
            }

            self._tests[test_id] = test_data
            return test_data

    async def update_test(self, test_id: str, **kwargs):

        async with self._lock:
            if test_id in self._tests:
                self._tests[test_id].update(kwargs)

    async def get_test(self, test_id: str):
        return self._tests.get(test_id)

    async def list_tests(self, limit: int = 50):

        tests = list(self._tests.values())
        tests.sort(key=lambda x: x["created_at"], reverse=True)
        return tests[:limit]


storage = TestStorage()


# ================================================
# FASTAPI APP
# ================================================

app = FastAPI(
    title="AI Security Lab API",
    version="1.0.0",
    description="Adversarial robustness testing for AI systems"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================================
# BACKGROUND TEST EXECUTION
# ================================================

async def execute_test_async(test_id: str, objective: str, rounds: int):

    try:

        logger.info(f"Starting test {test_id}")

        await storage.update_test(test_id, status=TestStatus.RUNNING)

        start = datetime.utcnow()

        loop = asyncio.get_event_loop()

        def run():
            tester = AdversarialRobustnessTest(Config.PRIMARY_GOAL)
            return tester.run_test(
                objective=objective,
                rounds=rounds
            )

        result = await loop.run_in_executor(None, run)

        end = datetime.utcnow()

        execution_time = (end - start).total_seconds()

        round_results = result.get("round_results", [])

        await storage.update_test(
            test_id,
            status=TestStatus.COMPLETED,
            completed_at=end.isoformat(),
            execution_time=execution_time,
            results={
                "round_results": round_results,
                "pressure": result.get("pressure"),
                "deviation": result.get("deviation"),
                "performance": result.get("performance")
            }
        )

        logger.info(f"Test {test_id} completed in {execution_time:.2f}s")

    except Exception as e:

        logger.error(f"Test {test_id} failed: {e}")

        await storage.update_test(
            test_id,
            status=TestStatus.FAILED,
            completed_at=datetime.utcnow().isoformat(),
            error=str(e)
        )


# ================================================
# ENDPOINTS
# ================================================

@app.get("/")
async def root():
    return {
        "status": "AI Security Lab API running",
        "version": "1.0.0"
    }


@app.post("/tests", response_model=TestResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_test(request: TestRequest, background_tasks: BackgroundTasks):

    test_id = f"test_{uuid.uuid4().hex[:12]}"

    await storage.create_test(test_id, request.objective, request.rounds)

    background_tasks.add_task(
        execute_test_async,
        test_id,
        request.objective,
        request.rounds
    )

    logger.info(f"Created test {test_id}: {request.objective[:50]}...")

    return TestResponse(
        test_id=test_id,
        status=TestStatus.PENDING,
        objective=request.objective,
        rounds=request.rounds,
        created_at=datetime.utcnow().isoformat()
    )


@app.get("/tests/{test_id}", response_model=TestResultDetail)
async def get_test_result(test_id: str):

    test = await storage.get_test(test_id)

    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Test {test_id} not found"
        )

    result = test.get("results") or {}

    return TestResultDetail(
        test_id=test["test_id"],
        status=test["status"],
        objective=test["objective"],
        rounds=test["rounds"],
        created_at=test["created_at"],
        completed_at=test.get("completed_at"),
        execution_time=test.get("execution_time"),
        round_results=result.get("round_results", []),
        pressure=result.get("pressure"),
        deviation=result.get("deviation"),
        performance=result.get("performance"),
        error=test.get("error")
    )


# ================================================
# EXPORT JSON REPORT
# ================================================

@app.get("/tests/{test_id}/export")
async def export_test_report(test_id: str):

    test = await storage.get_test(test_id)

    if not test:
        raise HTTPException(
            status_code=404,
            detail=f"Test {test_id} not found"
        )

    if not test.get("results"):
        raise HTTPException(
            status_code=400,
            detail="Test results not ready"
        )

    objective = test["objective"]

    safe_name = re.sub(r"[^a-zA-Z0-9]+", "_", objective.lower())[:40]

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    filename = f"{safe_name}_report_{timestamp}.json"

    output_dir = Path("test_results")
    output_dir.mkdir(exist_ok=True)

    filepath = output_dir / filename

    export_data = {
        "test_config": {
            "primary_goal": Config.PRIMARY_GOAL,
            "user_adversarial_objective": objective,
            "rounds": test["rounds"],
            "test_timestamp": test["created_at"],
            "export_timestamp": datetime.utcnow().isoformat()
        },
        "results": test["results"]
    }

    with open(filepath, "w") as f:
        json.dump(export_data, f, indent=2)

    logger.info(f"Exported report {filename}")

    return FileResponse(
        filepath,
        media_type="application/json",
        filename=filename
    )


@app.get("/tests")
async def list_tests(limit: int = 50):
    return await storage.list_tests(limit)


@app.get("/stats")
async def get_stats():

    all_tests = await storage.list_tests(limit=1000)

    total = len(all_tests)

    completed = sum(1 for t in all_tests if t["status"] == TestStatus.COMPLETED)
    failed = sum(1 for t in all_tests if t["status"] == TestStatus.FAILED)
    running = sum(1 for t in all_tests if t["status"] == TestStatus.RUNNING)
    pending = sum(1 for t in all_tests if t["status"] == TestStatus.PENDING)

    return {
        "api": {
            "total_tests": total,
            "successful_tests": completed,
            "failed_tests": failed,
            "success_rate": f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
        },
        "storage": {
            "total": total,
            "pending": pending,
            "running": running,
            "completed": completed,
            "failed": failed
        },
        "system": {
            "primary_goal": Config.PRIMARY_GOAL,
            "max_rounds": Config.MAX_ROUNDS
        }
    }


# ================================================
# STARTUP / SHUTDOWN
# ================================================

@app.on_event("startup")
async def startup_event():
    logger.info("AI Security Lab API starting...")
    logger.info(f"Primary Goal: {Config.PRIMARY_GOAL}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI Security Lab API shutting down...")
