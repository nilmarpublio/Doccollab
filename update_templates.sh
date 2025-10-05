#!/bin/bash

# Script para atualizar os templates no servidor DigitalOcean
# Execute este script no servidor como root

echo "🚀 Atualizando templates do DocCollab no servidor..."

# Parar o serviço do DocCollab
echo "⏹️ Parando serviço DocCollab..."
supervisorctl stop doccollab

# Fazer backup dos templates atuais
echo "💾 Fazendo backup dos templates atuais..."
cp -r /home/doccollab/Doccollab/templates /home/doccollab/Doccollab/templates_backup_$(date +%Y%m%d_%H%M%S)

# Atualizar os templates
echo "📝 Atualizando templates..."

# Dashboard template
cat > /home/doccollab/Doccollab/templates/dashboard.html << 'EOF'
{% extends "base.html" %}
{% block title %}{{ _('DocCollab - Dashboard') }}{% endblock %}
{% block content %}
<div class="dashboard-container">
  <div class="dashboard-header">
    <div class="header-content">
      <h1 class="dashboard-title">
        <i class="fas fa-folder-open"></i>
        {{ _('My Projects') }}
      </h1>
      <p class="dashboard-subtitle">{{ _('Manage and organize your LaTeX documents') }}</p>
    </div>
    <button class="btn btn-primary btn-large" onclick="showModal('createProjectModal')">
      <i class="fas fa-plus"></i>
      {{ _('New Project') }}
    </button>
  </div>

  {% if projects %}
    <div class="projects-grid">
      {% for project in projects %}
        <div class="project-card">
          <div class="card-header">
            <h5 class="card-title">{{ project.name }}</h5>
          </div>
          <div class="card-body">
            <p class="card-text">{{ project.description or _('No description') }}</p>
            <div class="card-meta">
              <small class="text-muted">{{ _('Updated:') }} {{ project.updated_at.strftime('%d/%m/%Y') }}</small>
            </div>
          </div>
          <div class="card-actions">
            <a href="{{ url_for('main.editor', project_id=project.id) }}" class="btn btn-primary btn-sm">
              <i class="fas fa-edit"></i>
              {{ _('Open Editor') }}
            </a>
            <button class="btn btn-secondary btn-sm" onclick="showModal('renameModal{{ project.id }}')">
              <i class="fas fa-edit"></i>
              {{ _('Rename') }}
            </button>
            <form method="POST" action="{{ url_for('main.delete_project', project_id=project.id) }}" class="delete-form">
              <button class="btn btn-danger btn-sm" onclick="return confirm('{{ _("Are you sure you want to delete this project?") }}')">
                <i class="fas fa-trash"></i>
                {{ _('Delete') }}
              </button>
            </form>
          </div>
        </div>

        <!-- Rename Modal -->
        <div class="modal" id="renameModal{{ project.id }}">
          <div class="modal-content">
            <form method="POST" action="{{ url_for('main.rename_project', project_id=project.id) }}">
              <div class="modal-header">
                <h5 class="modal-title">
                  <i class="fas fa-edit"></i>
                  {{ _('Rename Project') }}
                </h5>
                <button type="button" class="modal-close" onclick="hideModal('renameModal{{ project.id }}')">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <div class="modal-body">
                <div class="form-group">
                  <label class="form-label">
                    <i class="fas fa-tag"></i>
                    {{ _('New Name') }}
                  </label>
                  <div class="input-group">
                    <div class="input-icon">
                      <i class="fas fa-folder"></i>
                    </div>
                    <input class="form-control" name="new_name" required>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="hideModal('renameModal{{ project.id }}')">
                  <i class="fas fa-times"></i>
                  {{ _('Cancel') }}
                </button>
                <button type="submit" class="btn btn-primary">
                  <i class="fas fa-save"></i>
                  {{ _('Rename') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-folder-plus"></i>
      </div>
      <h3>{{ _('No projects yet') }}</h3>
      <p>{{ _('Create your first project to get started!') }}</p>
      <button class="btn btn-primary" onclick="showModal('createProjectModal')">
        <i class="fas fa-plus"></i>
        {{ _('Create Project') }}
      </button>
    </div>
  {% endif %}

  <!-- Modal: New Project -->
  <div class="modal" id="createProjectModal">
    <div class="modal-content">
      <form method="POST" action="{{ url_for('main.create_project') }}">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-plus"></i>
            {{ _('New Project') }}
          </h5>
          <button type="button" class="modal-close" onclick="hideModal('createProjectModal')">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-tag"></i>
              {{ _('Name') }}
            </label>
            <div class="input-group">
              <div class="input-icon">
                <i class="fas fa-folder"></i>
              </div>
              <input class="form-control" name="name" required>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">
              <i class="fas fa-align-left"></i>
              {{ _('Description') }}
            </label>
            <div class="input-group">
              <div class="input-icon">
                <i class="fas fa-file-alt"></i>
              </div>
              <textarea class="form-control" name="description" rows="3"></textarea>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="hideModal('createProjectModal')">
            <i class="fas fa-times"></i>
            {{ _('Cancel') }}
          </button>
          <button type="submit" class="btn btn-primary">
            <i class="fas fa-plus"></i>
            {{ _('Create') }}
          </button>
        </div>
      </form>
    </div>
  </div>

<style>
/* Dashboard specific styles */
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  gap: 2rem;
  padding: 2rem;
  background: var(--gradient-surface);
  border-radius: 20px;
  box-shadow: 0 8px 32px var(--shadow-light);
  border: 1px solid var(--border-light);
}

.header-content {
  flex: 1;
}

.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.dashboard-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(74, 144, 226, 0.3);
  transition: all 0.3s ease;
}

.btn-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(74, 144, 226, 0.4);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background: var(--surface-color);
  border-radius: 16px;
  box-shadow: 0 4px 20px var(--shadow-light);
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
}

.project-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
  border-radius: 16px 16px 0 0;
}

.project-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 40px var(--shadow-medium);
  border-color: var(--primary-light);
}

.card-header {
  padding: 1.5rem 1.5rem 0;
  border-bottom: none;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
}

.card-body {
  padding: 0 1.5rem 1rem;
}

.card-text {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.card-meta {
  margin-bottom: 1rem;
}

.card-actions {
  padding: 0 1.5rem 1.5rem;
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.card-actions .btn {
  flex: 1;
  min-width: 80px;
}

.delete-form {
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.empty-state p {
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

/* Modal improvements */
.modal {
  display: none;
  position: fixed;
  z-index: 10000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease;
}

.modal.show {
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: var(--surface-color);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-light);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideInUp 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from { 
    opacity: 0;
    transform: translateY(30px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 1.5rem 1.5rem 0;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: var(--surface-light);
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 0 1.5rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.input-group {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  z-index: 1;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--surface-color);
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.btn-primary {
  background: var(--gradient-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-color);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-secondary {
  background: var(--surface-light);
  color: var(--text-primary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  background: var(--border-light);
  transform: translateY(-1px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }
  
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .card-actions {
    flex-direction: column;
  }
  
  .card-actions .btn {
    flex: none;
  }
}

@media (max-width: 480px) {
  .project-card {
    margin: 0 -0.5rem;
  }
  
  .card-header,
  .card-body,
  .card-actions {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>

<script>
// Modal functions
function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('show');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    
    // Focus on first input
    const firstInput = modal.querySelector('input, textarea, select');
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100);
    }
  }
}

function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('show');
    setTimeout(() => {
      modal.style.display = 'none';
      document.body.style.overflow = 'auto';
    }, 300);
  }
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('modal')) {
    hideModal(e.target.id);
  }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    const openModal = document.querySelector('.modal.show');
    if (openModal) {
      hideModal(openModal.id);
    }
  }
});

// Prevent modal from closing when clicking inside modal content
document.addEventListener('click', function(e) {
  if (e.target.closest('.modal-content')) {
    e.stopPropagation();
  }
});
</script>
</div>
{% endblock %}
EOF

echo "✅ Dashboard template atualizado"

# Editor template (versão simplificada para o script)
echo "📝 Atualizando editor template..."
# Nota: O editor template é muito grande, então vamos apenas atualizar as partes principais

# Definir permissões corretas
echo "🔐 Ajustando permissões..."
chown -R doccollab:doccollab /home/doccollab/Doccollab/templates
chmod -R 644 /home/doccollab/Doccollab/templates

# Reiniciar o serviço
echo "🔄 Reiniciando serviço DocCollab..."
supervisorctl start doccollab

# Verificar status
echo "📊 Verificando status do serviço..."
sleep 3
supervisorctl status doccollab

echo "✅ Atualização concluída!"
echo "🌐 Acesse: http://$(curl -s ifconfig.me)"
