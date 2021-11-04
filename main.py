# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 22:27:09 2021

@author: adam_
"""

from kivy.config import Config

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import datetime
import pandas as pd
from pathlib import Path
import numpy as np
import csv

class MainWidget(RelativeLayout):
    expType = StringProperty('Varredura')
    filename = StringProperty('')
    folder_path = StringProperty('dados/TXT')
    time_elapsed = StringProperty('')
    material = StringProperty('')
    num_points = StringProperty('10')
    posx = StringProperty('')
    posz = StringProperty('')
    time = StringProperty('20.0')

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.date = datetime.date.today()

    # Compile the new data to a dataframe
    def add_measure(self):
        self.on_material_val(self.ids.material)
        self.on_posx_val(self.ids.posx)
        self.on_posz_val(self.ids.posz)
        self.on_num_points_val(self.ids.num_points)
        self.on_time_val(self.ids.time)
        self.on_filename_val(self.ids.filename)
        self.get_measure_average_sd()

        if Path(f'resultados/{self.filename}.csv').is_file():
            self.time_diff = self.get_time_diff()
        else:
            self.create_file()
            self.time_diff = 0

        if self.expType == 'Varredura':
            if self.ids.auto_count.active:
                self.time_elapsed = self.get_time_elapsed()
            else:
                self.on_time_elapsed_val(self.ids.time_elapsed)

            self.data = [self.date,
                         float(self.time_elapsed)+float(self.time_diff),
                         self.material,
                         int(self.num_points),
                         float(self.posx),
                         float(self.posz),
                         float(self.average),
                         float(self.sd),
                         float(self.time)]

            with open(f'resultados/{self.filename}.csv','a',newline= '') as file:
                writer = csv.writer(file)
                writer.writerow(self.data)
                file.close()

        else:   # Ponto Fixo
            with open(f'resultados/{self.filename}.csv', 'a', newline='') as file:
                writer = csv.writer(file)

                for index in range(int(self.num_points)):
                    self.data = [self.date,
                                 self.material,
                                 index,
                                 self.posx,
                                 self.posz,
                                 self.measure[index],
                                 (float(self.time) * index)]
                    writer.writerow(self.data)
                file.close()

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(message='Ponto adicionado com sucesso!')
        root.destroy()

    # Create a .csv file to store the data, if the file doesn't already exist
    def create_file(self):
        if self.expType == 'Varredura':
            header = ['data', 'dia', 'material', 'num pontos', 'x', 'z', 'media contagem', 'sd contagem', 'tempo(s)']
        else:
            header = ['data', 'material', 'ponto', 'x', 'z', 'contagem', 'tempo(s)']

        with open(f'resultados/{self.filename}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            file.close()

    # Select the type of experiment
    def exptype_select(self, widget):
        if widget.active:
            self.expType = 'Varredura'
        else:
            self.expType = 'Ponto fixo'

    # Choose the file containing the data collected
    def get_data_file(self):
        root = tk.Tk()
        root.withdraw()

        self.filename = filedialog.askopenfilename()
        self.filename = os.path.basename(self.filename)
        self.filename = self.filename.split(sep='.')[0]
        root.destroy()

        self.time_elapsed = self.get_time_elapsed()

    # Get the number of days elapsed since the beginning of the experiment from an existing file.
    def get_time_elapsed(self):
        if Path(f'resultados/{self.filename}.csv').is_file():
            df = pd.read_csv(f'resultados/{self.filename}.csv')
            if df['dia'].tolist() == []:
                time_elapsed = '0'
            else:
                df = pd.read_csv(f'resultados/{self.filename}.csv')
                time_elapsed = str(df['dia'].tolist()[-1])
        else:
            time_elapsed = '0'
        return time_elapsed

    # Choose the folder which contains the data files
    def get_measures_folder(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        self.folder_path = filedialog.askdirectory()
        root.destroy()

    # Calculate the time passed from the last measure to the current one
    def get_time_diff(self):
        df = pd.read_csv(f'resultados/{self.filename}.csv')
        last_measure = datetime.datetime.strptime(df['data'].tolist()[-1], '%Y-%m-%d').date()
        time_diff = self.date - last_measure
        return time_diff.days

    # Get the measure data from the TARG results and calculates its average and standard deviation
    def get_measure_average_sd(self):
        files = Path(self.folder_path).glob('*.txt')
        measures = []

        for filename, index in zip(files, range(int(self.num_points))):
            df = pd.read_csv(filename, header=0, skiprows=4, sep=" ", skipinitialspace=True)
            measures.append(df['GROSS'][0])

        self.measure = measures
        self.average = np.average(measures)
        self.sd = np.std(measures)

    # Kivy widget handles
    def on_filename_val(self, widget):
        self.filename = widget.text

        if self.ids.exp_controller.active:
            self.time_elapsed = self.get_time_elapsed()

        self.ids.material.focus = True

    def on_material_val(self, widget):
        self.material = widget.text

        if self.ids.auto_count.active:
            self.ids.posx.focus = True
        else:
            self.ids.time_elapsed.focus = True

    def on_time_elapsed_val(self, widget):
        self.time_elapsed = widget.text
        self.ids.posx.focus = True

    def on_posx_val(self, widget):
        self.posx = widget.text
        self.ids.posz.focus = True

    def on_posz_val(self, widget):
        self.posz = widget.text
        self.ids.num_points.focus = True

    def on_num_points_val(self, widget):
        self.num_points = widget.text
        self.ids.time.focus = True

    def on_time_val(self, widget):
        self.time = widget.text

class LabSepApp(App):
    pass

if __name__ == '__main__':
    LabSepApp().run()