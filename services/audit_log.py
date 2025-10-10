"""
Sistema de auditoria e logs estruturados
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, Any
from enum import Enum

class AuditEventType(Enum):
    """Tipos de eventos auditados"""
    # Ações do assistente
    SNIPPET_INSERT = "snippet_insert"
    PATCH_APPLY = "patch_apply"
    REFACTOR = "refactor"
    COMPILE = "compile"
    LINT = "lint"
    BIBTEX_GENERATE = "bibtex_generate"
    
    # Segurança
    DANGEROUS_COMMAND_BLOCKED = "dangerous_command_blocked"
    PERMISSION_DENIED = "permission_denied"
    CONFLICT_DETECTED = "conflict_detected"
    
    # Autenticação/Autorização
    LOGIN = "login"
    LOGOUT = "logout"
    PERMISSION_GRANT = "permission_grant"
    PERMISSION_REVOKE = "permission_revoke"
    
    # Sistema
    ERROR = "error"
    WARNING = "warning"

class AuditLogger:
    """Logger de auditoria com saída JSON estruturada"""
    
    def __init__(self, log_dir: str = None):
        """
        Inicializa o logger
        
        Args:
            log_dir: Diretório para logs (padrão: logs/)
        """
        if log_dir is None:
            # Diretório padrão relativo ao app
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Arquivo de log por dia
        self.current_date = datetime.utcnow().date()
        self.log_file = self._get_log_file()
    
    def _get_log_file(self) -> str:
        """Retorna caminho do arquivo de log do dia"""
        filename = f"audit_{self.current_date.isoformat()}.jsonl"
        return os.path.join(self.log_dir, filename)
    
    def _rotate_if_needed(self):
        """Rotaciona log se mudou de dia"""
        current_date = datetime.utcnow().date()
        if current_date != self.current_date:
            self.current_date = current_date
            self.log_file = self._get_log_file()
    
    def record(
        self, 
        event_type: AuditEventType,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error: Optional[str] = None,
        ip_address: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """
        Registra evento de auditoria
        
        Args:
            event_type: Tipo do evento
            user_id: ID do usuário (se aplicável)
            action: Descrição da ação
            details: Detalhes adicionais
            success: Se a ação foi bem-sucedida
            error: Mensagem de erro (se houver)
            ip_address: IP do cliente
            session_id: ID da sessão
        """
        self._rotate_if_needed()
        
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event_type': event_type.value,
            'user_id': user_id,
            'action': action,
            'success': success,
            'details': details or {},
            'error': error,
            'ip_address': ip_address,
            'session_id': session_id
        }
        
        # Escrever como JSON Lines (uma linha por evento)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False)
            f.write('\n')
    
    def record_assistant_action(
        self,
        action_type: str,
        user_id: Optional[int],
        payload: Dict,
        success: bool,
        result: Optional[Dict] = None,
        error: Optional[str] = None,
        ip_address: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """
        Registra ação do assistente virtual
        
        Args:
            action_type: Tipo da ação (insert_snippet, compile, etc.)
            user_id: ID do usuário
            payload: Payload da ação
            success: Se foi bem-sucedida
            result: Resultado da ação
            error: Mensagem de erro
            ip_address: IP do cliente
            session_id: ID da sessão SocketIO
        """
        # Mapear action_type para AuditEventType
        event_map = {
            'insert_snippet': AuditEventType.SNIPPET_INSERT,
            'apply_patch': AuditEventType.PATCH_APPLY,
            'suggest_refactors': AuditEventType.REFACTOR,
            'compile': AuditEventType.COMPILE,
            'lint': AuditEventType.LINT,
            'generate_bibtex': AuditEventType.BIBTEX_GENERATE
        }
        
        event_type = event_map.get(action_type, AuditEventType.WARNING)
        
        details = {
            'action_type': action_type,
            'payload_summary': self._sanitize_payload(payload),
            'result_summary': self._sanitize_result(result) if result else None
        }
        
        self.record(
            event_type=event_type,
            user_id=user_id,
            action=f"Assistant: {action_type}",
            details=details,
            success=success,
            error=error,
            ip_address=ip_address,
            session_id=session_id
        )
    
    def record_security_event(
        self,
        event_type: AuditEventType,
        user_id: Optional[int],
        reason: str,
        details: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        """
        Registra evento de segurança
        
        Args:
            event_type: Tipo do evento de segurança
            user_id: ID do usuário
            reason: Razão do bloqueio/alerta
            details: Detalhes adicionais
            ip_address: IP do cliente
            session_id: ID da sessão
        """
        self.record(
            event_type=event_type,
            user_id=user_id,
            action=f"Security: {reason}",
            details=details or {},
            success=False,
            error=reason,
            ip_address=ip_address,
            session_id=session_id
        )
    
    def _sanitize_payload(self, payload: Dict) -> Dict:
        """Remove dados sensíveis do payload para log"""
        sanitized = {}
        
        # Campos permitidos para log
        safe_fields = ['action_type', 'filename', 'entry_type', 'description', 'lang']
        
        for key in safe_fields:
            if key in payload:
                sanitized[key] = payload[key]
        
        # Adicionar tamanho do conteúdo (mas não o conteúdo)
        if 'content' in payload:
            sanitized['content_size'] = len(payload['content'])
        
        if 'snippet' in payload:
            sanitized['snippet_size'] = len(payload['snippet'])
        
        return sanitized
    
    def _sanitize_result(self, result: Dict) -> Dict:
        """Remove dados sensíveis do resultado para log"""
        sanitized = {}
        
        # Campos permitidos
        safe_fields = ['success', 'key', 'entry_type', 'has_conflict', 'message']
        
        for key in safe_fields:
            if key in result:
                sanitized[key] = result[key]
        
        # Resumo de issues/errors
        if 'issues' in result:
            sanitized['issues_count'] = len(result['issues'])
        
        if 'errors' in result:
            sanitized['errors_count'] = len(result['errors'])
        
        return sanitized
    
    def query_logs(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        user_id: Optional[int] = None,
        event_type: Optional[AuditEventType] = None,
        limit: int = 100
    ) -> list:
        """
        Consulta logs de auditoria
        
        Args:
            start_date: Data inicial
            end_date: Data final
            user_id: Filtrar por usuário
            event_type: Filtrar por tipo de evento
            limit: Máximo de resultados
        
        Returns:
            Lista de eventos
        """
        events = []
        
        # Determinar arquivos a ler
        if start_date and end_date:
            # Ler múltiplos dias
            current = start_date.date()
            end = end_date.date()
            files_to_read = []
            
            while current <= end:
                filename = f"audit_{current.isoformat()}.jsonl"
                filepath = os.path.join(self.log_dir, filename)
                if os.path.exists(filepath):
                    files_to_read.append(filepath)
                current = current.replace(day=current.day + 1)
        else:
            # Ler apenas arquivo atual
            files_to_read = [self.log_file] if os.path.exists(self.log_file) else []
        
        # Ler e filtrar eventos
        for filepath in files_to_read:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    event = json.loads(line)
                    
                    # Aplicar filtros
                    if user_id and event.get('user_id') != user_id:
                        continue
                    
                    if event_type and event.get('event_type') != event_type.value:
                        continue
                    
                    events.append(event)
                    
                    if len(events) >= limit:
                        return events
        
        return events

# Instância global
_audit_logger = None

def get_audit_logger() -> AuditLogger:
    """Retorna instância global do logger"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger



