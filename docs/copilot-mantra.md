# Mantra para Copilot / Assistente de Código

Use sempre este texto (mantra) ao formular prompts para o Copilot/assistente interno. Inclua-o no início do prompt ou em contexto permanente.

Mantra (Português):

"Implemente lógica determinística, modular e validável.
Não priorize estética.
Não crie atalhos fora do AST.
Não exponha LaTeX.
Não misture camadas."

Uso recomendado:
- Coloque o mantra como primeiras linhas do prompt quando pedir implementações ou alterações de arquitetura.
- Reforce que o AST JSON é a única fonte de verdade (FASE 0) quando relevante.
- Solicite testes automatizados e validação de regras (não apenas alterações visuais).

Exemplo de inclusão no prompt:

"[MANTRA] Implemente lógica determinística, modular e validável...\n\nObjetivo: adicionar endpoint X..."

*Arquivo criado automaticamente por script de projeto.*
