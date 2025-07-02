
; 🏢 DDIC-SM Clasificador de Delitos - Script de Instalación
; Contactos: Subtte Carrizo Jorge / Osa Grandolio Gabriel

[Setup]
AppName=DDIC-SM Clasificador de Delitos
AppVersion=1.0.0
AppPublisher=DDIC-SM
AppContact=Subtte Carrizo Jorge / Osa Grandolio Gabriel
DefaultDirName={pf}\DDIC-SM\Clasificador-Delitos
DefaultGroupName=DDIC-SM
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=DDIC-SM-Clasificador-Delitos-Setup
SetupIconFile=assets\logo.ico
UninstallDisplayIcon={app}\launcher\DDIC_SM_Launcher.exe
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\DDIC-SM Clasificador de Delitos"; Filename: "{app}\launcher\DDIC_SM_Launcher.exe"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,DDIC-SM Clasificador de Delitos}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\DDIC-SM Clasificador de Delitos"; Filename: "{app}\launcher\DDIC_SM_Launcher.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\DDIC-SM Clasificador"; Filename: "{app}\launcher\DDIC_SM_Launcher.exe"; WorkingDir: "{app}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\launcher\DDIC_SM_Launcher.exe"; Description: "{cm:LaunchProgram,DDIC-SM Clasificador}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('🏢 DDIC-SM Clasificador de Delitos' + #13#10 + 
         'Sistema de clasificación automática de hechos delictivos' + #13#10 + #13#10 +
         'Contactos:' + #13#10 +
         '• Subtte Carrizo Jorge' + #13#10 +
         '• Osa Grandolio Gabriel', mbInformation, MB_OK);
end;
