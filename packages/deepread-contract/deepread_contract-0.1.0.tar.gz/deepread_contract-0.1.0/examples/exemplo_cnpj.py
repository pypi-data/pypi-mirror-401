#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exemplo: Consulta de CNPJ

Este exemplo mostra como consultar dados de empresas na Receita Federal.
"""

from deepread_contract import (
    consultar_cnpj,
    validar_cnpj,
    formatar_cnpj,
    limpar_cnpj,
    buscar_cnpj_por_nome,
    buscar_empresa,
)


def exemplo_validacao():
    """Validação e formatação de CNPJ."""
    print("=" * 50)
    print("📋 VALIDAÇÃO E FORMATAÇÃO DE CNPJ")
    print("=" * 50)
    
    cnpjs = [
        "12.345.678/0001-99",
        "12345678000199",
        "123456",  # inválido
        "33.000.167/0001-01",  # Petrobras
    ]
    
    for cnpj in cnpjs:
        valido = validar_cnpj(cnpj)
        formatado = formatar_cnpj(cnpj)
        limpo = limpar_cnpj(cnpj)
        
        emoji = "✅" if valido else "❌"
        print(f"\n{emoji} CNPJ: {cnpj}")
        print(f"   Válido: {valido}")
        print(f"   Formatado: {formatado}")
        print(f"   Limpo: {limpo}")


def exemplo_consulta():
    """Consulta de CNPJ na Receita Federal."""
    print("\n" + "=" * 50)
    print("🔍 CONSULTA DE CNPJ NA RECEITA FEDERAL")
    print("=" * 50)
    
    # CNPJ da Petrobras
    cnpj = "33.000.167/0001-01"
    
    print(f"\nConsultando: {cnpj}...")
    
    dados = consultar_cnpj(cnpj)
    
    if dados:
        print(f"\n✅ Empresa encontrada!")
        print(f"   Razão Social: {dados['razao_social']}")
        print(f"   Nome Fantasia: {dados.get('nome_fantasia', 'N/A')}")
        print(f"   Situação: {dados['situacao']}")
        print(f"   Data Abertura: {dados.get('data_abertura', 'N/A')}")
        print(f"   Natureza Jurídica: {dados.get('natureza_juridica', 'N/A')}")
        print(f"   Capital Social: R$ {dados.get('capital_social', 0):,.2f}")
        
        # Endereço
        end = dados.get('endereco', {})
        if end:
            print(f"\n   📍 Endereço:")
            print(f"      {end.get('logradouro', '')}, {end.get('numero', '')}")
            print(f"      {end.get('bairro', '')} - {end.get('cidade', '')}/{end.get('uf', '')}")
            print(f"      CEP: {end.get('cep', '')}")
        
        # Sócios
        socios = dados.get('socios', [])
        if socios:
            print(f"\n   👥 Sócios/Administradores ({len(socios)}):")
            for s in socios[:5]:
                print(f"      • {s.get('nome', '')} - {s.get('qualificacao', '')}")
            if len(socios) > 5:
                print(f"      ... e mais {len(socios) - 5}")
    else:
        print("❌ CNPJ não encontrado")


def exemplo_busca_nome():
    """Busca de empresa por nome."""
    print("\n" + "=" * 50)
    print("🔎 BUSCA DE EMPRESA POR NOME")
    print("=" * 50)
    
    nome = "Petrobras"
    
    print(f"\nBuscando: {nome}...")
    
    dados = buscar_cnpj_por_nome(nome)
    
    if dados:
        print(f"\n✅ Empresa encontrada!")
        print(f"   CNPJ: {dados['cnpj']}")
        print(f"   Razão Social: {dados['razao_social']}")
        print(f"   Situação: {dados['situacao']}")
    else:
        print("❌ Empresa não encontrada")


def exemplo_busca_flexivel():
    """Busca flexível por CNPJ ou nome."""
    print("\n" + "=" * 50)
    print("🔄 BUSCA FLEXÍVEL (CNPJ OU NOME)")
    print("=" * 50)
    
    # Buscar por nome
    print("\nBuscando por nome 'Banco do Brasil'...")
    dados = buscar_empresa(nome="Banco do Brasil")
    
    if dados:
        print(f"   ✅ CNPJ: {dados['cnpj']}")
        print(f"   ✅ Razão Social: {dados['razao_social']}")
    
    # Buscar por CNPJ
    print("\nBuscando por CNPJ '00.000.000/0001-91'...")
    dados = buscar_empresa(cnpj="00.000.000/0001-91")
    
    if dados:
        print(f"   ✅ Razão Social: {dados['razao_social']}")


if __name__ == "__main__":
    exemplo_validacao()
    exemplo_consulta()
    exemplo_busca_nome()
    exemplo_busca_flexivel()
    
    print("\n" + "=" * 50)
    print("🎉 Exemplos concluídos!")
    print("=" * 50)
