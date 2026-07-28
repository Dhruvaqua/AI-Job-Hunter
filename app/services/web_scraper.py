import requests
from bs4 import BeautifulSoup


class WebScraper:

    @staticmethod
    def fetch_job_description(url: str) -> str:
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
                )
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=15,
            )

            if response.status_code != 200:
                return ""

            soup = BeautifulSoup(response.text, "lxml")

            text = soup.get_text(" ", strip=True)

            return text

        except Exception:
            return ""