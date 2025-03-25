import csv
import os
from storage.istorage import IStorage


class StorageCsv(IStorage):
    """Handles movie storage using a CSV file."""

    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster"])

    def list_movies(self):
        """Reads the CSV and returns a dictionary of movie data."""
        data = {}

        try:
            with open(self.file_path, "r", newline="") as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    if len(row) < 4:
                        continue

                    title = row[0]
                    rating = float(row[1])
                    year = int(row[2])
                    poster = row[3]

                    data[title] = {
                        "rating": rating,
                        "year": year,
                        "poster": poster
                    }

        except FileNotFoundError:
            pass

        return data

    def add_movie(self, title, year, rating, poster):
        """Adds a new movie to the CSV file."""
        movies = self.list_movies()

        if title in movies:
            return

        with open(self.file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([title, rating, year, poster])

    def delete_movie(self, title):
        """Deletes a movie from the CSV file."""
        movies = self.list_movies()

        if title in movies:
            del movies[title]

            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster"])

                for movie_title, info in movies.items():
                    writer.writerow([
                        movie_title,
                        info["rating"],
                        info["year"],
                        info["poster"]
                    ])

    def update_movie(self, title, rating):
        """Updates the rating of an existing movie."""
        movies = self.list_movies()

        if title in movies:
            movies[title]["rating"] = rating

            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "rating", "year", "poster"])

                for movie_title, info in movies.items():
                    writer.writerow([
                        movie_title,
                        info["rating"],
                        info["year"],
                        info["poster"]
                    ])
