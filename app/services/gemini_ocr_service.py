import requests
import base64
import json
import os
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

PROMPT = (
    "Extraia do PDF os dados de ativos financeiros e devolva EXCLUSIVAMENTE uma lista JSON, onde cada item contém TODOS os campos obrigatórios: "
    "name (string - nome do ativo), "
    "asset_type (string - um dos: renda_fixa, renda_variavel, multimercado, ativo_real, estrategico, internacional, alternativo, protecao), "
    "value (float - valor em reais), "
    "acquisition_date (string no formato YYYY-MM-DD - data de aquisição), "
    "details (objeto JSON com informações específicas do ativo), "
    "family_id (int - ID da família, use 1 como padrão). "
    "IMPORTANTE: Todos os campos são obrigatórios. Se não conseguir identificar algum campo, use valores padrão: "
    "- acquisition_date: use a data atual se não encontrar "
    "- family_id: sempre use 1 "
    "- details: use {} se não houver detalhes específicos "
    "Não inclua nenhum texto, explicação, comentário, markdown ou campo extra além do JSON. "
    "A resposta deve ser apenas o JSON, sem texto antes ou depois."
)

REQUIRED_FIELDS = {"name", "asset_type", "value", "acquisition_date", "details", "family_id"}


def clean_json_response(text):
    """Limpa a resposta da Gemini removendo markdown e texto extra"""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Remove espaços em branco no início e fim
    text = text.strip()
    
    # Se a resposta está vazia ou contém apenas "[]", retorna lista vazia
    if not text or text == "[]":
        return "[]"
    
    return text


def extract_assets_from_pdf(file):
    if not GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY não configurada no ambiente.")

    # Lê o PDF e codifica em base64
    file.seek(0)
    pdf_bytes = file.read()
    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

    # Monta o payload para a API Gemini
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT},
                    {
                        "inlineData": {
                            "mimeType": "application/pdf",
                            "data": pdf_b64
                        }
                    }
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro de conexão com a API Gemini: {str(e)}")

    if response.status_code != 200:
        error_msg = f"Erro na API Gemini: {response.status_code}"
        try:
            error_data = response.json()
            if 'error' in error_data:
                error_msg += f" - {error_data['error'].get('message', 'Erro desconhecido')}"
        except:
            error_msg += f" - {response.text[:200]}"
        raise Exception(error_msg)

    # Verifica se a resposta está vazia
    if not response.text.strip():
        raise Exception("Resposta vazia da API Gemini")

    # A resposta da Gemini vem em response.json()["candidates"][0]["content"]["parts"][0]["text"]
    try:
        gemini_json = response.json()
        
        # Verifica se a estrutura da resposta está correta
        if "candidates" not in gemini_json or not gemini_json["candidates"]:
            raise Exception("Estrutura de resposta da Gemini inválida: 'candidates' não encontrado")
        
        candidate = gemini_json["candidates"][0]
        if "content" not in candidate or "parts" not in candidate["content"]:
            raise Exception("Estrutura de resposta da Gemini inválida: 'content' ou 'parts' não encontrado")
        
        parts = candidate["content"]["parts"]
        if not parts or "text" not in parts[0]:
            raise Exception("Estrutura de resposta da Gemini inválida: 'text' não encontrado")
        
        text = parts[0]["text"]
        
        # Verifica se o texto está vazio
        if not text.strip():
            raise Exception("Texto vazio retornado pela Gemini")
        
        # Limpa a resposta removendo markdown e texto extra
        cleaned_text = clean_json_response(text)
        
        # Tenta converter o texto limpo em JSON
        assets = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise Exception(f"Erro ao processar resposta da Gemini: JSON inválido - {str(e)}")
    except KeyError as e:
        raise Exception(f"Erro ao processar resposta da Gemini: Campo não encontrado - {str(e)}")
    except Exception as e:
        raise Exception(f"Erro ao processar resposta da Gemini: {str(e)}")

    # Validação rigorosa da estrutura
    if not isinstance(assets, list):
        raise Exception("A resposta da Gemini não é uma lista.")
    
    for i, asset in enumerate(assets):
        if not isinstance(asset, dict):
            raise Exception(f"Item {i} deve ser um dicionário.")
        
        missing = REQUIRED_FIELDS - set(asset.keys())
        if missing:
            raise Exception(f"Campos obrigatórios ausentes no item {i}: {missing}")
        
        # Validação adicional de tipos
        if not isinstance(asset.get('name'), str):
            raise Exception(f"Campo 'name' deve ser string no item {i}")
        if not isinstance(asset.get('asset_type'), str):
            raise Exception(f"Campo 'asset_type' deve ser string no item {i}")
        if not isinstance(asset.get('value'), (int, float)):
            raise Exception(f"Campo 'value' deve ser número no item {i}")
        if not isinstance(asset.get('acquisition_date'), str):
            raise Exception(f"Campo 'acquisition_date' deve ser string no item {i}")
        if not isinstance(asset.get('details'), dict):
            raise Exception(f"Campo 'details' deve ser objeto no item {i}")
        if not isinstance(asset.get('family_id'), int):
            raise Exception(f"Campo 'family_id' deve ser inteiro no item {i}")
    
    return assets 