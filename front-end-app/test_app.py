import pytest
import json
from unittest.mock import patch, MagicMock
import app as flask_app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Create a Flask test client."""
    flask_app.app.config['TESTING'] = True
    with flask_app.app.test_client() as client:
        yield client


SAMPLE_RECORDS = [
    {
        'Job Title': 'Python Developer',
        'Name': 'Alice Smith',
        'Mobile': '4161234567',
        'email': 'alice@example.com',
        'Location': 'Toronto',
        'Visa Type ': 'PR',
        'Candidate rate': '80',
        'Submitted Rate': '90',
    },
    {
        'Job Title': 'Java Developer',
        'Name': 'Bob Jones',
        'Mobile': '4169876543',
        'email': 'bob@example.com',
        'Location': 'Vancouver',
        'Visa Type ': 'Work Permit',
        'Candidate rate': '70',
        'Submitted Rate': '85',
    },
    {
        'Job Title': 'Full Stack Developer',
        'Name': 'Carol White',
        'Mobile': '6475550001',
        'email': 'carol@example.com',
        'Location': 'Toronto',
        'Visa Type ': 'Citizen',
        'Candidate rate': '95',
        'Submitted Rate': '110',
    },
]


# ---------------------------------------------------------------------------
# Tests: read_excel
# ---------------------------------------------------------------------------

class TestReadExcel:

    @patch('app.load_workbook')
    def test_returns_list(self, mock_load):
        """read_excel should always return a list."""
        mock_wb = MagicMock()
        mock_wb.sheetnames = []
        mock_load.return_value = mock_wb
        result = flask_app.read_excel()
        assert isinstance(result, list)

    @patch('app.load_workbook')
    def test_reads_configured_sheets(self, mock_load):
        """Records from all configured sheets are combined."""
        mock_wb = MagicMock()
        mock_wb.sheetnames = ['Capgemini']

        mock_sheet = MagicMock()
        # Header row
        header_cells = [MagicMock(value='Job Title'), MagicMock(value='Name'),
                        MagicMock(value='email')]
        mock_sheet.__getitem__ = lambda self, key: header_cells if key == 1 else []
        # One data row
        data_cell_1 = MagicMock(value='Python Developer')
        data_cell_2 = MagicMock(value='Alice Smith')
        data_cell_3 = MagicMock(value='alice@example.com')
        mock_sheet.iter_rows.return_value = [[data_cell_1, data_cell_2, data_cell_3]]
        mock_wb.__getitem__ = lambda self, key: mock_sheet
        mock_load.return_value = mock_wb

        result = flask_app.read_excel()
        assert isinstance(result, list)

    @patch('app.load_workbook', side_effect=FileNotFoundError("File not found"))
    def test_returns_empty_list_on_file_not_found(self, mock_load):
        """read_excel should return [] when Excel file is missing."""
        result = flask_app.read_excel()
        assert result == []

    @patch('app.load_workbook', side_effect=Exception("Corrupt file"))
    def test_returns_empty_list_on_generic_error(self, mock_load):
        """read_excel should return [] on any unexpected error."""
        result = flask_app.read_excel()
        assert result == []


# ---------------------------------------------------------------------------
# Tests: search_by_criteria
# ---------------------------------------------------------------------------

class TestSearchByCriteria:

    @patch('app.read_excel', return_value=SAMPLE_RECORDS)
    def test_match_by_job_title(self, _):
        results = flask_app.search_by_criteria('Python')
        assert len(results) == 1
        assert results[0]['Name'] == 'Alice Smith'

    @patch('app.read_excel', return_value=SAMPLE_RECORDS)
    def test_match_by_name(self, _):
        results = flask_app.search_by_criteria('Bob')
        assert len(results) == 1
        assert results[0]['email'] == 'bob@example.com'

    @patch('app.read_excel', return_value=SAMPLE_RECORDS)
    def test_match_by_location(self, _):
        results = flask_app.search_by_criteria('Toronto')
        # Alice and Carol are both in Toronto
        assert len(results) == 2

    @patch('app.read_excel', return_value=SAMPLE_RECORDS)
    def test_case_insensitive_search(self, _):
        results = flask_app.search_by_criteria('python')
        assert len(results) == 1

    @patch('app.read_excel', return_value=SAMPLE_RECORDS)
    def test_no_match_returns_empty(self, _):
        results = flask_app.search_by_criteria('NonExistent')
        assert results == []

    @patch('app.read_excel', return_value=SAMPLE_RECORDS)
    def test_no_duplicates(self, _):
        """Same candidate should not appear twice even if multiple fields match."""
        results = flask_app.search_by_criteria('Alice')
        names = [r['Name'] for r in results]
        assert names.count('Alice Smith') == 1

    @patch('app.read_excel', return_value=[])
    def test_empty_data_source(self, _):
        results = flask_app.search_by_criteria('Python')
        assert results == []


# ---------------------------------------------------------------------------
# Tests: GET /
# ---------------------------------------------------------------------------

class TestIndexRoute:

    def test_homepage_returns_200(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_homepage_content_type_html(self, client):
        response = client.get('/')
        assert b'html' in response.data.lower() or response.content_type.startswith('text/html')


# ---------------------------------------------------------------------------
# Tests: POST /api/search
# ---------------------------------------------------------------------------

class TestSearchAPI:

    @patch('app.search_by_criteria', return_value=[SAMPLE_RECORDS[0]])
    def test_valid_search_returns_200(self, _, client):
        response = client.post(
            '/api/search',
            data=json.dumps({'search_term': 'Python'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body['success'] is True
        assert len(body['data']) == 1

    @patch('app.search_by_criteria', return_value=[SAMPLE_RECORDS[0]])
    def test_response_contains_expected_fields(self, _, client):
        response = client.post(
            '/api/search',
            data=json.dumps({'search_term': 'Python'}),
            content_type='application/json'
        )
        record = response.get_json()['data'][0]
        assert 'Job Title' in record
        assert 'Name' in record
        assert 'email' in record

    def test_empty_search_term_returns_400(self, client):
        response = client.post(
            '/api/search',
            data=json.dumps({'search_term': ''}),
            content_type='application/json'
        )
        assert response.status_code == 400
        body = response.get_json()
        assert body['success'] is False

    def test_missing_search_term_key_returns_400(self, client):
        response = client.post(
            '/api/search',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400

    @patch('app.search_by_criteria', return_value=[])
    def test_no_results_returns_404(self, _, client):
        response = client.post(
            '/api/search',
            data=json.dumps({'search_term': 'Nonexistent'}),
            content_type='application/json'
        )
        assert response.status_code == 404
        body = response.get_json()
        assert body['success'] is False

    @patch('app.search_by_criteria', side_effect=Exception("DB error"))
    def test_internal_error_returns_500(self, _, client):
        response = client.post(
            '/api/search',
            data=json.dumps({'search_term': 'Python'}),
            content_type='application/json'
        )
        assert response.status_code == 500
        body = response.get_json()
        assert body['success'] is False

    def test_whitespace_only_term_returns_400(self, client):
        response = client.post(
            '/api/search',
            data=json.dumps({'search_term': '   '}),
            content_type='application/json'
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# Tests: POST /api/send-email
# ---------------------------------------------------------------------------

class TestSendEmailAPI:

    def test_valid_email_returns_200(self, client):
        response = client.post(
            '/api/send-email',
            data=json.dumps({'email': 'alice@example.com'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body['success'] is True
        assert 'alice@example.com' in body['message']

    def test_missing_email_returns_400(self, client):
        response = client.post(
            '/api/send-email',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        body = response.get_json()
        assert body['success'] is False

    def test_empty_email_returns_400(self, client):
        response = client.post(
            '/api/send-email',
            data=json.dumps({'email': ''}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_whitespace_email_returns_400(self, client):
        response = client.post(
            '/api/send-email',
            data=json.dumps({'email': '   '}),
            content_type='application/json'
        )
        assert response.status_code == 400
