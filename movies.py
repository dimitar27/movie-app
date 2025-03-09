import movie_storage
import statistics
import random

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from fuzzywuzzy import process

RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'


def display_menu():
    """Displays the main menu with available options for managing movies."""
    menu = """
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
9. Create Rating Histogram

"""
    print(f"{GREEN}{menu}{RESET}")


def display_movies():
    """Lists all movies in the database with their year and rating."""
    movies_to_display = movie_storage.get_movies()
    print(f"{YELLOW}{len(movies_to_display)} in total{RESET}")
    for movie, attribute in movies_to_display.items():
        print(f"{CYAN}{movie} ({attribute['year']}): "
              f"{attribute['rating']}{CYAN}")


def add_new_movie():
    """Adds a new movie to the database with its name, year, and rating."""
    movies_database = movie_storage.get_movies()

    user_input_movie = input(f"{BLUE}Enter new movie name: {RESET}")
    if user_input_movie.strip() == "":
        print(f"{RED}Movie name cannot be empty!{RESET}")
        return

    if user_input_movie in movies_database:
        print(f"{RED}Movie {user_input_movie} already exists!{RESET}")
        return

    while True:
        try:
            user_input_year = input(f"{BLUE}Enter new movie year: {RESET}")
            if user_input_year.strip() == "":
                raise ValueError("Year cannot be empty.")
            user_input_year = int(user_input_year)
            if user_input_year < 1900 or user_input_year > 2025:
                raise ValueError(f"Please enter a valid year between 1900 and 2025.")
            break
        except ValueError as e:
            print(f"{RED}{e}{RESET}")

    while True:
        try:
            user_input_ranking = float(input(f"{BLUE}Enter new movie rating (0-10): {RESET}"))
            if 0 <= user_input_ranking <= 10:
                break
            else:
                print(f"{RED}Rating must be between 0 and 10!{RESET}")
        except ValueError:
            print(f"{RED}Please enter a valid rating (numbers only).{RESET}")

    movie_storage.add_movie(user_input_movie, user_input_ranking, user_input_year)
    print(f"{GREEN}Movie {user_input_movie} successfully added!{RESET}")


def delete_movie():
    """Deletes a movie from the database by its name."""
    movies_database = movie_storage.get_movies()
    movie_to_delete = input(f"{BLUE}Enter movie name to delete: {RESET}")
    if movie_to_delete in movies_database:
        movie_storage.delete_movie(movie_to_delete)
        print(f"{GREEN}Movie {movie_to_delete} successfully deleted{RESET}")

    else:
        print(f"{RED}Movie {movie_to_delete} doesn't exist!{RESET}")


def update_movie_rating():
    """Updates the rating of a movie specified by the user."""
    movies_database = movie_storage.get_movies()
    movie_to_update = input("Enter movie name: ")

    if movie_to_update in movies_database:
        while True:
            try:
                rating = float(input(f"{BLUE}Enter new movie rating (0-10): {RESET}"))
                if 0 <= rating <= 10:
                    movie_storage.update_movie(movie_to_update, rating)
                    print(f"Movie {movie_to_update} successfully updated")
                    break
                else:
                    print(f"{RED}Rating must be between 0 and 10!{RESET}")
            except ValueError:
                print(f"{RED}Please enter a valid rating (numbers only).{RESET}")

    else:
        print(f"{RED}Movie {movie_to_update} doesn't exist!{RESET}")


def display_stats():
    """Displays statistics for the movies, including the highest and lowest rated,
    average rating, and median rating."""
    movies_database = movie_storage.get_movies()
    movie_rating = {}
    for movie, rating in movies_database.items():
        movie_rating[movie] = rating["rating"]

    movie_ratings = list(movie_rating.values())
    max_rating = max(movie_ratings)
    min_rating = min(movie_ratings)

    movie_max_rating = []
    movie_min_rating = []

    for movie, rating in movies_database.items():
        if rating == max_rating:
            movie_max_rating.append(movie)
        elif rating == min_rating:
            movie_min_rating.append(movie)

    average_rating = sum(movie_ratings) / len(movie_ratings)
    print(f"{GREEN}Average rating: {average_rating}{RESET}")

    median_rating = statistics.median(movie_ratings)
    print(f"{GREEN}Median rating: {median_rating}{RESET}")

    for movie in movie_max_rating:
        print(f"{GREEN}Best movie: {movie}, {max_rating}{RESET}")

    for movie in movie_min_rating:
        print(f"{RED}Worst movie: {movie}, {min_rating}{RESET}")


def pick_a_random_movie():
    """Selects and prints a random movie from the database along with its rating."""
    movies_database = movie_storage.get_movies()
    movie_rating = {}
    for movie, rating in movies_database.items():
        movie_rating[movie] = rating["rating"]

    movie, rating = random.choice(list(movie_rating.items()))
    print(f"{MAGENTA}Your movie for tonight: {movie}, it's rated {rating}{RESET}")


def search_movie():
    """Searches for movies in the database by partial name match."""
    movies_database = movie_storage.get_movies()
    user_input = input(f"{BLUE}Enter part of movie name: {RESET}").lower()

    searched_movie = []
    searched_movie_attribute = []

    for movie, rating in movies_database.items():
        if user_input in movie.lower():
            searched_movie.append(movie)
            searched_movie_attribute.append(rating)

    if searched_movie:
        for i in range(len(searched_movie)):
            print(f"{searched_movie[i]}: {searched_movie_attribute[i]['rating']}")
    else:

         matches = process.extract(user_input,
                                   movies_database.keys(),
                                   limit=2)

         if matches:
             if matches[0][1] >= 96:
                 movie_name = matches[0][0]
                 print(f"{GREEN}{movie_name}, {movies_database[movie_name]}{RESET}")
             else:
                 print(f"{RED}Movie {user_input} not found. Did you mean:{RESET}")
                 for match in matches:
                     print(f"{CYAN}{match[0]}: {movies_database[match[0]]['rating']}{RESET}")


def movie_sorted_by_rating():
    """Sorts and prints movies in the database by their rating in descending order."""
    movies_database = movie_storage.get_movies()
    movies_sorted_by_rating = sorted(movies_database.items(),
    key=lambda x: x[1]["rating"], reverse=True)
    for movie in movies_sorted_by_rating:
        name, rating = movie[0], movie[1]["rating"]
        print(f"{BLUE}{name}: {rating}{RESET}")


def create_rating_histogram():
    """Creates a rating histogram"""
    movies_database = movie_storage.get_movies()
    movie_rating = {}
    for movie, rating in movies_database.items():
        movie_rating[movie] = rating["rating"]

    ratings = list(movie_rating.values())
    file_name = input(f"{BLUE}Enter the filename to save the histogram: {RESET}")

    plt.hist(ratings, bins=10, edgecolor='black')

    plt.xlabel('Movie Rating')
    plt.ylabel('Frequency (Number of Movies)')
    plt.title('Histogram of Movie Ratings')

    plt.savefig(file_name)
    plt.close()

    print(f"Plot saved as {file_name}.")


def main():

    print("********** My Movies Database **********")
    while True:
        display_menu()
        try:
            user_input = int(input("Enter choice (0-9): "))
        except ValueError:
            print(f"{RED}Invalid choice. Please enter a number between 1 and 9.{RESET}")
            continue
        print()
        if user_input == 0:
            print("Bye!")
            break
        elif user_input == 1:
            display_movies()
        elif user_input == 2:
            add_new_movie()
        elif user_input == 3:
            delete_movie()
        elif user_input == 4:
            update_movie_rating()
        elif user_input == 5:
            display_stats()
        elif user_input == 6:
            pick_a_random_movie()
        elif user_input == 7:
            search_movie()
        elif user_input == 8:
            movie_sorted_by_rating()
        elif user_input == 9:
            create_rating_histogram()

        else:
            print(f"{RED}Invalid choice.{RESET}")
            continue
        print()
        input("Press enter to continue")


if __name__ == "__main__":
    main()