import os
import re
import jieba
from utils import config


def get_file_list(work_dir):
    file_path_list = []
    walk = os.walk(work_dir)
    for root, dirs, files in walk:
        for name in files:
            file_path_list.append(os.path.join(root, name))
    return file_path_list


def load_train_data():
    x_train, y_train = [], []
    file_path_list = get_file_list(os.path.join(config.DATA_DIR,'question'))
    for file_path in file_path_list:
        label = re.sub(r"\D", "", file_path)
        if label.isnumeric():
            label = int(label)
            with open(file_path,'r',encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    tokens = jieba.lcut(str(line).strip())
                    x_train.append(' '.join(tokens))
                    y_train.append(label)
    return x_train, y_train


