"""Enum de assets"""
from enum import Enum

class AssetType(str, Enum):
    RENDA_FIXA = "renda_fixa"
    RENDA_VARIAVEL = "renda_variavel"
    MULTIMERCADO = "multimercado"
    ATIVO_REAL = "ativo_real"
    ESTRATEGICO = "estrategico"
    INTERNACIONAL = "internacional"
    ALTERNATIVO = "alternativo"
    PROTECAO = "protecao"

ASSET_TYPE_CHOICES = [e.value for e in AssetType]