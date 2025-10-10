/**
 * Gerenciador de Árvore de Arquivos do Projeto
 * DocCollab - Editor LaTeX Profissional
 */

class FileTreeManager {
    constructor(projectId, containerId) {
        this.projectId = projectId;
        this.container = document.getElementById(containerId);
        this.files = [];
        this.folders = [];
        this.selectedFile = null;
        this.onFileSelect = null; // Callback quando arquivo é selecionado
        this.onFileCreate = null; // Callback quando arquivo é criado
        this.onFolderCreate = null; // Callback quando pasta é criada
        
        this.init();
    }
    
    init() {
        this.loadFiles();
        this.setupEventListeners();
    }
    
    async loadFiles() {
        try {
            const response = await fetch(`/api/project/${this.projectId}/files`);
            const data = await response.json();
            
            if (data.success) {
                this.files = data.files;
                this.folders = data.folders;
                this.render();
            } else {
                console.error('Erro ao carregar arquivos:', data.error);
            }
        } catch (error) {
            console.error('Erro ao carregar arquivos:', error);
        }
    }
    
    render() {
        if (!this.container) return;
        
        // Construir árvore hierárquica
        const tree = this.buildTree();
        
        // Renderizar HTML
        this.container.innerHTML = `
            <div class="file-tree">
                <div class="file-tree-header">
                    <h3>Arquivos</h3>
                    <div class="file-tree-actions">
                        <button class="btn-icon" id="newFileBtn" title="Novo Arquivo">
                            <i class="fas fa-file-plus"></i>
                        </button>
                        <button class="btn-icon" id="newFolderBtn" title="Nova Pasta">
                            <i class="fas fa-folder-plus"></i>
                        </button>
                        <button class="btn-icon" id="uploadFileBtn" title="Upload">
                            <i class="fas fa-upload"></i>
                        </button>
                        <button class="btn-icon" id="downloadProjectBtn" title="Download ZIP">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
                <div class="file-tree-content">
                    ${this.renderTree(tree)}
                </div>
            </div>
        `;
        
        this.attachTreeEventListeners();
    }
    
    buildTree() {
        // Criar estrutura de árvore
        const tree = {
            folders: [],
            files: []
        };
        
        // Organizar pastas por parent_id
        const folderMap = new Map();
        this.folders.forEach(folder => {
            if (!folderMap.has(folder.parent_id)) {
                folderMap.set(folder.parent_id, []);
            }
            folderMap.get(folder.parent_id).push({
                ...folder,
                folders: [],
                files: []
            });
        });
        
        // Construir hierarquia de pastas
        const buildFolderHierarchy = (parentId) => {
            const children = folderMap.get(parentId) || [];
            children.forEach(folder => {
                folder.folders = buildFolderHierarchy(folder.id);
                folder.files = this.files.filter(f => f.folder_id === folder.id);
            });
            return children;
        };
        
        tree.folders = buildFolderHierarchy(null);
        tree.files = this.files.filter(f => !f.folder_id);
        
        return tree;
    }
    
    renderTree(tree, level = 0) {
        let html = '<ul class="file-tree-list">';
        
        // Renderizar pastas
        tree.folders.forEach(folder => {
            html += `
                <li class="file-tree-item folder" data-folder-id="${folder.id}">
                    <div class="file-tree-item-content" style="padding-left: ${level * 20}px">
                        <i class="fas fa-folder folder-icon"></i>
                        <span class="file-tree-item-name">${this.escapeHtml(folder.name)}</span>
                        <div class="file-tree-item-actions">
                            <button class="btn-icon-small" data-action="rename" title="Renomear">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-icon-small" data-action="delete" title="Excluir">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                    ${folder.folders.length > 0 || folder.files.length > 0 ? 
                        this.renderTree(folder, level + 1) : ''}
                </li>
            `;
        });
        
        // Renderizar arquivos
        tree.files.forEach(file => {
            const icon = this.getFileIcon(file.type);
            const isSelected = this.selectedFile && this.selectedFile.id === file.id;
            
            html += `
                <li class="file-tree-item file ${isSelected ? 'selected' : ''}" data-file-id="${file.id}">
                    <div class="file-tree-item-content" style="padding-left: ${level * 20}px">
                        <i class="${icon} file-icon"></i>
                        <span class="file-tree-item-name">${this.escapeHtml(file.name)}</span>
                        <span class="file-tree-item-meta">v${file.version}</span>
                        <div class="file-tree-item-actions">
                            <button class="btn-icon-small" data-action="copy" title="Copiar">
                                <i class="fas fa-copy"></i>
                            </button>
                            <button class="btn-icon-small" data-action="rename" title="Renomear">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-icon-small" data-action="download" title="Download">
                                <i class="fas fa-download"></i>
                            </button>
                            <button class="btn-icon-small" data-action="delete" title="Excluir">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </li>
            `;
        });
        
        html += '</ul>';
        return html;
    }
    
    getFileIcon(fileType) {
        const icons = {
            'tex': 'fas fa-file-code',
            'bib': 'fas fa-book',
            'pdf': 'fas fa-file-pdf',
            'png': 'fas fa-file-image',
            'jpg': 'fas fa-file-image',
            'jpeg': 'fas fa-file-image',
            'gif': 'fas fa-file-image',
            'svg': 'fas fa-file-image',
            'txt': 'fas fa-file-alt',
            'md': 'fas fa-file-alt'
        };
        return icons[fileType] || 'fas fa-file';
    }
    
    setupEventListeners() {
        // Event listeners para botões principais
        document.addEventListener('click', (e) => {
            if (e.target.closest('#newFileBtn')) {
                this.showNewFileDialog();
            } else if (e.target.closest('#newFolderBtn')) {
                this.showNewFolderDialog();
            } else if (e.target.closest('#uploadFileBtn')) {
                this.showUploadDialog();
            } else if (e.target.closest('#downloadProjectBtn')) {
                this.downloadProject();
            }
        });
    }
    
    attachTreeEventListeners() {
        // Event listeners para itens da árvore
        this.container.querySelectorAll('.file-tree-item.file').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.file-tree-item-actions')) {
                    const fileId = parseInt(item.dataset.fileId);
                    this.selectFile(fileId);
                }
            });
        });
        
        // Event listeners para ações
        this.container.querySelectorAll('[data-action]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const action = btn.dataset.action;
                const item = btn.closest('.file-tree-item');
                
                if (item.classList.contains('file')) {
                    const fileId = parseInt(item.dataset.fileId);
                    this.handleFileAction(action, fileId);
                } else if (item.classList.contains('folder')) {
                    const folderId = parseInt(item.dataset.folderId);
                    this.handleFolderAction(action, folderId);
                }
            });
        });
        
        // Toggle de pastas
        this.container.querySelectorAll('.file-tree-item.folder > .file-tree-item-content').forEach(content => {
            content.addEventListener('click', (e) => {
                if (!e.target.closest('.file-tree-item-actions')) {
                    const folder = content.closest('.file-tree-item.folder');
                    folder.classList.toggle('collapsed');
                }
            });
        });
    }
    
    selectFile(fileId) {
        const file = this.files.find(f => f.id === fileId);
        if (file) {
            this.selectedFile = file;
            
            // Atualizar UI
            this.container.querySelectorAll('.file-tree-item.file').forEach(item => {
                item.classList.remove('selected');
            });
            this.container.querySelector(`[data-file-id="${fileId}"]`)?.classList.add('selected');
            
            // Callback
            if (this.onFileSelect) {
                this.onFileSelect(file);
            }
        }
    }
    
    async handleFileAction(action, fileId) {
        const file = this.files.find(f => f.id === fileId);
        if (!file) return;
        
        switch (action) {
            case 'copy':
                await this.copyFile(fileId);
                break;
            case 'rename':
                await this.renameFile(fileId);
                break;
            case 'download':
                await this.downloadFile(fileId);
                break;
            case 'delete':
                await this.deleteFile(fileId);
                break;
        }
    }
    
    async handleFolderAction(action, folderId) {
        switch (action) {
            case 'rename':
                await this.renameFolder(folderId);
                break;
            case 'delete':
                await this.deleteFolder(folderId);
                break;
        }
    }
    
    showNewFileDialog() {
        const fileName = prompt('Nome do arquivo (ex: capitulo1.tex):');
        if (fileName) {
            this.createFile(fileName);
        }
    }
    
    showNewFolderDialog() {
        const folderName = prompt('Nome da pasta (ex: imagens):');
        if (folderName) {
            this.createFolder(folderName);
        }
    }
    
    showUploadDialog() {
        const input = document.createElement('input');
        input.type = 'file';
        input.multiple = true;
        input.accept = '.tex,.bib,.png,.jpg,.jpeg,.pdf,.txt,.md';
        
        input.onchange = async (e) => {
            const files = Array.from(e.target.files);
            for (const file of files) {
                await this.uploadFile(file);
            }
        };
        
        input.click();
    }
    
    async createFile(fileName, content = '') {
        try {
            const response = await fetch(`/api/project/${this.projectId}/file`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: fileName,
                    content: content
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadFiles();
                if (this.onFileCreate) {
                    this.onFileCreate(data.file);
                }
            } else {
                alert('Erro ao criar arquivo: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao criar arquivo:', error);
            alert('Erro ao criar arquivo');
        }
    }
    
    async createFolder(folderName, parentId = null) {
        try {
            const response = await fetch(`/api/project/${this.projectId}/folder`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: folderName,
                    parent_id: parentId
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadFiles();
                if (this.onFolderCreate) {
                    this.onFolderCreate(data.folder);
                }
            } else {
                alert('Erro ao criar pasta: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao criar pasta:', error);
            alert('Erro ao criar pasta');
        }
    }
    
    async uploadFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`/api/project/${this.projectId}/upload`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadFiles();
                alert(`Arquivo "${file.name}" enviado com sucesso!`);
            } else {
                alert('Erro ao enviar arquivo: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao enviar arquivo:', error);
            alert('Erro ao enviar arquivo');
        }
    }
    
    async copyFile(fileId) {
        const file = this.files.find(f => f.id === fileId);
        if (!file) return;
        
        const newName = prompt('Nome da cópia:', `${file.name.split('.')[0]}_copy.${file.name.split('.')[1]}`);
        if (!newName) return;
        
        try {
            const response = await fetch(`/api/project/${this.projectId}/file/${fileId}/copy`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: newName
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadFiles();
            } else {
                alert('Erro ao copiar arquivo: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao copiar arquivo:', error);
            alert('Erro ao copiar arquivo');
        }
    }
    
    async renameFile(fileId) {
        const file = this.files.find(f => f.id === fileId);
        if (!file) return;
        
        const newName = prompt('Novo nome:', file.name);
        if (!newName || newName === file.name) return;
        
        try {
            const response = await fetch(`/api/project/${this.projectId}/file/${fileId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: newName
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadFiles();
            } else {
                alert('Erro ao renomear arquivo: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao renomear arquivo:', error);
            alert('Erro ao renomear arquivo');
        }
    }
    
    async downloadFile(fileId) {
        window.open(`/api/project/${this.projectId}/file/${fileId}`, '_blank');
    }
    
    async deleteFile(fileId) {
        const file = this.files.find(f => f.id === fileId);
        if (!file) return;
        
        if (!confirm(`Deseja realmente excluir "${file.name}"?`)) return;
        
        try {
            const response = await fetch(`/api/project/${this.projectId}/file/${fileId}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadFiles();
            } else {
                alert('Erro ao excluir arquivo: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao excluir arquivo:', error);
            alert('Erro ao excluir arquivo');
        }
    }
    
    async renameFolder(folderId) {
        const folder = this.folders.find(f => f.id === folderId);
        if (!folder) return;
        
        const newName = prompt('Novo nome:', folder.name);
        if (!newName || newName === folder.name) return;
        
        // TODO: Implementar renomear pasta
        alert('Funcionalidade em desenvolvimento');
    }
    
    async deleteFolder(folderId) {
        const folder = this.folders.find(f => f.id === folderId);
        if (!folder) return;
        
        if (!confirm(`Deseja realmente excluir a pasta "${folder.name}" e todo seu conteúdo?`)) return;
        
        try {
            const response = await fetch(`/api/project/${this.projectId}/folder/${folderId}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.success) {
                await this.loadFiles();
            } else {
                alert('Erro ao excluir pasta: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao excluir pasta:', error);
            alert('Erro ao excluir pasta');
        }
    }
    
    async downloadProject() {
        window.location.href = `/api/project/${this.projectId}/download`;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Exportar para uso global
window.FileTreeManager = FileTreeManager;
