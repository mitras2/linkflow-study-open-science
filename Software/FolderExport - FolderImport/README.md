
# FolderExport und FolderImport

Die beiden Programme FolderExport (auch als *Ordnerstruktur exportieren.exe* bezeichnet) und FolderImport wurden programmiert um die persönliche Ordnerstruktur der Testpersonen zu exportieren und in der Textumgaung wieder anlegen zu können. 

Beide Programme können über die entsprechende exe-Datei gestartet werden. Bei FolderExport/Ordnerstruktur exportieren.exe muss das Verzeichniss das mit seiner Struktur exportiert werden sol ausgewählt werden. Außerdem muss der Benutzer einen Zielort angeben an dem die Export-Datei anbelegt wird.

In FolderImport muss sowohl eine erstellte Export-Datei als auch der Zielordner in dem die Struktur erstellt werden soll angegeben werden bevor der Import gestartet werden kann.

Da sich die beiden Programme einen kleinen Teil ihres QuellCodes mit LinkFlow teilen, ist ihr Quellcode im Quellcode des LinkFlow Projkts zu finden. Der genau Ordner ist *py/folder_scan*. Die beiden Start/Main-Dateien der Programme heißen *main_export_gui_wx_threading.py* und *main_import_gui_wx.py*.

Um die Programme direkt aus Python starten zu können muss wxPython <https://www.wxpython.org/> für die Benutzeroberfläche als Paket zur Verfügung stehen.
