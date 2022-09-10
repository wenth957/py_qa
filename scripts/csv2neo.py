from utils.common_utils import Neo4jQuery

movie_neo4j = Neo4jQuery()


def load_genre():
    """
    load 电影类型节点
    :return:
    """
    genre_node_cql = ''' LOAD CSV WITH HEADERS FROM 
                         "file:///genre.csv" AS line
                         MERGE(g:Genre {gid:toInteger(line.gid), name: line.gname})
                     '''
    movie_neo4j.run(genre_node_cql)


def load_person():
    """
    load 演员节点
    :return:
    """
    person_node_cql = ''' LOAD CSV WITH HEADERS FROM 
                         "file:///person.csv" AS line
                         MERGE(p: Person { pid:toInteger(line.pid), 
                                           birth: line.birth, 
                                           death:line.death,
                                           name: line.name,
                                           biography:line.biography,
                                           birthplace:line.birthplace})
                     '''
    movie_neo4j.run(person_node_cql)


def load_movie():
    """
    load 电影节点
    :return:
    """
    movie_node_cql = ''' LOAD CSV WITH HEADERS FROM 
                         "file:///movie.csv" AS line
                         MERGE(m: MOVIE { mid:toInteger(line.mid), 
                                           title: line.title, 
                                           introduction:line.introduction,
                                           rating: toFloat(line.rating),
                                           releasedate:line.releasedate})
                     '''
    movie_neo4j.run(movie_node_cql)


def load_movie_person_rel():
    """
    load 电影 演员关系
    :return:
    """
    movie_person_rel = ''' LOAD CSV WITH HEADERS FROM 
                         "file:///person_to_movie.csv" AS line
                        MATCH (p:Person {pid:toInteger(line.pid)}), (m:MOVIE {mid:toInteger(line.mid)})
                        MERGE (p) -[actor :acted {pid: toInteger(line.pid), mid:toInteger(line.mid)}] -> (m)
                     '''

    movie_neo4j.run(movie_person_rel)


def load_movie_genre_rel():
    """
    load 电影 电影类型关系
    :return:
    """
    movie_genre_rel = ''' LOAD CSV WITH HEADERS FROM 
                         "file:///movie_to_genre.csv" AS line
                        MATCH (m:MOVIE {mid:toInteger(line.mid)}), (g:Genre {gid:toInteger(line.gid)})
                        MERGE (m) -[belong :is {mid: toInteger(line.mid), gid:toInteger(line.gid)}] -> (g)
                     '''

    movie_neo4j.run(movie_genre_rel)