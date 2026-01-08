Write-Output "== Script: habilitar WSL / VM Platform / Hyper-V =="
Write-Output "ATENÇÃO: execute este script em uma sessão do PowerShell executada como Administrador."

# Habilita Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Habilita Subsistema do Windows para Linux (WSL)
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Habilita Hyper-V (opcional, mas útil para compatibilidade do Docker Desktop)
dism.exe /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart

Write-Output "Operações DISM concluídas (verifique erros acima). Se não houver erros, reinicie o sistema para aplicar as alterações."
Write-Output "Para reiniciar agora (EXECUTE como Administrador): shutdown /r /t 0"

Write-Output "Se preferir, execute este comando para abrir uma janela elevada que executa o script automaticamente:"
Write-Output "Start-Process powershell -Verb runAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""$PWD\\scripts\\enable-wsl.ps1""'"
