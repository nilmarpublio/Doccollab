"""
Cliente LLM (Large Language Model) - STUB
Suporta modo offline (rules-based) ou integração com LLMs externos

CONFIGURAÇÃO:
Para habilitar LLM externo, defina a variável de ambiente:
  LLM_API_KEY=sua-chave-aqui
  LLM_PROVIDER=openai  # ou 'anthropic', 'cohere', etc.

Sem LLM_API_KEY, o sistema funciona 100% offline com regras.
"""

import os
from typing import Dict, Optional, List
from enum import Enum

class LLMProvider(Enum):
    """Provedores de LLM suportados"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    LOCAL = "local"  # Modelos locais (Llama, etc.)
    NONE = "none"  # Modo offline

class LLMMode(Enum):
    """Modos de operação"""
    OFFLINE = "offline"  # Apenas regras
    HYBRID = "hybrid"   # Regras + LLM para casos complexos
    LLM_ONLY = "llm_only"  # Apenas LLM

class LLMClient:
    """Cliente para interação com LLMs (ou modo offline)"""
    
    def __init__(self):
        """Inicializa cliente LLM"""
        self.api_key = os.getenv('LLM_API_KEY')
        self.provider = self._detect_provider()
        self.mode = self._detect_mode()
        
        # Cliente do provedor (lazy loading)
        self._client = None
    
    def _detect_provider(self) -> LLMProvider:
        """Detecta provedor baseado em variáveis de ambiente"""
        provider_str = os.getenv('LLM_PROVIDER', 'none').lower()
        
        try:
            return LLMProvider(provider_str)
        except ValueError:
            return LLMProvider.NONE
    
    def _detect_mode(self) -> LLMMode:
        """Detecta modo de operação"""
        if not self.api_key or self.provider == LLMProvider.NONE:
            return LLMMode.OFFLINE
        
        mode_str = os.getenv('LLM_MODE', 'hybrid').lower()
        
        try:
            return LLMMode(mode_str)
        except ValueError:
            return LLMMode.HYBRID
    
    def is_enabled(self) -> bool:
        """Verifica se LLM está habilitado"""
        return self.mode != LLMMode.OFFLINE and self.api_key is not None
    
    def generate_response(
        self, 
        user_message: str,
        context: Optional[Dict] = None,
        language: str = 'pt'
    ) -> Dict:
        """
        Gera resposta para mensagem do usuário
        
        Args:
            user_message: Mensagem do usuário
            context: Contexto adicional (projeto, arquivo, etc.)
            language: Idioma da resposta
        
        Returns:
            Dict com 'text', 'actions', 'source'
        """
        if self.mode == LLMMode.OFFLINE:
            return self._rules_based_response(user_message, context, language)
        
        elif self.mode == LLMMode.HYBRID:
            # Tentar regras primeiro
            rules_response = self._rules_based_response(user_message, context, language)
            
            # Se regras não conseguiram resolver, tentar LLM
            if rules_response.get('source') == 'rules' and rules_response.get('confidence', 0) < 0.7:
                return self._llm_response(user_message, context, language)
            
            return rules_response
        
        else:  # LLM_ONLY
            return self._llm_response(user_message, context, language)
    
    def _rules_based_response(
        self, 
        user_message: str,
        context: Optional[Dict],
        language: str
    ) -> Dict:
        """
        Gera resposta baseada em regras (modo offline)
        
        Args:
            user_message: Mensagem do usuário
            context: Contexto
            language: Idioma
        
        Returns:
            Resposta estruturada
        """
        message_lower = user_message.lower()
        
        # Regras de resposta por idioma
        responses = {
            'pt': {
                'greeting': 'Olá! Como posso ajudar com seu documento LaTeX?',
                'help': 'Posso ajudar com:\n- Inserir snippets\n- Compilar documento\n- Verificar erros (lint)\n- Gerar BibTeX\n- Aplicar refatorações',
                'compile': 'Para compilar, use o botão "Compilar" ou envie o comando "compilar"',
                'bibtex': 'Para gerar BibTeX, use: "gerar bibtex para [descrição]"',
                'lint': 'Para verificar erros, use o botão "Lint" no painel lateral',
                'unknown': 'Desculpe, não entendi. Digite "ajuda" para ver o que posso fazer.'
            },
            'en': {
                'greeting': 'Hello! How can I help with your LaTeX document?',
                'help': 'I can help with:\n- Insert snippets\n- Compile document\n- Check errors (lint)\n- Generate BibTeX\n- Apply refactoring',
                'compile': 'To compile, use the "Compile" button or send the "compile" command',
                'bibtex': 'To generate BibTeX, use: "generate bibtex for [description]"',
                'lint': 'To check errors, use the "Lint" button in the side panel',
                'unknown': 'Sorry, I didn\'t understand. Type "help" to see what I can do.'
            },
            'es': {
                'greeting': '¡Hola! ¿Cómo puedo ayudar con su documento LaTeX?',
                'help': 'Puedo ayudar con:\n- Insertar snippets\n- Compilar documento\n- Verificar errores (lint)\n- Generar BibTeX\n- Aplicar refactorizaciones',
                'compile': 'Para compilar, use el botón "Compilar" o envíe el comando "compilar"',
                'bibtex': 'Para generar BibTeX, use: "generar bibtex para [descripción]"',
                'lint': 'Para verificar errores, use el botón "Lint" en el panel lateral',
                'unknown': 'Lo siento, no entendí. Escriba "ayuda" para ver qué puedo hacer.'
            }
        }
        
        lang_responses = responses.get(language, responses['pt'])
        
        # Detectar intenção
        if any(word in message_lower for word in ['olá', 'oi', 'hello', 'hi', 'hola']):
            return {
                'text': lang_responses['greeting'],
                'actions': [],
                'source': 'rules',
                'confidence': 1.0
            }
        
        elif any(word in message_lower for word in ['ajuda', 'help', 'ayuda', 'o que', 'what can']):
            return {
                'text': lang_responses['help'],
                'actions': [],
                'source': 'rules',
                'confidence': 1.0
            }
        
        elif any(word in message_lower for word in ['compilar', 'compile', 'compilación']):
            return {
                'text': lang_responses['compile'],
                'actions': [{'type': 'suggest_compile'}],
                'source': 'rules',
                'confidence': 0.9
            }
        
        elif any(word in message_lower for word in ['bibtex', 'citação', 'citation', 'referência']):
            return {
                'text': lang_responses['bibtex'],
                'actions': [{'type': 'suggest_bibtex'}],
                'source': 'rules',
                'confidence': 0.9
            }
        
        elif any(word in message_lower for word in ['lint', 'erros', 'errors', 'verificar', 'check']):
            return {
                'text': lang_responses['lint'],
                'actions': [{'type': 'suggest_lint'}],
                'source': 'rules',
                'confidence': 0.9
            }
        
        else:
            return {
                'text': lang_responses['unknown'],
                'actions': [],
                'source': 'rules',
                'confidence': 0.3
            }
    
    def _llm_response(
        self, 
        user_message: str,
        context: Optional[Dict],
        language: str
    ) -> Dict:
        """
        Gera resposta usando LLM externo
        
        Args:
            user_message: Mensagem do usuário
            context: Contexto
            language: Idioma
        
        Returns:
            Resposta estruturada
        """
        if not self.is_enabled():
            # Fallback para regras
            return self._rules_based_response(user_message, context, language)
        
        # TODO: Implementar chamada para LLM real
        # Exemplo para OpenAI:
        """
        if self.provider == LLMProvider.OPENAI:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a LaTeX assistant. Respond in {language}."},
                    {"role": "user", "content": user_message}
                ]
            )
            
            return {
                'text': response.choices[0].message.content,
                'actions': [],  # Parsear ações da resposta
                'source': 'llm',
                'confidence': 1.0
            }
        """
        
        # Por enquanto, retorna mensagem indicando que LLM não está implementado
        fallback_messages = {
            'pt': 'LLM configurado mas não implementado. Usando modo baseado em regras.',
            'en': 'LLM configured but not implemented. Using rules-based mode.',
            'es': 'LLM configurado pero no implementado. Usando modo basado en reglas.'
        }
        
        response = self._rules_based_response(user_message, context, language)
        response['text'] = fallback_messages.get(language, fallback_messages['pt']) + '\n\n' + response['text']
        return response

# Instância global
_llm_client = None

def get_llm_client() -> LLMClient:
    """Retorna instância global do cliente LLM"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

def is_llm_enabled() -> bool:
    """Verifica se LLM está habilitado"""
    return get_llm_client().is_enabled()







