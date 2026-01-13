# -*- coding: utf-8 -*-
"""
DeepRead Contract - Validação de Documentos e Contratos Brasileiros.

Biblioteca para validar contratos contra a Receita Federal.

Instalação:
    pip install deepread-contract

Uso básico:
    >>> from deepread_contract import consultar_cnpj, validar_cnpj
    >>> 
    >>> if validar_cnpj("12.345.678/0001-99"):
    ...     dados = consultar_cnpj("12.345.678/0001-99")
    ...     print(dados["razao_social"])
    ...     print(dados["situacao"])  # ATIVA, BAIXADA, etc.

Validação de documento:
    >>> from deepread_contract import validar_documento_contrato
    >>> 
    >>> eh_contrato, qtd, keywords = validar_documento_contrato(texto)
    >>> print(f"É contrato: {eh_contrato}")

Verificação completa (requer DeepRead):
    >>> from deepread_contract import ContractChecker
    >>> 
    >>> checker = ContractChecker()
    >>> resultado = checker.verificar("contrato.pdf")
    >>> print(resultado["resultado_final"])  # APROVADO, REPROVADO, PENDENTE
"""

__version__ = "0.1.0"
__author__ = "BeMonkAI"
__email__ = "contato@bemonk.ai"

# CNPJ - Funções principais
from deepread_contract.cnpj import (
    consultar_cnpj,
    validar_cnpj,
    formatar_cnpj,
    limpar_cnpj,
    buscar_cnpj_por_nome,
    buscar_empresa,
    buscar_empresa_completo,
    comparar_enderecos,
)

# Keywords - Validação de documento
from deepread_contract.keywords import (
    KEYWORDS_VALIDACAO,
    KEYWORDS_EXCLUSAO,
    MIN_KEYWORDS,
    validar_documento_contrato,
)

# Modelos Pydantic
from deepread_contract.models import (
    EmpresaExtraida,
    ExtracaoEmpresas,
    AssinaturaExtraida,
    ExtracaoAssinaturas,
    ExtracaoDadosContrato,
    CampoVerificado,
    EmpresaVerificada,
    AssinaturaVerificada,
    ClassificacaoLegitimidade,
    ResultadoVerificacao,
)

# Checker - Verificação completa (requer DeepRead)
from deepread_contract.checker import ContractChecker, verificar_contrato

# Autenticação
from deepread_contract.auth import (
    DeepReadAuth,
    AuthenticatedClient,
    TokenInfo,
    AzureConfig,
    get_auth,
    get_token,
)

__all__ = [
    # Versão
    "__version__",
    # Checker
    "ContractChecker",
    "verificar_contrato",
    # CNPJ
    "consultar_cnpj",
    "validar_cnpj",
    "formatar_cnpj",
    "limpar_cnpj",
    "buscar_cnpj_por_nome",
    "buscar_empresa",
    "buscar_empresa_completo",
    "comparar_enderecos",
    # Keywords
    "KEYWORDS_VALIDACAO",
    "KEYWORDS_EXCLUSAO",
    "MIN_KEYWORDS",
    "validar_documento_contrato",
    # Modelos
    "EmpresaExtraida",
    "ExtracaoEmpresas",
    "AssinaturaExtraida",
    "ExtracaoAssinaturas",
    "ExtracaoDadosContrato",
    "CampoVerificado",
    "EmpresaVerificada",
    "AssinaturaVerificada",
    "ClassificacaoLegitimidade",
    "ResultadoVerificacao",
    # Autenticação
    "DeepReadAuth",
    "AuthenticatedClient",
    "TokenInfo",
    "AzureConfig",
    "get_auth",
    "get_token",
]
