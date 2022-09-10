import re
from utils.nlp_utils import question_tag
from utils.common_utils import Neo4jQuery
from models.TextClassification import TextClassification


class QuestionTemplate:
    def __init__(self):
        self.template_dict = {
            0: self.get_movie_rating,
            1: self.get_movie_releasedate,
            2: self.get_movie_type,
            3: self.get_movie_introduction,
            4: self.get_movie_actor_list,#
            5: self.get_actor_info,
            6: self.get_actor_act_type_movie,
            7: self.get_actor_movie_list,
            8: self.get_movie_rating_bigger,
            9: self.get_movie_rating_smaller,
            10: self.get_actor_movie_type,
            11: self.get_cooperation_movie_list,
            12: self.get_actor_movie_num,
            13: self.get_actor_birthday,
        }

        self.neo4j_connect = Neo4jQuery()

    def get_answer(self, question, template_id):
        tokens = question_tag(question)
        question_word, question_flag = [], []
        for token in tokens:
            word, flag = token.split('/')
            question_word.append(word)
            question_flag.append(flag)
        self.src_question = question
        self.question_word = question_word
        self.question_flag = question_flag
        try:
            ans = self.template_dict[template_id]()
        except:
            ans = "抱歉，我是人工智障^^"
        return ans

    def get_name(self, type_str):
        """
        获取 实体名|不止一个
        :param type_str: 标签类型
        :return: list
        """
        count = self.question_flag.count(type_str)
        if count == 1:
            idx = self.question_flag.index(type_str)
            name = self.question_word[idx]
            return [name]
        else:
            result = []
            for i, flag in enumerate(self.question_flag):
                if flag == str(type_str):
                    result.append(self.question_word[i])
            return result

    def get_num(self):
        """
        获取数字如评分等
        :return: int
        """
        x = re.sub(r"\D", "", " ".join(self.question_word))
        return x

    def get_movie_rating(self):
        movie = self.get_name('nm')[0]
        cql = f"MATCH (m:MOVIE ) WHERE m.title='{movie}' RETURN m.rating"
        print(cql)
        ans = self.neo4j_connect.run(cql)[0]
        print(ans)
        ans = round(ans, 2)
        final_answer = movie + "的评分为：" + str(ans)
        return final_answer

    def get_movie_releasedate(self):
        movie = self.get_name('nm')[0]
        cql = f"MATCH (m:MOVIE ) WHERE m.title='{movie}' RETURN m.releasedate"
        print(cql)
        ans = self.neo4j_connect.run(cql)[0]
        print(ans)
        final_answer = movie + f"的上映时间为：{str(ans)}"
        return final_answer

    def get_movie_type(self):
        movie = self.get_name('nm')[0]
        cql = f"MATCH (m:MOVIE ) -[edge:is]-> (g:Genre)" \
              f"WHERE m.title='{movie}' RETURN g.name"
        print(cql)
        ans = self.neo4j_connect.run(cql)
        ans_set = set(ans)
        ans = '|'.join(list(ans_set))
        final_answer = movie + f"是{ans}等类型的电影!"
        return final_answer

    def get_movie_introduction(self):
        movie = self.get_name('nm')[0]
        cql = f"MATCH (m:MOVIE ) WHERE m.title='{movie}' RETURN m.introduction"
        print(cql)
        ans = self.neo4j_connect.run(cql)[0]
        print(ans)
        final_answer = movie + f"主要讲述了：{str(ans)}"
        return final_answer

    def get_movie_actor_list(self):
        movie = self.get_name('nm')[0]
        cql = f"MATCH (p:Person ) -[edge: acted]->(m:MOVIE)" \
              f" WHERE m.title='{movie}' RETURN p.name"
        print(cql)
        ans = self.neo4j_connect.run(cql)
        ans = '|'.join(list(set(ans)))
        final_answer = movie + f"由{ans}等主演。"
        return final_answer

    def get_actor_info(self):
        person = self.get_name('nr')[0]
        cql = f" MATCH (p:Person) -[]->() WHERE p.name = '{person}' " \
              f"return p.biography"
        print(cql)
        final_answer = self.neo4j_connect.run(cql)[0]
        return final_answer

    def get_actor_act_type_movie(self):
        print("select")
        person = self.get_name('nr')[0]
        genre = self.get_name('ng')
        print(genre)
        cql = f" MATCH (p:Person) -[]->(m:MOVIE) WHERE p.name='{person}'" \
              f" RETURN m.title"
        print(cql)
        movies = list(set(self.neo4j_connect.run(cql)))
        # 查询类型
        result = []
        for movie in movies:
            movie = str(movie).strip()
            try:
                cql = f"MATCH (m:MOVIE) -[edge:is]->(g:Genre)" \
                      f"WHERE m.title='{movie}' RETURN g.name"
                genres = self.neo4j_connect.run(cql)
                if len(genres) == 0:
                    continue
                if genre[0] in list(set(genres)):
                    result.append(movie)
            except:
                continue
        ans = '|'.join(result)
        final_answer = f"{person}演过的{genre[0]}片有{ans}等。"
        return final_answer

    def get_actor_movie_list(self):
        person = self.get_name('nr')[0]
        cql = f"MATCH (p:Person) -[edge:acted]-> (m:MOVIE) WHERE p.name='{person}' " \
              f" RETURN m.title"
        print(cql)
        ans = self.neo4j_connect.run(cql)
        ans = '|'.join(list(set(ans)))
        final_answer = f"{person}演过{str(ans)}等电影。"
        return final_answer

    def get_movie_rating_bigger(self):
        person = self.get_name('nr')[0]
        rating = self.get_num()
        cql = f"MATCH (p:Person) -[edge:acted]->(m:MOVIE) WHERE p.name='{person}'" \
              f"AND m.rating >= {rating} RETURN m.title"
        movies = self.neo4j_connect.run(cql)
        movies = '|'.join(list(set(movies)))
        final_answer = f"{person}演过的评分高于{rating}的电影有{movies}。"
        return final_answer

    def get_movie_rating_smaller(self):
        person = self.get_name('nr')[0]
        rating = self.get_num()
        cql = f"MATCH (p:Person) -[edge:acted]->(m:MOVIE) WHERE p.name='{person}'" \
              f" AND m.rating <= {rating} RETURN m.title"
        movies = self.neo4j_connect.run(cql)
        movies = '|'.join(list(set(movies)))
        final_answer = f"{person}演过的评分低于{rating}的电影有{movies}。"
        return final_answer

    def get_actor_movie_type(self):
        person = self.get_name('nr')[0]
        cql = f"MATCH (p:Person) -[edge:acted]-> (m:MOVIE) " \
              f"WHERE p.name='{person}' RETURN m.title"
        movies = self.neo4j_connect.run(cql)

        result = []
        for movie in movies:
            movie = str(movie).strip()
            try:
                cql = f"MATCH (m:MOVIE) -[edge:is]-> (g:Genre)" \
                      f"WHERE m.title='{movie}' RETURN g.name"
                genres = self.neo4j_connect.run(cql)
                if len(genres) == 0:
                    continue
                result += genres
            except:
                continue
        ans = '|'.join(list(set(result)))
        final_answer = f"{person}演过的电影类型有{ans}等"
        return final_answer

    def get_cooperation_movie_list(self):
        """
        输入问题中包含两个演员
        :return:
        """
        persons = self.get_name('nr')
        movies = []
        for i, person in enumerate(persons):
            cql = f"MATCH (p:Person) -[edge:acted]-> (m:MOVIE) WHERE p.name='{person}'" \
                  f"RETURN m.title"
            ans = self.neo4j_connect.run(cql)
            movies.append(list(set(ans)))
        ans_l = list(set(movies[0]).intersection(set(movies[1])))
        print(ans_l)
        ans = '|'.join(ans_l)
        final_answer = f"{persons[0]}和{persons[1]}一起演过的电影有：{ans}。"
        return final_answer

    def get_actor_movie_num(self):
        person = self.get_name('nr')[0]
        cql = f"MATCH (p:Person) -[edge: acted]->(m:MOVIE) " \
              f"WHERE p.name='{person}' RETURN m.title"
        print(cql)
        ans = self.neo4j_connect.run(cql)
        ans = len(set(ans))
        final_answer = person + "演过的电影数量为" + str(ans) + "。"
        return final_answer

    def get_actor_birthday(self):
        person = self.get_name('nr')[0]
        cql = f"MATCH (p:Person) WHERE p.name='{person}' RETURN p.birth"
        print(cql)
        ans = self.neo4j_connect.run(cql)[0]
        final_answer = person + "的生日是： " + ans + "。"
        return final_answer


if __name__ == "__main__":
    question = "英雄的主演有哪些？"
    template = QuestionTemplate()
    question_classify = TextClassification()
    template_id = question_classify.predict(question)
    print(template_id)
    result = template.get_answer(question, template_id[0])
    print(result)
