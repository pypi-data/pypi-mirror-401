"""Tests for the GeneratePDFs client class."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from generatepdfs import GeneratePDFs, InvalidArgumentException, Pdf


class TestGeneratePDFs:
    """Test cases for GeneratePDFs class."""

    @pytest.fixture
    def api_token(self):
        """Fixture providing a test API token."""
        return 'test-api-token'

    @pytest.fixture
    def client(self, api_token):
        """Fixture providing a GeneratePDFs client instance."""
        return GeneratePDFs.connect(api_token)

    def test_connect_creates_new_instance(self, api_token):
        """Test that connect creates a new GeneratePDFs instance."""
        client = GeneratePDFs.connect(api_token)
        assert isinstance(client, GeneratePDFs)

    def test_generate_from_html_throws_when_html_file_not_exists(self, client):
        """Test that generate_from_html throws when HTML file does not exist."""
        with pytest.raises(InvalidArgumentException) as exc_info:
            client.generate_from_html('/non/existent/file.html')
        assert 'HTML file not found or not readable' in str(exc_info.value)

    def test_generate_from_html_throws_when_css_file_not_exists(self, client):
        """Test that generate_from_html throws when CSS file does not exist."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            f.write('<html><body>Test</body></html>')

        try:
            with pytest.raises(InvalidArgumentException) as exc_info:
                client.generate_from_html(html_file, '/non/existent/file.css')
            assert 'CSS file not found or not readable' in str(exc_info.value)
        finally:
            Path(html_file).unlink()

    def test_generate_from_html_successfully_generates_pdf(self, client):
        """Test that generate_from_html successfully generates PDF from HTML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            f.write('<html><body>Test</body></html>')

        try:
            mock_response = {
                'data': {
                    'id': 123,
                    'name': 'test.pdf',
                    'status': 'pending',
                    'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
                    'created_at': '2024-01-01T12:00:00.000000Z',
                }
            }

            with patch.object(client._session, 'post') as mock_post:
                mock_response_obj = Mock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.raise_for_status = Mock()
                mock_post.return_value = mock_response_obj

                pdf = client.generate_from_html(html_file)

                assert isinstance(pdf, Pdf)
                assert pdf.get_id() == 123
                assert pdf.get_name() == 'test.pdf'
                assert pdf.get_status() == 'pending'

                # Verify the request was made correctly
                mock_post.assert_called_once()
                call_args = mock_post.call_args
                assert call_args[0][0] == 'https://api.generatepdfs.com/pdfs/generate'
                assert 'json' in call_args[1]
                assert 'html' in call_args[1]['json']
        finally:
            Path(html_file).unlink()

    def test_generate_from_html_includes_css_when_provided(self, client):
        """Test that generate_from_html includes CSS when provided."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as html_f:
            html_file = html_f.name
            html_f.write('<html><body>Test</body></html>')

        with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False) as css_f:
            css_file = css_f.name
            css_f.write('body { color: red; }')

        try:
            mock_response = {
                'data': {
                    'id': 123,
                    'name': 'test.pdf',
                    'status': 'pending',
                    'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
                    'created_at': '2024-01-01T12:00:00.000000Z',
                }
            }

            with patch.object(client._session, 'post') as mock_post:
                mock_response_obj = Mock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.raise_for_status = Mock()
                mock_post.return_value = mock_response_obj

                pdf = client.generate_from_html(html_file, css_file)

                assert isinstance(pdf, Pdf)

                # Verify CSS was included in the request
                call_args = mock_post.call_args
                assert 'css' in call_args[1]['json']
        finally:
            Path(html_file).unlink()
            Path(css_file).unlink()

    def test_generate_from_html_includes_images_when_provided(self, client):
        """Test that generate_from_html includes images when provided."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as html_f:
            html_file = html_f.name
            html_f.write('<html><body>Test</body></html>')

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.png', delete=False) as img_f:
            image_file = img_f.name
            img_f.write(b'fake-image-content')

        try:
            mock_response = {
                'data': {
                    'id': 123,
                    'name': 'test.pdf',
                    'status': 'pending',
                    'download_url': 'https://api.generatepdfs.com/pdfs/123/download/token',
                    'created_at': '2024-01-01T12:00:00.000000Z',
                }
            }

            with patch.object(client._session, 'post') as mock_post:
                mock_response_obj = Mock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.raise_for_status = Mock()
                mock_post.return_value = mock_response_obj

                pdf = client.generate_from_html(html_file, None, [
                    {
                        'name': 'test.png',
                        'path': image_file,
                    }
                ])

                assert isinstance(pdf, Pdf)

                # Verify images were included in the request
                call_args = mock_post.call_args
                assert 'images' in call_args[1]['json']
                assert isinstance(call_args[1]['json']['images'], list)
                assert len(call_args[1]['json']['images']) > 0
        finally:
            Path(html_file).unlink()
            Path(image_file).unlink()

    def test_generate_from_html_throws_when_api_response_invalid(self, client):
        """Test that generate_from_html throws when API response is invalid."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            f.write('<html><body>Test</body></html>')

        try:
            mock_response = {}  # Missing 'data' key

            with patch.object(client._session, 'post') as mock_post:
                mock_response_obj = Mock()
                mock_response_obj.json.return_value = mock_response
                mock_response_obj.raise_for_status = Mock()
                mock_post.return_value = mock_response_obj

                with pytest.raises(InvalidArgumentException) as exc_info:
                    client.generate_from_html(html_file)
                assert 'Invalid API response: missing data' in str(exc_info.value)
        finally:
            Path(html_file).unlink()

    def test_generate_from_url_throws_for_invalid_url(self, client):
        """Test that generate_from_url throws for invalid URL."""
        with pytest.raises(InvalidArgumentException) as exc_info:
            client.generate_from_url('not-a-valid-url')
        assert 'Invalid URL' in str(exc_info.value)

    def test_generate_from_url_successfully_generates_pdf(self, client):
        """Test that generate_from_url successfully generates PDF from URL."""
        mock_response = {
            'data': {
                'id': 456,
                'name': 'url-example.com-2024-01-01-12-00-00.pdf',
                'status': 'pending',
                'download_url': 'https://api.generatepdfs.com/pdfs/456/download/token',
                'created_at': '2024-01-01T12:00:00.000000Z',
            }
        }

        with patch.object(client._session, 'post') as mock_post:
            mock_response_obj = Mock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = Mock()
            mock_post.return_value = mock_response_obj

            pdf = client.generate_from_url('https://example.com')

            assert isinstance(pdf, Pdf)
            assert pdf.get_id() == 456
            assert pdf.get_name() == 'url-example.com-2024-01-01-12-00-00.pdf'

            # Verify the request was made correctly
            call_args = mock_post.call_args
            assert call_args[1]['json']['url'] == 'https://example.com'

    def test_get_pdf_throws_for_invalid_id(self, client):
        """Test that get_pdf throws for invalid ID."""
        with pytest.raises(InvalidArgumentException) as exc_info:
            client.get_pdf(0)
        assert 'Invalid PDF ID: 0' in str(exc_info.value)

        with pytest.raises(InvalidArgumentException) as exc_info:
            client.get_pdf(-1)
        assert 'Invalid PDF ID: -1' in str(exc_info.value)

    def test_get_pdf_successfully_retrieves_pdf(self, client):
        """Test that get_pdf successfully retrieves PDF by ID."""
        mock_response = {
            'data': {
                'id': 789,
                'name': 'retrieved.pdf',
                'status': 'completed',
                'download_url': 'https://api.generatepdfs.com/pdfs/789/download/token',
                'created_at': '2024-01-01T12:00:00.000000Z',
            }
        }

        with patch.object(client._session, 'get') as mock_get:
            mock_response_obj = Mock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = Mock()
            mock_get.return_value = mock_response_obj

            pdf = client.get_pdf(789)

            assert isinstance(pdf, Pdf)
            assert pdf.get_id() == 789
            assert pdf.get_name() == 'retrieved.pdf'
            assert pdf.get_status() == 'completed'

            # Verify the request was made correctly
            mock_get.assert_called_once_with('https://api.generatepdfs.com/pdfs/789')

    def test_get_pdf_throws_when_api_response_invalid(self, client):
        """Test that get_pdf throws when API response is invalid."""
        mock_response = {}  # Missing 'data' key

        with patch.object(client._session, 'get') as mock_get:
            mock_response_obj = Mock()
            mock_response_obj.json.return_value = mock_response
            mock_response_obj.raise_for_status = Mock()
            mock_get.return_value = mock_response_obj

            with pytest.raises(InvalidArgumentException) as exc_info:
                client.get_pdf(123)
            assert 'Invalid API response: missing data' in str(exc_info.value)

    def test_download_pdf_successfully_downloads_content(self, client):
        """Test that download_pdf successfully downloads PDF content."""
        download_url = 'https://api.generatepdfs.com/pdfs/123/download/token'
        pdf_content = b'%PDF-1.4 fake pdf content'

        with patch.object(client._session, 'get') as mock_get:
            mock_response_obj = Mock()
            mock_response_obj.content = pdf_content
            mock_response_obj.raise_for_status = Mock()
            mock_get.return_value = mock_response_obj

            content = client.download_pdf(download_url)

            assert content == pdf_content
            mock_get.assert_called_once_with(download_url)

    def test_generate_from_html_handles_http_errors(self, client):
        """Test that generate_from_html handles HTTP errors."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            html_file = f.name
            f.write('<html><body>Test</body></html>')

        try:
            with patch.object(client._session, 'post') as mock_post:
                mock_post.side_effect = requests.RequestException('Connection error')

                with pytest.raises(requests.RequestException):
                    client.generate_from_html(html_file)
        finally:
            Path(html_file).unlink()
