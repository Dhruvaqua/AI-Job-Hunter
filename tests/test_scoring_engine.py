from app.ai.scoring_engine import ScoringEngine


def test_perfect_skill_match():
    candidate = {
        "skills": ["Python", "FastAPI", "SQL", "Docker"],
        "location": "Hyderabad",
        "experience": 2,
    }

    job = {
        "required_skills": "Python, FastAPI, SQL, Docker",
        "location": "Hyderabad",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["score"] == 100
    assert result["matched_skills"] == [
        "docker",
        "fastapi",
        "python",
        "sql",
    ]
    assert result["missing_skills"] == []
    assert result["recommendation"] == "Apply"


def test_partial_skill_match():
    candidate = {
        "skills": ["Python", "SQL"],
        "location": "Hyderabad",
        "experience": 1,
    }

    job = {
        "required_skills": "Python, SQL, Docker, AWS",
        "location": "Hyderabad",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == ["aws", "docker"]
    assert result["breakdown"]["skills"] == 35
    assert result["breakdown"]["location"] == 20
    assert result["breakdown"]["experience"] == 10


def test_remote_job_matches_any_location():
    candidate = {
        "skills": ["Python"],
        "location": "Hyderabad",
        "experience": 1,
    }

    job = {
        "required_skills": "Python",
        "location": "Remote",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["breakdown"]["location"] == 20


def test_location_mismatch():
    candidate = {
        "skills": ["Python"],
        "location": "Hyderabad",
        "experience": 1,
    }

    job = {
        "required_skills": "Python",
        "location": "Bangalore",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["breakdown"]["location"] == 0
    assert "Location preference does not match." in result["improvements"]


def test_no_experience():
    candidate = {
        "skills": ["Python"],
        "location": "Hyderabad",
        "experience": 0,
    }

    job = {
        "required_skills": "Python",
        "location": "Hyderabad",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["breakdown"]["experience"] == 0
    assert "Gain more relevant professional or internship experience." in result[
        "improvements"
    ]


def test_empty_job_skills():
    candidate = {
        "skills": ["Python", "SQL"],
        "location": "Hyderabad",
        "experience": 1,
    }

    job = {
        "required_skills": "",
        "location": "Remote",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["breakdown"]["skills"] == 0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []


def test_case_insensitive_skill_matching():
    candidate = {
        "skills": ["PYTHON", "FastAPI"],
        "location": "Hyderabad",
        "experience": 1,
    }

    job = {
        "required_skills": "python, fastapi",
        "location": "Remote",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["matched_skills"] == ["fastapi", "python"]
    assert result["missing_skills"] == []


def test_skill_string_is_normalized():
    candidate = {
        "skills": "Python, SQL, Docker",
        "location": "Hyderabad",
        "experience": 1,
    }

    job = {
        "required_skills": "Python, SQL",
        "location": "Remote",
    }

    result = ScoringEngine.score(candidate, job)

    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == []