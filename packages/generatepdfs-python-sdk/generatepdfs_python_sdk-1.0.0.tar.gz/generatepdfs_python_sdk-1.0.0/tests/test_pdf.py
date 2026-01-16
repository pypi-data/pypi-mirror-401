"""Tests for the Pdf class."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from generatepdfs import GeneratePDFs, InvalidArgumentException, Pdf, RuntimeException


class TestPdf:
    """Test cases for Pdf class."""

    @pytest.fixture
    def client(self):
        """Fixture providing a GeneratePDFs client instance."""
        return GeneratePDFs.connect('test-api-token')

    def test_from_dict_creates_pdf_instance_from_valid_data(self, client):
        """Test that from_dict creates Pdf instance from valid data."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'completed',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf = Pdf.from_dict(data, client)

        assert isinstance(pdf, Pdf)
        assert pdf.get_id() == 123
        assert pdf.get_name() == 'test.pdf'
        assert pdf.get_status() == 'completed'
        assert pdf.get_download_url() == 'https://api.generatepdfs.com/pdfs/123/download/token'

    def test_from_dict_throws_when_required_fields_missing(self, client):
        """Test that from_dict throws when required fields are missing."""
        data = {
            'id': 123,
            # Missing other required fields
        }

        with pytest.raises(InvalidArgumentException) as exc_info:
            Pdf.from_dict(data, client)
        assert 'Invalid PDF data structure' in str(exc_info.value)

    def test_from_dict_throws_when_created_at_format_invalid(self, client):
        """Test that from_dict throws when created_at format is invalid."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'completed',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': 'invalid-date-format',
        }

        with pytest.raises(InvalidArgumentException) as exc_info:
            Pdf.from_dict(data, client)
        assert 'Invalid created_at format' in str(exc_info.value)

    def test_getters_return_correct_values(self, client):
        """Test that getters return correct values."""
        data = {
            'id': 456,
            'name': 'document.pdf',
            'status': 'pending',
            'download_url': 'https://api.generatepdfs.com/pdfs/456/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf = Pdf.from_dict(data, client)

        assert pdf.get_id() == 456
        assert pdf.get_name() == 'document.pdf'
        assert pdf.get_status() == 'pending'
        assert pdf.get_download_url() == 'https://api.generatepdfs.com/pdfs/456/download/token'
        assert pdf.get_created_at() is not None

    def test_is_ready_returns_true_when_status_completed(self, client):
        """Test that is_ready returns true when status is completed."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'completed',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf = Pdf.from_dict(data, client)

        assert pdf.is_ready() is True

    def test_is_ready_returns_false_when_status_not_completed(self, client):
        """Test that is_ready returns false when status is not completed."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'pending',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf = Pdf.from_dict(data, client)

        assert pdf.is_ready() is False

    def test_download_throws_when_pdf_not_ready(self, client):
        """Test that download throws when PDF is not ready."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'pending',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf = Pdf.from_dict(data, client)

        with pytest.raises(RuntimeException) as exc_info:
            pdf.download()
        assert 'PDF is not ready yet' in str(exc_info.value)

    def test_download_successfully_downloads_pdf_content(self, client):
        """Test that download successfully downloads PDF content."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'completed',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf_content = b'%PDF-1.4 fake pdf content'

        with patch.object(client, 'download_pdf') as mock_download:
            mock_download.return_value = pdf_content

            pdf = Pdf.from_dict(data, client)
            content = pdf.download()

            assert content == pdf_content
            mock_download.assert_called_once_with(data['download_url'])

    def test_download_to_file_successfully_saves_pdf(self, client):
        """Test that download_to_file successfully saves PDF to file."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'completed',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf_content = b'%PDF-1.4 fake pdf content'
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file_path = temp_file.name
        temp_file.close()

        try:
            with patch.object(client, 'download_pdf') as mock_download:
                mock_download.return_value = pdf_content

                pdf = Pdf.from_dict(data, client)
                result = pdf.download_to_file(temp_file_path)

                assert result is True
                assert Path(temp_file_path).exists()
                assert Path(temp_file_path).read_bytes() == pdf_content
        finally:
            if Path(temp_file_path).exists():
                Path(temp_file_path).unlink()

    def test_download_to_file_throws_when_file_write_fails(self, client):
        """Test that download_to_file throws when file write fails."""
        data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'completed',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf_content = b'%PDF-1.4 fake pdf content'

        with patch.object(client, 'download_pdf') as mock_download:
            mock_download.return_value = pdf_content

            pdf = Pdf.from_dict(data, client)

            # Try to write to a directory (should fail)
            with pytest.raises(RuntimeException) as exc_info:
                pdf.download_to_file('/non/existent/directory/file.pdf')
            assert 'Failed to write PDF to file' in str(exc_info.value)

    def test_from_dict_handles_different_status_values(self, client):
        """Test that from_dict handles different status values."""
        statuses = ['pending', 'processing', 'completed', 'failed']

        for status in statuses:
            data = {
                'id': 123,
                'name': 'test.pdf',
                'status': status,
                'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
                'created_at': '2024-01-01T12:00:00.000000Z',
            }

            pdf = Pdf.from_dict(data, client)

            assert pdf.get_status() == status
            assert pdf.is_ready() == (status == 'completed')

    def test_refresh_successfully_updates_pdf_data(self, client):
        """Test that refresh successfully updates PDF data."""
        initial_data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'pending',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        pdf = Pdf.from_dict(initial_data, client)

        # Verify initial state
        assert pdf.get_status() == 'pending'

        refreshed_data = {
            'id': 123,
            'name': 'test.pdf',
            'status': 'completed',
            'download_url': 'https://api.generatepdfs.com/pdfs/123/download/new-token',
            'created_at': '2024-01-01T12:00:00.000000Z',
        }

        with patch.object(client, 'get_pdf') as mock_get_pdf:
            refreshed_pdf = Pdf.from_dict(refreshed_data, client)
            mock_get_pdf.return_value = refreshed_pdf

            # Refresh the PDF
            result = pdf.refresh()

            # Verify refreshed state
            assert isinstance(result, Pdf)
            assert result.get_id() == 123
            assert result.get_status() == 'completed'
            assert result.get_download_url() == 'https://api.generatepdfs.com/pdfs/123/download/new-token'
            mock_get_pdf.assert_called_once_with(123)
