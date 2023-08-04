#define MyAppName "GitWorkItems"
#define MyAppVersion "1.0"
#define MyAppPublisher "CAMEO"

[Setup]
AppId={{90CFDDE4-28B8-4AD0-83E3-CEE7EA98507A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputBaseFilename=GitWorkitemsSetup.{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=true

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: modifypath; Description: &Add application directory to your system path

[Files]
Source: "C:\Users\DRAGOTIA\source\repos\GitCheckin\src\*"; Excludes: "\config.yaml, \.gitignore, \*.ui, \*.qrc, \*.png, __pycache__, \python3\Scripts"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
Filename: "{app}\python3\python.exe"; Parameters: "{app}\create_config.py"

[UninstallDelete]
Type: filesandordirs; Name:"{app}\__pycache__"
Type: filesandordirs; Name:"{app}\python3"
Type: dirifempty; Name: "{app}"

[Code]
const
	ModPathName = 'modifypath';
	ModPathType = 'user';

function ModPathDir(): TArrayOfString;
begin
	setArrayLength(Result, 1)
	Result[0] := ExpandConstant('{app}');
end;
#include "modpath.iss"