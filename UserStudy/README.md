
# README - Benutzerstudie

## Videodaten
Aus Speicherplatz-Gründen sind die Video-Aufzeichungen des Desktops bei den verschiedenen Aufgabenblöcken nicht in dieser Dateisammlung enthalten. Bei wissenschaftlich begründetem Bedarf kann gerne unter <userstudy@jumpdrive.de> angefragt werden. Die sind allerdings einige Gigabyte groß. 

## Studien-Daten
Die Messdaten der Interaktionen und die Antworten auf die Fragebögen finden sich unter *Auswertung Benutzerstudie/data*.
Die Antworten der Fragebögen sind zur einfacheren verarbeitung in die SQLite-Datenbank *data.sqlite* eingelesen worden, liegen als SQL-Statement aber auch im unterordner *Auswertung Benutzerstudie/data/sql* bereit.  
Die Messdaten finden sie unter *Auswertung Benutzerstudie/data/interactions*  

Die beiden Dateien *values_linkedinfo_2019-07-15_12-32.csv* und *variables_linkedinfo_2019-07-15_12-32.csv* geben Auskunft über den Aufbau des Fragebogens und die entsprechende Kodierung der Spalten in der Datenbank.  

## Studienauswertung
Mit dem Script *main.py* in *Auswertung Benutzerstudie/data* kann die Auswertung der Daten nachvollzogen werden. Die verwendeten Librarys sind sowohl über die Importe am Anfang der Datei als auch durch das Kapitel "Auswertung und Interpretation" in der Masterarbeit zu erfahren.
