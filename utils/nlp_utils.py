import os
import re
import jieba
from jieba import posseg
from utils import config


def pos_tag(text):
    """
    词性标注base方法
    :param text:文本
    :return: 词性标注元组
    """
    jieba.load_userdict(os.path.join(config.DATA_DIR, 'userdict3.txt'))
    clean_text = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+","", text)
    tokens = jieba.posseg.cut(clean_text)
    return tokens


def question_tag(question):
    """
    问句词性标注
    :param question: 问句
    :return: 词性标注结果
    """
    tokens = pos_tag(question)
    result = []
    question_word, question_flag = [], []
    for word in tokens:
        result.append(f"{word.word}/{word.flag}")
        question_word.append(word.word)
        question_flag.append(word.flag)
        assert len(question_word) == len(question_flag)
    return result
