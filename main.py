import tensorflow as tf
import pandas as pd
import load_dataset as load
import preprocess
from categorizing_model import CModel
import debug_util as dutil

# load dataset
#FILENAME = 'Dataset.txt'
FILENAME = 'Dataset_without_general.txt'
dataset = load.load_dataset(FILENAME)

tensor, config = preprocess.tokenize(dataset['titles'].to_list())

# split and shuffle dataset
X_train, X_test, Y_train, Y_test = preprocess.split_dataset(tensor, dataset['labels'].to_list())

# make dataset pairs (title, labels)
train_dataset = tf.data.Dataset.from_tensor_slices((X_train, Y_train))
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, Y_test))

# split dataset to batches
BATCH_SIZE = 64
train_dataset = train_dataset.batch(BATCH_SIZE)
test_dataset = test_dataset.batch(BATCH_SIZE)
# word and index mapping dictionaries
index_word = preprocess.convert_to_dict(config, 'index_word')
word_index = preprocess.convert_to_dict(config, 'word_index')

HIDDEN_UNITS = 64
FINAL_OUTPUT_UNITS = 6
DROPOUT_RATE = 0.4
DENSE_LAYERS = 1
L2_RATE = 0.01
LEARNING_RATE = 1e-4
EPOCHS = 50

model = CModel(len(index_word),
               HIDDEN_UNITS,
               FINAL_OUTPUT_UNITS,
               DROPOUT_RATE,
               DENSE_LAYERS,
               L2_RATE)
model.compile(LEARNING_RATE)
history = model.fit(train_dataset, test_dataset, EPOCHS)
test_loss, test_acc = model.evaluate()
print(test_loss)
print(test_acc)

s = input()
