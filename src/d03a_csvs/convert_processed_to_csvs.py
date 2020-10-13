import pickle
import os
import pandas
directory = '../../data/03_processed/'
for filename in os.listdir(directory):
     df = pickle.load(open(directory + filename, "rb" ))
     df.to_csv('../../data/04_processed_csv/' + filename[:-2] + '.csv')
