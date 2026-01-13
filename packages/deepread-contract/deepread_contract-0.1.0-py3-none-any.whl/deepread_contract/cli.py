#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CLI para DeepRead Contract.

Uso:
    deepread-contract verificar contrato.pdf
    deepread-contract cnpj 12.345.678/0001-99
"""
from __future__ import annotations

import argparse
import sys
import json

from deepread_contract.cnpj import (
    consultar_cnpj,
    validar_cnpj,
    formatar_cnpj,
    buscar_cnpj_por_nome,
)


def cmd_verificar(args):
    """Comando para verificar contrato."""
    from deepread_contract.checker import ContractChecker
    
    checker = ContractChecker(
        model=args.modelo,
        verbose=not args.silencioso
    )
    
    resultado = checker.verificar(args.documento)
    
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"\n🎯 Resultado: {resultado['resultado_final']}")
    
    return 0 if resultado['resultado_final'] == 'APROVADO' else 1


def cmd_cnpj(args):
    """Comando para consultar CNPJ."""
    cnpj = args.cnpj
    
    if not validar_cnpj(cnpj):
        print(f"❌ CNPJ inválido: {cnpj}")
        return 1
    
    print(f"🔍 Consultando CNPJ: {formatar_cnpj(cnpj)}...")
    
    dados = consultar_cnpj(cnpj)
    
    if not dados:
        print(f"❌ CNPJ não encontrado")
        return 1
    
    if args.json:
        print(json.dumps(dados, ensure_ascii=False, indent=2))
    else:
        situacao = dados.get('situacao', '').upper()
        emoji = "✅" if 'ATIVA' in situacao else "❌"
        
        print(f"\n{emoji} {dados['razao_social']}")
        print(f"   CNPJ: {dados['cnpj']}")
        print(f"   Situação: {situacao}")
        print(f"   Fonte: {dados['fonte']}")
        
        if dados.get('socios'):
            print(f"\n   👥 Sócios ({len(dados['socios'])}):")
            for s in dados['socios'][:5]:
                print(f"      • {s['nome']} - {s['qualificacao']}")
    
    return 0


def cmd_buscar(args):
    """Comando para buscar empresa por nome."""
    nome = args.nome
    
    print(f"🔍 Buscando empresa: {nome}...")
    
    dados = buscar_cnpj_por_nome(nome, uf=args.uf)
    
    if not dados:
        print(f"❌ Empresa não encontrada")
        return 1
    
    if args.json:
        print(json.dumps(dados, ensure_ascii=False, indent=2))
    else:
        print(f"\n✅ {dados['razao_social']}")
        print(f"   CNPJ: {dados['cnpj']}")
        print(f"   Situação: {dados.get('situacao', 'N/A')}")
    
    return 0


def main():
    """Ponto de entrada do CLI."""
    parser = argparse.ArgumentParser(
        prog='deepread-contract',
        description='DeepRead Contract - Validação de Documentos e Contratos'
    )
    
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponíveis')
    
    # Comando: verificar
    parser_verificar = subparsers.add_parser('verificar', help='Verifica legitimidade de um contrato')
    parser_verificar.add_argument('documento', help='Caminho do PDF do contrato')
    parser_verificar.add_argument('--modelo', default='gpt-4o', help='Modelo OpenAI')
    parser_verificar.add_argument('--silencioso', '-s', action='store_true', help='Modo silencioso')
    parser_verificar.add_argument('--json', '-j', action='store_true', help='Saída em JSON')
    parser_verificar.set_defaults(func=cmd_verificar)
    
    # Comando: cnpj
    parser_cnpj = subparsers.add_parser('cnpj', help='Consulta dados de um CNPJ')
    parser_cnpj.add_argument('cnpj', help='CNPJ a consultar')
    parser_cnpj.add_argument('--json', '-j', action='store_true', help='Saída em JSON')
    parser_cnpj.set_defaults(func=cmd_cnpj)
    
    # Comando: buscar
    parser_buscar = subparsers.add_parser('buscar', help='Busca empresa por nome')
    parser_buscar.add_argument('nome', help='Nome da empresa')
    parser_buscar.add_argument('--uf', help='UF para filtrar')
    parser_buscar.add_argument('--json', '-j', action='store_true', help='Saída em JSON')
    parser_buscar.set_defaults(func=cmd_buscar)
    
    args = parser.parse_args()
    
    if not args.comando:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
