import gc
import sys
from time import time

from guppy import hpy
from scipy.sparse import csr_matrix

import evaluation
import fit_multi_label_mnb
import predict_multi_label_mnb
import reader

sample_path = sys.argv[1] if len(sys.argv) > 1 else '/Users/wumengling/PycharmProjects/kaggle/input_data/train.csv'
size_of_sample = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
size_of_train_sample = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
predict_block_size = int(sys.argv[4]) if len(sys.argv) > 4 else 1000

start_time = time()

# read data from file
train_smp, test_smp = reader.read_sample(sample_path, size_of_sample, size_of_train_sample)
n_feature = max(train_smp.max_feature, test_smp.max_feature) + 1
n_class_label = max(train_smp.max_class_label, test_smp.max_class_label) + 1
train_x = csr_matrix((train_smp.element_x, (train_smp.row_index_x, train_smp.col_index_x)),
                     shape=(max(train_smp.row_index_x) + 1, n_feature))
test_x = csr_matrix((test_smp.element_x, (test_smp.row_index_x, test_smp.col_index_x)),
                    shape=(max(test_smp.row_index_x) + 1, n_feature))

# fit non-smoothed mnb model
model = fit_multi_label_mnb.fit(train_smp.y, train_x)

# make prediction on test sample
h = hpy()
del train_smp
del train_x
gc.collect()
# todo: predict result seems weird, need to be confirmed.
predict_sample_per_label = predict_multi_label_mnb.predict(test_x, model, predict_block_size)

# evaluation
print(evaluation.macro_precision_recall(test_smp.y, predict_sample_per_label, n_class_label))

print(time() - start_time)
