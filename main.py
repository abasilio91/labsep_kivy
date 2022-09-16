# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 22:27:09 2021

@author: adam_
"""

from kivy.config import Config

# Config.set('graphics', 'width', '1200')
# Config.set('graphics', 'height', '600')

import tkinter as tk
import os
import datetime
import pandas as pd
import csv

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock

from tkinter import filedialog, messagebox
from pathlib import Path

from graphs import count_over_time

class MainWidget(BoxLayout):
    filename = StringProperty('')
    folder_path = StringProperty('dados/TXT')
    material = StringProperty('')
    num_points = StringProperty('10')
    posx = StringProperty('')
    posz = StringProperty('')
    time = StringProperty('20.0')
    angle = StringProperty('90')
    temperature = StringProperty('25')
    plot_img = StringProperty('imgs/empty.png')

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.date = datetime.date.today()
        Clock.schedule_interval(self.update, 30)

    # Compile the new data to a dataframe
    def add_measure(self):
        self.on_material_val(self.ids.material)
        self.on_posx_val(self.ids.posx)
        self.on_posz_val(self.ids.posz)
        self.on_num_points_val(self.ids.num_points)
        self.on_time_val(self.ids.time)
        self.on_filename_val(self.ids.filename)
        self.on_angle_val(self.ids.angle)
        self.on_temperature_val(self.ids.temperature)
        self.get_measure()

        if not Path(f'resultados/{self.filename}.csv').is_file():
            self.create_file()

        with open(f'resultados/{self.filename}.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            for index in range(int(self.num_points)):
                self.data = [self.date,
                            self.material,
                            index,
                            self.posx,
                            self.posz,
                            self.measure[index],
                            (float(self.time) * index),
                            self.angle,
                            self.temperature]
                writer.writerow(self.data)

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(message='Ponto adicionado com sucesso!')
        root.destroy()

    # Create a .csv file to store the data, if the file doesn't already exist
    def create_file(self):
        header = ['data', 'material', 'ponto', 'x', 'z', 'contagem', 'tempo(s)','inclinação (graus)', 'Temperatura (ºC)']

        with open(f'resultados/{self.filename}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            file.close()

    # Choose the file containing the data collected
    def get_data_file(self):
        root = tk.Tk()
        root.withdraw()

        self.filename = filedialog.askopenfilename()
        self.filename = os.path.basename(self.filename)
        self.filename = self.filename.split(sep='.')[0]
        root.destroy()

    # Choose the folder which contains the data files
    def get_measures_folder(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        self.folder_path = filedialog.askdirectory()
        root.destroy()

    # Get the measure data from the TARG results
    def get_measure(self):
        files = Path(self.folder_path).glob('*.txt')
        measures = []

        for filename in files:
            df = pd.read_csv(filename, header=0, skiprows=4, sep=" ", skipinitialspace=True)
            measures.append(df['GROSS'][0])

        self.measure = measures

    # Kivy widget handles
    def on_filename_val(self, widget):
        self.filename = widget.text
        self.ids.material.focus = True

    def on_material_val(self, widget):
        self.material = widget.text
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
        self.ids.angle.focus = True

    def on_angle_val(self, widget):
        self.angle = widget.text
        self.ids.temperature.focus = True

    def on_temperature_val(self, widget):
        self.temperature = widget.text

    def update(self, dt):
        count_over_time(self.folder_path, self.posx, self.posz)
        self.plot_img = "imgs/count_over_time.png"
        self.ids.img_plot.reload()

class LabSepApp(App):
    pass

LabSepApp().run()