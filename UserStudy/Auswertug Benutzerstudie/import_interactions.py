
import sqlite3
import re
import os


class InteractionImport:

    sql = 'INSERT INTO interactions (timestamp, interaction, interaction_detail, "case", qnr, position, system) ' \
          'VALUES (?, ?, ?, ?, ?, ?, ?)'

    def __init__(self):
        self.db = sqlite3.connect('data/data.sqlite')

    def import_interactions(self, filename: str, case: str, aufgabe: str, system: str):
        cursor = self.db.cursor()

        with open(filename, 'r', encoding='iso-8859-15') as file:
            imported: int = 0
            # items = []
            for l in file:
                data = re.search('(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d):(.+),(.+),(.+)', l)
                if data.re.groups is 4:
                    item = (data[1], data[2], data[3], case, aufgabe, data[4], system)
                    # items.append(item)
                    cursor.execute(self.sql, item)

                    imported += 1
                else:
                    print('[WARNING]: Nicht die korrekte Anzahl an Daten in der Zeile:')
                    print(l)
            print(f'Imported {imported} items')
        cursor.execute('COMMIT')
        cursor.close()
        print('Done')



c = InteractionImport()
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 CD173789 LinkFlow.txt', 'CD173789', 'qnr2', 'LF')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 CD173789 Ordner.txt', 'CD173789', 'qnr2', 'Folder')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 TP178163 LinkFlow.txt', 'TP178163', 'qnr2', 'LF')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 TP178163 Ordner.txt', 'TP178163', 'qnr2', 'Folder')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 AF689975 LinkFlow.txt', 'AF689975', 'qnr2', 'LF')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 AF689975 Ordner.txt', 'AF689975', 'qnr2', 'Folder')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 TB749451 LinkFlow.txt', 'TB749451', 'qnr2', 'LF')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 TB749451 Ordner.txt', 'TB749451', 'qnr2', 'Folder')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 QK371974 LinkFlow.txt', 'QK371974', 'qnr2', 'LF')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 QK371974 Ordner.txt', 'QK371974', 'qnr2', 'Folder')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 GZ384373 LinkFlow.txt', 'GZ384373', 'qnr2', 'LF')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 GZ384373 Ordner.txt', 'GZ384373', 'qnr2', 'Folder')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 EY196957 LinkFlow.txt', 'EY196957', 'qnr2', 'LF')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe1 EY196957 Ordner.txt', 'EY196957', 'qnr2', 'Folder')

c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe2 CD173789.txt', 'CD173789', 'qnr3', 'both')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe2 TP178163.txt', 'TP178163', 'qnr3', 'both')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe2 AF689975.txt', 'AF689975', 'qnr3', 'both')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe2 TB749451 - kein Video.txt', 'TB749451', 'qnr3', 'both')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe2 QK371974.txt', 'QK371974', 'qnr3', 'both')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe2 GZ384373.txt', 'GZ384373', 'qnr3', 'both')
c.import_interactions(f'data{os.sep}interactions{os.sep}logger Aufgabe2 EY196957.txt', 'EY196957', 'qnr3', 'both')
