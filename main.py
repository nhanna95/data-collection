from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import pandas as pd
import numpy as np
import sys

crop_data = dict(pd.read_csv('crop_data.csv'))
total_data = [[crop_data['crop'][i], crop_data['temperature'][i], crop_data['humidity']
               [i], crop_data['rainfall'][i]] for i in range(len(crop_data['crop']))]


def order_crops(temp, moisture, humidity):
    try:
        temp = float(temp)
        moisture = float(moisture)
        humidity = float(humidity)
    except:
        return None
    l = []
    for i in range(len(total_data)):
        diff = [total_data[i][1]-temp, total_data[i]
                [2]-humidity, total_data[i][3]-moisture]
        l.append([total_data[i][0], np.linalg.norm(diff)])

    l_sorted = sorted(l, key=lambda x: x[1])
    return l_sorted


def get_temp_num(temp):
    temp = float(temp)
    thing = [18.87284, 21.8378, 22.3892, 23.6893,
             25.5404, 25.5917, 27.4098, 27.3767, 31.2087]
    for i in range(len(thing)):
        if thing[i] > temp:
            return i
    return len(thing) - 1


def get_moisture_num(moisture):
    moisture = float(moisture)
    thing = [45.6804, 50.7862, 69.6118, 80.398, 84.766, 94.704,
             104.626, 110.474, 112.654, 142.627, 158.066, 175.686, 236.181]
    for i in range(len(thing)):
        if thing[i] > moisture:
            return i
    return len(thing) - 1


def get_humidity_num(humidity):
    humidity = float(humidity)
    thing = [50.156, 65.0922, 80.358, 82.2728,
             92.1702, 92.403387, 92.3333, 94.8442]
    for i in range(len(thing)):
        if thing[i] > humidity:
            return i
    return len(thing) - 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Crop Finder")

        layout = QGridLayout()
        self.temp_input = QLineEdit()
        self.temp_input.setValidator(QDoubleValidator(0.01, 99.99, 2))
        layout.addWidget(self.temp_input, 0, 1)
        layout.addWidget(QLabel('Temperature: '), 0, 0)
        self.moisture_input = QLineEdit()
        self.moisture_input.setValidator(QDoubleValidator(0.01, 99.99, 2))
        layout.addWidget(self.moisture_input, 1, 1)
        layout.addWidget(QLabel('Moisture: '), 1, 0)
        self.humidity_input = QLineEdit()
        self.humidity_input.setValidator(QDoubleValidator(0.01, 99.99, 2))
        layout.addWidget(self.humidity_input, 2, 1)
        layout.addWidget(QLabel('Humidity: '), 2, 0)

        button = QPushButton("Find Best Crops")
        button.clicked.connect(self.get)
        layout.addWidget(button, 3, 0, 1, 2)

        button = QPushButton("Turn On High Contrast Mode")
        button.clicked.connect(self.high_contrast)
        layout.addWidget(button, 5, 0, 1, 2)

        starting_text = '\n' * 22
        self.crop_text_box = QLabel(starting_text)
        self.crop_text_box.setWordWrap(True)
        layout.addWidget(self.crop_text_box, 4, 0, 1, 2)

        thermo_image = QPixmap('temp0.png')
        thermo_image = thermo_image.scaled(350, 450)
        self.thermo_label = QLabel()
        self.thermo_label.setPixmap(thermo_image)
        layout.addWidget(self.thermo_label, 0, 2, 5, 1)

        guage_image = QPixmap('moisture0.png')
        guage_image = guage_image.scaled(350, 450)
        self.guage_label = QLabel()
        self.guage_label.setPixmap(guage_image)
        layout.addWidget(self.guage_label, 0, 3, 5, 1)

        rain_image = QPixmap('humidity0.png')
        rain_image = rain_image.scaled(275, 450)
        self.rain_label = QLabel()
        self.rain_label.setPixmap(rain_image)
        layout.addWidget(self.rain_label, 0, 4, 5, 1)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    def get(self):
        temp = self.temp_input.text()
        moisture = float(self.moisture_input.text()) * 10
        humidity = self.humidity_input.text()
        ranked_crops = order_crops(temp, moisture, humidity)
        label_text = ''
        for i in range(len(ranked_crops)):
            line = str(i + 1) + '. ' + ranked_crops[i][0] + ' (' + \
                str(round(float(ranked_crops[i][1]), 2)) + ')\n'
            label_text += line

        label_text = label_text[:-1]

        self.crop_text_box.setText(label_text)

        temp_num = get_temp_num(temp)
        thermo_image = QPixmap(f'temp{temp_num}.png')
        thermo_image = thermo_image.scaled(350, 450)
        self.thermo_label.setPixmap(thermo_image)

        moisture_temp = get_moisture_num(moisture)
        guage_image = QPixmap(f'moisture{moisture_temp}.png')
        guage_image = guage_image.scaled(350, 450)
        self.guage_label.setPixmap(guage_image)

        humidity_num = get_humidity_num(humidity)
        rain_image = QPixmap(f'humidity{humidity_num}.png')
        rain_image = rain_image.scaled(275, 450)
        self.rain_label.setPixmap(rain_image)

    def high_contrast(self):
        self.setStyleSheet('background-color: white;')


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
