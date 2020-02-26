import cv2
import numpy as np
import pandas as pd

from scipy.stats import bernoulli
DRIVING_LOG_FILE = './Data/example.csv'

data = pd.read_csv(DRIVING_LOG_FILE)
num_of_img = len(data)
non_zero = data['x'][data['x'] != 0]
zeros = data['x'][data['x'] == 0]
print("Non_Zero : " + str(len(non_zero)))
print("Zeros : " + str(len(zeros)))
print("Total : " + str(num_of_img))

