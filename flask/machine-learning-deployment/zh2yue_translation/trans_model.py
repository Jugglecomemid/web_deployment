#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 12:08 PM
# @Author  : Charles He
# @File    : regression_model.py
# @Software: PyCharm

import tensorflow as tf
from tqdm import tqdm
import numpy as np
import os
from transformer import Transformer
from nltk.translate import bleu

"""- zh数据获取"""


class Zh2yue(object):
    def __init__(self, vacob_input, vacob_output, model_path):
        self.zh_list_in = Zh2yue.input_zhvob(path=vacob_input)
        self.zh_vocab_in = Zh2yue.built_zhvob(self.zh_list_in)
        self.zh_list_out = Zh2yue.input_zhvob(path=vacob_output)
        self.zh_vocab_out = Zh2yue.built_zhvob(self.zh_list_out)
        self.model = model_path

    @staticmethod
    def input_zhvob(path):
        with open(path, 'r', encoding='utf8') as f:
            data = f.readlines()

        symbol_list = ['\xa0', '\n', ' ', '\t', '\u200b', '\u3000', '\xad']
        zh_list = []
        for line in tqdm(data):
            for c in symbol_list:
                line = line.replace(c, '')
            zh_list.append(line)

        # for line in zh_list[:10]: print(line)
        return zh_list

    """- 构造中文字典"""

    @staticmethod
    def built_zhvob(zh_list):
        zh_vocab = {'<PAD>': 0, '<GO>': 1, '<EOS>': 2}
        index = 2
        for line in tqdm(zh_list):
            for char in line:
                if char not in zh_vocab:
                    index += 1
                    zh_vocab[char] = index

        return zh_vocab

    @staticmethod
    def get_batch(encoder_inputs, decoder_inputs, decoder_targets, batch_size=4):
        batch_num = len(encoder_inputs) // batch_size
        for k in range(batch_num):
            begin = k * batch_size
            end = begin + batch_size
            en_input_batch = encoder_inputs[begin:end]
            de_input_batch = decoder_inputs[begin:end]
            de_target_batch = decoder_targets[begin:end]
            max_en_len = max([len(line) for line in en_input_batch])
            max_de_len = max([len(line) for line in de_input_batch])
            en_input_batch = np.array([line + [0] * (max_en_len - len(line)) for line in en_input_batch])
            de_input_batch = np.array([line + [0] * (max_de_len - len(line)) for line in de_input_batch])
            de_target_batch = np.array([line + [0] * (max_de_len - len(line)) for line in de_target_batch])
            yield en_input_batch, de_input_batch, de_target_batch

    def create_hparams(self):
        params = tf.contrib.training.HParams(
            num_heads=4,
            num_blocks=2,
            # vocab
            input_vocab_size=50,
            label_vocab_size=50,
            # embedding size
            max_length=10000,
            hidden_units=512,
            dropout_rate=0.1,
            lr=0.0001,
            is_training=True)
        return params

    def run_test(self, test_num=100, model_name='logs/model-zh2yue-300'):

        zh_vocab_in = self.zh_list_in
        zh_vocab_out = self.zh_list_out

        encoder_inputs = [[zh_vocab_in[word] for word in line] for line in tqdm(self.zh_list_in)]
        decoder_inputs = [[zh_vocab_out['<GO>']] + [zh_vocab_out[word] for word in line] for line in tqdm(self.zh_list_out)]
        decoder_targets = [[zh_vocab_out[word] for word in line] + [zh_vocab_out['<EOS>']] for line in
                           tqdm(self.zh_list_out)]

        arg = Zh2yue.create_hparams()
        arg.input_vocab_size = len(zh_vocab_in)
        arg.label_vocab_size = len(zh_vocab_out)

        g = Transformer(arg)

        saver = tf.train.Saver()

        de_zh_vocab = {v: k for k, v in zh_vocab_out.items()}

        result = []
        with tf.Session() as sess:
            saver.restore(sess, model_name)
            for i in range(test_num):
                line = encoder_inputs[i]
                x = np.array(line)
                x = x.reshape(1, -1)
                de_inp = [[zh_vocab_out['<GO>']]]
                while True:
                    y = np.array(de_inp)
                    preds = sess.run(g.preds, {g.x: x, g.de_inp: y})
                    if preds[0][-1] == zh_vocab_out['<EOS>']:
                        break
                    de_inp[0].append(preds[0][-1])
                got = ''.join(de_zh_vocab[idx] for idx in de_inp[0][1:])
                print('测试语言:', self.zh_list_in[i])
                # print('sen2：', zh_list_out[i * 10])
                print('生成语言：', got)

                sen1_lst = [word for word in self.zh_list_in[i]]
                sen2_lst = [word for word in self.zh_list_out[i]]
                sen3_lst = [word for word in got]

                score = bleu([sen1_lst], sen3_lst)
                print(score)

                strt = str(self.zh_list_in[i]) + "\t" + str(got) + "\t" + str(score)
                result.append(strt)

        fileObject = open('intial_result_zh2yue.txt', 'w')
        for ip in result:
            fileObject.write(ip)
            fileObject.write('\n')
        fileObject.close()

    def predict(self, input_str):

        arg = self.create_hparams()
        arg.input_vocab_size = len(self.zh_vocab_in)
        arg.label_vocab_size = len(self.zh_vocab_out)

        g = Transformer(arg)

        saver = tf.train.Saver()

        de_zh_vocab = {v: k for k, v in self.zh_vocab_out.items()}

        result = []

        with tf.Session() as sess:
            saver.restore(sess, self.model)
            line = input_str
            x = np.array([self.zh_vocab_in[word] for word in line])
            x = x.reshape(1, -1)
            de_inp = [[self.zh_vocab_out['<GO>']]]
            while True:
                y = np.array(de_inp)
                preds = sess.run(g.preds, {g.x: x, g.de_inp: y})
                if preds[0][-1] == self.zh_vocab_out['<EOS>']:
                    break
                de_inp[0].append(preds[0][-1])
                got = ''.join(de_zh_vocab[idx] for idx in de_inp[0][1:])

        return got


if __name__ == '__main__':
    trans = Zh2yue()
    result = trans.predict(input_str='我要回家')
    print(result)
