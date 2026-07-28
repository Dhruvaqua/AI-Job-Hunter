from app.services.web_scraper import WebScraper
from app.ai.skill_extractor import SkillExtractor

url = "https://job-boards.greenhouse.io/discord/jobs/8642220002"

text = WebScraper.fetch_job_description(url)

print(text[:1000])

print()

print(SkillExtractor.extract(text))