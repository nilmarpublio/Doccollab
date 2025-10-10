# 🚀 Deploy Rápido - DocCollab

## 📦 Pré-requisitos

- Servidor Ubuntu 20.04+ com IP público
- Acesso SSH (root ou sudo)
- Mínimo 2GB RAM, 20GB disco

---

## ⚡ Deploy em 3 Passos

### 1️⃣ Preparar

```bash
cd DocCollab
chmod +x deploy.sh
```

### 2️⃣ Executar

```bash
./deploy.sh SEU_IP root
```

Exemplo:
```bash
./deploy.sh 142.93.123.45 root
```

### 3️⃣ Acessar

Abra no navegador:
```
http://SEU_IP
```

**Login padrão:**
- Email: `admin@doccollab.com`
- Senha: `admin123`

⚠️ **ALTERE A SENHA IMEDIATAMENTE!**

---

## 🔒 Configurar SSL (Opcional mas Recomendado)

```bash
ssh root@SEU_IP
certbot --nginx -d seu-dominio.com
```

---

## 📊 Comandos Úteis

```bash
# Ver logs
ssh root@SEU_IP 'tail -f /var/log/doccollab/error.log'

# Reiniciar aplicação
ssh root@SEU_IP 'supervisorctl restart doccollab'

# Status
ssh root@SEU_IP 'supervisorctl status doccollab'
```

---

## 📖 Documentação Completa

Para mais detalhes, consulte: **[docs/DEPLOY.md](docs/DEPLOY.md)**

---

## ❓ Problemas?

1. **Erro 502**: `ssh root@SEU_IP 'supervisorctl restart doccollab'`
2. **Logs**: `ssh root@SEU_IP 'tail -n 50 /var/log/doccollab/error.log'`
3. **Firewall**: Verifique se portas 80/443 estão abertas

---

**Pronto! Seu DocCollab está no ar! 🎉**


