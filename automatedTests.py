import b3
import time
import tensorflow as tf
import os

stock = ['PETR3', 'VALE3', 'ITUB3', 'ABEV3']

year = '2018'
for s in stock:
    for i in range(20, 220, 20):
        command = 'python b3.py ' + s + ' ' + year + ' ' + str(i)
        os.system(command)
