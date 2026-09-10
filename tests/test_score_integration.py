from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database.session import get_db
from app.main import app
from app.models.job import Job


TEST_DATABASE_URL = "sqlite:///./test_score.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_module():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    job = Job(
        title="Backend Engineer",
        company="Test Company",
        location="Hyderabad",
        salary="₹12 LPA",
        url="https://example.com/test-backend-engineer",
        description="Backend engineering role.",
        required_skills="Python, FastAPI, SQL, Docker",
    )

    db.add(job)
    db.commit()
    db.close()


def teardown_module():
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_score_existing_job():
    db = TestingSessionLocal()

    job = db.query(Job).filter(
        Job.url == "https://example.com/test-backend-engineer"
    ).first()

    db.close()

    response = client.post(
        "/score/",
        json={
            "job_id": job.id,
            "candidate": {
                "name": "Test Candidate",
                "location": "Hyderabad",
                "experience": 2,
                "skills": [
                    "Python",
                    "FastAPI",
                    "SQL",
                ],
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["score"] == 72
    assert data["matched_skills"] == [
        "fastapi",
        "python",
        "sql",
    ]
    assert data["missing_skills"] == ["docker"]
    assert data["breakdown"]["skills"] == 52
    assert data["breakdown"]["location"] == 20
    assert data["breakdown"]["experience"] == 10