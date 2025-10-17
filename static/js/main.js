/**
 * CHAT COLABORATIVO - JavaScript Principal
 */

// ============================================================================
// SISTEMA DE TOAST NOTIFICATIONS
// ============================================================================

function showToast(message, type = 'info', title = '') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast show`;
    toast.setAttribute('role', 'alert');
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    const titles = {
        success: title || 'Sucesso',
        error: title || 'Erro',
        warning: title || 'Atenção',
        info: title || 'Informação'
    };
    
    const bgColors = {
        success: 'bg-success',
        error: 'bg-danger',
        warning: 'bg-warning',
        info: 'bg-info'
    };
    
    toast.innerHTML = `
        <div class="toast-header ${bgColors[type]} text-white">
            <strong class="me-auto">${icons[type]} ${titles[type]}</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    container.appendChild(toast);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        const bsToast = new bootstrap.Toast(toast);
        bsToast.hide();
        setTimeout(() => toast.remove(), 500);
    }, 5000);
}

// ============================================================================
// UTILITÁRIOS
// ============================================================================

function formatTimestamp(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (seconds < 60) {
        return 'Agora';
    } else if (minutes < 60) {
        return `${minutes}min atrás`;
    } else if (hours < 24) {
        return `${hours}h atrás`;
    } else if (days === 1) {
        return 'Ontem';
    } else if (days < 7) {
        return `${days} dias atrás`;
    } else {
        return date.toLocaleDateString('pt-BR');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================================
// BUSCA DE GRUPOS
// ============================================================================

const searchInput = document.getElementById('searchGroups');
if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        const groups = document.querySelectorAll('.group-item');
        
        groups.forEach(group => {
            const name = group.querySelector('h6').textContent.toLowerCase();
            if (name.includes(query)) {
                group.style.display = 'block';
            } else {
                group.style.display = 'none';
            }
        });
    });
}

// ============================================================================
// NOTIFICAÇÃO DE TÍTULO
// ============================================================================

let originalTitle = document.title;
let newMessagesCount = 0;
let titleInterval = null;

function notifyNewMessage() {
    newMessagesCount++;
    updatePageTitle();
}

function updatePageTitle() {
    if (newMessagesCount > 0) {
        if (!titleInterval) {
            let showAlert = true;
            titleInterval = setInterval(() => {
                document.title = showAlert ? `(${newMessagesCount}) Nova${newMessagesCount > 1 ? 's' : ''} mensagem${newMessagesCount > 1 ? 'ns' : ''}!` : originalTitle;
                showAlert = !showAlert;
            }, 1000);
        }
    } else {
        clearInterval(titleInterval);
        titleInterval = null;
        document.title = originalTitle;
    }
}

// Resetar contador quando a janela estiver focada
window.addEventListener('focus', () => {
    newMessagesCount = 0;
    updatePageTitle();
});

// ============================================================================
// MOBILE MENU
// ============================================================================

function toggleSidebar() {
    const sidebar = document.querySelector('.chat-sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

function toggleMembersPanel() {
    const panel = document.getElementById('membersPanel');
    if (panel) {
        panel.classList.toggle('open');
    }
}

// ============================================================================
// TECLADO ATALHOS
// ============================================================================

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K = Foco no campo de busca
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('searchGroups');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape = Fechar modals/painéis
    if (e.key === 'Escape') {
        const membersPanel = document.getElementById('membersPanel');
        if (membersPanel && membersPanel.style.display !== 'none') {
            toggleMembersPanel();
        }
    }
});

// ============================================================================
// INICIALIZAÇÃO
// ============================================================================

console.log('✅ Chat Colaborativo carregado');
console.log('📍 Versão 1.0 - Flask + SQLite');
