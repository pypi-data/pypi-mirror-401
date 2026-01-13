# -*- coding: utf-8 -*-
"""
Modelos Pydantic para extração e validação de contratos.
"""
from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# =============================================================================
# MODELOS DE EXTRAÇÃO
# =============================================================================

class EmpresaExtraida(BaseModel):
    """Empresa extraída do contrato."""
    cnpj: Optional[str] = Field(None, description="CNPJ da empresa (14 dígitos)")
    razao_social: Optional[str] = Field(None, description="Razão social da empresa")
    nome_fantasia: Optional[str] = Field(None, description="Nome fantasia")
    endereco: Optional[str] = Field(None, description="Endereço completo")
    papel_no_contrato: str = Field(
        default="",
        description="Papel: contratante, contratada, interveniente, etc"
    )


class ExtracaoEmpresas(BaseModel):
    """Extração de empresas do contrato."""
    empresas: List[EmpresaExtraida] = Field(default_factory=list)
    total_empresas: int = Field(default=0)
    contratante_principal: Optional[str] = Field(None, description="CNPJ do contratante")
    contratada_principal: Optional[str] = Field(None, description="CNPJ da contratada")


class AssinaturaExtraida(BaseModel):
    """Assinatura extraída do contrato."""
    nome_signatario: str = Field(description="Nome completo da pessoa que assinou")
    cargo: Optional[str] = Field(None, description="Cargo do signatário")
    cpf: Optional[str] = Field(None, description="CPF do signatário")
    empresa_representada: Optional[str] = Field(None, description="Empresa que representa")
    cnpj_empresa: Optional[str] = Field(None, description="CNPJ da empresa")
    tipo_assinatura: str = Field(default="digital", description="digital ou manuscrita")
    certificado_info: Optional[str] = Field(None, description="Info do certificado digital")
    data_assinatura: Optional[str] = Field(None, description="Data da assinatura")


class ExtracaoAssinaturas(BaseModel):
    """Extração de assinaturas do contrato."""
    assinaturas: List[AssinaturaExtraida] = Field(default_factory=list)
    total_assinaturas: int = Field(default=0)
    assinaturas_digitais: int = Field(default=0)
    assinaturas_manuscritas: int = Field(default=0)


class ExtracaoDadosContrato(BaseModel):
    """Dados gerais do contrato."""
    tipo_contrato: Optional[str] = Field(None, description="Tipo de contrato")
    objeto: Optional[str] = Field(None, description="Objeto/finalidade")
    data_contrato: Optional[str] = Field(None, description="Data de celebração")
    prazo_vigencia: Optional[str] = Field(None, description="Prazo de vigência")
    valor_total: Optional[str] = Field(None, description="Valor total")
    foro: Optional[str] = Field(None, description="Foro de eleição")


# =============================================================================
# MODELOS DE VALIDAÇÃO
# =============================================================================

class CampoVerificado(BaseModel):
    """Resultado da verificação de um campo."""
    campo: str
    status: Literal["aprovado", "reprovado", "pendente", "nao_verificado"]
    valor_contrato: Optional[str] = None
    valor_receita: Optional[str] = None
    mensagem: str = ""
    
    @property
    def emoji(self) -> str:
        return {
            "aprovado": "✅",
            "reprovado": "❌",
            "pendente": "⚠️",
            "nao_verificado": "➖"
        }.get(self.status, "❓")


class EmpresaVerificada(BaseModel):
    """Empresa verificada contra Receita Federal."""
    cnpj: str
    razao_social_contrato: Optional[str] = None
    razao_social_receita: Optional[str] = None
    papel_no_contrato: str = ""
    campos: List[CampoVerificado] = Field(default_factory=list)
    cnpj_encontrado: bool = False
    cnpj_buscado_por_nome: bool = False
    empresa_ativa: bool = False
    razao_social_confere: bool = False
    socios: List[dict] = Field(default_factory=list)
    problemas: List[str] = Field(default_factory=list)


class AssinaturaVerificada(BaseModel):
    """Assinatura verificada contra QSA."""
    nome_signatario: str
    cargo: Optional[str] = None
    empresa_representada: Optional[str] = None
    cnpj_empresa: Optional[str] = None
    tipo_assinatura: str = "digital"
    campos: List[CampoVerificado] = Field(default_factory=list)
    tem_poder_assinatura: bool = False
    qualificacao_qsa: Optional[str] = None
    problemas: List[str] = Field(default_factory=list)


# =============================================================================
# MODELO DE CLASSIFICAÇÃO FINAL
# =============================================================================

class ClassificacaoLegitimidade(BaseModel):
    """Classificação final de legitimidade do contrato."""
    resultado_final: Literal["APROVADO", "REPROVADO", "PENDENTE"]
    
    campos_aprovados: List[str] = Field(default_factory=list)
    campos_reprovados: List[str] = Field(default_factory=list)
    campos_pendentes: List[str] = Field(default_factory=list)
    
    total_campos: int = 0
    total_aprovados: int = 0
    total_reprovados: int = 0
    total_pendentes: int = 0
    
    justificativa: str = ""
    recomendacoes: List[str] = Field(default_factory=list)
    confianca: float = Field(default=0.9, ge=0, le=1)


# =============================================================================
# MODELO DE RESULTADO
# =============================================================================

class ResultadoVerificacao(BaseModel):
    """Resultado completo da verificação de um contrato."""
    resultado_final: Literal["APROVADO", "REPROVADO", "PENDENTE"]
    justificativa: str
    
    campos_aprovados: List[str] = Field(default_factory=list)
    campos_reprovados: List[str] = Field(default_factory=list)
    campos_pendentes: List[str] = Field(default_factory=list)
    
    total_campos: int = 0
    total_aprovados: int = 0
    total_reprovados: int = 0
    total_pendentes: int = 0
    
    empresas: List[EmpresaVerificada] = Field(default_factory=list)
    assinaturas: List[AssinaturaVerificada] = Field(default_factory=list)
    dados_contrato: dict = Field(default_factory=dict)
    
    metricas: dict = Field(default_factory=dict)
