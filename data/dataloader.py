#! /user/bin/evn python
# -*- coding:utf8 -*-

"""

@Author   : Lau James
@Contact  : LauJames2017@whu.edu.cn
@Project  : MVLSTM 
@File     : dataloader.py
@Time     : 2018/11/19 14:29
@Software : PyCharm
@Copyright: "Copyright (c) 2018 Lau James. All Rights Reserved"
"""
import numpy as np
import codecs
import tensorflow as tf
import tensorflow.contrib as tc
import os
import pickle as pkl
from sklearn.model_selection import train_test_split


q2q_file = 'q2q_pair_merged.txt'
q2q_divided = 'q2q_match.pkl'


def get_q2q_label(file_path):
    questions1 = []
    questions2 = []
    labels = []
    with open(file_path, 'r', encoding='utf-8') as fp:
        while True:
            line = fp.readline()
            if not line:
                print('loading dataset successfully!')
                return [questions1, questions2, np.array(labels)]
            tmp = line.strip().split('\t')
            label, question1, question2 = tmp[0], tmp[1], tmp[2]
            labels.append(label)
            questions1.append(question1)
            questions2.append(question2)


def batch_iter_per_epoch(q1, q2, labels, batch_size=64, shuffle=True):
    """为每个epoch随机生成批次数据"""
    data_len = len(q1)
    num_batch = int((data_len-1)/batch_size) + 1

    if shuffle:
        indices = np.random.permutation(np.arange(data_len))
        q1_shuffle = q1[indices]
        q2_shuffle = q2[indices]
        labels_shuffle = labels[indices]
    else:
        q1_shuffle = q1
        q2_shuffle = q2
        labels_shuffle = labels

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield q1_shuffle[start_id:end_id], q2_shuffle[start_id:end_id], labels_shuffle[start_id:end_id]


def split_data(data_file, vocab_path, pkl_path, dev_sample_percentage=0.1, test_sample_percentage=0.1):
    q1, q2, y = get_q2q_label(data_file)

    # Build vocabulary
    vocab_processor = tc.learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    # padding to max length
    q1_pad = np.array(list(vocab_processor.transform(q1)))
    q2_pad = np.array(list(vocab_processor.transform(q2)))

    # Write vocabulary
    # vocab_processor.save(os.path.join(save_vocab_dir, "vocab"))

    # Randomly shuffle data
    np.random.seed(7)
    shuffle_indices = np.random.permutation(np.arange(len(y)))
    q1_shuffled = q1_pad[shuffle_indices]
    q2_shuffled = q2_pad[shuffle_indices]
    y_shuffled = y[shuffle_indices]

    # Split train/dev
    dev_sample_indices = -1 * int(dev_sample_percentage * float(len(y)))
    test_sample_indices = -1 * int(test_sample_percentage * float(len(y)))

    q1_train = q1_shuffled[: dev_sample_indices + test_sample_indices]
    q1_dev = q1_shuffled[dev_sample_indices + test_sample_indices: test_sample_indices]
    q1_test = q1_shuffled[test_sample_indices:]

    q2_train = q2_shuffled[: dev_sample_indices + test_sample_indices]
    q2_dev = q2_shuffled[dev_sample_indices + test_sample_indices: test_sample_indices]
    q2_test = q2_shuffled[test_sample_indices:]

    y_train = y_shuffled[: dev_sample_indices + test_sample_indices]
    y_dev = y_shuffled[dev_sample_indices + test_sample_indices: test_sample_indices]
    y_test = y_shuffled[test_sample_indices:]

    del q1, q2, y, q1_pad, q2_pad, q1_shuffled, q2_shuffled, y_shuffled

    vocab_size = len(vocab_processor.vocabulary_)

    print("Vocabulary Size: {:d}".format(vocab_size))
    print("Train/Dev/test split: {:d}/{:d}/{:d}".format(len(y_train), len(y_dev), len(y_test)))

    with open(pkl_path, 'wb') as pkl_file:
        try:
            pkl.dump(q1_train, pkl_file)
            pkl.dump(q2_train, pkl_file)
            pkl.dump(y_train, pkl_file)
            pkl.dump(q1_dev, pkl_file)
            pkl.dump(q2_dev, pkl_file)
            pkl.dump(y_dev, pkl_file)
            pkl.dump(q1_test, pkl_file)
            pkl.dump(q2_test, pkl_file)
            pkl.dump(y_test, pkl_file)
            pkl.dump(vocab_size, pkl_file)
        except Exception as e:
            print(e)


def load_pkl_set(pkl_path):
    with open(pkl_path, 'rb') as pkl_file:
        q1_train = pkl.load(pkl_file)
        q2_train = pkl.load(pkl_file)
        y_train = pkl.load(pkl_file)
        q1_dev = pkl.load(pkl_file)
        q2_dev = pkl.load(pkl_file)
        y_dev = pkl.load(pkl_file)
        q1_test = pkl.load(pkl_file)
        q2_test = pkl.load(pkl_file)
        y_test = pkl.load(pkl_file)
        vocab_size = pkl.load(pkl_file)

    return q1_train, q2_train, y_train, q1_dev, q2_dev, y_dev, q1_test, q2_test, y_test, vocab_size


if __name__ == '__main__':
    pass
