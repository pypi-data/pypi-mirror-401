# -*- coding: utf-8 -*-
"""
Autenticação e gerenciamento de tokens para DeepRead Contract.

Suporta OpenAI e Azure OpenAI.

Uso com OpenAI:
    >>> from deepread_contract.auth import DeepReadAuth
    >>> 
    >>> auth = DeepReadAuth(openai_api_key="sk-...")
    >>> token = auth.get_token()

Uso com Azure:
    >>> auth = DeepReadAuth(
    ...     provider="azure",
    ...     azure_api_key="sua-chave",
    ...     azure_endpoint="https://seu-recurso.openai.azure.com",
    ...     azure_deployment="gpt-4o"
    ... )
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional, List, Literal
from datetime import datetime, timedelta


# Providers suportados
Provider = Literal["openai", "azure"]


@dataclass
class TokenInfo:
    """Informações do token de autenticação."""
    token: str
    user_id: str
    permissions: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    source: str = "internal"  # internal, external, deepread
    
    @property
    def is_expired(self) -> bool:
        """Verifica se o token expirou."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Verifica se o token é válido."""
        return bool(self.token) and not self.is_expired


@dataclass
class AzureConfig:
    """Configuração para Azure OpenAI."""
    api_key: str
    endpoint: str
    deployment: str
    api_version: str = "2024-02-15-preview"
    
    @classmethod
    def from_env(cls) -> Optional["AzureConfig"]:
        """Carrega configuração do ambiente."""
        api_key = os.getenv("AZURE_API_KEY")
        endpoint = os.getenv("AZURE_API_ENDPOINT")
        deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
        api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
        
        if api_key and endpoint and deployment:
            return cls(
                api_key=api_key,
                endpoint=endpoint,
                deployment=deployment,
                api_version=api_version
            )
        return None
    
    def to_dict(self) -> dict:
        """Retorna configuração como dicionário."""
        return {
            "azure_api_key": self.api_key,
            "azure_endpoint": self.endpoint,
            "azure_deployment": self.deployment,
            "azure_api_version": self.api_version,
        }


class DeepReadAuth:
    """
    Gerenciador de autenticação para DeepRead Contract.
    
    Suporta:
    - OpenAI (padrão)
    - Azure OpenAI
    - Token externo ou gerado internamente
    
    Exemplo OpenAI:
        ```python
        auth = DeepReadAuth(openai_api_key="sk-...")
        ```
    
    Exemplo Azure:
        ```python
        auth = DeepReadAuth(
            provider="azure",
            azure_api_key="sua-chave",
            azure_endpoint="https://seu-recurso.openai.azure.com",
            azure_deployment="gpt-4o"
        )
        ```
    
    Exemplo com variáveis de ambiente:
        ```python
        # .env
        # OPENAI_PROVIDER=azure
        # AZURE_API_KEY=sua-chave
        # AZURE_API_ENDPOINT=https://seu-recurso.openai.azure.com
        # AZURE_DEPLOYMENT_NAME=gpt-4o
        
        auth = DeepReadAuth()  # Detecta automaticamente
        ```
    """
    
    # Variáveis de ambiente
    ENV_TOKEN_KEY = "DEEPREAD_API_TOKEN"
    ENV_OPENAI_KEY = "OPENAI_API_KEY"
    ENV_PROVIDER = "OPENAI_PROVIDER"
    
    DEFAULT_PERMISSIONS = ["read", "process", "classify", "extract"]
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        # OpenAI
        openai_api_key: Optional[str] = None,
        # Provider
        provider: Optional[Provider] = None,
        # Azure
        azure_api_key: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        azure_api_version: str = "2024-02-15-preview",
        # Geral
        user_id: str = "deepread_contract",
        permissions: Optional[List[str]] = None,
    ):
        self._api_token = api_token
        self._user_id = user_id
        self._permissions = permissions or self.DEFAULT_PERMISSIONS
        
        # Detectar provider
        self._provider: Provider = self._detect_provider(
            provider=provider,
            openai_api_key=openai_api_key,
            azure_api_key=azure_api_key
        )
        
        # Configurar OpenAI
        self._openai_api_key = openai_api_key or os.getenv(self.ENV_OPENAI_KEY)
        
        # Configurar Azure
        self._azure_config: Optional[AzureConfig] = None
        if self._provider == "azure":
            if azure_api_key and azure_endpoint and azure_deployment:
                self._azure_config = AzureConfig(
                    api_key=azure_api_key,
                    endpoint=azure_endpoint,
                    deployment=azure_deployment,
                    api_version=azure_api_version
                )
            else:
                # Tentar carregar do ambiente
                self._azure_config = AzureConfig.from_env()
        
        self._token_info: Optional[TokenInfo] = None
        self._deepread_available: Optional[bool] = None
    
    def _detect_provider(
        self,
        provider: Optional[Provider],
        openai_api_key: Optional[str],
        azure_api_key: Optional[str]
    ) -> Provider:
        """Detecta o provider a ser usado."""
        # Provider explícito
        if provider:
            return provider
        
        # Variável de ambiente
        env_provider = os.getenv(self.ENV_PROVIDER, "").lower()
        if env_provider == "azure":
            return "azure"
        
        # Azure key fornecida
        if azure_api_key or os.getenv("AZURE_API_KEY"):
            return "azure"
        
        # Padrão: OpenAI
        return "openai"
    
    @property
    def provider(self) -> Provider:
        """Retorna o provider configurado."""
        return self._provider
    
    @property
    def is_azure(self) -> bool:
        """Verifica se está usando Azure."""
        return self._provider == "azure"
    
    @property
    def is_openai(self) -> bool:
        """Verifica se está usando OpenAI."""
        return self._provider == "openai"
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Retorna a chave da API OpenAI."""
        return self._openai_api_key
    
    @openai_api_key.setter
    def openai_api_key(self, value: str):
        """Define a chave da API OpenAI."""
        self._openai_api_key = value
    
    @property
    def azure_config(self) -> Optional[AzureConfig]:
        """Retorna a configuração Azure."""
        return self._azure_config
    
    @property
    def has_api_key(self) -> bool:
        """Verifica se há uma chave de API configurada."""
        if self.is_azure:
            return self._azure_config is not None
        return bool(self._openai_api_key)
    
    # Alias para compatibilidade
    @property
    def has_openai_key(self) -> bool:
        """Verifica se há credenciais configuradas (OpenAI ou Azure)."""
        return self.has_api_key
    
    @property
    def is_deepread_available(self) -> bool:
        """Verifica se a biblioteca DeepRead está disponível."""
        if self._deepread_available is None:
            try:
                from deepread.auth import generate_token
                self._deepread_available = True
            except ImportError:
                self._deepread_available = False
        return self._deepread_available
    
    @property
    def token_info(self) -> Optional[TokenInfo]:
        """Retorna informações do token atual."""
        return self._token_info
    
    @property
    def has_valid_token(self) -> bool:
        """Verifica se há um token válido."""
        return self._token_info is not None and self._token_info.is_valid
    
    def set_external_token(self, token: str, user_id: str = "external") -> TokenInfo:
        """
        Define um token externo.
        
        Args:
            token: Token de autenticação
            user_id: ID do usuário (opcional)
            
        Returns:
            TokenInfo com informações do token
        """
        self._token_info = TokenInfo(
            token=token,
            user_id=user_id,
            permissions=self._permissions,
            source="external"
        )
        return self._token_info
    
    def generate_internal_token(
        self,
        user_id: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        expires_in_hours: int = 24
    ) -> TokenInfo:
        """
        Gera um token interno usando a biblioteca DeepRead.
        
        Args:
            user_id: ID do usuário (usa padrão se não informado)
            permissions: Permissões do token
            expires_in_hours: Tempo de expiração em horas
            
        Returns:
            TokenInfo com informações do token gerado
            
        Raises:
            ImportError: Se DeepRead não estiver instalado
        """
        if not self.is_deepread_available:
            raise ImportError(
                "DeepRead não está instalado. "
                "Instale com: pip install deepread"
            )
        
        from deepread.auth import generate_token
        
        _user_id = user_id or self._user_id
        _permissions = permissions or self._permissions
        
        token_result = generate_token(
            user_id=_user_id,
            permissions=_permissions
        )
        
        self._token_info = TokenInfo(
            token=token_result.token,
            user_id=_user_id,
            permissions=_permissions,
            expires_at=datetime.now() + timedelta(hours=expires_in_hours),
            source="deepread"
        )
        
        return self._token_info
    
    def get_token(self, auto_generate: bool = True) -> Optional[str]:
        """
        Obtém o token de autenticação.
        
        Ordem de prioridade:
        1. Token já configurado (externo ou interno)
        2. Token via variável de ambiente
        3. Gera novo token interno (se auto_generate=True)
        
        Args:
            auto_generate: Se deve gerar token automaticamente
            
        Returns:
            Token de autenticação ou None
        """
        # 1. Token já configurado
        if self.has_valid_token:
            return self._token_info.token
        
        # 2. Token externo passado no construtor
        if self._api_token:
            self.set_external_token(self._api_token)
            return self._token_info.token
        
        # 3. Token via variável de ambiente
        env_token = os.getenv(self.ENV_TOKEN_KEY)
        if env_token:
            self.set_external_token(env_token, user_id="env")
            return self._token_info.token
        
        # 4. Gerar token interno
        if auto_generate and self.is_deepread_available:
            self.generate_internal_token()
            return self._token_info.token
        
        return None
    
    def get_deepread_kwargs(self) -> dict:
        """
        Retorna os kwargs para inicializar DeepRead.
        
        Returns:
            Dict com parâmetros para DeepRead()
        """
        kwargs = {
            "api_token": self.get_token(),
            "provider": self._provider,
        }
        
        if self.is_azure and self._azure_config:
            kwargs.update(self._azure_config.to_dict())
        else:
            kwargs["openai_api_key"] = self._openai_api_key
        
        return kwargs
    
    def validate_token(self) -> bool:
        """Valida o token atual."""
        if not self._token_info:
            return False
        return not self._token_info.is_expired
    
    def refresh_token(self) -> Optional[TokenInfo]:
        """Atualiza o token se expirado."""
        if self._token_info and self._token_info.source == "deepread":
            return self.generate_internal_token()
        return self._token_info
    
    def clear_token(self):
        """Remove o token atual."""
        self._token_info = None
    
    def __repr__(self) -> str:
        status = "valid" if self.has_valid_token else "no token"
        return f"DeepReadAuth(provider={self._provider}, status={status})"


class AuthenticatedClient:
    """
    Cliente autenticado para operações com DeepRead.
    
    Suporta OpenAI e Azure OpenAI.
    
    Exemplo OpenAI:
        ```python
        client = AuthenticatedClient(openai_api_key="sk-...")
        ```
    
    Exemplo Azure:
        ```python
        client = AuthenticatedClient(
            provider="azure",
            azure_api_key="sua-chave",
            azure_endpoint="https://seu-recurso.openai.azure.com",
            azure_deployment="gpt-4o"
        )
        ```
    """
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        # OpenAI
        openai_api_key: Optional[str] = None,
        # Provider
        provider: Optional[Provider] = None,
        # Azure
        azure_api_key: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        azure_api_version: str = "2024-02-15-preview",
        # DeepRead
        model: str = "gpt-4o",
        verbose: bool = True
    ):
        self.auth = DeepReadAuth(
            api_token=api_token,
            openai_api_key=openai_api_key,
            provider=provider,
            azure_api_key=azure_api_key,
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            azure_api_version=azure_api_version,
        )
        self.model = model
        self.verbose = verbose
        self._client = None
    
    @property
    def is_ready(self) -> bool:
        """Verifica se o cliente está pronto para uso."""
        return (
            self.auth.is_deepread_available and
            self.auth.has_api_key
        )
    
    @property
    def provider(self) -> Provider:
        """Retorna o provider configurado."""
        return self.auth.provider
    
    def get_deepread_client(self):
        """
        Obtém instância do cliente DeepRead autenticado.
        
        Returns:
            Instância do DeepRead configurada
            
        Raises:
            ImportError: Se DeepRead não estiver instalado
            ValueError: Se credenciais não estiverem configuradas
        """
        if not self.auth.is_deepread_available:
            raise ImportError(
                "DeepRead não está instalado. "
                "Instale com: pip install deepread"
            )
        
        if not self.auth.has_api_key:
            if self.auth.is_azure:
                raise ValueError(
                    "Credenciais Azure não configuradas. "
                    "Defina AZURE_API_KEY, AZURE_API_ENDPOINT e AZURE_DEPLOYMENT_NAME."
                )
            else:
                raise ValueError(
                    "OpenAI API key não configurada. "
                    "Defina OPENAI_API_KEY ou passe openai_api_key."
                )
        
        if self._client is None:
            from deepread import DeepRead
            
            kwargs = self.auth.get_deepread_kwargs()
            kwargs["model"] = self.model
            kwargs["verbose"] = self.verbose
            
            self._client = DeepRead(**kwargs)
        
        return self._client
    
    def reset_client(self):
        """Reseta o cliente para forçar nova inicialização."""
        self._client = None
        self.auth.clear_token()


# Funções de conveniência
def get_auth(
    api_token: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    provider: Optional[Provider] = None,
    **azure_kwargs
) -> DeepReadAuth:
    """
    Cria instância de autenticação.
    
    Args:
        api_token: Token de API (opcional)
        openai_api_key: Chave OpenAI (opcional)
        provider: "openai" ou "azure"
        **azure_kwargs: azure_api_key, azure_endpoint, etc.
        
    Returns:
        DeepReadAuth configurado
    """
    return DeepReadAuth(
        api_token=api_token,
        openai_api_key=openai_api_key,
        provider=provider,
        **azure_kwargs
    )


def get_token(
    api_token: Optional[str] = None,
    auto_generate: bool = True
) -> Optional[str]:
    """
    Obtém token de autenticação.
    
    Args:
        api_token: Token externo (opcional)
        auto_generate: Se deve gerar automaticamente
        
    Returns:
        Token de autenticação
    """
    auth = DeepReadAuth(api_token=api_token)
    return auth.get_token(auto_generate=auto_generate)
