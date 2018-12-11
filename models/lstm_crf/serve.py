#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Reload and serve a saved model"""

import glob
import os
__author__ = 'Guillaume Genthial'

from pathlib import Path
from tensorflow.contrib import predictor

# LINE = 'John lives in New York'

if __name__ == '__main__':
    export_dir = 'saved_model'
    subdirs = [x for x in Path(export_dir).iterdir() if x.is_dir()
               and 'temp' not in str(x)]
    latest = str(sorted(subdirs)[-1])
    predict_fn = predictor.from_saved_model(latest)
    mypath = '/Users/kilol.guptaibm.com/Downloads/historyLab/ner_dl/lowerCase-textFiles/train/no_punctuation_splitlined/*.txt'
    onlyfiles = glob.glob(mypath)
    count = 0
    for file in onlyfiles:
        print(os.path.basename(file))
        count += 1
        outfile = open(os.path.basename(file)[:-4] + '_predictions.txt', 'w+')
        lines = open(file).read().splitlines()
        for line in lines:
            line = line.strip()
            if line:
                words = [w.encode() for w in line.split()]
                nwords = len(words)
                predictions = predict_fn({'words': [words],
                        'nwords': [nwords]})
                outfile.write(str(predictions.get('pred_ids')[0].tolist()))
                outfile.write('\n')
        outfile.close()
    print(count)