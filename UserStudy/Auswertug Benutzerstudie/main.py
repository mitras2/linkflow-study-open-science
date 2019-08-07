import matplotlib
import sqlite3
import os
from builtins import DeprecationWarning
from random import uniform

import pandas

import seaborn as sns
import matplotlib.pyplot as plt
import scipy
import numpy as np

# Daten importieren und in eine große grund-Tabelle einlesen
# Daten sind in Datenbank - Datenbank-Verbindung bereit stellen
from pandas import DataFrame


class AnalystMain:
    tam: DataFrame = None
    messwerte: DataFrame = None
    attribute: DataFrame = None

    def __init__(self):
        self.db = sqlite3.connect('data/data.sqlite')

    def get_query(self, name: str):
        try:
            with open(f'sql_querys{os.sep}{name}.sql', 'r') as file:
                sql = ''
                for line in file.readlines():
                    sql = sql + line.rstrip('\n') + ' '
                return sql
        except:
            print(f'[Error]')
            return False

    def plots(self):
        if self.tam is None:
            self.tam = self.tam_dataframe()

        # sns.set(style="darkgrid")
        # g = sns.FacetGrid(tips, row="sex", col="time", margin_titles=True)
        # bins = np.linspace(0, 60, 13)
        # g.map(plt.hist, "total_bill", color="steelblue", bins=bins)

        def sus_kde():
            sns.set(style="white", palette="muted", color_codes=True)
            # SUS Score KDE
            # fig, ax = plt.subplots(figsize=(10,7))
            # plot = sns.distplot(ax=ax, a=self.tam.query('qnr == "qnr2"')['usability'], hist=False, color="m", label='Aufgabe Einsortieren', axlabel='SUS Score')
            plot_sus_kde = sns.distplot(a=self.tam.query('qnr == "qnr2"')['usability'], hist=False, color="m",
                                        label='Aufgabe Einsortieren', axlabel='SUS Score')
            sns.distplot(self.tam.query('qnr == "qnr3"')['usability'], hist=False, color="g", label='Aufgabe Auffinden')
            sns.distplot(self.tam['usability'], hist=False, color="r", label='Gesammt')
            plot_sus_kde.set_title('KDE SUS Score\n\n')
            plt.xlim(0, 100)
            plt.show()

        def utility_kde():
            # Utility KDE
            plot_utility_kde = sns.distplot(a=self.tam.query('qnr == "qnr2"')['utility'], hist=False, color="m",
                                            label='Aufgabe Einsortieren')
            # sns.distplot(self.tam.query('qnr == "qnr3"')['utility'], hist=False, color="g", label='Aufgabe Auffinden')
            sns.distplot(self.tam['utility'], hist=False, color="r", label='Gesammt', axlabel='Nützlichkeit')
            plot_utility_kde.set_title('KDE - Nützlichkeit\n\n')
            plot_utility_kde.set_xticklabels(['Völlig unbrauchbar (0)', '', '', '', '', '', 'Sehr nützlich (6)'])
            plt.xlim(0, 7)
            plt.ylim(0, 2)
            plt.show()

        def utility_bar():
            # sns.set(style="white", palette="muted", color_codes=True)
            ax = plt.hist(
                [self.tam.query('qnr == "qnr2"')['utility'],
                 self.tam.query('qnr == "qnr3"')['utility'],
                 self.tam['utility']],
                color=['r', 'b', 'm'], alpha=0.5,
                label=['Aufgabe Einsortieren', 'Aufgabe Aufrufen', 'Gesamt'],
                histtype='bar',
                align='mid',
                bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
            )
            # utility_count = sns.distplot(self.tam.query('qnr == "qnr2"')['utility'], hist=True, kde=False, color="r", axlabel='Nützlichkeit', label='Aufgabe Einsortieren')
            # utility_count = sns.distplot(self.tam.query('qnr == "qnr3"')['utility'], hist=True, kde=False, color="b", axlabel='Nützlichkeit', label='Aufgabe Auffinden')
            # sns.distplot(self.tam['utility'], hist=True, kde=False, color="m", axlabel='Nützlichkeit', label='Gesammt')
            # utility_count.set_title('KDE - Nützlichkeit\n\n')
            # plt.set_title('Bewertungen Nützlichkeit\n\n')
            plt.title('Bewertungen Nützlichkeit\n', fontsize=16)
            plt.xlabel('Nützlichkeit', fontsize=12)
            plt.ylabel('Anzahl an\nBewertungen', fontsize=12)
            plt.legend()
            plt.xlim(0, 7)
            plt.xticks([0, 1, 2, 3, 4, 5, 6, 7],
                       ['0\nVöllig\nunbrauchbar', '1', '2', '3', '4', '5', '6\nSehr\nnützlich', ''])
            plt.grid(axis='y')
            plt.show()

        # utility_kde()
        utility_bar()
        # sus_kde()

    # GET/LOAD DATA
    def tam_dataframe(self):
        # tam
        cursor = self.db.cursor()
        sql = self.get_query('tam')
        cursor.execute(sql)
        data = {'case': [], 'qnr': [], 'utility': [], 'usability': [], 'attitude': [], 'choise': []}
        for row in cursor:
            utility = ((row[
                            12] * -1) + 7)  # Korrigiere die Werte auf den Bereich zwischen 0 und 6 wobei 6 für die höchste Nützlichkeit und 0 für keine Nützlichkeit steht
            attitude = row[13] - 1
            choise = row[14] - 1
            sus_point = 0
            for i in range(2, 12, 1):
                sus_point += (row[i] - 1)
            sus = sus_point * 2.5
            data['case'].append(row[0])
            data['qnr'].append(row[1])
            data['utility'].append(utility)
            data['usability'].append(sus)
            data['attitude'].append(attitude)
            data['choise'].append(choise)
        df = pandas.DataFrame(data)
        return df

    def tam_dataframe_typed_values(self):
        # tam
        cursor = self.db.cursor()
        sql = self.get_query('tam')
        cursor.execute(sql)
        data = {'case': [], 'qnr': [], 'type': [], 'value': []}
        for row in cursor:
            utility = ((row[
                            12] * -1) + 7)  # Korrigiere die Werte auf den Bereich zwischen 0 und 6 wobei 6 für die höchste Nützlichkeit und 0 für keine Nützlichkeit steht
            attitude = row[13] - 1
            choise = row[14] - 1
            sus_point = 0
            for i in range(2, 12, 1):
                sus_point += (row[i] - 1)
            sus = sus_point * 2.5
            for i in range(0,5,1):
                data['case'].append(row[0])
                data['qnr'].append(row[1])
            data['type'].append('utility')
            data['value'].append(utility)
            data['type'].append('usability_sus')
            data['value'].append(sus)
            data['type'].append('usability_sus_6')
            data['value'].append((sus/100)*6)
            data['type'].append('attitude')
            data['value'].append(attitude)
            data['type'].append('choise')
            data['value'].append(choise)
        df = pandas.DataFrame(data)
        return df

    def att_size_dataframe(self):
        # tam
        cursor = self.db.cursor()
        sql = self.get_query('att_size')
        cursor.execute(sql)
        data = {'qnr': [], 'att_6': [], 'att_100': [], 'size': []}
        for row in cursor:
            data['qnr'].append(row[0])
            data['att_6'].append(row[1])
            data['att_100'].append(row[2])
            data['size'].append(row[3])
        df = pandas.DataFrame(data)
        return df

    def messwerte_dataframe(self):
        cursor = self.db.cursor()
        sql = self.get_query('messwerte')
        cursor.execute(sql)
        cases_prepare = {}
        data = {'case': [], 'LF-qnr2': [], 'Folder-qnr2': [], 'LF-qnr3': [], 'Folder-qnr3': []}
        for row in cursor:
            if not row[0] in cases_prepare.keys():
                cases_prepare[row[0]] = {'LF-qnr2': 0, 'Folder-qnr2': 0, 'LF-qnr3': 0, 'Folder-qnr3': 0}
            cases_prepare[row[0]][row[4]] = row[3]
        for case_key in cases_prepare.keys():
            data['case'].append(case_key)
            data['LF-qnr2'].append(cases_prepare[case_key]['LF-qnr2'])
            data['Folder-qnr2'].append(cases_prepare[case_key]['Folder-qnr2'])
            data['LF-qnr3'].append(cases_prepare[case_key]['LF-qnr3'])
            data['Folder-qnr3'].append(cases_prepare[case_key]['Folder-qnr3'])
        df = pandas.DataFrame(data)
        return df

    def attributes_dataframe(self):
        # FB12_01
        # Create a Data-Frame for the Utility scale
        # sql = self.get_query('utility')
        # df = pandas.read_sql(sql, 'sqlite:///data/data.sqlite')
        # return df
        cursor = self.db.cursor()
        sql = self.get_query('attributes')
        cursor.execute(sql)
        data = {'case': [], 'qnr': [], 'Fall': [], 'Konzept': [], 'Attribut': [], 'Bereich': [], 'Bewertung': []}
        for row in cursor:
            for i in range(0, 6):
                for j in range(1, 5):
                    data['case'].append(row[0])
                    data['qnr'].append(row[1])
                    bereich = ''
                    if i is 0 or i is 3:
                        bereich = 'Insgesamt'
                        data['Bereich'].append(bereich)
                    elif i is 1 or i is 4:
                        bereich = 'Dateiverwaltung'
                        data['Bereich'].append(bereich)
                    elif i is 2 or i is 5:
                        bereich = 'Informationsverwaltung'
                        data['Bereich'].append(bereich)
                    data['Konzept'].append('Ordner' if i <= 2 else 'LinkFlow')
                    data['Fall'].append(('Ordner' if i <= 2 else 'LinkFlow') +
                                        (' Einsortieren' if row[1] == 'qnr2' else ' Auffinden') + ' (' + bereich + ')')
                    if j is 1:
                        data['Attribut'].append('langsam/schnell')
                    elif j is 2:
                        data['Attribut'].append('chaotisch/übersichtlich')
                    elif j is 3:
                        data['Attribut'].append('kompliziert/einfach')
                    elif j is 4:
                        data['Attribut'].append('zeitraubend/unterstützend')
                    data['Bewertung'].append(row[2 + (4 * i) + (j - 1)])
        df = pandas.DataFrame(data)
        return df



    # MAIN LEVEL
    def analyse(self):
        sns.set_context("paper")
        p = matplotlib.rcParams
        matplotlib.rcParams['axes.titleweight'] = 'bold'
        matplotlib.rcParams['axes.titlesize'] = 'x-large'
        matplotlib.rcParams['figure.dpi'] = 250
        # matplotlib.rcParams['figure.figsize'] = [8.5, 6]
        self.set_color_palette_1_hues()
        self.analyse_tam()
        self.set_color_palett_2()
        self.analyse_messwerte()
        self.analyse_attribute()

    # SECOND LEVELS
    def analyse_tam(self):
        if self.tam is None:
            self.tam = self.tam_dataframe()
        print('')
        print('# 1. Analyse TAM')
        self.analyse_tam_mean_sd()
        print('')
        print('')
        print('==============================')
        print('')

        pass

    def analyse_messwerte(self):
        if self.messwerte is None:
            self.messwerte = self.messwerte_dataframe()
        print('')
        print('# 2. Analyse Messwerte')
        self.analyse_messwerte_alles()
        print('')
        print('')
        print('==============================')
        print('')

    def analyse_attribute(self):
        pass

    # THIRD LEVEL
    def analyse_tam_mean_sd(self):
        # UTILITY / NÜTZLICHKEIT
        utility_mean = self.tam['utility'].mean()
        utility_sd = self.tam['utility'].std()
        utility_qnr2_mean = self.tam.query('qnr == "qnr2"')['utility'].mean()
        utility_qnr2_sd = self.tam.query('qnr == "qnr2"')['utility'].std()
        utility_qnr3_mean = self.tam.query('qnr == "qnr3"')['utility'].mean()
        utility_qnr3_sd = self.tam.query('qnr == "qnr3"')['utility'].std()
        # utility verteilung:
        verteilung = {'Bewertung': [], 'Anzahl Bewertungen': [], 'Anzahl Bewertungen qnr2': [],
                      'Anzahl Bewertungen qnr3': []}
        for i in range(0, 7, 1):
            verteilung['Bewertung'].append(i)
            bewertungen_gesamt = self.tam.query(f'utility == "{i}"')['utility'].count()
            bewertungen_qnr2 = self.tam.query(f'qnr == "qnr2" & utility == "{i}"')['utility'].count()
            bewertungen_qnr3 = self.tam.query(f'qnr == "qnr3" & utility == "{i}"')['utility'].count()
            verteilung['Anzahl Bewertungen'].append(bewertungen_gesamt)
            verteilung['Anzahl Bewertungen qnr2'].append(bewertungen_qnr2)
            verteilung['Anzahl Bewertungen qnr3'].append(bewertungen_qnr3)
        print('')
        print('## Nützlichkeit:')
        print('### Gesamt:')
        print('Mean | SD')
        print(f'{utility_mean} | {utility_sd}')
        print('### Einordnen:')
        print('Mean | SD')
        print(f'{utility_qnr2_mean} | {utility_qnr2_sd}')
        print('### Aufrufen:')
        print('Mean | SD')
        print(f'{utility_qnr3_mean} | {utility_qnr3_sd}')
        print('')
        print('Verteilung:')
        print('Durchgang: 0 | 1 | 2 | 3 | 4 | 5 | 6')
        print(f'qnr2:      ', *verteilung["Anzahl Bewertungen qnr2"], sep=' | ')
        print(f'qnr3:      ', *verteilung["Anzahl Bewertungen qnr3"], sep=' | ')
        print(f'gesamt:    ', *verteilung["Anzahl Bewertungen"], sep=' | ')

        sns.set_style('whitegrid')
        verteilung_df = verteilung
        verteilung_df.pop('Anzahl Bewertungen')
        df = DataFrame(verteilung_df)
        self.barchart_count_plot(data=df, x='Bewertung', y=None,
                                 series_lables=['Bewertung nach\ndem Einsortieren', 'Bewertung nach\ndem Aufrufen'],
                                 title='Bewertung der Nützlichkeit\nnach Aufgabe 1 und 2',
                                 ylabel='Anzahl\nBewertungen',
                                 xtickslabels=['0\nVöllig\nunbrauchbar', '1', '2', '3', '4', '5',
                                                 '6\nSehr\nnützlich'], y_scale_max=13,
                                 show_bar_values=True, bar_width=0.4, stacked=True)

        # USABILITY
        sus_mean = self.tam['usability'].mean()
        sus_sd = self.tam['usability'].std()
        sus_qnr2_mean = self.tam.query('qnr == "qnr2"')['usability'].mean()
        sus_qnr2_sd = self.tam.query('qnr == "qnr2"')['usability'].std()
        sus_qnr3_mean = self.tam.query('qnr == "qnr3"')['usability'].mean()
        sus_qnr3_sd = self.tam.query('qnr == "qnr3"')['usability'].std()
        # usability Verteilung:
        verteilung_sus = {'Bewertung': [], 'Anzahl Bewertungen': [], 'Anzahl Bewertungen qnr2': [],
                          'Anzahl Bewertungen qnr3': []}
        sus_stepsize = 10
        for i in range(0, (100 + sus_stepsize), sus_stepsize):
            verteilung_sus['Bewertung'].append(i - sus_stepsize/2)
            bewertungen_sus_gesamt = self.tam.query(f'usability > {i - sus_stepsize} & usability <= {i}')[
                'usability'].count()
            bewertungen_sus_qnr2 = self.tam.query(f'qnr == "qnr2" & usability > {i - sus_stepsize} & usability <= {i}')[
                'usability'].count()
            bewertungen_sus_qnr3 = self.tam.query(f'qnr == "qnr3" & usability > {i - sus_stepsize} & usability <= {i}')[
                'usability'].count()
            verteilung_sus['Anzahl Bewertungen'].append(bewertungen_sus_gesamt)
            verteilung_sus['Anzahl Bewertungen qnr2'].append(bewertungen_sus_qnr2)
            verteilung_sus['Anzahl Bewertungen qnr3'].append(bewertungen_sus_qnr3)
        print('')
        print('## Usability (SUS):')
        print('### Gesamt:')
        print('Mean | SD')
        print(f'{sus_mean} | {sus_sd}')
        print('### Einordnen:')
        print('Mean | SD')
        print(f'{sus_qnr2_mean} | {sus_qnr2_sd}')
        print('### Aufrufen:')
        print('Mean | SD')
        print(f'{sus_qnr3_mean} | {sus_qnr3_sd}')
        print('')
        print('Verteilung:')
        print('Durchgang:  ',
              ' '.join([str(i - sus_stepsize) + ' - ' + str(i) + ' | ' for i in verteilung_sus["Bewertung"]]))
        print(f'qnr2:  ', *verteilung_sus["Anzahl Bewertungen qnr2"], sep='  |       ')
        print(f'qnr3:  ', *verteilung_sus["Anzahl Bewertungen qnr3"], sep='  |       ')
        print(f'gesamt:', *verteilung_sus["Anzahl Bewertungen"], sep='  |       ')
        print('')

        verteilung_sus_df = verteilung_sus
        verteilung_sus_df.pop('Anzahl Bewertungen')
        df_sus = DataFrame(verteilung_sus_df)
        self.barchart_count_plot(data=df_sus, x='Bewertung', y=None,
                                 series_lables=['Bewertung nach\ndem Einsortieren', 'Bewertung nach\ndem Aufrufen'],
                                 title='Usability (SUS) Score\nnach Aufgabe 1 und 2',
                                 ylabel='Anzahl\nBewertungen', xlabel='SUS Score',
                                 x_ticks=range(0,11,1),
                                 xtickslabels=['', '0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'],
                                 x_scale_min=0, y_scale_max=8, show_bar_values=True, bar_width=0.4, stacked=True)

        # ATTITUDE TOWADS USING
        att_mean = self.tam['attitude'].mean()
        att_sd = self.tam['attitude'].std()
        att_qnr2_mean = self.tam.query('qnr == "qnr2"')['attitude'].mean()
        att_qnr2_sd = self.tam.query('qnr == "qnr2"')['attitude'].std()
        att_qnr3_mean = self.tam.query('qnr == "qnr3"')['attitude'].mean()
        att_qnr3_sd = self.tam.query('qnr == "qnr3"')['attitude'].std()
        # usability Verteilung:
        verteilung_att = {'Bewertung': [], 'Anzahl Bewertungen': [], 'Anzahl Bewertungen qnr2': [],
                          'Anzahl Bewertungen qnr3': []}
        for i in range(0, 7, 1):
            verteilung_att['Bewertung'].append(i)
            bewertungen_att_gesamt = self.tam.query(f'attitude == {i}')['attitude'].count()
            bewertungen_att_qnr2 = self.tam.query(f'qnr == "qnr2" & attitude == {i}')[
                'attitude'].count()
            bewertungen_att_qnr3 = self.tam.query(f'qnr == "qnr3" & attitude == {i}')[
                'attitude'].count()
            verteilung_att['Anzahl Bewertungen'].append(bewertungen_att_gesamt)
            verteilung_att['Anzahl Bewertungen qnr2'].append(bewertungen_att_qnr2)
            verteilung_att['Anzahl Bewertungen qnr3'].append(bewertungen_att_qnr3)
        print('')
        print('## Attitude towards using:')
        print('### Gesamt:')
        print('Mean | SD')
        print(f'{att_mean} | {att_sd}')
        print('### Einordnen:')
        print('Mean | SD')
        print(f'{att_qnr2_mean} | {att_qnr2_sd}')
        print('### Aufrufen:')
        print('Mean | SD')
        print(f'{att_qnr3_mean} | {att_qnr3_sd}')
        print('')
        print('Verteilung:')
        print('Durchgang: 0 | 1 | 2 | 3 | 4 | 5 | 6 ')
        print(f'qnr2:   ', *verteilung_att["Anzahl Bewertungen qnr2"], sep=' | ')
        print(f'qnr3:   ', *verteilung_att["Anzahl Bewertungen qnr3"], sep=' | ')
        print(f'gesamt: ', *verteilung_att["Anzahl Bewertungen"], sep=' | ')
        print('')
        print('')
        print('---')
        print('')

        verteilung_att_df = verteilung_att
        verteilung_att_df.pop('Anzahl Bewertungen')
        df_att = DataFrame(verteilung_att_df)
        self.barchart_count_plot(data=df_att, x='Bewertung', y=None,
                                 series_lables=['Bewertung nach\ndem Einsortieren', 'Bewertung nach\ndem Aufrufen'],
                                 title='Bereitschaft eine Software nach\n diesem Konzept zu nutzen\n(nach Aufgabe 1 und 2)',
                                 ylabel='Anzahl\nBewertungen', xlabel='',
                                 xtickslabels=['0\nNein, auf\nkeinen Fall', '1', '2', '3', '4', '5',
                                               '6\nJa, auf\njeden Fall'], show_bar_values=True,
                                 bar_width=0.4, stacked=True, y_scale_max=8.9)

        # Scatterplot TAM
        s = [0,0,0,0,0,0,0]
        attsize = {'att_6': [], 'att_100': [], 'size': []}
        for a in self.tam['attitude'].values:
            s[a] += 1
        for i in range(0, len(s), 1):
            attsize['att_6'].append(i)
            attsize['att_100'].append((i/6)*100)
            attsize['size'].append(s[i])
        att_size_df = DataFrame(attsize)

        # TODO Die ATT noch zeigen
        # TODO Werte überdecken sich und sind so nicht gut sichtbar
        # ax_scat_tam = sns.scatterplot(x="utility", y="usability", hue="qnr", data=self.tam, alpha=0.7, markers='qnr')
        ax_scat_tam = sns.scatterplot(x="utility", y="usability", data=self.tam.query('qnr == "qnr2"'), alpha=0.8, marker='X')
        sns.scatterplot(x="utility", y="usability", data=self.tam.query('qnr == "qnr3"'), ax=ax_scat_tam, alpha=0.6, marker='o')
        # colors = sns.color_palette("Greens_r")
        # sns.scatterplot(x='att_6', y='att_100', data=att_size_df, size='size', alpha=0.3, sizes=(0, 400), palette=colors)
        ax_scat_tam.set_xlim(0, 6.9)
        ax_scat_tam.set_ylim(0, 110)
        ax_scat_tam.set_xlabel('Bewertung Nützlichkeit')
        ax_scat_tam.set_ylabel('Bewertung Usability\n(SUS Score)')
        ax_scat_tam.set_title('Verteilung der Bewertungen von\nUsability und Nützlichkeit\n')
        # current_handles, current_labels = plt.gca().get_legend_handles_labels()
        # ax_scat_tam.legend(current_handles, ['Bewertungen Einsortieren', 'Bewertungen Auffinden'])
        ax_scat_tam.legend(['Bewertungen Einsortieren', 'Bewertungen Auffinden'], loc='upper left')
        plt.show()

        # Boxplot TAM
        df_tam_typed = self.tam_dataframe_typed_values()
        ax = sns.boxplot(x="value", y="type",
                         hue="qnr", data=df_tam_typed.query('type != "usability_sus" & type!= "choise"'),
                         width=0.4)
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('')
        ax.set_yticklabels(['Nützlichkeit', 'Usability (SUS)', 'Bereitschaft\nzur Nutzung'])
        ax.set_title('Verteilung der Bewertungen\n')
        ax.set_xlim(0, 6.5)
        current_handles, current_labels = plt.gca().get_legend_handles_labels()
        plt.legend(current_handles, ['Bewertungen Einsortieren', 'Bewertungen Auffinden'])
        plt.show()



        # ENTSCHEIDUNG ORDNER/LINKFLOW
        choise_total_mean = self.tam['choise'].mean()
        choise_total_sd = self.tam['choise'].std()
        choise_qnr2_mean = self.tam.query('qnr == "qnr2"')['choise'].mean()
        choise_qnr2_sd = self.tam.query('qnr == "qnr2"')['choise'].std()
        choise_qnr3_mean = self.tam.query('qnr == "qnr3"')['choise'].mean()
        choise_qnr3_sd = self.tam.query('qnr == "qnr3"')['choise'].std()
        # usability Verteilung:
        verteilung_choise = {'Bewertung': [], 'Anzahl Bewertungen': [], 'Anzahl Bewertungen qnr2': [],
                             'Anzahl Bewertungen qnr3': []}
        for i in range(0, 7, 1):
            verteilung_choise['Bewertung'].append(i)
            bewertungen_choise_gesamt = self.tam.query(f'choise == {i}')['choise'].count()
            bewertungen_choise_qnr2 = self.tam.query(f'qnr == "qnr2" & choise == {i}')['choise'].count()
            bewertungen_choise_qnr3 = self.tam.query(f'qnr == "qnr3" & choise == {i}')['choise'].count()
            verteilung_choise['Anzahl Bewertungen'].append(bewertungen_choise_gesamt)
            verteilung_choise['Anzahl Bewertungen qnr2'].append(bewertungen_choise_qnr2)
            verteilung_choise['Anzahl Bewertungen qnr3'].append(bewertungen_choise_qnr3)
        print('')
        print('## Entscheidung Ordner/LinkFlow:')
        print('')
        print('### Gesamt:')
        print('Mean | SD')
        print(f'{choise_total_mean} | {choise_total_sd}')
        print('### Einordnen:')
        print('Mean | SD')
        print(f'{choise_qnr2_mean} | {choise_qnr2_sd}')
        print('### Aufrufen:')
        print('Mean | SD')
        print(f'{choise_qnr3_mean} | {choise_qnr3_sd}')
        print('')
        print('Verteilung:')
        print('Fall:    Ordner --- |  -- |  -  |  0  |  +  | ++  | +++ LinkFlow')
        print(f'qnr2:       ', *verteilung_choise["Anzahl Bewertungen qnr2"], sep='  |  ')
        print(f'qnr3:       ', *verteilung_choise["Anzahl Bewertungen qnr3"], sep='  |  ')
        print(f'gesamt:     ', *verteilung_choise["Anzahl Bewertungen"], sep='  |  ')
        print('')
        print('')
        print('---')
        print('')

        verteilung_choise_df_prepare = verteilung_choise
        verteilung_choise_df_prepare.pop('Anzahl Bewertungen')
        df_choise = DataFrame(verteilung_choise_df_prepare)
        self.barchart_count_plot(data=df_choise, x='Bewertung', y=None,
                                 series_lables=['Bewertung nach\ndem Einsortieren', 'Bewertung nach\ndem Aufrufen'],
                                 title='Einschätzung der Tendenz ob eher\nOrdner oder LinkFlow verwendet werden würden',
                                 ylabel='Anzahl der\nEinschätzungen', xlabel='',
                                 xtickslabels=['0\nOrdner', '1', '2', '3\nunentschieden', '4', '5',
                                               '6\nLinkFlow'], show_bar_values=True,
                                 bar_width=0.4, stacked=True, x_scale_max=6.5, y_scale_max=8.9)

    def analyse_messwerte_alles(self):
        mean_interaktionen_einsortieren_LF = self.messwerte['LF-qnr2'].mean()
        sd_interaktionen_einsortieren_LF = self.messwerte['LF-qnr2'].std()
        mean_interaktionen_einsortieren_Folder = self.messwerte['Folder-qnr2'].mean()
        sd_interaktionen_einsortieren_Folder = self.messwerte['Folder-qnr2'].std()
        mean_interaktionen_aufrufen_LF = self.messwerte['LF-qnr3'].mean()
        sd_interaktionen_aufrufen_LF = self.messwerte['LF-qnr3'].std()
        mean_interaktionen_aufrufen_Folder = self.messwerte['Folder-qnr3'].mean()
        sd_interaktionen_aufrufen_Folder = self.messwerte['Folder-qnr3'].std()
        print('')
        print('## Übersicht Personen:')
        print(self.messwerte)
        print('')
        print('## Überblick Interaktionen Gesamt:')
        print('Fall: Mean | SD')
        print(f'Einsortieren LF:     {mean_interaktionen_einsortieren_LF} | {sd_interaktionen_einsortieren_LF}')
        print(f'Einsortieren Ordner: {mean_interaktionen_einsortieren_Folder} | {sd_interaktionen_einsortieren_Folder}')
        print(f'Aufrufen LF:         {mean_interaktionen_aufrufen_LF} | {sd_interaktionen_aufrufen_LF}')
        print(f'Aufrufen Ordner:     {mean_interaktionen_aufrufen_Folder} | {sd_interaktionen_aufrufen_Folder}')
        print('')
        print('')
        print('---')
        print('')

        # Barchart/Counts Anzahl Interaktionen
        c = sns.color_palette()
        c = c[:2]
        # colors = crayon_palette(["amber", "greyish", "faded green", "dusty purple"])
        sns.set_palette(c)

        daten_messwerte = {'qnr': [], 'mean_LF': [], 'mean_Folder': []}
        daten_messwerte['qnr'].append('qnr2')
        daten_messwerte['qnr'].append('qnr3')
        daten_messwerte['mean_LF'].append(round(mean_interaktionen_einsortieren_LF, 2))
        daten_messwerte['mean_Folder'].append(round(mean_interaktionen_einsortieren_Folder, 2))
        daten_messwerte['mean_LF'].append(round(mean_interaktionen_aufrufen_LF, 2))
        daten_messwerte['mean_Folder'].append(round(mean_interaktionen_aufrufen_Folder, 2))
        messwerte_gesamt = DataFrame(daten_messwerte)
        self.barchart_count_plot(data=messwerte_gesamt, x='qnr', y=None,
                                 series_lables=['Interaktionen LinkFlow', 'Interaktionen Ordner'],
                                 title='Durchschnittliche Anzahl an Interaktionen\nzum Einsortieren/Auffinden einer Items',
                                 ylabel='Anzahl Interaktionen', xlabel='', xtickslabels=['Einsortieren', 'Auffinden'],
                                 y_scale_max=110)
        # TODO Barchart mit SD (Standartabwichung)

        # Scatterplot Anzahl Interaktionen
        ax_scat_int = sns.scatterplot(x="LF-qnr2", y="LF-qnr3", data=self.messwerte)
        sns.scatterplot(x="Folder-qnr2", y="Folder-qnr3", data=self.messwerte, ax=ax_scat_int)
        ax_scat_int.set_xlabel('Anzahl Interaktionen\nbeim Einsortieren')
        ax_scat_int.set_ylabel('Anzahl Interaktionen\nbeim Auffinden')
        ax_scat_int.legend(['LinkFlow', 'Ordner'])
        ax_scat_int.set_xlim(left=0)
        ax_scat_int.set_ylim(bottom=0)
        ax_scat_int.set_title('Verhältnis aus Interaktionen beim Einsortiern\ngegen Interaktionen beim Auffinden\n')
        plt.show()

        # Scatterplot Interaktionen Retrival
        ax_scat_int = sns.scatterplot(x="LF-qnr3", y="Folder-qnr3", data=self.messwerte)
        ax_scat_int.set_xlabel('Durchschnitt Interaktionen\nLinkFlow')
        ax_scat_int.set_ylabel('Durchschnitt Interaktionen\nOrdner')
        #ax_scat_int.legend(['LinkFlow', 'Ordner'])
        ax_scat_int.set_xlim(left=0)
        ax_scat_int.set_ylim(bottom=0)
        ax_scat_int.set_title('Verhältniss der Interaktionen\n beim Auffinden in beiden Systemen\n')
        plt.show()

        # Zweiseitiger Wilcoxon Vorzeichen-Rang-Summentest
        statistic, pvalue = scipy.stats.wilcoxon(x=self.messwerte['LF-qnr2'], y=self.messwerte['Folder-qnr2'])
        statistic_1, pvalue_1 = scipy.stats.wilcoxon(x=self.messwerte['LF-qnr2'], y=self.messwerte['Folder-qnr2'], alternative='two-sided')
        statistic_2, pvalue_2 = scipy.stats.wilcoxon(x=self.messwerte['LF-qnr3'], y=self.messwerte['Folder-qnr3'])
        statistic_3, pvalue_3 = scipy.stats.wilcoxon(x=self.messwerte['LF-qnr3'], y=self.messwerte['Folder-qnr3'], alternative='two-sided')
        print('')
        print('')
        print('Messdaten - Einsortieren')
        print('Zweiseitiger Wilcoxon Vorzeichen-Rang-Summentest')
        print(f'Kleinster W-Wert (kleinester Vorzeichenwert): {statistic}')
        print(f'P-Wert (laut SciPy): {pvalue}')
        print('')
        print('')


        '''
        data_mess = {'case': [], 'System': [], 'Aufgabe': [], 'Wert': []}
        for index, i in self.messwerte.iterrows():
            for j in range(0,4,1):
                data_mess['case'].append(i['case'])
            data_mess['System'].append('LinkFlow')
            data_mess['Aufgabe'].append('Aufgabe Einsortieren')
            data_mess['Wert'].append(i['LF-qnr2'])
            data_mess['System'].append('Ordner')
            data_mess['Aufgabe'].append('Aufgabe Einsortieren')
            data_mess['Wert'].append(i['Folder-qnr2'])
            data_mess['System'].append('LinkFlow')
            data_mess['Aufgabe'].append('Aufgabe Auffinden')
            data_mess['Wert'].append(i['LF-qnr3'])
            data_mess['System'].append('Ordner')
            data_mess['Aufgabe'].append('Aufgabe Auffinden')
            data_mess['Wert'].append(i['Folder-qnr3'])

        messwerte_df_2 = DataFrame(data_mess)

        # Boxplot Interaktionen
        ax = sns.boxplot(x="Wert", y="Aufgabe",
                         data=messwerte_df_2, hue='System',
                         width=0.5)
        ax.set_xlabel('Durchscnittliche Anzahl an Interaktionen')
        ax.set_ylabel('Aufgabe')
        # ax.set_xticklabels(['', '1\nschlecht', '', '2', '', '3', '', '4', '', '5\ngut'])
        ax.set_title('Attribute nach System und Anwendungsfall\n')
        # plt.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))
        # plt.tight_layout(pad=8)
        # plt.legend(loc=9, bbox_to_anchor=(0.33, -0.22), ncol=2)
        # current_handles, current_labels = plt.gca().get_legend_handles_labels()
        # plt.legend(current_handles, ['Bewertungen Einsortieren', 'Bewertungen Auffinden'])
        plt.show()
        '''

    def analyse_attribute(self):
        if self.attribute is None:
            self.attribute = self.attributes_dataframe()

        df_att_ordner_gesamt = self.attribute.query('Bereich == "Insgesamt" & Konzept == "Ordner"')
        df_att_LF_gesamt = self.attribute.query('Bereich == "Insgesamt" & Konzept == "LinkFlow"')

        schnelligkeit_LF_qnr2_mean = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "langsam/schnell"')['Bewertung'].mean()
        schnelligkeit_LF_qnr2_sd = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "langsam/schnell"')['Bewertung'].std()
        schnelligkeit_Folder_qnr2_mean = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "langsam/schnell"')['Bewertung'].mean()
        schnelligkeit_Folder_qnr2_sd = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "langsam/schnell"')['Bewertung'].std()
        übersichtlichkeit_LF_qnr2_mean = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "chaotisch/übersichtlich"')['Bewertung'].mean()
        übersichtlichkeit_LF_qnr2_sd = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "chaotisch/übersichtlich"')['Bewertung'].std()
        übersichtlichkeit_Folder_qnr2_mean = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "chaotisch/übersichtlich"')['Bewertung'].mean()
        übersichtlichkeit_Folder_qnr2_sd = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "chaotisch/übersichtlich"')['Bewertung'].std()
        einfachkeit_LF_qnr2_mean = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "kompliziert/einfach"')['Bewertung'].mean()
        einfachkeit_LF_qnr2_sd = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "kompliziert/einfach"')['Bewertung'].std()
        einfachkeit_Folder_qnr2_mean = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "kompliziert/einfach"')['Bewertung'].mean()
        einfachkeit_Folder_qnr2_sd = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "kompliziert/einfach"')['Bewertung'].std()
        unterstützend_LF_qnr2_mean = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'].mean()
        unterstützend_LF_qnr2_sd = df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'].std()
        unterstützend_Folder_qnr2_mean = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'].mean()
        unterstützend_Folder_qnr2_sd = df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'].std()

        schnelligkeit_LF_qnr3_mean = df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "langsam/schnell"')[
            'Bewertung'].mean()
        schnelligkeit_LF_qnr3_sd = df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "langsam/schnell"')[
            'Bewertung'].std()
        schnelligkeit_Folder_qnr3_mean = df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "langsam/schnell"')[
            'Bewertung'].mean()
        schnelligkeit_Folder_qnr3_sd = df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "langsam/schnell"')[
            'Bewertung'].std()
        übersichtlichkeit_LF_qnr3_mean = \
        df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "chaotisch/übersichtlich"')['Bewertung'].mean()
        übersichtlichkeit_LF_qnr3_sd = df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "chaotisch/übersichtlich"')[
            'Bewertung'].std()
        übersichtlichkeit_Folder_qnr3_mean = \
        df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "chaotisch/übersichtlich"')['Bewertung'].mean()
        übersichtlichkeit_Folder_qnr3_sd = \
        df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "chaotisch/übersichtlich"')['Bewertung'].std()
        einfachkeit_LF_qnr3_mean = df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "kompliziert/einfach"')[
            'Bewertung'].mean()
        einfachkeit_LF_qnr3_sd = df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "kompliziert/einfach"')[
            'Bewertung'].std()
        einfachkeit_Folder_qnr3_mean = df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "kompliziert/einfach"')[
            'Bewertung'].mean()
        einfachkeit_Folder_qnr3_sd = df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "kompliziert/einfach"')[
            'Bewertung'].std()
        unterstützend_LF_qnr3_mean = df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "zeitraubend/unterstützend"')[
            'Bewertung'].mean()
        unterstützend_LF_qnr3_sd = df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "zeitraubend/unterstützend"')[
            'Bewertung'].std()
        unterstützend_Folder_qnr3_mean = \
        df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "zeitraubend/unterstützend"')['Bewertung'].mean()
        unterstützend_Folder_qnr3_sd = \
        df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "zeitraubend/unterstützend"')['Bewertung'].std()

        print('')
        print('')
        print('Attribute - Mean+SD')
        print('Durchschnitt (arithmetisches Mittel) und Standartabweichung der Bewertungen der Attribute')
        print('Das Ergebnis sagt: Mit welcher Signifikant kann die Nullhypothese (die Bewertung beider Systeme ist ungefähr gleich, die unterschiede bestehen nur aus Zufall) verworfen werden?')
        print(f'| Attribut           | LinkFlow Einsortieren | LinkFlow Aufrufen | Ordner Einsortieren | Ordner Aufrufen |')
        print(f'|--------------------|-----------------------|-------------------|---------------------|-----------------|')
        print(f'| Schnelligkeit:     | {schnelligkeit_LF_qnr2_mean} (sd={schnelligkeit_LF_qnr2_sd}) | {schnelligkeit_LF_qnr3_mean} (sd={schnelligkeit_LF_qnr3_sd}) | {schnelligkeit_Folder_qnr2_mean} (sd={schnelligkeit_Folder_qnr2_sd}) | {schnelligkeit_Folder_qnr3_mean} (sd={schnelligkeit_Folder_qnr3_sd}) |')
        print(f'| Übersichtlichkeit: | {übersichtlichkeit_LF_qnr2_mean} (sd={übersichtlichkeit_LF_qnr2_sd}) | {übersichtlichkeit_LF_qnr3_mean} (sd={übersichtlichkeit_LF_qnr3_sd}) | {übersichtlichkeit_Folder_qnr2_mean} (sd={übersichtlichkeit_Folder_qnr2_sd}) | {übersichtlichkeit_Folder_qnr3_mean} (sd={übersichtlichkeit_Folder_qnr3_sd}) |')
        print(f'| Einfachkeit:       | {einfachkeit_LF_qnr2_mean} (sd={einfachkeit_LF_qnr2_sd}) | {einfachkeit_LF_qnr3_mean} (sd={einfachkeit_LF_qnr3_sd}) | {einfachkeit_Folder_qnr2_mean} (sd={einfachkeit_Folder_qnr2_sd}) | {einfachkeit_Folder_qnr3_mean} (sd={einfachkeit_Folder_qnr3_sd}) |')
        print(f'| Unterstützend:     | {unterstützend_LF_qnr2_mean} (sd={unterstützend_LF_qnr2_sd}) | {unterstützend_LF_qnr3_mean} (sd={unterstützend_LF_qnr3_sd}) | {unterstützend_Folder_qnr2_mean} (sd={unterstützend_Folder_qnr2_sd}) | {unterstützend_Folder_qnr3_mean} (sd={unterstützend_Folder_qnr3_sd}) |')
        print('')
        print('')

        self.attribute.sort_values(by=['Fall'])
        # Boxplot Attribute
        # palette = dict('Ordner Einsortieren (Insgesamt)': "#9b59b6", virginica="#3498db", versicolor="#95a5a6")
        c_muted = sns.color_palette("muted")
        c_pastel = sns.color_palette("pastel")
        palette =[c_muted[2], c_pastel[2], c_muted[8], c_pastel[8]]
        ax = sns.boxplot(x="Bewertung", y="Attribut",
                         hue="Fall", data=self.attribute.query('Bereich == "Insgesamt"').sort_values(by=['Konzept', 'qnr']), width=0.5, palette=palette)
        # ax = sns.swarmplot(x="Bewertung", y="Attribut", hue="Fall", data=self.attribute.query('Bereich == "Insgesamt"').sort_values(by=['Konzept', 'qnr']), color="r", size=2)
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Eingenschaft')
        ax.set_xticklabels(['', '1\nschlecht', '', '2', '', '3', '', '4', '', '5\ngut'])
        ax.set_title('Attribute nach System und Anwendungsfall\n')
        # plt.legend(loc='upper left', prop={'size': 7}, bbox_to_anchor=(1, 1))
        # plt.tight_layout(pad=8)
        plt.legend(loc=9, bbox_to_anchor=(0.33, -0.22), ncol=2)
        # current_handles, current_labels = plt.gca().get_legend_handles_labels()
        # plt.legend(current_handles, ['Bewertungen Einsortieren', 'Bewertungen Auffinden'])
        plt.show()

        df_att_ordner_gesamt = self.attribute.query('Bereich == "Insgesamt" & Konzept == "Ordner"')
        df_att_LF_gesamt = self.attribute.query('Bereich == "Insgesamt" & Konzept == "LinkFlow"')
        schnelligkeit_einsortieren_w_value, schnelligkeit_einsortieren_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "langsam/schnell"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "langsam/schnell"')['Bewertung'],
            alternative='two-sided')
        schnelligkeit_aufrufen_w_value, schnelligkeit_aufrufen_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "langsam/schnell"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "langsam/schnell"')['Bewertung'],
            alternative='two-sided')
        übersichtlichkeit_einsortieren_w_value, übersichtlichkeit_einsortieren_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "chaotisch/übersichtlich"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "chaotisch/übersichtlich"')['Bewertung'],
            alternative='two-sided')
        übersichtlichkeit_aufrufen_w_value, übersichtlichkeit_aufrufen_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "chaotisch/übersichtlich"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "chaotisch/übersichtlich"')['Bewertung'],
            alternative='two-sided')
        einfachkeit_einsortieren_w_value, einfachkeit_einsortieren_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "kompliziert/einfach"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "kompliziert/einfach"')['Bewertung'],
            alternative='two-sided')
        einfachkeit_aufrufen_w_value, einfachkeit_aufrufen_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr3" & Attribut == "kompliziert/einfach"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr3" & Attribut == "kompliziert/einfach"')['Bewertung'],
            alternative='two-sided')
        unterstützend_einsortieren_w_value, unterstützend_einsortieren_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'],
            alternative='two-sided')
        unterstützend_aufrufen_w_value, unterstützend_aufrufen_p_values = scipy.stats.wilcoxon(
            x=df_att_ordner_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'],
            y=df_att_LF_gesamt.query('qnr == "qnr2" & Attribut == "zeitraubend/unterstützend"')['Bewertung'],
            alternative='two-sided')

        print('')
        print('')
        print('Attribute - Signifikanz')
        print('Signifikanz nach dem Zweiseitigen Wilcoxon Vorzeichen-Rang-Summentest')
        print('Das Ergebnis sagt: Mit welcher Signifikant kann die Nullhypothese (die Bewertung beider Systeme ist ungefähr gleich, die unterschiede bestehen nur aus Zufall) verworfen werden?')
        print(f'| Attribut          | Einsortieren: p-Wert (w-Wert) | Aufrufen: p-Wert (w-Wert) |')
        print(f'|-------------------|-------------------------------|---------------------------|')
        print(f'| Schnelligkeit     | {schnelligkeit_einsortieren_p_values} ({schnelligkeit_einsortieren_w_value}) | {schnelligkeit_aufrufen_p_values} ({schnelligkeit_aufrufen_w_value}) |')
        print(f'| Übersichtlichkeit | {übersichtlichkeit_einsortieren_p_values} ({übersichtlichkeit_einsortieren_w_value}) | {übersichtlichkeit_aufrufen_p_values} ({übersichtlichkeit_aufrufen_w_value}) |')
        print(f'| Einfachheit       | {einfachkeit_einsortieren_p_values} ({einfachkeit_einsortieren_w_value}) | {einfachkeit_aufrufen_p_values} ({einfachkeit_aufrufen_w_value}) |')
        print(f'| Unterstützend     | {unterstützend_einsortieren_p_values} ({unterstützend_einsortieren_w_value}) | {unterstützend_aufrufen_p_values} ({unterstützend_aufrufen_w_value}) |')
        print('')
        print('')

    def set_color_palette_1_hues(self):
        c_muted = sns.color_palette("muted")
        c_pastel = sns.color_palette("pastel")
        c = []
        for i in range(0,len(c_muted),1):
            c.append(c_muted[i])
            c.append(c_pastel[i])
        sns.set_palette(c)

    def set_color_palett_2(self):
        c = sns.color_palette("deep")
        c = [c[2], c[8], c[3], c[4], c[5], c[6], c[7], c[9]]
        sns.set_palette(c)

    def barchart_count_plot(self, data: DataFrame, x: str, y:str, series_lables: [str],
                            title: str = None, ylabel: str = None, xlabel: str = None, xtickslabels: [str] = None,
                            show_legend: bool = True, bar_width: float = 0.35, chart_type:str = 'bar',
                            show_bar_values: bool = True, stacked: bool = False, hide_zero: bool = True,
                            show_stacked_sum: bool = False, bar_values_offset: int = 1,
                            x_ticks: [] = None,
                            x_scale_min: float = None, x_scale_max: float = None,
                            y_scale_min: float = None, y_scale_max: float = None):

        ax = data.plot(x=x, y=y, kind=chart_type, width=bar_width, alpha=0.85, rot=0, stacked=stacked)
        # Add some text for labels, title and custom x-axis tick labels, etc.
        if len(series_lables) > 0 and show_legend:
            ax.legend(series_lables)
        elif show_legend:
            ax.legend()
        if x_scale_min is not None:
            ax.set_xlim(left=x_scale_min)
        if x_scale_max is not None:
            ax.set_xlim(right=x_scale_max)
        if y_scale_min is not None:
            ax.set_ylim(bottom=y_scale_min)
        if y_scale_max is not None:
            ax.set_ylim(top=y_scale_max)
        if title is not None:
            ax.set_title(title + '\n')
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if x_ticks is not None:
            ax.set_xticks(x_ticks, minor=True)
        if xtickslabels is not None:
            ax.set_xticklabels(xtickslabels)

        def autolabel():
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in ax.patches:
                rect  # type: plt.Rectangle
                height = rect.get_height() + rect.get_y()
                height_text = height
                if hide_zero and height == 0:
                    continue
                if show_stacked_sum and rect.get_y() != 0:
                    height_text = f'{height}\n({rect.get_y()}+{rect.get_height()})'
                ax.annotate('{}'.format(height_text),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, bar_values_offset),  # 1 point vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        if show_bar_values:
                autolabel()
        plt.show()



e = AnalystMain()
e.analyse()

