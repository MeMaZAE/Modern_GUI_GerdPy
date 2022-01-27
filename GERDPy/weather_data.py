# -*- coding: utf-8 -*-
""" Import der notwendigen Wetterdaten aus .csv-File

    Autor: Yannick Apfel
"""


def get_weather_data(Nt, self):

    import numpy as np
    import pandas as pd

    # Dateipfad der Wetterdaten-Datei definieren
    path = self.ui.line_weather_file.text()  # './data/Wetterdaten_München-Riem_h.xlsx'

    # Wetterdaten importieren
    data = pd.read_excel(path)

    # 1.) Windgeschwindigkeit [m/s]
    u_inf = np.array(data.iloc[4:(Nt+4), 6], dtype='float')

    # 2.) Umgebungstemperatur [°C]
    Theta_inf = np.array(data.iloc[4:(Nt+4), 4], dtype='float')

    # 3.) Schneefallrate [mm/h]
    S_w = np.array(data.iloc[4:(Nt + 4), 3], dtype='float')
    # Einträge zu null setzen, falls Theta_inf >= 1 °C (Niederschlag fällt als Regen)
    for i, j in enumerate(Theta_inf):
        if j >= 1:
            S_w[i] = 0

    # 4.) Bewölkungsgrad [-]
    '''  zwischen 0/8 - wolkenlos und 8/8 - bedeckt
    '''
    B = np.array(data.iloc[4:(Nt + 4), 7], dtype='int') / 8

    # 5.) rel. Luftfeuchte [-]
    Phi = np.array(data.iloc[4:(Nt + 4), 5], dtype='float') / 100

    # 6.) gesamte Niederschlagsmenge [mm/h]
    RR = np.array(data.iloc[4:(Nt + 4), 3], dtype='float')

    return u_inf, Theta_inf, S_w, B, Phi, RR
