from storage.istorage import IStorage
import json


class StorageCsv(IStorage):
    """Handles movie storage using a JSON file."""

    def __init__(self, file_path):
        """Initializes the storage with the given file path."""
        self.file_path = file_path

    def list_movies(self):
        """Retrieves the list of movies from the
        JSON file and returns the data."""
        try:
            with open(self.file_path, "r") as fileobj:
                data = json.load(fileobj)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        return data

    def add_movie(self, title, year: int, rating: int, poster):
        """Adds a movie to the movies database.
        Loads the information from the JSON file,
        add the movie, and saves it."""
        data = self.list_movies()  # Load existing data

        if title in data:
            return

        data[title] = {
            "rating": rating,
            "year": year,
            "poster": poster
        }

        with open(self.file_path, 'w') as fileobj:
            json.dump(data, fileobj, indent=4)

    def delete_movie(self, title):
        """Deletes a movie from the movies database.
        Loads the information from the JSON file,
        deletes the movie, and saves it."""
        data = self.list_movies()

        if title in data:
            del data[title]
            with open(self.file_path, 'w') as fileobj:
                json.dump(data, fileobj, indent=4)

    def update_movie(self, title, rating):
        """Updates a movie from the movies database."""
        data = self.list_movies()

        if title in data:
            data[title]["rating"] = rating
            with open(self.file_path, 'w') as fileobj:
                json.dump(data, fileobj, indent=4)



