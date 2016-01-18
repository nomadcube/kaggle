import sys

from time import time
from data_processing.transformation import sample_reader

path_train_sample = sys.argv[1] if len(
        sys.argv) >= 2 else '/Users/wumengling/PycharmProjects/kaggle/input_data/train.csv'

max_line = 2365436
sample_size = 100000

start_time = time()
samples = sample_reader(path_train_sample, sample_size)
print(time() - start_time)
print(type(samples.y))
print(len(samples.y))
