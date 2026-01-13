#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exemplo: Validação de Documento

Este exemplo mostra como identificar se um documento é um contrato válido.
"""

from deepread_contract import (
    validar_documento_contrato,
    KEYWORDS_VALIDACAO,
    KEYWORDS_EXCLUSAO,
    MIN_KEYWORDS,
)


def exemplo_validacao_contrato():
    """Valida se um texto é um contrato."""
    print("=" * 60)
    print("📄 VALIDAÇÃO DE DOCUMENTO - É UM CONTRATO?")
    print("=" * 60)
    
    # Exemplo de contrato válido
    texto_contrato = """
    CONTRATO DE PRESTAÇÃO DE SERVIÇOS
    
    Pelo presente instrumento particular, as partes abaixo qualificadas:
    
    CONTRATANTE: EMPRESA XPTO LTDA, pessoa jurídica de direito privado, 
    inscrita no CNPJ sob nº 12.345.678/0001-99, com sede na Rua das Flores, 
    nº 100, São Paulo/SP, neste ato representada por seu Diretor.
    
    CONTRATADA: SERVIÇOS ABC S/A, inscrita no CNPJ sob nº 98.765.432/0001-11,
    doravante denominada simplesmente CONTRATADA.
    
    CLÁUSULA PRIMEIRA - DO OBJETO
    O presente contrato tem por objeto a prestação de serviços de consultoria.
    
    CLÁUSULA SEGUNDA - DO VALOR E PAGAMENTO
    O valor total do contrato é de R$ 50.000,00 (cinquenta mil reais).
    
    CLÁUSULA TERCEIRA - DA VIGÊNCIA
    O prazo de vigência é de 12 (doze) meses.
    
    CLÁUSULA QUARTA - DA RESCISÃO
    O contrato poderá ser rescindido por qualquer das partes.
    
    CLÁUSULA QUINTA - DO FORO
    Fica eleito o foro da Comarca de São Paulo/SP.
    
    E por estarem justas e contratadas, as partes assinam o presente.
    
    ________________________
    CONTRATANTE
    
    ________________________
    CONTRATADA
    
    Testemunhas:
    1. _______________
    2. _______________
    """
    
    print("\n📝 Analisando texto de CONTRATO...")
    eh_contrato, qtd, keywords = validar_documento_contrato(texto_contrato)
    
    print(f"\n   É contrato: {'✅ SIM' if eh_contrato else '❌ NÃO'}")
    print(f"   Keywords encontradas: {qtd}")
    print(f"   Mínimo necessário: {MIN_KEYWORDS}")
    print(f"\n   Keywords identificadas:")
    for kw in keywords[:10]:
        print(f"      • {kw}")
    if len(keywords) > 10:
        print(f"      ... e mais {len(keywords) - 10}")


def exemplo_documento_nao_contrato():
    """Valida documento que NÃO é contrato."""
    print("\n" + "=" * 60)
    print("📄 VALIDAÇÃO - DOCUMENTO QUE NÃO É CONTRATO")
    print("=" * 60)
    
    # Exemplo de nota fiscal (não é contrato)
    texto_nf = """
    NOTA FISCAL DE SERVIÇOS ELETRÔNICA
    
    Número: 12345
    Data de Emissão: 01/01/2024
    
    PRESTADOR:
    Empresa ABC Ltda
    CNPJ: 12.345.678/0001-99
    
    TOMADOR:
    Empresa XYZ S/A
    CNPJ: 98.765.432/0001-11
    
    DESCRIÇÃO DO SERVIÇO:
    Consultoria em TI - Janeiro/2024
    
    VALOR TOTAL: R$ 5.000,00
    
    ISS RETIDO: R$ 100,00
    """
    
    print("\n📝 Analisando texto de NOTA FISCAL...")
    eh_contrato, qtd, keywords = validar_documento_contrato(texto_nf)
    
    print(f"\n   É contrato: {'✅ SIM' if eh_contrato else '❌ NÃO'}")
    print(f"   Keywords encontradas: {qtd}")
    if keywords:
        print(f"   Keywords: {keywords}")


def exemplo_edital_licitacao():
    """Valida edital de licitação (exclusão)."""
    print("\n" + "=" * 60)
    print("📄 VALIDAÇÃO - EDITAL DE LICITAÇÃO (EXCLUSÃO)")
    print("=" * 60)
    
    texto_edital = """
    EDITAL DE LICITAÇÃO
    PREGÃO ELETRÔNICO Nº 001/2024
    
    A Prefeitura Municipal torna público que realizará licitação
    na modalidade Pregão Eletrônico para contratação de serviços.
    
    OBJETO: Contratação de empresa especializada em TI.
    
    DATA: 15/02/2024
    """
    
    print("\n📝 Analisando texto de EDITAL...")
    eh_contrato, qtd, keywords = validar_documento_contrato(texto_edital)
    
    print(f"\n   É contrato: {'✅ SIM' if eh_contrato else '❌ NÃO'}")
    print(f"   Motivo: {keywords[0] if keywords else 'N/A'}")


def mostrar_keywords():
    """Mostra as keywords configuradas."""
    print("\n" + "=" * 60)
    print("📚 KEYWORDS CONFIGURADAS")
    print("=" * 60)
    
    print(f"\n✅ Keywords de VALIDAÇÃO ({len(KEYWORDS_VALIDACAO)}):")
    for i, kw in enumerate(KEYWORDS_VALIDACAO, 1):
        print(f"   {i:2}. {kw}")
    
    print(f"\n❌ Keywords de EXCLUSÃO ({len(KEYWORDS_EXCLUSAO)}):")
    for i, kw in enumerate(KEYWORDS_EXCLUSAO, 1):
        print(f"   {i:2}. {kw}")
    
    print(f"\n⚙️ Mínimo de keywords para validar: {MIN_KEYWORDS}")


if __name__ == "__main__":
    exemplo_validacao_contrato()
    exemplo_documento_nao_contrato()
    exemplo_edital_licitacao()
    mostrar_keywords()
    
    print("\n" + "=" * 60)
    print("🎉 Exemplos concluídos!")
    print("=" * 60)
