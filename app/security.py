import ipaddress
import secrets
import socket
from urllib.parse import urlparse

from fastapi import Header, HTTPException, status

from app.config import (
    ALLOWED_EXTERNAL_HOSTS,
    API_KEY,
    ENVIRONMENT,
)


def require_api_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> None:
    """
    Require API-key authentication in production.

    Development remains unauthenticated so the existing local
    workflow continues to work.
    """

    if ENVIRONMENT != "production":
        return

    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API authentication is not configured",
        )

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    if not secrets.compare_digest(
        x_api_key,
        API_KEY,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


def validate_external_url(
    url: str,
    allowed_hosts: set[str] | None = None,
) -> str:
    """
    Validate an external URL before the server makes a request.

    Protects against SSRF by enforcing:
    - HTTPS
    - hostname presence
    - no embedded credentials
    - allowlisted domains
    - no private/loopback/link-local/reserved IPs
    """

    allowed_hosts = (
        allowed_hosts
        if allowed_hosts is not None
        else ALLOWED_EXTERNAL_HOSTS
    )

    parsed = urlparse(url)

    if parsed.scheme.lower() != "https":
        raise ValueError(
            "Only HTTPS URLs are allowed"
        )

    if not parsed.hostname:
        raise ValueError(
            "URL must contain a hostname"
        )

    if parsed.username or parsed.password:
        raise ValueError(
            "URLs containing credentials are not allowed"
        )

    hostname = parsed.hostname.lower().rstrip(".")

    if not any(
        hostname == allowed
        or hostname.endswith("." + allowed)
        for allowed in allowed_hosts
    ):
        raise ValueError(
            "External host is not allowlisted"
        )

    try:
        addresses = {
            result[4][0]
            for result in socket.getaddrinfo(
                hostname,
                443,
                type=socket.SOCK_STREAM,
            )
        }
    except socket.gaierror as exc:
        raise ValueError(
            "External host could not be resolved"
        ) from exc

    for address in addresses:
        ip = ipaddress.ip_address(address)

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_unspecified
            or ip.is_multicast
        ):
            raise ValueError(
                "External host resolves to a restricted address"
            )

    return url


def validate_pdf_signature(file_header: bytes) -> bool:
    """
    Verify that an uploaded file starts with the PDF magic bytes.
    """

    return file_header.startswith(b"%PDF-")


def safe_filename() -> str:
    """
    Generate a random filename.

    Never use the user's original filename as a filesystem path.
    """

    return f"{secrets.token_hex(16)}.pdf"