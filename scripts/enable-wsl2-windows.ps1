<#
Enable WSL2 and Virtual Machine Platform on Windows

Run this script as Administrator. It will:
- Check virtualization support in firmware
- Enable VirtualMachinePlatform and WSL feature
- (Optionally) enable Hyper-V on supported editions
- Offer to restart the machine

Usage (PowerShell as Admin):
  .\scripts\enable-wsl2-windows.ps1
#>

function Assert-Admin {
  $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
  if (-not $isAdmin) {
    Write-Error 'Este script precisa ser executado como Administrador. Abra o PowerShell como Administrador e execute novamente.'
    exit 1
  }
}

Assert-Admin

Write-Host 'Verificando suporte à virtualização na firmware...'
$sysinfo = systeminfo 2>$null | Out-String
if ($sysinfo -match 'Virtualization.*:\s*Yes') {
  Write-Host 'Virtualização habilitada na firmware.' -ForegroundColor Green
} else {
  Write-Warning 'Virtualização NÃO habilitada na firmware. Habilite VT-x/AMD-V no BIOS/UEFI e execute este script novamente.'
  Write-Host 'Para instruções, visite https://aka.ms/enablevirtualization'
  $resp = Read-Host 'Deseja continuar e tentar habilitar recursos do Windows mesmo assim? (s/N)'
  if ($resp -notin @('s','S','y','Y')) { exit 2 }
}

Write-Host 'Habilitando recursos do Windows necessários (pode demorar)...' -ForegroundColor Cyan
try {
  Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart -ErrorAction Stop | Out-Null
  Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart -ErrorAction Stop | Out-Null
  Write-Host 'Recursos WSL e VirtualMachinePlatform habilitados.' -ForegroundColor Green
} catch {
  Write-Error "Falha ao habilitar recursos: $($_.Exception.Message)"
  exit 3
}

# For Windows Pro/Enterprise, enabling Hyper-V is optional but can help
if ((Get-CimInstance -ClassName Win32_OperatingSystem).Caption -match 'Windows 10|Windows 11') {
  $wantHyperV = Read-Host 'Deseja habilitar o recurso Hyper-V (recomendado em Pro/Enterprise)? (s/N)'
  if ($wantHyperV -in @('s','S','y','Y')) {
    try {
      Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -All -NoRestart -ErrorAction Stop | Out-Null
      Write-Host 'Hyper-V habilitado.' -ForegroundColor Green
    } catch {
      Write-Warning "Não foi possível habilitar Hyper-V: $($_.Exception.Message)"
    }
  }
}

Write-Host 'Configurando WSL2 como padrão...' -ForegroundColor Cyan
try {
  wsl --set-default-version 2 2>$null
  Write-Host 'WSL2 definido como versão padrão.' -ForegroundColor Green
} catch {
  Write-Warning 'wsl não pôde definir versão padrão automaticamente — execute `wsl --install --no-distribution` se necessário.'
}

$restart = Read-Host 'É necessário reiniciar para aplicar alterações. Reiniciar agora? (s/N)'
if ($restart -in @('s','S','y','Y')) {
  Write-Host 'Reiniciando agora...'
  Restart-Computer
} else {
  Write-Host 'Concluído. Reinicie manualmente o sistema e inicie o Docker Desktop.'
}
