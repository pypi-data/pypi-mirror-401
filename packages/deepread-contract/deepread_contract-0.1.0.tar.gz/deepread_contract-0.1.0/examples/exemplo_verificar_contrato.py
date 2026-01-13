#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exemplo: Verificação Completa de Contrato

Este exemplo mostra como usar o ContractChecker para verificar
a legitimidade de um contrato PDF.

REQUISITOS:
- deepread instalado (pip install deepread)
- OPENAI_API_KEY configurada
"""

import os
from pathlib import Path

# Verificar API key
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  OPENAI_API_KEY não configurada!")
    print("   Execute: export OPENAI_API_KEY='sua-chave-aqui'")
    print()

from deepread_contract import ContractChecker


def exemplo_verificacao_basica():
    """Verificação básica de contrato."""
    print("=" * 60)
    print("🔍 VERIFICAÇÃO DE CONTRATO")
    print("=" * 60)
    
    # Caminho do PDF
    pdf_path = "contrato.pdf"
    
    if not Path(pdf_path).exists():
        print(f"\n⚠️  Arquivo não encontrado: {pdf_path}")
        print("   Crie um arquivo contrato.pdf para testar.")
        return
    
    # Criar verificador
    checker = ContractChecker(
        verbose=True,  # Mostra logs detalhados
        model="gpt-4o"  # Modelo a usar
    )
    
    # Verificar contrato
    resultado = checker.verificar(pdf_path)
    
    # Exibir resultado
    print("\n" + "=" * 60)
    print("📊 RESULTADO DA VERIFICAÇÃO")
    print("=" * 60)
    
    print(f"\n🎯 Status: {resultado['resultado_final']}")
    print(f"   Justificativa: {resultado['justificativa']}")
    
    print(f"\n📋 Campos verificados: {resultado['total_campos']}")
    print(f"   ✅ Aprovados: {resultado['total_aprovados']}")
    print(f"   ❌ Reprovados: {resultado['total_reprovados']}")
    print(f"   ⚠️  Pendentes: {resultado['total_pendentes']}")
    
    # Empresas
    if resultado['empresas']:
        print(f"\n🏢 Empresas ({len(resultado['empresas'])}):")
        for emp in resultado['empresas']:
            status = "✅" if emp['empresa_ativa'] else "❌"
            nome = emp.get('razao_social_receita') or emp.get('razao_social_contrato') or 'N/A'
            print(f"   {status} {nome}")
            print(f"      CNPJ: {emp.get('cnpj', 'N/A')}")
    
    # Assinaturas
    if resultado['assinaturas']:
        print(f"\n✍️  Assinaturas ({len(resultado['assinaturas'])}):")
        for ass in resultado['assinaturas']:
            status = "✅" if ass['tem_poder_assinatura'] else "❌"
            print(f"   {status} {ass['nome_signatario']}")
            if ass.get('qualificacao_qsa'):
                print(f"      Qualificação: {ass['qualificacao_qsa']}")
    
    # Métricas
    metricas = resultado.get('metricas', {})
    if metricas:
        print(f"\n💰 Métricas:")
        print(f"   Tokens: {metricas.get('tokens', 0):,}")
        print(f"   Custo: ${metricas.get('custo_usd', 0):.4f}")
        print(f"   Tempo: {metricas.get('tempo_segundos', 0):.1f}s")
    
    return resultado


def exemplo_verificacao_silenciosa():
    """Verificação silenciosa (sem logs)."""
    print("\n" + "=" * 60)
    print("🔇 VERIFICAÇÃO SILENCIOSA")
    print("=" * 60)
    
    pdf_path = "contrato.pdf"
    
    if not Path(pdf_path).exists():
        print(f"\n⚠️  Arquivo não encontrado: {pdf_path}")
        return
    
    # Verificador silencioso
    checker = ContractChecker(verbose=False)
    resultado = checker.verificar(pdf_path)
    
    # Só mostra resultado final
    print(f"\n🎯 Resultado: {resultado['resultado_final']}")
    
    return resultado


def exemplo_com_api_key():
    """Exemplo passando API key diretamente."""
    print("\n" + "=" * 60)
    print("🔑 VERIFICAÇÃO COM API KEY")
    print("=" * 60)
    
    # Passar API key diretamente (não recomendado em produção)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("\n⚠️  Configure OPENAI_API_KEY primeiro")
        return
    
    checker = ContractChecker(
        openai_api_key=api_key,
        model="gpt-4o-mini",  # Modelo mais barato
        verbose=True
    )
    
    print("✅ Checker configurado com API key!")
    print(f"   Modelo: gpt-4o-mini")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║     DEEPREAD CONTRACT - EXEMPLO DE VERIFICAÇÃO           ║
╠══════════════════════════════════════════════════════════╣
║  Este exemplo requer:                                    ║
║  1. DeepRead instalado (pip install deepread)            ║
║  2. OPENAI_API_KEY configurada                           ║
║  3. Um arquivo contrato.pdf no diretório atual           ║
╚══════════════════════════════════════════════════════════╝
""")
    
    exemplo_com_api_key()
    
    # Descomente para testar com PDF real:
    # exemplo_verificacao_basica()
    # exemplo_verificacao_silenciosa()
