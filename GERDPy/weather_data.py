# -*- coding: utf-8 -*-
""" GERDPy - 'weather_data.py'
    
    Import of weather data from Excel-File

    Authors: Yannick Apfel, Meike Martin
"""
def get_weather_data(Nt, self):

    import sys
    import numpy as np
    import pandas as pd

    # path to excel-file
    path = self.ui.line_weather_file.text()  # './data/Wetterdaten_München-Riem_h.xlsx'

    # import data
    data = pd.read_excel(path, skiprows=3, header=1)

    # get startdate
    day = self.ui.sb_day.value()
    month = int(self.ui.cb_month.currentData())

    # create a list of row indices based on startdate
    start_index = data.index[(data.iloc[:, 0] == month) & (data.iloc[:, 1] == day)].tolist()[0]

    if start_index+Nt > len(data):
        if 0 != start_index:
            rows = list(range(start_index, len(data), 1)) + list(range(0, start_index, 1))
        else:
            rows = list(range(len(data)))
    else:
        rows = list(range(start_index, start_index+Nt, 1))

    # 1.) ambient wind speed [m/s]
    u_inf = np.array(data.iloc[rows, 6])

    # 2.) ambient temperature [°C]
    Theta_inf = np.array(data.iloc[rows, 4])

    # 3.) snowfall rate [mm/h]
    S_w = np.array(data.iloc[rows, 3])
    # sets entries to 0, in case Theta_inf >= 1 °C (precipitation comes down as rain)
    for i, j in enumerate(Theta_inf):
        if j >= 1:
            S_w[i] = 0

    # 4.) cloudiness [octal units/8]
    ''' between 0/8 - cloudless and 
                8/8 - fully overcast
    '''
    B = np.array(data.iloc[rows, 7]) / 8

    # 5.) relative humidity [-]
    Phi = np.array(data.iloc[rows, 5]) / 100

    # 6.) total precipitation [mm/h]
    RR = np.array(data.iloc[rows, 3])

    return u_inf, Theta_inf, S_w, B, Phi, RR
