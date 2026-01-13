# -*- coding: utf-8 -*-
"""
Keywords para validação de documentos como contratos.
"""
from __future__ import annotations

from typing import Tuple
import unicodedata


# Keywords para identificar contratos
KEYWORDS_VALIDACAO = [
    # Tipos de contrato
    "contrato",
    "acordo",
    "termo",
    "instrumento",
    "aditivo",
    "distrato",
    
    # Partes do contrato
    "contratante",
    "contratada",
    "contratado",
    "prestador",
    "prestadora",
    "tomador",
    "tomadora",
    
    # Cláusulas típicas
    "cláusula",
    "clausula",
    "objeto",
    "vigência",
    "vigencia",
    "valor",
    "pagamento",
    "obrigações",
    "obrigacoes",
    "rescisão",
    "rescisao",
    "foro",
    
    # Identificação
    "cnpj",
    "inscrita",
    "inscrito",
    "neste ato representada",
    "neste ato representado",
    "doravante denominada",
    "doravante denominado",
    
    # Assinaturas
    "assinatura",
    "assinado",
    "firmado",
    "testemunha",
    "certificado digital",
    "icp-brasil",
]

# Keywords que indicam que NÃO é um contrato
KEYWORDS_EXCLUSAO = [
    "edital de licitação",
    "pregão eletrônico",
    "tomada de preços",
    "concorrência pública",
    "carta convite",
    "nota fiscal",
    "recibo",
    "boleto",
    "fatura",
]

# Mínimo de keywords para considerar válido
MIN_KEYWORDS = 3


def normalizar_texto(texto: str) -> str:
    """Normaliza texto removendo acentos e convertendo para minúsculas."""
    if not texto:
        return ""
    texto_norm = unicodedata.normalize('NFD', texto)
    texto_sem_acentos = ''.join(c for c in texto_norm if unicodedata.category(c) != 'Mn')
    return texto_sem_acentos.lower()


def validar_documento_contrato(texto: str) -> Tuple[bool, int, list]:
    """
    Valida se um documento é um contrato com base nas keywords.
    
    Args:
        texto: Texto do documento
        
    Returns:
        Tuple com:
        - bool: Se é um contrato válido
        - int: Quantidade de keywords encontradas
        - list: Keywords encontradas
    """
    if not texto:
        return False, 0, []
    
    texto_norm = normalizar_texto(texto)
    
    # Verificar exclusões primeiro
    for keyword in KEYWORDS_EXCLUSAO:
        if normalizar_texto(keyword) in texto_norm:
            return False, 0, [f"EXCLUSÃO: {keyword}"]
    
    # Contar keywords de validação
    keywords_encontradas = []
    for keyword in KEYWORDS_VALIDACAO:
        if normalizar_texto(keyword) in texto_norm:
            keywords_encontradas.append(keyword)
    
    quantidade = len(keywords_encontradas)
    eh_contrato = quantidade >= MIN_KEYWORDS
    
    return eh_contrato, quantidade, keywords_encontradas
