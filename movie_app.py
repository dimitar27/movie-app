import random
import statistics

from fuzzywuzzy import process


class MovieApp:
    """Movie management application using JSON storage."""

    def __init__(self, storage):
        """Initializes the MovieApp with a storage instance."""
        self._storage = storage

    def _command_list_movies(self):
        """Lists all movies in the database with their year and rating."""
        movies = self._storage.list_movies()
        print(f"{len(movies)} in total")
        for movie, attribute in movies.items():
            print(f"{movie} ({attribute['year']}): "
                  f"{attribute['rating']}")

    def _command_add_new_movie(self):
        """Adds a new movie to the database with its name, year, and rating."""
        movies_database = self._storage.list_movies()

        user_input_movie = input("Enter new movie name: ")
        if user_input_movie.strip() == "":
            print(f"Movie name cannot be empty!")
            return

        if user_input_movie in movies_database:
            print(f"Movie {user_input_movie} already exists!")
            return

        while True:
            try:
                user_input_year = input("Enter new movie year: ")
                if user_input_year.strip() == "":
                    raise ValueError("Year cannot be empty.")
                user_input_year = int(user_input_year)
                if user_input_year < 1900 or user_input_year > 2025:
                    raise ValueError(f"Please enter a valid year between 1900 and 2025.")
                break
            except ValueError as e:
                print(e)

        while True:
            try:
                user_input_ranking = float(input(f"Enter new movie rating (0-10): "))
                if 0 <= user_input_ranking <= 10:
                    break
                else:
                    print(f"Rating must be between 0 and 10!")
            except ValueError:
                print(f"Please enter a valid rating (numbers only).")

        self._storage.add_movie(user_input_movie, user_input_year, user_input_ranking)
        print(f"Movie {user_input_movie} successfully added!")

    def _command_delete_movie(self):
        """Deletes a movie from the database by its name."""
        title = input("Enter movie name to delete: ")
        self._storage.delete_movie(title)

    def _command_update_movie(self):
        """Prompts the user to update movie details (year and/or rating)."""
        movie_to_update = input("Enter movie name: ")
        movies = self._storage.list_movies()

        if movie_to_update in movies:
            while True:
                try:
                    rating = float(input(f"Enter new movie rating (0-10): "))
                    if 0 <= rating <= 10:
                        self._storage.update_movie(movie_to_update, rating)
                        print(f"Movie {movie_to_update} successfully updated.")
                        break
                    else:
                        print(f"Rating must be between 0 and 10!")
                except ValueError:
                    print(f"Please enter a valid rating (numbers only).")
        else:
            print(f"Movie {movie_to_update} doesn't exist!")

    def _command_movie_stats(self):
        """Displays statistics for the movies."""
        movies = self._storage.list_movies()

        movie_rating = {}
        for movie, rating in movies.items():
            movie_rating[movie] = rating["rating"]

        movie_ratings = list(movie_rating.values())
        max_rating = max(movie_ratings)
        min_rating = min(movie_ratings)

        movie_max_rating = []
        movie_min_rating = []

        for movie, rating in movies.items():
            if rating == max_rating:
                movie_max_rating.append(movie)
            elif rating == min_rating:
                movie_min_rating.append(movie)

        average_rating = sum(movie_ratings) / len(movie_ratings)
        print(f"Average rating: {average_rating}")

        median_rating = statistics.median(movie_ratings)
        print(f"Median rating: {median_rating}")

        for movie in movie_max_rating:
            print(f"Best movie: {movie}, {max_rating}")

        for movie in movie_min_rating:
            print(f"Worst movie: {movie}, {min_rating}")

    def _command_random_movie(self):
        """Selects a random movie from the database."""
        movies = self._storage.list_movies()
        movie_rating = {}
        for movie, rating in movies.items():
            movie_rating[movie] = rating["rating"]

        movie, rating = random.choice(list(movie_rating.items()))
        print(f"Your movie for tonight: {movie}, it's rated {rating}")

    def _command_search_movie(self):
        """Searches for a movie name."""
        movies = self._storage.list_movies()
        user_input = input(f"Enter part of movie name: ").lower()

        searched_movie = []
        searched_movie_attribute = []

        for movie, rating in movies.items():
            if user_input in movie.lower():
                searched_movie.append(movie)
                searched_movie_attribute.append(rating)

        if searched_movie:
            for i in range(len(searched_movie)):
                print(f"{searched_movie[i]}: {searched_movie_attribute[i]['rating']}")
        else:

            matches = process.extract(user_input,
                                      movies.keys(),
                                      limit=2)

            if matches:
                if matches[0][1] >= 96:
                    movie_name = matches[0][0]
                    print(f"{movie_name}, {movies[movie_name]}")
                else:
                    print(f"Movie {user_input} not found. Did you mean: ")
                    for match in matches:
                        print(f"{match[0]}: {movies[match[0]]['rating']}")

    def _command_movie_by_rating(self):
        """Displays movies sorted by rating."""
        movies = self._storage.list_movies()
        movies_sorted_by_rating = sorted(movies.items(),
                                         key=lambda x: x[1]["rating"], reverse=True)
        for movie in movies_sorted_by_rating:
            name, rating = movie[0], movie[1]["rating"]
            print(f"{name}: {rating}")

    def _generate_website(self):
        pass

    def run(self):
        """Runs the main program loop."""
        while True:
            print("""
    ********** My Movies Database **********

    Menu:
    0. Exit
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Movies sorted by rating 
    9. Generate website
    """)

            try:
                user_input = int(input("Enter choice (0-9): "))
            except ValueError:
                print(f"Invalid choice. Please enter a number between 0 and 9.")
                continue

            if user_input == 0:
                print("Bye!")
                break
            elif user_input == 1:
                self._command_list_movies()
            elif user_input == 2:
                self._command_add_new_movie()
            elif user_input == 3:
                self._command_delete_movie()
            elif user_input == 4:
                self._command_update_movie()
            elif user_input == 5:
                self._command_movie_stats()
            elif user_input == 6:
                self._command_random_movie()
            elif user_input == 7:
                self._command_search_movie()
            elif user_input == 8:
                self._command_movie_by_rating()
            else:
                print(f"Invalid choice.")
                continue

            input("Press Enter to continue")
