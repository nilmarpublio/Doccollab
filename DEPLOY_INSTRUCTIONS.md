# 🚀 Instruções de Deploy - DigitalOcean

## 📋 Resumo das Mudanças

### ✅ Implementações Principais:
1. **API de Gerenciador de Arquivos** (`/api/open-file-manager`)
2. **Sidebar Simplificada** - Apenas Snippets LaTeX
3. **Botões de Ação** - Salvar, Novo e Nova Pasta abrem gerenciador
4. **Remoção de Traduções** - Simplificação dos templates
5. **Pasta Aplicativos** - Criada na raiz do sistema

---

## 🔧 Comandos para Deploy no DigitalOcean

### 1. Conectar via SSH
```bash
ssh root@64.23.136.220
```

### 2. Navegar para o diretório do projeto
```bash
cd /home/doccollab/Doccollab
```

### 3. Fazer backup (opcional mas recomendado)
```bash
sudo cp -r . ../doccollab_backup_$(date +%Y%m%d_%H%M%S)
```

### 4. Adicionar diretório como seguro
```bash
git config --global --add safe.directory /home/doccollab/Doccollab
```

### 5. Atualizar código do GitHub
```bash
git fetch origin
git checkout feature/payment-system
git pull origin feature/payment-system
```

### 6. Ativar ambiente virtual
```bash
source venv/bin/activate
```

### 7. Instalar/Atualizar dependências
```bash
pip install -r requirements.txt
```

### 8. Compilar arquivos Python
```bash
python -m py_compile app.py
python -m py_compile routes/main.py
```

### 9. Reiniciar serviço Supervisor
```bash
sudo supervisorctl restart doccollab
```

### 10. Verificar status
```bash
sudo supervisorctl status doccollab
```

### 11. Ver logs (se necessário)
```bash
sudo supervisorctl tail doccollab
sudo supervisorctl tail doccollab stderr
```

### 12. Testar acesso
```bash
curl -I http://localhost:5000/
```

---

## 🔍 Verificações Importantes

### ✅ Checklist Pós-Deploy:

- [ ] Serviço `doccollab` está rodando
- [ ] Não há erros nos logs
- [ ] Site acessível externamente
- [ ] Editor LaTeX carrega corretamente
- [ ] Botão "Compile" funciona
- [ ] Gerenciador de arquivos abre (se aplicável no servidor)
- [ ] Snippets LaTeX aparecem na sidebar

---

## 🐛 Troubleshooting

### Se o serviço não iniciar:
```bash
# Ver logs completos
sudo supervisorctl tail -f doccollab

# Verificar sintaxe Python
python -m py_compile app.py

# Reiniciar manualmente
sudo supervisorctl stop doccollab
sudo supervisorctl start doccollab
```

### Se houver erro de importação:
```bash
# Verificar pacotes instalados
pip list | grep -i flask

# Reinstalar requirements
pip install --upgrade -r requirements.txt
```

### Se o site não carregar:
```bash
# Verificar se está escutando na porta correta
netstat -tulpn | grep 5000

# Verificar firewall
sudo ufw status
sudo ufw allow 5000
```

---

## 📝 Notas Importantes

1. **Branch**: Estamos usando `feature/payment-system`
2. **Porta**: 5000 (configurada no app.py)
3. **Host**: 0.0.0.0 (para aceitar conexões externas)
4. **Supervisor**: Gerencia o processo do Flask
5. **Virtual Environment**: Sempre ativar antes de instalar pacotes

---

## 🎯 Próximos Passos (Após Deploy)

1. Testar todas as funcionalidades principais
2. Verificar compilação LaTeX no servidor
3. Testar upload de imagens
4. Verificar se os snippets funcionam
5. Fazer merge para `main` se tudo estiver OK

---

## 📞 Contato

Em caso de problemas, verificar:
- Logs do Supervisor: `/var/log/supervisor/`
- Logs do Flask: Usar `sudo supervisorctl tail doccollab`
- Status do serviço: `sudo supervisorctl status`

---

**Data do Deploy**: $(date)
**Branch**: feature/payment-system
**Commit**: 61c90c1

