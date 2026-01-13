#!/bin/bash
# Exemplos de uso do CLI deepread-contract

echo "========================================"
echo "🖥️  EXEMPLOS DE USO DO CLI"
echo "========================================"

echo ""
echo "1️⃣  Consultar CNPJ:"
echo "    deepread-contract cnpj 33.000.167/0001-01"
echo ""

echo "2️⃣  Consultar CNPJ (saída JSON):"
echo "    deepread-contract cnpj 33.000.167/0001-01 --json"
echo ""

echo "3️⃣  Buscar empresa por nome:"
echo "    deepread-contract buscar 'Petrobras'"
echo ""

echo "4️⃣  Buscar empresa por nome com UF:"
echo "    deepread-contract buscar 'Banco do Brasil' --uf DF"
echo ""

echo "5️⃣  Verificar contrato (requer DeepRead + OpenAI):"
echo "    deepread-contract verificar contrato.pdf"
echo ""

echo "6️⃣  Verificar contrato (silencioso):"
echo "    deepread-contract verificar contrato.pdf --silencioso"
echo ""

echo "7️⃣  Verificar contrato (saída JSON):"
echo "    deepread-contract verificar contrato.pdf --json"
echo ""

echo "8️⃣  Verificar contrato com modelo específico:"
echo "    deepread-contract verificar contrato.pdf --modelo gpt-4o-mini"
echo ""

echo "========================================"
echo "📚 Para mais informações:"
echo "    deepread-contract --help"
echo "    deepread-contract cnpj --help"
echo "    deepread-contract verificar --help"
echo "========================================"
