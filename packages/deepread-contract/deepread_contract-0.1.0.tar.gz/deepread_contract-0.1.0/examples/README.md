# 📚 Exemplos de Uso - DeepRead Contract

## 🔧 Instalação

```bash
pip install deepread-contract
```

## 📁 Arquivos de Exemplo

| Arquivo | Descrição |
|---------|-----------|
| `exemplo_cnpj.py` | Consulta de CNPJ na Receita Federal |
| `exemplo_validacao_documento.py` | Validação de documento (é contrato?) |
| `exemplo_verificar_contrato.py` | Verificação completa de contrato PDF |
| `exemplo_cli.sh` | Comandos do CLI |

## 🚀 Executando os Exemplos

### 1. Consulta de CNPJ

```bash
python exemplo_cnpj.py
```

**Funcionalidades demonstradas:**
- Validação de formato de CNPJ
- Formatação de CNPJ
- Consulta na Receita Federal (BrasilAPI/ReceitaWS)
- Busca de empresa por nome

### 2. Validação de Documento

```bash
python exemplo_validacao_documento.py
```

**Funcionalidades demonstradas:**
- Identificar se um texto é um contrato
- Keywords de validação e exclusão
- Análise de diferentes tipos de documentos

### 3. Verificação de Contrato

```bash
# Primeiro configure a API key
export OPENAI_API_KEY="sua-chave-aqui"

# Depois execute
python exemplo_verificar_contrato.py
```

**Requisitos:**
- DeepRead instalado (`pip install deepread`)
- OPENAI_API_KEY configurada
- Arquivo `contrato.pdf` no diretório

**Funcionalidades demonstradas:**
- Extração de dados do PDF
- Validação de empresas na Receita Federal
- Verificação de poder de assinatura (QSA)
- Classificação de legitimidade

### 4. CLI

```bash
# Ver todos os comandos
bash exemplo_cli.sh

# Ou use diretamente:
deepread-contract cnpj 33.000.167/0001-01
deepread-contract buscar "Petrobras"
deepread-contract verificar contrato.pdf
```

## 📖 Uso Rápido

```python
# Consultar CNPJ
from deepread_contract import consultar_cnpj

dados = consultar_cnpj("33.000.167/0001-01")
print(dados["razao_social"])  # PETROLEO BRASILEIRO S A PETROBRAS
print(dados["situacao"])       # ATIVA

# Validar documento
from deepread_contract import validar_documento_contrato

eh_contrato, qtd, keywords = validar_documento_contrato(texto)
print(f"É contrato: {eh_contrato}")

# Verificar contrato (requer DeepRead + OpenAI)
from deepread_contract import ContractChecker

checker = ContractChecker()
resultado = checker.verificar("contrato.pdf")
print(resultado["resultado_final"])  # APROVADO, REPROVADO ou PENDENTE
```

## ❓ Problemas Comuns

### CNPJ não encontrado
- Verifique se o CNPJ está correto (14 dígitos)
- A API pode estar temporariamente indisponível

### DeepRead não disponível
- Instale com: `pip install deepread`
- Sem DeepRead, apenas funções de CNPJ funcionam

### API key não configurada
- Configure: `export OPENAI_API_KEY="sk-..."`
- Ou passe diretamente: `ContractChecker(openai_api_key="sk-...")`
