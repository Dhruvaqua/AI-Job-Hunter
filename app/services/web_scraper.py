import requests
from bs4 import BeautifulSoup

from app.security import validate_external_url


class WebScraper:

    @staticmethod
    def fetch_job_description(
        url: str,
    ) -> str:

        try:
            validate_external_url(url)

            headers = {
                "User-Agent": (
                    "AI-Job-Hunter/1.0 "
                    "(job-description-fetcher)"
                )
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=(5, 10),
                allow_redirects=False,
            )

            if response.status_code != 200:
                return ""

            content_type = (
                response.headers.get(
                    "Content-Type",
                    "",
                ).lower()
            )

            if (
                "text/html" not in content_type
                and "application/xhtml+xml"
                not in content_type
            ):
                return ""

            # Prevent unnecessarily large HTTP responses.
            content_length = response.headers.get(
                "Content-Length"
            )

            if content_length:
                try:
                    if int(content_length) > 2 * 1024 * 1024:
                        return ""
                except ValueError:
                    pass

            soup = BeautifulSoup(
                response.text,
                "lxml",
            )

            text = soup.get_text(
                " ",
                strip=True,
            )

            return text[:200000]

        except (
            ValueError,
            requests.RequestException,
        ):
            return ""