#!/usr/bin/env python3
"""
Script para corrigir todas as traduções do DocCollab
"""

import os
import re
import polib

def extract_strings_from_templates():
    """Extrai todas as strings dos templates"""
    strings = set()
    project_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(project_dir, 'templates')
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Encontrar todas as strings {{ _('...') }}
                    matches = re.findall(r"\{\{\s*_\('([^']+)'\)\s*\}\}", content)
                    strings.update(matches)
    
    return sorted(strings)

def update_translation_file(po_file, translations):
    """Atualiza arquivo de tradução"""
    if os.path.exists(po_file):
        po = polib.pofile(po_file)
    else:
        po = polib.POFile()
        po.metadata = {
            'Project-Id-Version': 'DocCollab 1.0',
            'Report-Msgid-Bugs-To': 'team@doccollab.com',
            'POT-Creation-Date': '2025-01-01 12:00-0300',
            'PO-Revision-Date': '2025-01-01 12:00-0300',
            'Last-Translator': 'DocCollab Team <team@doccollab.com>',
            'Language': 'pt',
            'Language-Team': 'pt <pt@li.org>',
            'Plural-Forms': 'nplurals=2; plural=(n != 1);',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
            'Generated-By': 'Babel 2.17.0'
        }
    
    # Adicionar/atualizar traduções
    for msgid, msgstr in translations.items():
        entry = po.find(msgid)
        if entry:
            entry.msgstr = msgstr
        else:
            entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
            po.append(entry)
    
    po.save(po_file)
    return po

def main():
    """Função principal"""
    print("Extraindo strings dos templates...")
    strings = extract_strings_from_templates()
    print(f"Encontradas {len(strings)} strings para traduzir")
    
    # Traduções em português
    pt_translations = {
        "Home": "Início",
        "DocCollab": "DocCollab",
        "Sign in": "Entrar",
        "Sign up": "Cadastrar",
        "Language": "Idioma",
        "Sign out": "Sair",
        "Dashboard": "Painel",
        "Upgrade Plan": "Upgrade do Plano",
        "Email": "E-mail",
        "Password": "Senha",
        "Full name": "Nome completo",
        "Confirm password": "Confirmar senha",
        "Create account": "Criar conta",
        "Already have an account?": "Já tem uma conta?",
        "No account?": "Não tem conta?",
        "My Projects": "Meus Projetos",
        "Create New Project": "Criar Novo Projeto",
        "Project Name": "Nome do Projeto",
        "Description": "Descrição",
        "Create": "Criar",
        "Edit": "Editar",
        "Delete": "Excluir",
        "Open": "Abrir",
        "Free Plan": "Plano Gratuito",
        "Paid Plan": "Plano Pago",
        "Files": "Arquivos",
        "Save": "Salvar",
        "Compile PDF": "Compilar PDF",
        "Auto-save:": "Salvamento automático:",
        "Enabled": "Habilitado",
        "Disabled": "Desabilitado",
        "Project saved successfully!": "Projeto salvo com sucesso!",
        "Error saving project": "Erro ao salvar projeto",
        "PDF compiled successfully!": "PDF compilado com sucesso!",
        "Error compiling PDF": "Erro ao compilar PDF",
        "Compiling PDF...": "Compilando PDF...",
        "PDF Preview": "Visualização do PDF",
        "Back to Editor": "Voltar ao Editor",
        "Close": "Fechar",
        "Refresh": "Atualizar",
        "Download": "Baixar",
        "Fit": "Ajustar",
        "Create New File": "Criar Novo Arquivo",
        "Filename": "Nome do arquivo",
        "File Type": "Tipo de arquivo",
        "LaTeX Document (.tex)": "Documento LaTeX (.tex)",
        "Bibliography (.bib)": "Bibliografia (.bib)",
        "Other": "Outro",
        "Cancel": "Cancelar",
        "Select File": "Selecionar arquivo",
        "Upload": "Fazer upload",
        "Enter new filename:": "Digite o novo nome do arquivo:",
        "Are you sure you want to delete this file?": "Tem certeza que deseja excluir este arquivo?",
        "File created successfully": "Arquivo criado com sucesso",
        "Error creating file": "Erro ao criar arquivo",
        "File uploaded successfully": "Arquivo enviado com sucesso",
        "Error uploading file": "Erro ao fazer upload do arquivo",
        "File renamed successfully": "Arquivo renomeado com sucesso",
        "Error renaming file": "Erro ao renomear arquivo",
        "File deleted successfully": "Arquivo excluído com sucesso",
        "Error deleting file": "Erro ao excluir arquivo",
        "Error loading files": "Erro ao carregar arquivos",
        "Only .tex files can be edited": "Apenas arquivos .tex podem ser editados",
        "Error loading file": "Erro ao carregar arquivo",
        "Main file updated": "Arquivo principal atualizado",
        "Error updating main file": "Erro ao atualizar arquivo principal",
        "Upgrade to Paid Plan": "Upgrade para Plano Pago",
        "1 projeto": "1 projeto",
        "1 arquivo (.tex)": "1 arquivo (.tex)",
        "Upload de imagens": "Upload de imagens",
        "Múltiplos arquivos": "Múltiplos arquivos",
        "Colaboração": "Colaboração",
        "Projetos ilimitados": "Projetos ilimitados",
        "Arquivos ilimitados": "Arquivos ilimitados",
        "Colaboração em tempo real": "Colaboração em tempo real",
        "Suporte prioritário": "Suporte prioritário",
        "Recursos avançados": "Recursos avançados",
        "Cancel anytime. No hidden fees.": "Cancele a qualquer momento. Sem taxas ocultas.",
        "Maybe Later": "Talvez Depois",
        "Upgrade Now": "Fazer Upgrade Agora",
        "Payment integration coming soon!": "Integração de pagamento em breve!",
        "All new accounts start with a free plan. You can upgrade anytime!": "Todas as novas contas começam com um plano gratuito. Você pode fazer upgrade a qualquer momento!",
        "Free (1 project)": "Gratuito (1 projeto)",
        "Paid (unlimited)": "Pago (ilimitado)",
        "Feature Comparison": "Comparação de Recursos",
        "Feature": "Recurso",
        "Free": "Gratuito",
        "Paid": "Pago",
        "Projects": "Projetos",
        "Files per project": "Arquivos por projeto",
        "Image uploads": "Upload de imagens",
        "Real-time collaboration": "Colaboração em tempo real",
        "Priority support": "Suporte prioritário",
        "Frequently Asked Questions": "Perguntas Frequentes",
        "Can I cancel anytime?": "Posso cancelar a qualquer momento?",
        "Yes! You can cancel your subscription at any time. You will continue to have access to paid features until the end of your billing period.": "Sim! Você pode cancelar sua assinatura a qualquer momento. Você continuará tendo acesso aos recursos pagos até o final do período de cobrança.",
        "What payment methods do you accept?": "Quais métodos de pagamento vocês aceitam?",
        "We accept all major credit cards (Visa, MasterCard, American Express) and PayPal.": "Aceitamos todos os cartões de crédito principais (Visa, MasterCard, American Express) e PayPal.",
        "Is my data secure?": "Meus dados estão seguros?",
        "Absolutely! We use industry-standard encryption to protect your data and never share your information with third parties.": "Absolutamente! Usamos criptografia de padrão da indústria para proteger seus dados e nunca compartilhamos suas informações com terceiros.",
        "Payment Information": "Informações de Pagamento",
        "Card Number": "Número do Cartão",
        "Expiry": "Validade",
        "CVV": "CVV",
        "Cardholder Name": "Nome do Portador",
        "Complete Payment": "Finalizar Pagamento",
        "Payment integration coming soon! This is a demo.": "Integração de pagamento em breve! Esta é uma demonstração.",
        "Simulate successful payment?": "Simular pagamento bem-sucedido?",
        "Unlock unlimited projects, files, and collaboration features": "Desbloqueie projetos ilimitados, arquivos e recursos de colaboração",
        "1 project, 1 file": "1 projeto, 1 arquivo",
        "Unlimited projects & files": "Projetos e arquivos ilimitados",
        "Upgrade to create more files": "Faça upgrade para criar mais arquivos",
        "Upgrade to upload files": "Faça upgrade para fazer upload de arquivos",
        "Create File": "Criar Arquivo",
        "Upload File": "Fazer Upload",
        "Main File:": "Arquivo Principal:",
        "Rename": "Renomear",
        "PDF refreshed": "PDF atualizado",
        "PDF download started": "Download do PDF iniciado",
        "1 projeto": "1 projeto",
        "1 arquivo (.tex)": "1 arquivo (.tex)",
        "Upload de imagens": "Upload de imagens",
        "Múltiplos arquivos": "Múltiplos arquivos",
        "Colaboração": "Colaboração",
        "Projetos ilimitados": "Projetos ilimitados",
        "Arquivos ilimitados": "Arquivos ilimitados",
        "Colaboração em tempo real": "Colaboração em tempo real",
        "Suporte prioritário": "Suporte prioritário",
        "Recursos avançados": "Recursos avançados",
        "Current Plan": "Plano Atual",
        "Please select a file": "Por favor, selecione um arquivo",
        "Plan upgraded successfully!": "Plano atualizado com sucesso!",
        "Error upgrading plan:": "Erro ao atualizar plano:",
        "Error upgrading plan. Please try again.": "Erro ao atualizar plano. Tente novamente.",
        "Sessão encerrada.": "Sessão encerrada."
    }
    
    # Traduções em inglês
    en_translations = {
        "Home": "Home",
        "DocCollab": "DocCollab",
        "Sign in": "Sign in",
        "Sign up": "Sign up",
        "Language": "Language",
        "Sign out": "Sign out",
        "Dashboard": "Dashboard",
        "Upgrade Plan": "Upgrade Plan",
        "Email": "Email",
        "Password": "Password",
        "Full name": "Full name",
        "Confirm password": "Confirm password",
        "Create account": "Create account",
        "Already have an account?": "Already have an account?",
        "No account?": "No account?",
        "My Projects": "My Projects",
        "Create New Project": "Create New Project",
        "Project Name": "Project Name",
        "Description": "Description",
        "Create": "Create",
        "Edit": "Edit",
        "Delete": "Delete",
        "Open": "Open",
        "Free Plan": "Free Plan",
        "Paid Plan": "Paid Plan",
        "Files": "Files",
        "Save": "Save",
        "Compile PDF": "Compile PDF",
        "Auto-save:": "Auto-save:",
        "Enabled": "Enabled",
        "Disabled": "Disabled",
        "Project saved successfully!": "Project saved successfully!",
        "Error saving project": "Error saving project",
        "PDF compiled successfully!": "PDF compiled successfully!",
        "Error compiling PDF": "Error compiling PDF",
        "Compiling PDF...": "Compiling PDF...",
        "PDF Preview": "PDF Preview",
        "Back to Editor": "Back to Editor",
        "Close": "Close",
        "Refresh": "Refresh",
        "Download": "Download",
        "Fit": "Fit",
        "Create New File": "Create New File",
        "Filename": "Filename",
        "File Type": "File Type",
        "LaTeX Document (.tex)": "LaTeX Document (.tex)",
        "Bibliography (.bib)": "Bibliography (.bib)",
        "Other": "Other",
        "Cancel": "Cancel",
        "Select File": "Select File",
        "Upload": "Upload",
        "Enter new filename:": "Enter new filename:",
        "Are you sure you want to delete this file?": "Are you sure you want to delete this file?",
        "File created successfully": "File created successfully",
        "Error creating file": "Error creating file",
        "File uploaded successfully": "File uploaded successfully",
        "Error uploading file": "Error uploading file",
        "File renamed successfully": "File renamed successfully",
        "Error renaming file": "Error renaming file",
        "File deleted successfully": "File deleted successfully",
        "Error deleting file": "Error deleting file",
        "Error loading files": "Error loading files",
        "Only .tex files can be edited": "Only .tex files can be edited",
        "Error loading file": "Error loading file",
        "Main file updated": "Main file updated",
        "Error updating main file": "Error updating main file",
        "Upgrade to Paid Plan": "Upgrade to Paid Plan",
        "1 projeto": "1 project",
        "1 arquivo (.tex)": "1 file (.tex)",
        "Upload de imagens": "Image uploads",
        "Múltiplos arquivos": "Multiple files",
        "Colaboração": "Collaboration",
        "Projetos ilimitados": "Unlimited projects",
        "Arquivos ilimitados": "Unlimited files",
        "Colaboração em tempo real": "Real-time collaboration",
        "Suporte prioritário": "Priority support",
        "Recursos avançados": "Advanced features",
        "Cancel anytime. No hidden fees.": "Cancel anytime. No hidden fees.",
        "Maybe Later": "Maybe Later",
        "Upgrade Now": "Upgrade Now",
        "Payment integration coming soon!": "Payment integration coming soon!",
        "All new accounts start with a free plan. You can upgrade anytime!": "All new accounts start with a free plan. You can upgrade anytime!",
        "Free (1 project)": "Free (1 project)",
        "Paid (unlimited)": "Paid (unlimited)",
        "Feature Comparison": "Feature Comparison",
        "Feature": "Feature",
        "Free": "Free",
        "Paid": "Paid",
        "Projects": "Projects",
        "Files per project": "Files per project",
        "Image uploads": "Image uploads",
        "Real-time collaboration": "Real-time collaboration",
        "Priority support": "Priority support",
        "Frequently Asked Questions": "Frequently Asked Questions",
        "Can I cancel anytime?": "Can I cancel anytime?",
        "Yes! You can cancel your subscription at any time. You will continue to have access to paid features until the end of your billing period.": "Yes! You can cancel your subscription at any time. You will continue to have access to paid features until the end of your billing period.",
        "What payment methods do you accept?": "What payment methods do you accept?",
        "We accept all major credit cards (Visa, MasterCard, American Express) and PayPal.": "We accept all major credit cards (Visa, MasterCard, American Express) and PayPal.",
        "Is my data secure?": "Is my data secure?",
        "Absolutely! We use industry-standard encryption to protect your data and never share your information with third parties.": "Absolutely! We use industry-standard encryption to protect your data and never share your information with third parties.",
        "Payment Information": "Payment Information",
        "Card Number": "Card Number",
        "Expiry": "Expiry",
        "CVV": "CVV",
        "Cardholder Name": "Cardholder Name",
        "Complete Payment": "Complete Payment",
        "Payment integration coming soon! This is a demo.": "Payment integration coming soon! This is a demo.",
        "Simulate successful payment?": "Simulate successful payment?",
        "Unlock unlimited projects, files, and collaboration features": "Unlock unlimited projects, files, and collaboration features",
        "1 project, 1 file": "1 project, 1 file",
        "Unlimited projects & files": "Unlimited projects & files",
        "Upgrade to create more files": "Upgrade to create more files",
        "Upgrade to upload files": "Upgrade to upload files",
        "Create File": "Create File",
        "Upload File": "Upload File",
        "Main File:": "Main File:",
        "Rename": "Rename",
        "PDF refreshed": "PDF refreshed",
        "PDF download started": "PDF download started",
        "1 projeto": "1 project",
        "1 arquivo (.tex)": "1 file (.tex)",
        "Upload de imagens": "Image uploads",
        "Múltiplos arquivos": "Multiple files",
        "Colaboração": "Collaboration",
        "Projetos ilimitados": "Unlimited projects",
        "Arquivos ilimitados": "Unlimited files",
        "Colaboração em tempo real": "Real-time collaboration",
        "Suporte prioritário": "Priority support",
        "Recursos avançados": "Advanced features",
        "Current Plan": "Current Plan",
        "Please select a file": "Please select a file",
        "Plan upgraded successfully!": "Plan upgraded successfully!",
        "Error upgrading plan:": "Error upgrading plan:",
        "Error upgrading plan. Please try again.": "Error upgrading plan. Please try again.",
        "Sessão encerrada.": "Session ended."
    }
    
    # Traduções em espanhol
    es_translations = {
        "Home": "Inicio",
        "Sign in": "Iniciar sesión",
        "Sign up": "Registrarse",
        "Language": "Idioma",
        "DocCollab - Home": "DocCollab - Inicio",
        "Welcome to DocCollab": "Bienvenido a DocCollab",
        "Create and collaborate on documents easily.": "Crea y colabora en documentos fácilmente.",
        "Dashboard": "Panel",
        "My Projects": "Mis Proyectos",
        "New Project": "Nuevo Proyecto",
        "No description": "Sin descripción",
        "Updated:": "Actualizado:",
        "Open Editor": "Abrir Editor",
        "Delete": "Eliminar",
        "Create Project": "Crear Proyecto",
        "Project Name": "Nombre del Proyecto",
        "Description": "Descripción",
        "Create": "Crear",
        "Cancel": "Cancelar",
        "Sign out": "Cerrar sesión",
        "Upgrade Plan": "Actualizar Plan",
        "Free Plan": "Plan Gratuito",
        "Paid Plan": "Plan de Pago",
        "1 project": "1 proyecto",
        "1 file (.tex)": "1 archivo (.tex)",
        "Image uploads": "Subida de imágenes",
        "Multiple files": "Múltiples archivos",
        "Collaboration": "Colaboración",
        "Unlimited projects": "Proyectos ilimitados",
        "Unlimited files": "Archivos ilimitados",
        "Real-time collaboration": "Colaboración en tiempo real",
        "Priority support": "Soporte prioritario",
        "Advanced features": "Características avanzadas",
        "Current Plan": "Plan Actual",
        "Please select a file": "Por favor, selecciona un archivo",
        "Plan upgraded successfully!": "¡Plan actualizado con éxito!",
        "Error upgrading plan:": "Error al actualizar plan:",
        "Error upgrading plan. Please try again.": "Error al actualizar plan. Inténtalo de nuevo.",
        "Sessão encerrada.": "Sesión cerrada."
    }
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(project_dir, 'translations')
    
    # Atualizar português
    print("Atualizando traduções em português...")
    pt_po_file = os.path.join(translations_dir, 'pt', 'LC_MESSAGES', 'messages.po')
    update_translation_file(pt_po_file, pt_translations)
    
    # Atualizar inglês
    print("Atualizando traduções em inglês...")
    en_po_file = os.path.join(translations_dir, 'en', 'LC_MESSAGES', 'messages.po')
    update_translation_file(en_po_file, en_translations)
    
    # Atualizar espanhol
    print("Atualizando traduções em espanhol...")
    es_po_file = os.path.join(translations_dir, 'es', 'LC_MESSAGES', 'messages.po')
    update_translation_file(es_po_file, es_translations)
    
    # Compilar traduções
    print("Compilando traduções...")
    for lang in ['pt', 'en', 'es']:
        po_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
        mo_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.mo')
        
        if os.path.exists(po_file):
            po = polib.pofile(po_file)
            po.save_as_mofile(mo_file)
            print(f"Tradução {lang} compilada")
    
    print("Todas as traduções foram atualizadas!")

if __name__ == "__main__":
    main()
