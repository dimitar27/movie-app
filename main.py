from movie_app import MovieApp
from storage_csv import StorageCsv
from storage_json import StorageJson


def main():
    storage = StorageJson('movies.json')
    movie_app = MovieApp(storage)
    movie_app.run()

    storage2 = StorageCsv('movies.csv')
    movie_app2 = MovieApp(storage2)
    movie_app2.run()



if __name__ == "__main__":
    main()

