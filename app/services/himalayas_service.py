import requests

BASE_URL = "https://himalayas.app/jobs/api/search"

ROLE_QUERY_TERMS = (
    "software engineer",
    "backend",
    "python",
    "data engineer",
    "cloud",
    "ai engineer",
    "machine learning",
    "developer",
    "platform engineer",
)

class HimalayasService:
    """Read-only adapter for the public Himalayas remote-jobs API."""

    @classmethod
    def fetch_jobs(cls, keyword: str | None = None, country: str | None = None, limit: int = 20):
        params = {"sort": "recent", "limit": min(max(limit, 1), 20)}
        if keyword:
            params["q"] = keyword
        if country:
            params["country"] = country

        response = requests.get(BASE_URL, params=params, timeout=20)
        response.raise_for_status()

        jobs = []
        for item in response.json().get("jobs", []):
            jobs.append({
                "title": item.get("title") or "",
                "company": item.get("companyName") or "Unknown",
                "location": ", ".join(item.get("locationRestrictions") or []) or "Remote",
                "salary": cls._salary(item),
                "url": item.get("applicationLink") or item.get("guid"),
                "description": item.get("description") or item.get("excerpt") or "",
            })
        return jobs

    @staticmethod
    def _salary(item):
        low = item.get("minSalary")
        high = item.get("maxSalary")
        currency = item.get("currency") or ""
        period = item.get("salaryPeriod") or ""
        if low is None and high is None:
            return None
        if low is not None and high is not None:
            return f"{currency} {low:g}-{high:g} {period}".strip()
        value = low if low is not None else high
        return f"{currency} {value:g} {period}".strip()
