# -*- coding: utf-8 -*-
"""
Utilitários para consulta de CNPJ via APIs públicas da Receita Federal.

Usa BrasilAPI como fonte principal e ReceitaWS como fallback.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Dict, Optional, Any, Tuple

import requests


# =============================================================================
# CONFIGURAÇÃO DAS APIs
# =============================================================================

BRASIL_API_URL = "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
RECEITA_WS_URL = "https://receitaws.com.br/v1/cnpj/{cnpj}"
CASADOSDADOS_API = "https://api.casadosdados.com.br/v2/public/cnpj/search"
REQUEST_TIMEOUT = 10


# =============================================================================
# FUNÇÕES DE FORMATAÇÃO
# =============================================================================

def limpar_cnpj(cnpj: str) -> str:
    """
    Remove formatação do CNPJ (pontos, barras, hífens).
    
    Args:
        cnpj: CNPJ com ou sem formatação
        
    Returns:
        CNPJ apenas com dígitos (14 caracteres)
        
    Exemplo:
        >>> limpar_cnpj("12.345.678/0001-99")
        '12345678000199'
    """
    if not cnpj:
        return ""
    return re.sub(r'\D', '', cnpj)


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida se o CNPJ tem 14 dígitos.
    
    Args:
        cnpj: CNPJ com ou sem formatação
        
    Returns:
        True se o CNPJ é válido (14 dígitos)
        
    Exemplo:
        >>> validar_cnpj("12.345.678/0001-99")
        True
        >>> validar_cnpj("123456")
        False
    """
    cnpj_limpo = limpar_cnpj(cnpj)
    return len(cnpj_limpo) == 14


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX.
    
    Args:
        cnpj: CNPJ sem formatação (14 dígitos)
        
    Returns:
        CNPJ formatado
        
    Exemplo:
        >>> formatar_cnpj("12345678000199")
        '12.345.678/0001-99'
    """
    cnpj_limpo = limpar_cnpj(cnpj)
    if len(cnpj_limpo) == 14:
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    return cnpj


# =============================================================================
# FUNÇÕES DE CONSULTA
# =============================================================================

def _consultar_brasil_api(cnpj: str) -> Optional[Dict[str, Any]]:
    """Consulta CNPJ na BrasilAPI (fonte principal)."""
    cnpj_limpo = limpar_cnpj(cnpj)
    url = BRASIL_API_URL.format(cnpj=cnpj_limpo)
    
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            
            socios_raw = data.get('qsa', [])
            socios = []
            for s in socios_raw:
                socio = {
                    'nome': s.get('nome_socio', ''),
                    'qualificacao': s.get('qualificacao_socio', ''),
                    'data_entrada': s.get('data_entrada_sociedade', ''),
                    'cpf_representante': s.get('cpf_representante_legal', ''),
                    'nome_representante': s.get('nome_representante_legal', ''),
                    'qualificacao_representante': s.get('qualificacao_representante_legal', ''),
                }
                socios.append(socio)
            
            return {
                'fonte': 'BrasilAPI',
                'cnpj': formatar_cnpj(cnpj_limpo),
                'razao_social': data.get('razao_social', ''),
                'nome_fantasia': data.get('nome_fantasia', ''),
                'situacao': data.get('descricao_situacao_cadastral', ''),
                'data_situacao': data.get('data_situacao_cadastral', ''),
                'data_abertura': data.get('data_inicio_atividade', ''),
                'natureza_juridica': data.get('natureza_juridica', ''),
                'porte': data.get('porte', ''),
                'capital_social': data.get('capital_social', 0),
                'endereco': {
                    'logradouro': data.get('logradouro', ''),
                    'numero': data.get('numero', ''),
                    'complemento': data.get('complemento', ''),
                    'bairro': data.get('bairro', ''),
                    'cidade': data.get('municipio', ''),
                    'uf': data.get('uf', ''),
                    'cep': data.get('cep', ''),
                },
                'email': data.get('email', ''),
                'socios': socios,
            }
        return None
    except Exception:
        return None


def _consultar_receita_ws(cnpj: str) -> Optional[Dict[str, Any]]:
    """Consulta CNPJ na ReceitaWS (fallback)."""
    cnpj_limpo = limpar_cnpj(cnpj)
    url = RECEITA_WS_URL.format(cnpj=cnpj_limpo)
    
    try:
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'ERROR':
                return None
            
            capital = data.get('capital_social', '0')
            if isinstance(capital, str):
                capital = float(capital.replace('.', '').replace(',', '.')) if capital else 0
            
            socios = []
            for s in data.get('qsa', []):
                socio = {
                    'nome': s.get('nome', ''),
                    'qualificacao': s.get('qual', ''),
                    'data_entrada': '',
                    'cpf_representante': '',
                    'nome_representante': '',
                    'qualificacao_representante': '',
                }
                socios.append(socio)
            
            return {
                'fonte': 'ReceitaWS',
                'cnpj': formatar_cnpj(cnpj_limpo),
                'razao_social': data.get('nome', ''),
                'nome_fantasia': data.get('fantasia', ''),
                'situacao': data.get('situacao', ''),
                'data_situacao': data.get('data_situacao', ''),
                'data_abertura': data.get('abertura', ''),
                'natureza_juridica': data.get('natureza_juridica', ''),
                'porte': data.get('porte', ''),
                'capital_social': capital,
                'endereco': {
                    'logradouro': data.get('logradouro', ''),
                    'numero': data.get('numero', ''),
                    'complemento': data.get('complemento', ''),
                    'bairro': data.get('bairro', ''),
                    'cidade': data.get('municipio', ''),
                    'uf': data.get('uf', ''),
                    'cep': data.get('cep', ''),
                },
                'email': data.get('email', ''),
                'socios': socios,
            }
        return None
    except Exception:
        return None


def consultar_cnpj(cnpj: str) -> Optional[Dict[str, Any]]:
    """
    Consulta CNPJ online usando BrasilAPI com fallback para ReceitaWS.
    
    Args:
        cnpj: CNPJ (com ou sem formatação)
        
    Returns:
        Dict com dados da empresa ou None se não encontrado
        
    Exemplo:
        >>> dados = consultar_cnpj("12.345.678/0001-99")
        >>> if dados:
        ...     print(dados["razao_social"])
        ...     print(dados["situacao"])  # ATIVA, BAIXADA, etc.
    """
    if not validar_cnpj(cnpj):
        return None
    
    resultado = _consultar_brasil_api(cnpj)
    if resultado is None:
        resultado = _consultar_receita_ws(cnpj)
    
    return resultado


# Alias para compatibilidade
consultar_cnpj_online = consultar_cnpj


# =============================================================================
# BUSCA POR NOME
# =============================================================================

def buscar_cnpj_por_nome(nome_empresa: str, uf: str = None) -> Optional[Dict[str, Any]]:
    """
    Busca CNPJ pelo nome da empresa usando Casa dos Dados API.
    
    Args:
        nome_empresa: Nome ou razão social da empresa
        uf: UF para filtrar (opcional)
        
    Returns:
        Dict com dados da empresa ou None se não encontrado
        
    Exemplo:
        >>> dados = buscar_cnpj_por_nome("Petrobras")
        >>> if dados:
        ...     print(dados["cnpj"])
    """
    if not nome_empresa or len(nome_empresa) < 3:
        return None
    
    try:
        query = {
            "query": {
                "termo": [nome_empresa],
                "situacao_cadastral": "ATIVA"
            },
            "range_query": {},
            "extras": {
                "somente_mei": False,
                "excluir_mei": False,
                "com_email": False,
                "incluir_atividade_secundaria": False,
                "com_contato_telefonico": False,
                "somente_fixo": False,
                "somente_celular": False,
                "somente_matriz": False,
                "somente_filial": False
            },
            "page": 1
        }
        
        if uf:
            query["query"]["uf"] = [uf]
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            CASADOSDADOS_API,
            json=query,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("data", {}).get("count", 0) > 0:
                empresas = data.get("data", {}).get("cnpj", [])
                
                if empresas:
                    emp = empresas[0]
                    cnpj = emp.get("cnpj", "")
                    
                    if cnpj:
                        dados_completos = consultar_cnpj(cnpj)
                        if dados_completos:
                            dados_completos["busca_por_nome"] = True
                            dados_completos["termo_busca"] = nome_empresa
                            return dados_completos
        
        return None
        
    except Exception:
        return None


def buscar_empresa(cnpj: str = None, nome: str = None, uf: str = None) -> Optional[Dict[str, Any]]:
    """
    Busca empresa por CNPJ ou nome.
    
    Primeiro tenta por CNPJ, se não tiver, busca por nome.
    
    Args:
        cnpj: CNPJ da empresa (opcional)
        nome: Nome/razão social da empresa (opcional)
        uf: UF para filtrar busca por nome (opcional)
        
    Returns:
        Dict com dados da empresa ou None
        
    Exemplo:
        >>> dados = buscar_empresa(nome="Petrobras", uf="RJ")
        >>> # ou
        >>> dados = buscar_empresa(cnpj="12.345.678/0001-99")
    """
    if cnpj:
        cnpj_limpo = limpar_cnpj(cnpj)
        if validar_cnpj(cnpj_limpo):
            resultado = consultar_cnpj(cnpj_limpo)
            if resultado:
                return resultado
    
    if nome:
        resultado = buscar_cnpj_por_nome(nome, uf)
        if resultado:
            return resultado
    
    return None


def buscar_empresa_completo(
    cnpj: str = None,
    nome: str = None,
    uf: str = None,
    usar_ai_search: bool = False,
    openai_api_key: str = None
) -> Optional[Dict[str, Any]]:
    """
    Busca empresa usando todas as estratégias disponíveis.
    
    Ordem de tentativas:
    1. Por CNPJ direto (se fornecido)
    2. Por nome na API Casa dos Dados
    3. Por nome via AI web search (se habilitado e configurado)
    
    Args:
        cnpj: CNPJ da empresa (opcional)
        nome: Nome/razão social da empresa (opcional)
        uf: UF para filtrar (opcional)
        usar_ai_search: Se deve usar AI para buscar CNPJ
        openai_api_key: Chave da API OpenAI para AI search
        
    Returns:
        Dict com dados da empresa incluindo metadados de busca
    """
    # 1. Tentar por CNPJ direto
    if cnpj:
        cnpj_limpo = limpar_cnpj(cnpj)
        if validar_cnpj(cnpj_limpo):
            resultado = consultar_cnpj(cnpj_limpo)
            if resultado:
                resultado["_metodo_busca"] = "cnpj_direto"
                return resultado
    
    # 2. Tentar busca por nome na API
    if nome:
        resultado = buscar_cnpj_por_nome(nome, uf)
        if resultado:
            resultado["_metodo_busca"] = "api_nome"
            return resultado
    
    # 3. Tentar busca via AI web search
    if nome and usar_ai_search and openai_api_key:
        try:
            from deepread_contract.ai_search import buscar_cnpj_via_ai
            cnpj_encontrado = buscar_cnpj_via_ai(nome, openai_api_key)
            
            if cnpj_encontrado:
                resultado = consultar_cnpj(cnpj_encontrado)
                
                if resultado:
                    resultado["_metodo_busca"] = "ai_web_search"
                    resultado["_cnpj_buscado_por_ai"] = True
                    return resultado
        except ImportError:
            pass
    
    return None


# =============================================================================
# COMPARAÇÃO DE ENDEREÇOS
# =============================================================================

def _normalizar_endereco(endereco: str) -> str:
    """Normaliza endereço para comparação."""
    if not endereco:
        return ""
    
    texto = unicodedata.normalize('NFD', endereco)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = texto.lower().strip()
    
    substituicoes = [
        (r'\s+', ' '),
        (r'[.,;:\-/\\]', ' '),
        (r'\bn[ºo]?\s*', ''),
        (r'\brua\b', 'r'),
        (r'\bavenida\b', 'av'),
        (r'\bavda?\b', 'av'),
        (r'\btravessa\b', 'tv'),
        (r'\bpracas?\b', 'pc'),
        (r'\bedificio\b', 'ed'),
        (r'\bpredio\b', 'ed'),
        (r'\bconjunto\b', 'cj'),
        (r'\bconj\b', 'cj'),
        (r'\bsala\b', 'sl'),
        (r'\bandar\b', 'and'),
        (r'\bbairro\b', ''),
        (r'\bcep\b', ''),
    ]
    
    for pattern, replacement in substituicoes:
        texto = re.sub(pattern, replacement, texto)
    
    return texto.strip()


def comparar_enderecos(endereco_contrato: str, dados_receita: dict) -> Tuple[bool, float, str]:
    """
    Compara endereço do contrato com o da Receita Federal.
    
    Args:
        endereco_contrato: Endereço extraído do contrato
        dados_receita: Dados da empresa da Receita Federal
        
    Returns:
        tuple: (confere: bool, similaridade: float, endereco_receita: str)
        
    Exemplo:
        >>> confere, sim, end_rf = comparar_enderecos(
        ...     "Av Paulista 1000, Bela Vista, São Paulo",
        ...     dados_empresa
        ... )
        >>> print(f"Confere: {confere} ({sim:.0%})")
    """
    if not endereco_contrato or not dados_receita:
        return False, 0.0, ""
    
    end = dados_receita.get('endereco', {})
    partes_receita = []
    
    if end.get('logradouro'):
        partes_receita.append(end['logradouro'])
    if end.get('numero'):
        partes_receita.append(end['numero'])
    if end.get('complemento'):
        partes_receita.append(end['complemento'])
    if end.get('bairro'):
        partes_receita.append(end['bairro'])
    if end.get('cidade'):
        partes_receita.append(end['cidade'])
    if end.get('uf'):
        partes_receita.append(end['uf'])
    if end.get('cep'):
        partes_receita.append(end['cep'])
    
    endereco_receita = " ".join(partes_receita)
    
    if not endereco_receita:
        return False, 0.0, ""
    
    contrato_norm = _normalizar_endereco(endereco_contrato)
    receita_norm = _normalizar_endereco(endereco_receita)
    
    # Comparação exata
    if contrato_norm == receita_norm:
        return True, 1.0, endereco_receita
    
    # Comparação por inclusão
    if contrato_norm in receita_norm or receita_norm in contrato_norm:
        return True, 0.9, endereco_receita
    
    # Comparação por palavras
    palavras_contrato = set(w for w in contrato_norm.split() if len(w) > 2)
    palavras_receita = set(w for w in receita_norm.split() if len(w) > 2)
    
    if not palavras_contrato or not palavras_receita:
        return False, 0.0, endereco_receita
    
    intersecao = palavras_contrato & palavras_receita
    uniao = palavras_contrato | palavras_receita
    
    similaridade = len(intersecao) / len(uniao) if uniao else 0
    
    # Verificar CEP
    cep_contrato = re.search(r'\d{5}\s*-?\s*\d{3}', endereco_contrato)
    cep_receita = end.get('cep', '')
    
    if cep_contrato and cep_receita:
        cep_c = re.sub(r'\D', '', cep_contrato.group())
        cep_r = re.sub(r'\D', '', cep_receita)
        if cep_c == cep_r:
            similaridade = max(similaridade, 0.8)
    
    return similaridade >= 0.5, similaridade, endereco_receita
