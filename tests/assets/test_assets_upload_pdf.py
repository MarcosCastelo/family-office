import io
import pytest
from unittest.mock import patch

def make_pdf_content():
    # Simula um PDF binário simples
    return b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n'

@pytest.fixture
def pdf_file():
    return io.BytesIO(make_pdf_content())

@patch('app.services.gemini_ocr_service.extract_assets_from_pdf')
def test_upload_pdf_success(mock_gemini, client, headers, family, pdf_file):
    mock_gemini.return_value = [
        {
            "name": "Tesouro Selic",
            "asset_type": "renda_fixa",
            "value": 10000.0,
            "acquisition_date": "2024-01-01",
            "details": {"indexador": "SELIC"},
            "family_id": family.id
        },
        {
            "name": "Ação XPTO",
            "asset_type": "renda_variavel",
            "value": 5000.0,
            "acquisition_date": "2023-12-01",
            "details": {"ticker": "XPTO3"},
            "family_id": family.id
        }
    ]
    data = {'file': (pdf_file, 'ativos.pdf')}
    response = client.post(f'/assets/upload-pdf?family_id={family.id}', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 201
    assert isinstance(response.json, list)
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Tesouro Selic"
    assert response.json[1]["asset_type"] == "renda_variavel"

@patch('app.services.gemini_ocr_service.extract_assets_from_pdf')
def test_upload_pdf_invalid_format(mock_gemini, client, headers, family):
    data = {'file': (io.BytesIO(b'not a pdf'), 'ativos.txt')}
    response = client.post(f'/assets/upload-pdf?family_id={family.id}', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400

@patch('app.services.gemini_ocr_service.extract_assets_from_pdf')
def test_upload_pdf_gemini_error(mock_gemini, client, headers, family, pdf_file):
    mock_gemini.side_effect = Exception('Erro Gemini')
    data = {'file': (pdf_file, 'ativos.pdf')}
    response = client.post(f'/assets/upload-pdf?family_id={family.id}', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 502

@patch('app.services.gemini_ocr_service.extract_assets_from_pdf')
def test_upload_pdf_invalid_json(mock_gemini, client, headers, family, pdf_file):
    mock_gemini.return_value = "not a list"
    data = {'file': (pdf_file, 'ativos.pdf')}
    response = client.post(f'/assets/upload-pdf?family_id={family.id}', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400

@patch('app.services.gemini_ocr_service.extract_assets_from_pdf')
def test_upload_pdf_unauthenticated(mock_gemini, client, pdf_file):
    data = {'file': (pdf_file, 'ativos.pdf')}
    response = client.post('/assets/upload-pdf?family_id=1', content_type='multipart/form-data', data=data)
    assert response.status_code == 401

@patch('app.services.gemini_ocr_service.extract_assets_from_pdf')
def test_upload_pdf_missing_family_overrides_correctly(mock_gemini, client, headers, family, pdf_file):
    """Test that controller correctly overrides family_id even when Gemini doesn't provide it"""
    mock_gemini.return_value = [{
        "name": "Tesouro Selic",
        "asset_type": "renda_fixa",
        "value": 10000.0,
        "acquisition_date": "2024-01-01",
        "details": {"indexador": "SELIC"}
        # family_id ausente - controller deve sobrescrever
    }]
    data = {'file': (pdf_file, 'ativos.pdf')}
    response = client.post(f'/assets/upload-pdf?family_id={family.id}', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 201
    assert len(response.json) == 1
    assert response.json[0]["family_id"] == family.id 