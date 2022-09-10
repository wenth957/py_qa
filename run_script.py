from scripts import csv2neo

if __name__ == "__main__":
    csv2neo.load_genre()
    csv2neo.load_person()
    csv2neo.load_movie()
    csv2neo.load_movie_person_rel()
    csv2neo.load_movie_genre_rel()