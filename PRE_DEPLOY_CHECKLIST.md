# ✅ Checklist Pré-Deploy - DocCollab

Use este checklist antes de fazer o deploy em produção.

---

## 📋 Preparação Local

### Código
- [ ] Todo o código está commitado no Git
- [ ] Não há arquivos `.pyc` ou `__pycache__` no repositório
- [ ] Arquivo `.gitignore` está configurado corretamente
- [ ] Não há senhas ou chaves de API no código

### Dependências
- [ ] `requirements.txt` está atualizado
- [ ] Todas as dependências estão com versões fixas
- [ ] Testado localmente com `pip install -r requirements.txt`

### Configuração
- [ ] Arquivo `env.example` existe e está completo
- [ ] Variáveis de ambiente documentadas
- [ ] SECRET_KEY não está hardcoded no código

### Traduções
- [ ] Traduções compiladas: `pybabel compile -d translations`
- [ ] Todos os idiomas (PT/EN/ES) testados

### Testes
- [ ] Aplicação roda localmente sem erros
- [ ] Login/Logout funcionam
- [ ] Criação de projetos funciona
- [ ] Editor LaTeX funciona
- [ ] Compilação LaTeX funciona
- [ ] Chat assistente funciona
- [ ] Linter funciona

---

## 🖥️ Servidor

### Acesso
- [ ] Acesso SSH configurado
- [ ] Chave SSH adicionada (se aplicável)
- [ ] Usuário tem permissões sudo/root

### Recursos
- [ ] Mínimo 2GB RAM
- [ ] Mínimo 20GB disco livre
- [ ] IP público ou domínio configurado

### DNS (se usar domínio)
- [ ] Registro A apontando para o IP do servidor
- [ ] Registro AAAA (IPv6) se aplicável
- [ ] TTL configurado (recomendado: 300-3600)
- [ ] DNS propagado (teste: `nslookup seu-dominio.com`)

---

## 🔐 Segurança

### Senhas
- [ ] Senha forte para usuário SSH
- [ ] Senha forte para usuário admin da aplicação
- [ ] SECRET_KEY gerada aleatoriamente

### Firewall
- [ ] Portas desnecessárias fechadas
- [ ] Apenas 22 (SSH), 80 (HTTP), 443 (HTTPS) abertas
- [ ] Fail2ban instalado (recomendado)

### SSL/HTTPS
- [ ] Domínio configurado (necessário para SSL)
- [ ] Certbot instalado
- [ ] Certificado SSL obtido e configurado

### Backups
- [ ] Estratégia de backup definida
- [ ] Backup do banco de dados configurado
- [ ] Backup dos uploads configurado
- [ ] Testado restauração de backup

---

## 📦 Deploy

### Script de Deploy
- [ ] `deploy.sh` tem permissão de execução (`chmod +x`)
- [ ] Testado em ambiente de staging (se disponível)
- [ ] IP/domínio do servidor confirmado

### Pós-Deploy
- [ ] Aplicação acessível via navegador
- [ ] Login funciona
- [ ] Criar projeto funciona
- [ ] Compilar LaTeX funciona
- [ ] Socket.IO funciona (chat em tempo real)
- [ ] Uploads funcionam
- [ ] Logs não mostram erros críticos

### Configuração Inicial
- [ ] Senha do admin alterada
- [ ] Usuários de teste criados (se necessário)
- [ ] Projetos de exemplo criados (se necessário)
- [ ] Configurações de email (se aplicável)

---

## 📊 Monitoramento

### Logs
- [ ] Logs da aplicação acessíveis
- [ ] Logs do Nginx acessíveis
- [ ] Logs do Supervisor acessíveis
- [ ] Rotação de logs configurada

### Performance
- [ ] Tempo de resposta aceitável (< 2s)
- [ ] Compilação LaTeX funciona (< 30s)
- [ ] Uso de memória normal (< 70%)
- [ ] Uso de CPU normal (< 80%)

### Alertas (Opcional)
- [ ] Monitoramento de uptime configurado
- [ ] Alertas de erro configurados
- [ ] Alertas de espaço em disco configurados

---

## 📝 Documentação

### Para Usuários
- [ ] Manual de uso disponível
- [ ] FAQ criado
- [ ] Vídeos tutoriais (opcional)

### Para Administradores
- [ ] Documentação de deploy atualizada
- [ ] Comandos úteis documentados
- [ ] Troubleshooting documentado
- [ ] Contatos de suporte definidos

---

## 🎯 Checklist Final

Antes de considerar o deploy completo:

- [ ] ✅ Aplicação acessível publicamente
- [ ] ✅ HTTPS configurado (se domínio disponível)
- [ ] ✅ Senha admin alterada
- [ ] ✅ Backup configurado
- [ ] ✅ Firewall ativo
- [ ] ✅ Logs funcionando
- [ ] ✅ Todas as funcionalidades testadas
- [ ] ✅ Documentação completa
- [ ] ✅ Equipe treinada (se aplicável)
- [ ] ✅ Plano de rollback definido

---

## 📞 Contatos de Emergência

Preencha antes do deploy:

- **Responsável Técnico**: _______________
- **Telefone**: _______________
- **Email**: _______________
- **Provedor de Hospedagem**: _______________
- **Suporte do Provedor**: _______________

---

## 🚨 Plano de Rollback

Se algo der errado:

1. **Parar aplicação**: `supervisorctl stop doccollab`
2. **Restaurar backup**: `cp backup.db instance/doccollab.db`
3. **Reverter código**: `git checkout TAG_ANTERIOR`
4. **Reiniciar**: `supervisorctl start doccollab`

---

**Data do Deploy**: _______________  
**Responsável**: _______________  
**Status**: _______________

---

✅ **Tudo pronto? Vamos ao deploy!** 🚀

```bash
./deploy.sh SEU_IP root
```






