"""PDF object representing a PDF document from the API."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict

from generatepdfs.exceptions import InvalidArgumentException, RuntimeException

if TYPE_CHECKING:
    from generatepdfs.generate_pdfs import GeneratePDFs


class Pdf:
    """PDF object representing a PDF document from the API."""

    def __init__(
        self,
        pdf_id: int,
        name: str,
        status: str,
        download_url: str,
        created_at: datetime,
        client: 'GeneratePDFs',
    ) -> None:
        """Initialize a new Pdf instance.

        Args:
            pdf_id: PDF ID
            name: PDF name
            status: PDF status
            download_url: Download URL
            created_at: Creation date
            client: The GeneratePDFs client instance
        """
        self._id = pdf_id
        self._name = name
        self._status = status
        self._download_url = download_url
        self._created_at = created_at
        self._client = client

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client: 'GeneratePDFs') -> 'Pdf':
        """Create a Pdf instance from API response data.

        Args:
            data: API response data with keys: id, name, status, download_url, created_at
            client: The GeneratePDFs client instance

        Returns:
            A new Pdf instance

        Raises:
            InvalidArgumentException: If data structure is invalid
        """
        required_keys = {'id', 'name', 'status', 'download_url', 'created_at'}
        if not required_keys.issubset(data.keys()):
            raise InvalidArgumentException('Invalid PDF data structure')

        # Parse the created_at date
        try:
            created_at_str = str(data['created_at'])
            # Try parsing with different formats
            for fmt in [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%dT%H:%M:%S.%f%z',
                '%Y-%m-%dT%H:%M:%S%z',
            ]:
                try:
                    created_at = datetime.strptime(created_at_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                # Fallback to ISO format parser
                created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        except (ValueError, KeyError) as e:
            raise InvalidArgumentException(f'Invalid created_at format: {data.get("created_at")}') from e

        return cls(
            int(data['id']),
            str(data['name']),
            str(data['status']),
            str(data['download_url']),
            created_at,
            client,
        )

    def get_id(self) -> int:
        """Get the PDF ID.

        Returns:
            PDF ID
        """
        return self._id

    def get_name(self) -> str:
        """Get the PDF name.

        Returns:
            PDF name
        """
        return self._name

    def get_status(self) -> str:
        """Get the PDF status.

        Returns:
            PDF status
        """
        return self._status

    def get_download_url(self) -> str:
        """Get the download URL.

        Returns:
            Download URL
        """
        return self._download_url

    def get_created_at(self) -> datetime:
        """Get the creation date.

        Returns:
            Creation date
        """
        return self._created_at

    def is_ready(self) -> bool:
        """Check if the PDF is ready for download.

        Returns:
            True if PDF is ready
        """
        return self._status == 'completed'

    def download(self) -> bytes:
        """Download the PDF content.

        Returns:
            PDF binary content as bytes

        Raises:
            RuntimeException: If the PDF is not ready or download fails
        """
        if not self.is_ready():
            raise RuntimeException(f'PDF is not ready yet. Current status: {self._status}')

        return self._client.download_pdf(self._download_url)

    def download_to_file(self, file_path: str) -> bool:
        """Download the PDF and save it to a file.

        Args:
            file_path: Path where to save the PDF file

        Returns:
            True on success

        Raises:
            RuntimeException: If the PDF is not ready or download fails
        """
        content = self.download()

        try:
            with open(file_path, 'wb') as f:
                f.write(content)
            return True
        except OSError as e:
            raise RuntimeException(f'Failed to write PDF to file: {file_path}') from e

    def refresh(self) -> 'Pdf':
        """Refresh the PDF data from the API.

        Returns:
            A new Pdf instance with updated data
        """
        return self._client.get_pdf(self._id)
