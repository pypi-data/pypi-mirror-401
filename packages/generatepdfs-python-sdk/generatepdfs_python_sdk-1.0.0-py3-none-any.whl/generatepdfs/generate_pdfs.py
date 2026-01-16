"""Main client class for interacting with the GeneratePDFs API."""

import base64
import mimetypes
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests

from generatepdfs.exceptions import InvalidArgumentException
from generatepdfs.pdf import Pdf


class GeneratePDFs:
    """Client for interacting with the GeneratePDFs API."""

    BASE_URL = 'https://api.generatepdfs.com'

    def __init__(self, api_token: str) -> None:
        """Initialize a new GeneratePDFs client.

        Args:
            api_token: The API token for authentication
        """
        self._api_token = api_token
        self._base_url = self.BASE_URL
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {self._api_token}',
            'Content-Type': 'application/json',
        })

    @classmethod
    def connect(cls, api_token: str) -> 'GeneratePDFs':
        """Create a new GeneratePDFs instance with the provided API token.

        Args:
            api_token: The API token for authentication

        Returns:
            A new GeneratePDFs instance
        """
        return cls(api_token)

    def generate_from_html(
        self,
        html_path: str,
        css_path: Optional[str] = None,
        images: Optional[List[Dict[str, str]]] = None,
    ) -> Pdf:
        """Generate a PDF from HTML file(s) with optional CSS and images.

        Args:
            html_path: Path to the HTML file
            css_path: Optional path to the CSS file
            images: Optional list of image dictionaries with keys:
                - name: Image filename
                - path: Path to the image file
                - mime_type: Optional MIME type (will be auto-detected if not provided)

        Returns:
            Pdf object containing PDF information

        Raises:
            InvalidArgumentException: If files are invalid
            requests.RequestException: If the HTTP request fails
        """
        html_file = Path(html_path)
        if not html_file.exists() or not html_file.is_file():
            raise InvalidArgumentException(f'HTML file not found or not readable: {html_path}')

        html_content = html_file.read_bytes()
        html_base64 = base64.b64encode(html_content).decode('utf-8')

        data: Dict[str, Any] = {
            'html': html_base64,
        }

        if css_path is not None:
            css_file = Path(css_path)
            if not css_file.exists() or not css_file.is_file():
                raise InvalidArgumentException(f'CSS file not found or not readable: {css_path}')

            css_content = css_file.read_bytes()
            data['css'] = base64.b64encode(css_content).decode('utf-8')

        if images:
            data['images'] = self._process_images(images)

        response = self._make_request('/pdfs/generate', data)

        if 'data' not in response:
            raise InvalidArgumentException('Invalid API response: missing data')

        return Pdf.from_dict(response['data'], self)

    def generate_from_url(self, url: str) -> Pdf:
        """Generate a PDF from a URL.

        Args:
            url: The URL to convert to PDF

        Returns:
            Pdf object containing PDF information

        Raises:
            InvalidArgumentException: If URL is invalid
            requests.RequestException: If the HTTP request fails
        """
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError('Invalid URL')
        except Exception as e:
            raise InvalidArgumentException(f'Invalid URL: {url}') from e

        data = {
            'url': url,
        }

        response = self._make_request('/pdfs/generate', data)

        if 'data' not in response:
            raise InvalidArgumentException('Invalid API response: missing data')

        return Pdf.from_dict(response['data'], self)

    def get_pdf(self, pdf_id: int) -> Pdf:
        """Get a PDF by its ID.

        Args:
            pdf_id: The PDF ID

        Returns:
            Pdf object containing PDF information

        Raises:
            InvalidArgumentException: If ID is invalid
            requests.RequestException: If the HTTP request fails
        """
        if pdf_id <= 0:
            raise InvalidArgumentException(f'Invalid PDF ID: {pdf_id}')

        response = self._make_get_request(f'/pdfs/{pdf_id}')

        if 'data' not in response:
            raise InvalidArgumentException('Invalid API response: missing data')

        return Pdf.from_dict(response['data'], self)

    def download_pdf(self, download_url: str) -> bytes:
        """Download a PDF from the API.

        Args:
            download_url: The download URL for the PDF

        Returns:
            PDF binary content as bytes

        Raises:
            requests.RequestException: If the HTTP request fails
        """
        response = self._session.get(download_url)
        response.raise_for_status()
        return response.content

    def _process_images(self, images: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Process image files and return formatted list for API.

        Args:
            images: List of image dictionaries with keys: name, path, mime_type

        Returns:
            List of processed image dictionaries
        """
        processed = []

        for image in images:
            if 'path' not in image or 'name' not in image:
                continue

            path = Path(image['path'])
            name = image['name']

            if not path.exists() or not path.is_file():
                continue

            content = path.read_bytes()
            content_base64 = base64.b64encode(content).decode('utf-8')

            # Detect mime type if not provided
            mime_type = image.get('mime_type') or self._detect_mime_type(str(path))

            processed.append({
                'name': name,
                'content': content_base64,
                'mime_type': mime_type,
            })

        return processed

    def _detect_mime_type(self, file_path: str) -> str:
        """Detect MIME type of a file.

        Args:
            file_path: Path to the file

        Returns:
            MIME type string
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            return mime_type

        # Fallback to extension-based detection
        extension = Path(file_path).suffix.lower().lstrip('.')
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'svg': 'image/svg+xml',
        }

        return mime_types.get(extension, 'application/octet-stream')

    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make an HTTP POST request to the API.

        Args:
            endpoint: API endpoint
            data: Request data

        Returns:
            Decoded JSON response

        Raises:
            requests.RequestException: If the HTTP request fails
        """
        url = f'{self._base_url}{endpoint}'
        response = self._session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def _make_get_request(self, endpoint: str) -> Dict[str, Any]:
        """Make an HTTP GET request to the API.

        Args:
            endpoint: API endpoint

        Returns:
            Decoded JSON response

        Raises:
            requests.RequestException: If the HTTP request fails
        """
        url = f'{self._base_url}{endpoint}'
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()
