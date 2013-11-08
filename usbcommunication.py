# -*- coding: utf-8 -*-

import serial
ser = serial.Serial('COM6', 9600)
while True:
    print ser.readline();
    