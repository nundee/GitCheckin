param (
    [Parameter(Mandatory=$false)]
    $DestDir="dist"
)
$buildDir = Join-Path $DestDir "build"
dotnet build -c Release --output $buildDir
if ($?) {
    $zipFile= join-path $DestDir "UpdateCameoDev.zip"
    Write-Host "Creating $zipFile"
    if(Test-Path $zipFile) {
        Remove-Item -Force $zipFile
    }
    Remove-Item -Path $buildDir/*.pdb, $buildDir/Microsoft*.dll, $buildDir/TomsToolbox.Essentials.dll, $buildDir/TomsToolbox.ObservableCollections.dll, $buildDir/TomsToolbox.Wpf.dll
    Compress-Archive -Path $buildDir/* -DestinationPath $zipFile
    Remove-Item -Force -Recurse $buildDir
}