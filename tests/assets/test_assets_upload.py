import io
import json
import pytest

def make_csv_content(family_id):
    return (
        "name,asset_type,value,acquisition_date,details,family_id\n"
        f"Tesouro Selic,renda_fixa,10000.0,2024-01-01,{json.dumps({'indexador': 'SELIC'})},{family_id}\n"
        f"Ação XPTO,renda_variavel,5000.0,2023-12-01,{json.dumps({'ticker': 'XPTO3'})},{family_id}\n"
    )

def test_upload_csv_success(client, headers, family):
    data = {
        'file': (io.BytesIO(make_csv_content(family.id).encode()), 'ativos.csv')
    }
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 201
    assert isinstance(response.json, list)
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Tesouro Selic"
    assert response.json[1]["asset_type"] == "renda_variavel"

def test_upload_csv_invalid_format(client, headers, family):
    data = {
        'file': (io.BytesIO(b"nome,valor\nfoo,bar\n"), 'ativos.csv')
    }
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400

def test_upload_csv_unauthenticated(client, family):
    data = {
        'file': (io.BytesIO(make_csv_content(family.id).encode()), 'ativos.csv')
    }
    response = client.post('/assets/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 401

def test_upload_csv_missing_family(client, headers):
    # family_id ausente
    csv = (
        "name,asset_type,value,acquisition_date,details\n"
        "Tesouro Selic,renda_fixa,10000.0,2024-01-01,\"{\"indexador\": \"SELIC\"}\"\n"
    )
    data = {
        'file': (io.BytesIO(csv.encode()), 'ativos.csv')
    }
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400 

def make_xlsx_content(family_id):
    import openpyxl
    from tempfile import NamedTemporaryFile
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["name", "asset_type", "value", "acquisition_date", "details", "family_id"])
    ws.append(["Tesouro Selic", "renda_fixa", 10000.0, "2024-01-01", '{"indexador": "SELIC"}', family_id])
    ws.append(["Ação XPTO", "renda_variavel", 5000.0, "2023-12-01", '{"ticker": "XPTO3"}', family_id])
    with NamedTemporaryFile(suffix=".xlsx") as tmp:
        wb.save(tmp.name)
        tmp.seek(0)
        return tmp.read()

def test_upload_xlsx_success(client, headers, family):
    data = {
        'file': (io.BytesIO(make_xlsx_content(family.id)), 'ativos.xlsx')
    }
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 201
    assert isinstance(response.json, list)
    assert len(response.json) == 2
    assert response.json[0]["name"] == "Tesouro Selic"
    assert response.json[1]["asset_type"] == "renda_variavel"

def test_upload_xlsx_invalid_format(client, headers, family):
    data = {
        'file': (io.BytesIO(b"not an excel file"), 'ativos.xlsx')
    }
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400

def test_upload_xlsx_unauthenticated(client, family):
    data = {
        'file': (io.BytesIO(make_xlsx_content(family.id)), 'ativos.xlsx')
    }
    response = client.post('/assets/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 401 

def test_upload_csv_real_file(client, headers):
    with open('ativos_exemplo.csv', 'rb') as f:
        data = {'file': (f, 'ativos_exemplo.csv')}
        response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
        assert response.status_code == 201
        assert isinstance(response.json, list)
        assert len(response.json) == 3
        assert response.json[0]["name"] == "Tesouro Selic"
        assert response.json[1]["asset_type"] == "renda_variavel"

def test_upload_xlsx_real_file(client, headers):
    with open('ativos_exemplo.xlsx', 'rb') as f:
        data = {'file': (f, 'ativos_exemplo.xlsx')}
        response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
        assert response.status_code == 201
        assert isinstance(response.json, list)
        assert len(response.json) == 3
        assert response.json[0]["name"] == "Tesouro Selic"
        assert response.json[1]["asset_type"] == "renda_variavel" 

def test_upload_csv_invalid_line_rejects_all(client, headers, family):
    import io
    csv = (
        "name,asset_type,value,acquisition_date,details,family_id\n"
        f"Ativo1,renda_fixa,10000.0,2024-01-01,{{\"indexador\": \"IPCA\", \"vencimento\": \"2030-01-01\"}},{family.id}\n"
        f"Ativo2,renda_fixa,-5000.0,2024-01-01,{{\"indexador\": \"IPCA\", \"vencimento\": \"2030-01-01\"}},{family.id}\n"  # valor negativo
    )
    data = {'file': (io.BytesIO(csv.encode()), 'ativos.csv')}
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400

def test_upload_csv_duplicate_rejects(client, headers, family):
    import io
    csv = (
        "name,asset_type,value,acquisition_date,details,family_id\n"
        f"Ativo1,renda_fixa,10000.0,2024-01-01,{{\"indexador\": \"IPCA\", \"vencimento\": \"2030-01-01\"}},{family.id}\n"
        f"Ativo1,renda_fixa,20000.0,2024-01-01,{{\"indexador\": \"IPCA\", \"vencimento\": \"2030-01-01\"}},{family.id}\n"
    )
    data = {'file': (io.BytesIO(csv.encode()), 'ativos.csv')}
    response = client.post('/assets/upload', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400

def test_upload_csv_no_permission(client, family):
    import io
    csv = (
        "name,asset_type,value,acquisition_date,details,family_id\n"
        f"Ativo1,renda_fixa,10000.0,2024-01-01,{{\"indexador\": \"IPCA\", \"vencimento\": \"2030-01-01\"}},{family.id}\n"
    )
    data = {'file': (io.BytesIO(csv.encode()), 'ativos.csv')}
    response = client.post('/assets/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 401

def test_upload_pdf_invalid_json(client, headers, family, monkeypatch):
    import io
    # Mocka o serviço Gemini para retornar JSON inválido
    def fake_extract_assets_from_pdf(file):
        return "not a list"
    monkeypatch.setattr("app.services.gemini_ocr_service.extract_assets_from_pdf", fake_extract_assets_from_pdf)
    pdf = b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n'
    data = {'file': (io.BytesIO(pdf), 'ativos.pdf')}
    response = client.post('/assets/upload-pdf', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code == 400

def test_upload_pdf_no_permission(client, family):
    import io
    pdf = b'%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n'
    data = {'file': (io.BytesIO(pdf), 'ativos.pdf')}
    response = client.post('/assets/upload-pdf', content_type='multipart/form-data', data=data)
    assert response.status_code == 401 