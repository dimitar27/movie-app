from istorage import IStorage
import json


class StorageJson(IStorage):
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

    def add_movie(self, title, year: int, rating: int, poster=None):
        """Adds a movie to the movies database.
        Loads the information from the JSON file,
        add the movie, and saves it."""
        try:
            year = int(year)
            rating = float(rating)
        except ValueError:
            print("Please enter a valid rating (numbers only)!")
            return

        try:
            with open(self.file_path, 'r') as fileobj:
                data = json.load(fileobj)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if title in data:
            print(f"Movie {title} already exists!")
        elif year < 1900 or year > 2025:
            print(f"Please enter a valid year between 1900 and 2025.")
        elif rating < 0 or rating > 10:
            print(f"Rating must be between 0 and 10!")
        else:
            new_move = {title: {"rating": rating, "year": year}}
            data.update(new_move)

            with open(self.file_path, 'w') as fileobj:
                json.dump(data, fileobj, indent=4)

    def delete_movie(self, title):
        """Deletes a movie from the movies database.
        Loads the information from the JSON file,
        deletes the movie, and saves it."""
        try:
            with open(self.file_path, 'r') as fileobj:
                data = json.load(fileobj)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if title in data:
            del data[title]
            with open(self.file_path, 'w') as fileobj:
                json.dump(data, fileobj, indent=4)
            print(f"Movie {title} successfully deleted")
        else:
            print(f"Movie {title} doesn't exist!")

    def update_movie(self, title, rating):
        """Updates a movie from the movies database."""
        try:
            with open(self.file_path, 'r') as fileobj:
                data = json.load(fileobj)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if title not in data:
            print(f"Movie {title} doesn't exist!")
        elif 0 <= rating <= 10:
            data[title]["rating"] = rating
            with open(self.file_path, 'w') as fileobj:
                json.dump(data, fileobj, indent=4)
        else:
            print("Rating must be between 0 and 10!")



