# This installs two files, app.exe and logo.ico, creates a start menu shortcut, builds an uninstaller, and
# adds uninstall information to the registry for Add/Remove Programs
 
# To get started, put this script into a folder with the two files (app.exe, logo.ico, and license.rtf -
# You'll have to create these yourself) and run makensis on it
 
# If you change the names "app.exe", "logo.ico", or "license.rtf" you should do a search and replace - they
# show up in a few places.
# All the other settings can be tweaked by editing the !defines at the top of this script
!define APPNAME "Joytan"
!define COMPANYNAME "Koki Mametani"
!define DESCRIPTION "Create Audio/Textbooks for your study"
# These three must be integers
!define VERSIONMAJOR 0
!define VERSIONMINOR 0
!define VERSIONBUILD 0
# These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
# It is possible to use "mailto:" links in here to open the email client
!define HELPURL "https://kokimame.github.io/joytan/" # "Support Information" link
!define UPDATEURL "https://github.com/kokimame/joytan"
!define ABOUTURL "https://github.com/kokimame/joytan" # "Publisher" link
# This is the size (in kB) of all the files copied into "Program Files"
!define INSTALLSIZE 7233
 
RequestExecutionLevel admin ;Require admin rights on NT6+ (When UAC is turned on)
 
InstallDir "$PROGRAMFILES\${APPNAME}"
 
# rtf or txt file - remember if it is txt, it must be in the DOS text format (\r\n)
LicenseData "LICENSE.txt"
# This will be in the installer/uninstaller's title bar
Name "${APPNAME}"
Icon "${APPNAME}.ico"
outFile "${APPNAME}-installer.exe"
 
!include LogicLib.nsh
 
# Just three pages - license agreement, install location, and installation
page license
page directory
Page instfiles
 
!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
        messageBox mb_iconstop "Administrator rights required!"
        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        quit
${EndIf}
!macroend
 
function .onInit
	setShellVarContext all
	!insertmacro VerifyUserIsAdmin
functionEnd
 
section "install"
	# Files for the install directory - to build the installer, these should be in the same directory as the install script (this file)
	setOutPath $INSTDIR
	# Files added here should be removed by the uninstaller (see section "uninstall")
	file "joytan.exe"
	file "joytan.ico"
	# Add any other files for the install directory (license files, app data, etc) here
	file "ffmpeg.exe"
	file "lame.exe"
	file "default_textbook.html"
 
	# Uninstaller - See function un.onInit and section "uninstall" for configuration
	writeUninstaller "$INSTDIR\uninstall.exe"
 
	# Start Menu
	createDirectory "$SMPROGRAMS\${APPNAME}"
	createShortCut "$SMPROGRAMS\${APPNAME}.lnk" "$INSTDIR\joytan.exe" "" "$INSTDIR\joytan.ico"
	CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\joytan.exe" ""
 
	# Registry information for add/remove programs
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME} - ${DESCRIPTION}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\joytan.ico$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "$\"${COMPANYNAME}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "$\"${HELPURL}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "$\"${UPDATEURL}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "$\"${ABOUTURL}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "$\"${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}$\""
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
	# There is no option for modifying or repairing the install
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
	# Set the INSTALLSIZE constant (!defined at the top of this script) so Add/Remove Programs can accurately report the size
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
sectionEnd
 
# Uninstaller
 
function un.onInit
	SetShellVarContext all
 
	#Verify the uninstaller - last chance to back out
	MessageBox MB_OKCANCEL "Permanantly remove ${APPNAME}?" IDOK next
		Abort
	next:
	!insertmacro VerifyUserIsAdmin
functionEnd
 
section "uninstall"
 
	# Remove Start Menu launcher
	delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
	# Try to remove the Start Menu folder - this will only happen if it is empty
	rmDir "$SMPROGRAMS\${APPNAME}"
 
	# Remove files
	delete $INSTDIR\joytan.exe
	delete $INSTDIR\joytan.ico
	delete $INSTDIR\ffmpeg.exe
	delete $INSTDIR\lame.exe
	delete $INSTDIR\default_textbook.html
 
	# Always delete uninstaller as the last action
	delete $INSTDIR\uninstall.exe
 
	# Try to remove the install directory - this will only happen if it is empty
	rmDir $INSTDIR
 
	# Remove uninstaller information from the registry
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
sectionEnd