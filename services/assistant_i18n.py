"""
Sistema de internacionalização para mensagens do assistente
"""

MESSAGES = {
    # Ações confirmadas
    'action_confirmed': {
        'pt': 'Ação {action_type} confirmada com sucesso',
        'en': 'Action {action_type} confirmed successfully',
        'es': 'Acción {action_type} confirmada con éxito'
    },
    
    # Erros de segurança
    'dangerous_command': {
        'pt': 'Comando perigoso detectado: {pattern}',
        'en': 'Dangerous command detected: {pattern}',
        'es': 'Comando peligroso detectado: {pattern}'
    },
    
    'snippet_too_large': {
        'pt': 'Snippet muito grande (máx {max_size}KB)',
        'en': 'Snippet too large (max {max_size}KB)',
        'es': 'Snippet demasiado grande (máx {max_size}KB)'
    },
    
    'user_not_authenticated': {
        'pt': 'Usuário não autenticado',
        'en': 'User not authenticated',
        'es': 'Usuario no autenticado'
    },
    
    'action_not_permitted': {
        'pt': 'Ação \'{action_type}\' não permitida',
        'en': 'Action \'{action_type}\' not permitted',
        'es': 'Acción \'{action_type}\' no permitida'
    },
    
    'no_permission': {
        'pt': 'Você não tem permissão para esta ação',
        'en': 'You don\'t have permission for this action',
        'es': 'No tienes permiso para esta acción'
    },
    
    # Conflitos
    'conflict_detected': {
        'pt': 'Conflito detectado: documento foi modificado',
        'en': 'Conflict detected: document was modified',
        'es': 'Conflicto detectado: documento fue modificado'
    },
    
    'snapshot_mismatch': {
        'pt': 'Versões do documento não coincidem',
        'en': 'Document versions do not match',
        'es': 'Las versiones del documento no coinciden'
    },
    
    # Compilação
    'compilation_success': {
        'pt': 'Compilação bem-sucedida',
        'en': 'Compilation successful',
        'es': 'Compilación exitosa'
    },
    
    'compilation_success_warnings': {
        'pt': 'Compilação bem-sucedida com {count} avisos',
        'en': 'Compilation successful with {count} warnings',
        'es': 'Compilación exitosa con {count} advertencias'
    },
    
    'compilation_failed': {
        'pt': 'Compilação falhou com {count} erros',
        'en': 'Compilation failed with {count} errors',
        'es': 'Compilación falló con {count} errores'
    },
    
    'compilation_timeout': {
        'pt': 'Timeout na compilação (máximo {seconds} segundos)',
        'en': 'Compilation timeout (maximum {seconds} seconds)',
        'es': 'Tiempo de espera de compilación agotado (máximo {seconds} segundos)'
    },
    
    'pdflatex_not_found': {
        'pt': 'pdflatex não encontrado. Instale o LaTeX no sistema.',
        'en': 'pdflatex not found. Install LaTeX on the system.',
        'es': 'pdflatex no encontrado. Instale LaTeX en el sistema.'
    },
    
    # Rate limiting
    'rate_limited': {
        'pt': 'Aguarde {seconds} segundos entre compilações',
        'en': 'Wait {seconds} seconds between compilations',
        'es': 'Espere {seconds} segundos entre compilaciones'
    },
    
    # Lint
    'lint_complete': {
        'pt': 'Lint completo: {total} issues encontrados',
        'en': 'Lint complete: {total} issues found',
        'es': 'Lint completo: {total} problemas encontrados'
    },
    
    'lint_error': {
        'pt': 'Erro ao executar lint: {error}',
        'en': 'Error running lint: {error}',
        'es': 'Error al ejecutar lint: {error}'
    },
    
    # BibTeX
    'bibtex_generated': {
        'pt': 'BibTeX gerado com sucesso: {key}',
        'en': 'BibTeX generated successfully: {key}',
        'es': 'BibTeX generado con éxito: {key}'
    },
    
    'bibtex_description_required': {
        'pt': 'Forneça uma descrição para gerar BibTeX',
        'en': 'Provide a description to generate BibTeX',
        'es': 'Proporcione una descripción para generar BibTeX'
    },
    
    'bibtex_error': {
        'pt': 'Erro ao gerar BibTeX: {error}',
        'en': 'Error generating BibTeX: {error}',
        'es': 'Error al generar BibTeX: {error}'
    },
    
    # Patches/Refatorações
    'patch_rejected': {
        'pt': 'Patch rejeitado: {reason}',
        'en': 'Patch rejected: {reason}',
        'es': 'Parche rechazado: {reason}'
    },
    
    'patch_applied': {
        'pt': 'Patch aplicado com sucesso',
        'en': 'Patch applied successfully',
        'es': 'Parche aplicado con éxito'
    },
    
    'refactors_found': {
        'pt': '{count} sugestões de refatoração encontradas',
        'en': '{count} refactoring suggestions found',
        'es': '{count} sugerencias de refactorización encontradas'
    },
    
    # Snippets
    'snippet_not_found': {
        'pt': 'Snippet "{snippet_id}" não encontrado',
        'en': 'Snippet "{snippet_id}" not found',
        'es': 'Snippet "{snippet_id}" no encontrado'
    },
    
    'snippet_not_specified': {
        'pt': 'Snippet não especificado',
        'en': 'Snippet not specified',
        'es': 'Snippet no especificado'
    },
    
    # Genérico
    'internal_error': {
        'pt': 'Erro interno: {error}',
        'en': 'Internal error: {error}',
        'es': 'Error interno: {error}'
    },
    
    'processing_action': {
        'pt': 'Processando ação...',
        'en': 'Processing action...',
        'es': 'Procesando acción...'
    },
    
    'empty_content': {
        'pt': 'Conteúdo vazio',
        'en': 'Empty content',
        'es': 'Contenido vacío'
    }
}

def get_message(key: str, lang: str = 'pt', **kwargs) -> str:
    """
    Obtém mensagem traduzida
    
    Args:
        key: Chave da mensagem
        lang: Idioma (pt, en, es)
        **kwargs: Parâmetros para formatação
    
    Returns:
        Mensagem traduzida e formatada
    """
    if key not in MESSAGES:
        return f"[Missing translation: {key}]"
    
    translations = MESSAGES[key]
    
    # Usar idioma solicitado ou fallback para português
    if lang not in translations:
        lang = 'pt'
    
    message = translations[lang]
    
    # Formatar com parâmetros se fornecidos
    if kwargs:
        try:
            message = message.format(**kwargs)
        except KeyError as e:
            return f"[Translation error: missing parameter {e}]"
    
    return message

def get_available_languages() -> list:
    """Retorna lista de idiomas disponíveis"""
    return ['pt', 'en', 'es']

def detect_language(payload: dict, default: str = 'pt') -> str:
    """
    Detecta idioma a partir do payload
    
    Args:
        payload: Dados da requisição
        default: Idioma padrão
    
    Returns:
        Código do idioma (pt, en, es)
    """
    # Tentar obter do payload
    lang = payload.get('lang') or payload.get('language')
    
    if lang and lang in get_available_languages():
        return lang
    
    return default







