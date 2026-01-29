import json
from base64 import b64encode
from dataclasses import (
    asdict,
    dataclass,
)
from functools import cached_property
from hashlib import sha256
from io import BytesIO
from typing import Any

import requests.adapters

from .config import get_config


def json_bytes(obj: object) -> bytes:
    """
    Convert a Python object to a compact JSON-encoded byte string.

    Parameters
    ----------
    obj : object
        The Python object to encode.

    Returns
    -------
    bytes
        The JSON-encoded byte string.
    """
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()


def b64_sha256(string: bytes) -> str:
    """
    Compute the Base64-encoded SHA-256 hash of a byte string.

    Parameters
    ----------
    string : bytes
        The input byte string.

    Returns
    -------
    str
        The Base64-encoded SHA-256 hash.
    """
    return b64encode(sha256(string).digest()).decode()


@dataclass(frozen=True)
class Payload:
    """
    A workflow payload containing a list of circuits.

    This class provides methods for serialisation, checksum calculation,
    and uploading with automatic retry logic and checksum validation.

    Attributes
    ----------
    circuits : list[str]
        A list of circuits.
    """

    circuits: list[str]

    def __len__(self) -> int:
        """
        Get the length of the payload body in bytes.

        Returns
        -------
        int
            The length of the payload body.
        """
        return len(self.body)

    @cached_property
    def body(self) -> bytes:
        """
        Serialise the payload to a JSON-encoded byte string.

        Returns
        -------
        bytes
            The JSON-encoded byte string representation of the payload.
        """
        return json_bytes(asdict(self))

    @cached_property
    def checksum(self) -> str:
        """
        Compute the Base64-encoded SHA-256 checksum of the payload body.

        Returns
        -------
        str
            The Base64-encoded SHA-256 checksum.
        """
        return b64_sha256(self.body)

    def upload(self, url: str, *, timeout: float = 120) -> requests.Response:
        """
        Upload the payload to a pre-signed PUT URL with checksum validation.

        Uses automatic retry logic for server errors and includes SHA-256
        checksum validation via AWS headers.

        Parameters
        ----------
        url : str
            The pre-signed PUT URL.
        timeout : float, optional
            The timeout for the upload request in seconds. Defaults to 120.

        Returns
        -------
        requests.Response
            The HTTP response from the upload request.

        Raises
        ------
        requests.exceptions.RequestException
            If the upload request fails after retries.
        """
        with requests.Session() as session:
            retries = requests.adapters.Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=(500, 502, 503, 504),
                allowed_methods=frozenset(["PUT"]),
            )
            for prefix in "https://", "http://":
                session.mount(
                    prefix, requests.adapters.HTTPAdapter(max_retries=retries)
                )

            response = session.put(
                url,
                data=BytesIO(self.body),
                headers={
                    "Content-Type": "application/json",
                    "Content-Length": str(len(self)),
                    "x-amz-checksum-sha256": self.checksum,
                },
                timeout=timeout,
            )
            response.raise_for_status()

        return response


def upload_payload(payload: Payload, registry: str) -> str:
    """
    Upload a payload to a persistent storage backend and return an ID referencing the
    storage location.

    Parameters
    ----------
    payload : Payload
        A payload.
    registry : str
        The registry name.

    Returns
    -------
    str
        The ID of the storage location.
    """
    presigned_url_data = (
        get_config()
        .get_router()
        .create_presigned_url_upload(payload.checksum, registry)
    )
    payload.upload(url=presigned_url_data["url"])
    return presigned_url_data["id"]


def download_result(results_url: str) -> dict[str, Any]:
    """
    Download and parse JSON results from a URL.

    Downloads data from the specified URL in chunks and parses it as JSON.
    Uses streaming to handle large files efficiently.

    Parameters
    ----------
    results_url : str
        The URL to download results from.

    Returns
    -------
    dict[str, Any]
        The parsed JSON data as a dictionary.

    Raises
    ------
    requests.exceptions.RequestException
        If the HTTP request fails.
    json.JSONDecodeError
        If the downloaded content is not valid JSON.
    """
    chunks: list[bytes] = []

    with requests.get(
        results_url,
        timeout=600,
        stream=True,
    ) as response:
        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=1_048_576):
            if chunk:  # skip keep-alive chunks
                chunks.append(chunk)

    return json.loads(b"".join(chunks))
