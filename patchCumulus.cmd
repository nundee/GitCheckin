<# :
  @echo off
    powershell -nologo -noprofile -command ^
         "&{[ScriptBlock]::Create((cat """%~f0""") -join [Char[]]10).Invoke(@(&{$args}%*))}"
  exit /b
#>
Write-Host "Hello, I'm patching the service gateway configuration to use localhost only" -fo Green
$cameoDir=(Get-ItemProperty -Path Registry::HKEY_LOCAL_MACHINE\SOFTWARE\AVL\CAMEO).InstallDir
Write-Host "Cameo is installed in: " -noNewLine 
Write-Host $cameoDir -fo Yellow
$faasFolder="$cameoDir\Services\faas"
$sgConfig = "$faasFolder\SG.config.json"
Write-Host Patching "$sgConfig"
(Get-Content $sgConfig) -replace '"BindTo"\s*:\s*"\*"', '"BindTo": "127.0.0.1"' | Set-Content $sgConfig
Write-Host delete firewall rules
netsh.exe advfirewall firewall delete rule name=all program="$faasFolder\ServiceGatewayS.exe" | Out-Default
netsh.exe advfirewall firewall delete rule name=all program="$faasFolder\jobstatusprovider.exe" | Out-Default
netsh.exe advfirewall firewall delete rule name=all program="$faasFolder\http_facade.exe" | Out-Default

netsh.exe advfirewall firewall delete rule name=all program="$cameoDir\AVL.CAMEO.Launcher.exe" | Out-Default
netsh.exe advfirewall firewall delete rule name=all program="$cameoDir\AVL.CAMEO.Distributed.Service.exe" | Out-Default
netsh.exe advfirewall firewall delete rule name=all program="$cameoDir\Bin\AVL.CAMEO.Drivers.TCPDriver.TCPServer.exe" | Out-Default
netsh.exe advfirewall firewall delete rule name=all program="$cameoDir\Bin\AVL.CAMEO.IndiComTCPServer.exe" | Out-Default
netsh.exe advfirewall firewall add rule name="cameo" dir=in action=block program="$cameoDir\AVL.CAMEO.Launcher.exe" | Out-Default

Write-Host Done -fo Green