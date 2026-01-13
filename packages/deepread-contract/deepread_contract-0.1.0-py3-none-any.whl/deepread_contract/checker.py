#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ContractChecker - Verificador de Legitimidade de Contratos.

Usa DeepRead para extrair dados e valida contra Receita Federal.
"""
from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import List, Optional, Dict, Any

from deepread_contract.auth import DeepReadAuth, AuthenticatedClient
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
)
from deepread_contract.cnpj import (
    consultar_cnpj,
    validar_cnpj,
    formatar_cnpj,
    limpar_cnpj,
    buscar_cnpj_por_nome,
    comparar_enderecos,
)


class ContractChecker:
    """
    Verificador de Legitimidade de Contratos.
    
    Usa DeepRead para extrair dados de PDFs e valida contra a Receita Federal.
    Suporta OpenAI e Azure OpenAI.
    
    Exemplo OpenAI:
        ```python
        checker = ContractChecker(openai_api_key="sk-...")
        resultado = checker.verificar("contrato.pdf")
        print(resultado["resultado_final"])
        ```
    
    Exemplo Azure:
        ```python
        checker = ContractChecker(
            provider="azure",
            azure_api_key="sua-chave",
            azure_endpoint="https://seu-recurso.openai.azure.com",
            azure_deployment="gpt-4o"
        )
        resultado = checker.verificar("contrato.pdf")
        ```
    
    Args:
        api_token: Token de autenticação DeepRead
        openai_api_key: Chave da API OpenAI
        provider: "openai" ou "azure"
        azure_api_key: Chave da API Azure
        azure_endpoint: Endpoint Azure OpenAI
        azure_deployment: Nome do deployment Azure
        azure_api_version: Versão da API Azure
        model: Modelo a usar
        verbose: Se deve exibir logs
        usar_ai_search: Se deve usar AI para buscar CNPJs
    """
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        # OpenAI
        openai_api_key: Optional[str] = None,
        # Provider
        provider: Optional[str] = None,
        # Azure
        azure_api_key: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        azure_api_version: str = "2024-02-15-preview",
        # Geral
        model: str = "gpt-4o",
        verbose: bool = True,
        usar_ai_search: bool = True
    ):
        self.verbose = verbose
        self.model = model
        self.usar_ai_search = usar_ai_search
        
        # Autenticação (suporta OpenAI e Azure)
        self._auth = DeepReadAuth(
            api_token=api_token,
            openai_api_key=openai_api_key,
            provider=provider,
            azure_api_key=azure_api_key,
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            azure_api_version=azure_api_version,
        )
        
        if not self._auth.has_api_key:
            if self._auth.is_azure:
                raise ValueError(
                    "Credenciais Azure não configuradas. "
                    "Defina AZURE_API_KEY, AZURE_API_ENDPOINT e AZURE_DEPLOYMENT_NAME."
                )
            else:
                raise ValueError(
                    "OpenAI API key não configurada. "
                    "Defina OPENAI_API_KEY ou passe openai_api_key."
                )
        
        # Lazy load do DeepRead
        self._client = None
        self._deepread_available = None
    
    @property
    def auth(self) -> DeepReadAuth:
        """Retorna o gerenciador de autenticação."""
        return self._auth
    
    @property
    def token(self) -> Optional[str]:
        """Retorna o token de autenticação atual."""
        return self._auth.get_token()
    
    @property
    def provider(self) -> str:
        """Retorna o provider configurado (openai ou azure)."""
        return self._auth.provider
    
    def _log(self, msg: str, emoji: str = "📋"):
        """Log condicional."""
        if self.verbose:
            print(f"{emoji} {msg}")
    
    def _init_deepread(self):
        """Inicializa DeepRead se disponível."""
        if self._deepread_available is not None:
            return self._deepread_available
        
        if not self._auth.is_deepread_available:
            self._log("DeepRead não disponível. Instale com: pip install deepread", "⚠️")
            self._deepread_available = False
            return False
        
        try:
            from deepread import DeepRead
            
            # Obter kwargs via auth (suporta OpenAI e Azure)
            kwargs = self._auth.get_deepread_kwargs()
            kwargs["model"] = self.model
            kwargs["verbose"] = self.verbose
            
            self._client = DeepRead(**kwargs)
            
            self._setup_questions()
            self._deepread_available = True
            return True
            
        except Exception as e:
            self._log(f"Erro ao inicializar DeepRead: {e}", "❌")
            self._deepread_available = False
            return False
    
    def _setup_questions(self):
        """Configura as perguntas de extração."""
        from deepread import Question, QuestionConfig
        
        # Pergunta 1: Extrair empresas
        self._client.add_question(Question(
            config=QuestionConfig(
                id="empresas",
                name="Empresas do Contrato",
                tag="empresas"
            ),
            system_prompt="""Você é um especialista em análise de contratos brasileiros.
Extraia TODAS as empresas mencionadas com CNPJ, razão social e papel no contrato.

REGRAS:
1. CNPJ deve ter 14 dígitos (com ou sem formatação)
2. Identifique claramente: contratante (quem paga) vs contratada (quem presta serviço)
3. Extraia TODAS as empresas, incluindo intervenientes e fiadoras""",
            user_prompt="""Analise o contrato e extraia todas as empresas:

{texto}

Para cada empresa extraia: CNPJ, razão social, nome fantasia, endereço e papel no contrato.""",
            keywords=["cnpj", "contratante", "contratada", "inscrita", "razão social", "ltda", "s/a"],
            response_model=ExtracaoEmpresas
        ))
        
        # Pergunta 2: Extrair assinaturas
        self._client.add_question(Question(
            config=QuestionConfig(
                id="assinaturas",
                name="Assinaturas do Contrato",
                tag="assinaturas"
            ),
            system_prompt="""Você é um especialista em análise de contratos.
Extraia TODAS as pessoas físicas que assinaram ou são representantes.

ONDE PROCURAR:
1. Bloco de assinaturas no final
2. Cláusula de representação legal
3. Qualificação das partes
4. Cláusula de NOTIFICAÇÕES
5. Assinaturas digitais
6. Testemunhas""",
            user_prompt="""Extraia todas as pessoas físicas mencionadas como representantes:

{texto}

Para cada pessoa extraia: nome completo, cargo, CPF (se houver), empresa que representa.""",
            keywords=["assinatura", "assinado", "certificado", "representante", "testemunha", "cpf"],
            response_model=ExtracaoAssinaturas
        ))
        
        # Pergunta 3: Dados gerais
        self._client.add_question(Question(
            config=QuestionConfig(
                id="dados_contrato",
                name="Dados do Contrato",
                tag="dados_contrato"
            ),
            system_prompt="""Você é um especialista em análise de contratos.
Extraia os dados gerais do contrato.""",
            user_prompt="""Extraia os dados gerais do contrato:

{texto}

Extraia: tipo de contrato, objeto, data, vigência, valor, foro.""",
            keywords=["contrato", "objeto", "vigência", "valor", "cláusula", "foro"],
            response_model=ExtracaoDadosContrato
        ))
    
    def _normalizar_texto(self, texto: str) -> str:
        """Normaliza texto para comparação."""
        if not texto:
            return ""
        texto_norm = unicodedata.normalize('NFD', texto)
        texto_sem_acentos = ''.join(c for c in texto_norm if unicodedata.category(c) != 'Mn')
        return texto_sem_acentos.lower().strip()
    
    def _comparar_nomes(self, nome1: str, nome2: str) -> bool:
        """Compara dois nomes de forma flexível."""
        n1 = self._normalizar_texto(nome1)
        n2 = self._normalizar_texto(nome2)
        
        if not n1 or not n2:
            return False
        
        if n1 in n2 or n2 in n1:
            return True
        
        palavras1 = set(w for w in n1.split() if len(w) > 2)
        palavras2 = set(w for w in n2.split() if len(w) > 2)
        return len(palavras1 & palavras2) >= 2
    
    def _verificar_poder_assinatura(
        self, 
        nome_signatario: str, 
        dados_receita: dict
    ) -> tuple:
        """Verifica se signatário está no QSA."""
        socios = dados_receita.get('socios', [])
        
        for socio in socios:
            nome_socio = socio.get('nome', '')
            if self._comparar_nomes(nome_signatario, nome_socio):
                return True, socio.get('qualificacao')
            
            nome_rep = socio.get('nome_representante', '')
            if nome_rep and self._comparar_nomes(nome_signatario, nome_rep):
                return True, socio.get('qualificacao_representante')
        
        return False, None
    
    def _validar_empresas(
        self, 
        empresas: List[EmpresaExtraida]
    ) -> tuple:
        """Valida empresas contra Receita Federal."""
        
        empresas_verificadas = []
        dados_receita_cache = {}
        
        for emp in empresas:
            campos = []
            problemas = []
            cnpj_buscado_por_nome = False
            
            self._log(f"\n--- Verificando: {emp.razao_social or 'Empresa'} ---", "🏢")
            
            dados_receita = None
            cnpj = emp.cnpj
            
            # 1. Tentar por CNPJ direto
            if cnpj and validar_cnpj(limpar_cnpj(cnpj)):
                self._log(f"Consultando CNPJ {formatar_cnpj(limpar_cnpj(cnpj))}...", "🔍")
                dados_receita = consultar_cnpj(limpar_cnpj(cnpj))
            
            # 2. Buscar pelo nome
            if not dados_receita and emp.razao_social:
                self._log(f"Buscando por nome: {emp.razao_social}...", "🔎")
                dados_receita = buscar_cnpj_por_nome(emp.razao_social)
                if dados_receita:
                    cnpj_buscado_por_nome = True
                    cnpj = dados_receita.get('cnpj', '')
                    self._log(f"✅ Encontrado: {cnpj}", "")
            
            if dados_receita:
                # CNPJ
                campos.append(CampoVerificado(
                    campo="CNPJ",
                    status="aprovado",
                    valor_contrato=emp.cnpj or "(buscado automaticamente)",
                    valor_receita=dados_receita.get('cnpj'),
                    mensagem="CNPJ encontrado"
                ))
                
                # Situação
                situacao = dados_receita.get('situacao', '').upper()
                empresa_ativa = 'ATIVA' in situacao
                
                campos.append(CampoVerificado(
                    campo="Situação Cadastral",
                    status="aprovado" if empresa_ativa else "reprovado",
                    valor_contrato="-",
                    valor_receita=situacao,
                    mensagem=f"Empresa {'ATIVA' if empresa_ativa else situacao}"
                ))
                
                if not empresa_ativa:
                    problemas.append(f"Empresa com situação: {situacao}")
                
                # Razão Social
                razao_receita = dados_receita.get('razao_social', '')
                razao_confere = self._comparar_nomes(emp.razao_social or '', razao_receita)
                
                campos.append(CampoVerificado(
                    campo="Razão Social",
                    status="aprovado" if razao_confere else "pendente",
                    valor_contrato=emp.razao_social,
                    valor_receita=razao_receita,
                    mensagem="Confere" if razao_confere else "Divergente"
                ))
                
                # Endereço
                if emp.endereco:
                    endereco_confere, similaridade, endereco_receita = comparar_enderecos(
                        emp.endereco, 
                        dados_receita
                    )
                    
                    campos.append(CampoVerificado(
                        campo="Endereço",
                        status="aprovado" if endereco_confere else "pendente",
                        valor_contrato=emp.endereco,
                        valor_receita=endereco_receita,
                        mensagem=f"Similaridade: {similaridade:.0%}"
                    ))
                
                # Cache
                cnpj_limpo = limpar_cnpj(cnpj) if cnpj else ""
                if cnpj_limpo:
                    dados_receita_cache[cnpj_limpo] = dados_receita
                if emp.razao_social:
                    dados_receita_cache[self._normalizar_texto(emp.razao_social)] = dados_receita
                
                empresas_verificadas.append(EmpresaVerificada(
                    cnpj=dados_receita.get('cnpj', ''),
                    razao_social_contrato=emp.razao_social,
                    razao_social_receita=razao_receita,
                    papel_no_contrato=emp.papel_no_contrato,
                    campos=campos,
                    cnpj_encontrado=True,
                    cnpj_buscado_por_nome=cnpj_buscado_por_nome,
                    empresa_ativa=empresa_ativa,
                    razao_social_confere=razao_confere,
                    socios=dados_receita.get('socios', []),
                    problemas=problemas
                ))
            else:
                campos.append(CampoVerificado(
                    campo="CNPJ",
                    status="reprovado",
                    valor_contrato=emp.cnpj or "(não informado)",
                    valor_receita=None,
                    mensagem="CNPJ não encontrado na Receita Federal"
                ))
                problemas.append("CNPJ não encontrado")
                
                empresas_verificadas.append(EmpresaVerificada(
                    cnpj=emp.cnpj or "",
                    razao_social_contrato=emp.razao_social,
                    papel_no_contrato=emp.papel_no_contrato,
                    campos=campos,
                    problemas=problemas
                ))
        
        return empresas_verificadas, dados_receita_cache
    
    def _validar_assinaturas(
        self,
        assinaturas: List[AssinaturaExtraida],
        dados_receita_cache: dict
    ) -> List[AssinaturaVerificada]:
        """Valida assinaturas contra QSA."""
        
        assinaturas_verificadas = []
        
        self._log(f"\n--- Verificando Assinaturas ---", "✍️")
        
        for ass in assinaturas:
            campos = []
            problemas = []
            tem_poder = False
            qualificacao = None
            
            nome = ass.nome_signatario
            if not nome or nome == "N/A":
                assinaturas_verificadas.append(AssinaturaVerificada(
                    nome_signatario="(não identificado)",
                    tipo_assinatura=ass.tipo_assinatura,
                    campos=[CampoVerificado(
                        campo="Identificação",
                        status="nao_verificado",
                        mensagem="Signatário não identificado"
                    )],
                    problemas=["Signatário não identificado"]
                ))
                continue
            
            self._log(f"Verificando: {nome}", "👤")
            
            dados_receita = None
            
            if ass.cnpj_empresa:
                cnpj_limpo = limpar_cnpj(ass.cnpj_empresa)
                dados_receita = dados_receita_cache.get(cnpj_limpo)
            
            if not dados_receita and ass.empresa_representada:
                empresa_norm = self._normalizar_texto(ass.empresa_representada)
                dados_receita = dados_receita_cache.get(empresa_norm)
            
            if not dados_receita:
                for dados in dados_receita_cache.values():
                    tem_poder, qualificacao = self._verificar_poder_assinatura(nome, dados)
                    if tem_poder:
                        dados_receita = dados
                        break
            else:
                tem_poder, qualificacao = self._verificar_poder_assinatura(nome, dados_receita)
            
            if tem_poder:
                campos.append(CampoVerificado(
                    campo="Poder de Assinatura",
                    status="aprovado",
                    valor_contrato=nome,
                    valor_receita=qualificacao or "Encontrado no QSA",
                    mensagem=f"Signatário tem poder ({qualificacao or 'Sócio/Admin'})"
                ))
                self._log(f"✅ {nome} TEM PODER ({qualificacao})", "")
            elif dados_receita:
                socios_nomes = [s.get('nome', '') for s in dados_receita.get('socios', [])[:3]]
                campos.append(CampoVerificado(
                    campo="Poder de Assinatura",
                    status="reprovado",
                    valor_contrato=nome,
                    valor_receita=f"QSA: {', '.join(socios_nomes)}..." if socios_nomes else "QSA vazio",
                    mensagem="Signatário NÃO encontrado no QSA"
                ))
                problemas.append("Signatário sem poder de assinatura")
                self._log(f"❌ {nome} NÃO TEM PODER", "")
            else:
                campos.append(CampoVerificado(
                    campo="Poder de Assinatura",
                    status="pendente",
                    valor_contrato=nome,
                    mensagem="Não foi possível verificar"
                ))
                self._log(f"⚠️ {nome} - não foi possível verificar", "")
            
            assinaturas_verificadas.append(AssinaturaVerificada(
                nome_signatario=nome,
                cargo=ass.cargo,
                empresa_representada=ass.empresa_representada,
                cnpj_empresa=ass.cnpj_empresa,
                tipo_assinatura=ass.tipo_assinatura,
                campos=campos,
                tem_poder_assinatura=tem_poder,
                qualificacao_qsa=qualificacao,
                problemas=problemas
            ))
        
        return assinaturas_verificadas
    
    def verificar(self, documento: str | Path) -> Dict[str, Any]:
        """
        Verifica a legitimidade de um contrato.
        
        Args:
            documento: Caminho do PDF do contrato
            
        Returns:
            dict com resultado da verificação:
            - resultado_final: APROVADO, REPROVADO ou PENDENTE
            - campos_aprovados: Lista de campos aprovados
            - campos_reprovados: Lista de campos reprovados
            - empresas: Detalhes das empresas verificadas
            - assinaturas: Detalhes das assinaturas verificadas
            
        Exemplo:
            >>> resultado = checker.verificar("contrato.pdf")
            >>> print(resultado["resultado_final"])
            APROVADO
        """
        documento = Path(documento)
        
        if not documento.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {documento}")
        
        self._log(f"\n{'='*60}", "")
        self._log(f"VERIFICAÇÃO DE LEGITIMIDADE DE CONTRATO", "🔍")
        self._log(f"Arquivo: {documento.name}", "📄")
        self._log(f"{'='*60}", "")
        
        # Verificar se DeepRead está disponível
        if not self._init_deepread():
            return {
                "resultado_final": "PENDENTE",
                "justificativa": "DeepRead não disponível. Instale com: pip install deepread",
                "campos_aprovados": [],
                "campos_reprovados": [],
                "campos_pendentes": ["Extração de dados não disponível"],
                "empresas": [],
                "assinaturas": [],
            }
        
        # 1. Extrair dados com DeepRead
        self._log("\n📤 Extraindo dados do contrato...", "")
        resultado_extracao = self._client.process(str(documento))
        
        # 2. Obter resultados
        empresas_raw = resultado_extracao.get_result("empresas")
        assinaturas_raw = resultado_extracao.get_result("assinaturas")
        dados_contrato_raw = resultado_extracao.get_result("dados_contrato")
        
        empresas = []
        if empresas_raw and empresas_raw.raw_result:
            empresas = [EmpresaExtraida(**e) for e in empresas_raw.raw_result.get("empresas", [])]
        
        assinaturas = []
        if assinaturas_raw and assinaturas_raw.raw_result:
            assinaturas = [AssinaturaExtraida(**a) for a in assinaturas_raw.raw_result.get("assinaturas", [])]
        
        dados_contrato = {}
        if dados_contrato_raw and dados_contrato_raw.raw_result:
            dados_contrato = dados_contrato_raw.raw_result
        
        self._log(f"Empresas extraídas: {len(empresas)}", "🏢")
        self._log(f"Assinaturas extraídas: {len(assinaturas)}", "✍️")
        
        # 3. Validar empresas
        self._log("\n🔍 Validando empresas na Receita Federal...", "")
        empresas_verificadas, dados_receita_cache = self._validar_empresas(empresas)
        
        # 4. Validar assinaturas
        assinaturas_verificadas = self._validar_assinaturas(assinaturas, dados_receita_cache)
        
        # 5. Consolidar campos
        campos_aprovados = []
        campos_reprovados = []
        campos_pendentes = []
        
        for emp in empresas_verificadas:
            nome = emp.razao_social_receita or emp.razao_social_contrato or emp.cnpj
            for campo in emp.campos:
                item = f"{campo.campo} - {nome}"
                if campo.status == "aprovado":
                    campos_aprovados.append(item)
                elif campo.status == "reprovado":
                    campos_reprovados.append(item)
                elif campo.status == "pendente":
                    campos_pendentes.append(item)
        
        for ass in assinaturas_verificadas:
            for campo in ass.campos:
                item = f"{campo.campo} - {ass.nome_signatario}"
                if campo.status == "aprovado":
                    campos_aprovados.append(item)
                elif campo.status == "reprovado":
                    campos_reprovados.append(item)
                elif campo.status == "pendente":
                    campos_pendentes.append(item)
        
        # 6. Determinar resultado final
        total_aprovados = len(campos_aprovados)
        total_reprovados = len(campos_reprovados)
        total_pendentes = len(campos_pendentes)
        total_campos = total_aprovados + total_reprovados + total_pendentes
        
        if total_reprovados > 0:
            resultado_final = "REPROVADO"
            justificativa = f"{total_reprovados} campo(s) reprovado(s)"
        elif total_pendentes > 0:
            resultado_final = "PENDENTE"
            justificativa = f"{total_pendentes} campo(s) requer(em) análise manual"
        else:
            resultado_final = "APROVADO"
            justificativa = f"Todos os {total_aprovados} campos verificados foram aprovados"
        
        # 7. Imprimir relatório
        if self.verbose:
            self._imprimir_relatorio(
                resultado_final=resultado_final,
                justificativa=justificativa,
                campos_aprovados=campos_aprovados,
                campos_reprovados=campos_reprovados,
                campos_pendentes=campos_pendentes,
                empresas=empresas_verificadas,
                assinaturas=assinaturas_verificadas,
                dados_contrato=dados_contrato,
                metricas=resultado_extracao.total_metrics
            )
        
        return {
            "resultado_final": resultado_final,
            "justificativa": justificativa,
            "campos_aprovados": campos_aprovados,
            "campos_reprovados": campos_reprovados,
            "campos_pendentes": campos_pendentes,
            "total_campos": total_campos,
            "total_aprovados": total_aprovados,
            "total_reprovados": total_reprovados,
            "total_pendentes": total_pendentes,
            "empresas": [e.model_dump() for e in empresas_verificadas],
            "assinaturas": [a.model_dump() for a in assinaturas_verificadas],
            "dados_contrato": dados_contrato,
            "metricas": {
                "tokens": resultado_extracao.total_metrics.tokens,
                "custo_usd": resultado_extracao.total_metrics.cost_usd,
                "tempo_segundos": resultado_extracao.total_metrics.time_seconds
            }
        }
    
    def _imprimir_relatorio(
        self,
        resultado_final: str,
        justificativa: str,
        campos_aprovados: List[str],
        campos_reprovados: List[str],
        campos_pendentes: List[str],
        empresas: List[EmpresaVerificada],
        assinaturas: List[AssinaturaVerificada],
        dados_contrato: dict,
        metricas
    ):
        """Imprime relatório detalhado."""
        
        emoji_final = {"APROVADO": "✅", "REPROVADO": "❌", "PENDENTE": "⚠️"}.get(resultado_final, "❓")
        
        print(f"\n{'='*60}")
        print(f"{emoji_final * 3} RESULTADO FINAL: {resultado_final} {emoji_final * 3}")
        print(f"{'='*60}")
        print(f"   {justificativa}")
        
        print(f"\n{'─'*60}")
        print(f"📋 CAMPOS VERIFICADOS")
        print(f"{'─'*60}")
        print(f"   ✅ Aprovados: {len(campos_aprovados)}")
        print(f"   ❌ Reprovados: {len(campos_reprovados)}")
        print(f"   ⚠️ Pendentes: {len(campos_pendentes)}")
        
        if campos_aprovados:
            print(f"\n   ✅ APROVADOS:")
            for c in campos_aprovados:
                print(f"      • {c}")
        
        if campos_reprovados:
            print(f"\n   ❌ REPROVADOS:")
            for c in campos_reprovados:
                print(f"      • {c}")
        
        if campos_pendentes:
            print(f"\n   ⚠️ PENDENTES:")
            for c in campos_pendentes:
                print(f"      • {c}")
        
        print(f"\n{'─'*60}")
        print(f"🏢 EMPRESAS ({len(empresas)})")
        print(f"{'─'*60}")
        
        for emp in empresas:
            status = "✅" if emp.empresa_ativa else "❌"
            print(f"\n   {status} {emp.razao_social_receita or emp.razao_social_contrato or 'N/A'}")
            print(f"      CNPJ: {emp.cnpj or 'N/A'}", end="")
            if emp.cnpj_buscado_por_nome:
                print(" (encontrado por busca)")
            else:
                print()
            for campo in emp.campos:
                print(f"      {campo.emoji} {campo.campo}: {campo.mensagem}")
        
        print(f"\n{'─'*60}")
        print(f"✍️ ASSINATURAS ({len(assinaturas)})")
        print(f"{'─'*60}")
        
        for ass in assinaturas:
            status = "✅" if ass.tem_poder_assinatura else "❌"
            print(f"\n   {status} {ass.nome_signatario}")
            if ass.cargo:
                print(f"      Cargo: {ass.cargo}")
            for campo in ass.campos:
                print(f"      {campo.emoji} {campo.campo}: {campo.mensagem}")
        
        print(f"\n{'─'*60}")
        print(f"💰 MÉTRICAS")
        print(f"{'─'*60}")
        print(f"   Tokens: {metricas.tokens:,}")
        print(f"   Custo: ${metricas.cost_usd:.4f}")
        print(f"   Tempo: {metricas.time_seconds:.1f}s")
        
        print(f"\n{'='*60}")


def verificar_contrato(
    documento: str | Path,
    openai_api_key: Optional[str] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Função de conveniência para verificar um contrato.
    
    Args:
        documento: Caminho do PDF
        openai_api_key: Chave da API OpenAI (opcional se OPENAI_API_KEY definida)
        verbose: Se deve exibir logs
        
    Returns:
        Resultado da verificação
        
    Exemplo:
        >>> from deepread_contract import verificar_contrato
        >>> resultado = verificar_contrato("contrato.pdf")
        >>> print(resultado["resultado_final"])
    """
    checker = ContractChecker(openai_api_key=openai_api_key, verbose=verbose)
    return checker.verificar(documento)
