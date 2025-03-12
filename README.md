# 🎬 Movie Management App

This is a **Movie Management Application** that allows users to:

- Store and manage movies using JSON.
- Fetch movie details from the **OMDb API**.
- Search for movies.
- Generate an HTML-based movie website.

## Installation

1. **Clone this repository**:

   ```sh
   git clone https://github.com/dimitar27/movie-app.git
   cd movie-app
   ```

2. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

3. **Set up your API Key**:

   - Go to [OMDb API](https://www.omdbapi.com/) and register for a free API key.
   - Create a `.env` file in the root directory.
   - Add the following line:
     ```
     API_KEY=your_omdb_api_key_here
     ```

## Usage

Run the application with:

```sh
python main.py
```

## Features

- **List Movies**: Displays all movies stored.
- **Add a Movie**: Fetches movie details from the OMDb API and stores them.
- **Delete a Movie**: Removes a movie from storage.
- **Update a Movie**: Updates the rating of a movie.
- **Movie Stats**: Shows average and median ratings.
- **Random Movie Suggestion**: Suggests a random movie.
- **Search Movies**: Finds movies by name or partial match.
- **Sort Movies by Rating**: Displays movies ranked by rating.
- **Generate Website**: Creates an HTML page with movie details.

## Dependencies

This project uses:

- `requests` → Handles API requests.
- `python-dotenv` → Loads the API key from `.env`.
- `fuzzywuzzy` → Enables fuzzy movie searching.
- `python-Levenshtein` → Optimizes fuzzy matching.
- **Built-in Modules**: `json`, `random`, `statistics`, `os`.
