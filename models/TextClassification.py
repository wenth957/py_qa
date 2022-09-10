from scripts import load_train
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import nlp_utils


class TextClassification:

    def __init__(self):
        self.x_train, self.y_train = load_train.load_train_data()
        self.Tfidf = TfidfVectorizer()
        self.vectors = self.Tfidf.fit_transform(self.x_train).toarray()
        self.model = self.train()

    def train(self):
        model = MultinomialNB()
        model.fit(self.vectors, self.y_train)
        return model

    def predict(self, question):
        # 词性标注结果
        tokens_tag = nlp_utils.question_tag(question)
        src_question_l = []
        process_question_l = []
        for token in tokens_tag:
            word, flag = token.split('/')
            src_question_l.append(word)
            if flag in ['nr', 'nm', 'ng']:
                # 将中文替换为对应的词性：人、电影、类型
                process_question_l.append(flag)
            else:
                process_question_l.append(word)
        process_question = [" ".join(process_question_l)]
        question_vector = self.Tfidf.transform(process_question)
        predict = self.model.predict(question_vector)
        return predict


def test():
    question = "巩俐演过哪些电影？"
    # question = "英雄的主演有谁？"
    question_classify = TextClassification()
    result = question_classify.predict(question)
    print(result)
    return result

