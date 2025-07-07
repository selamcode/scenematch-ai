import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Config and Setup
def get_dataset_path():
    return os.getenv("DATASET_PATH")

# Cleaning Helpers
def clean_genres(genres_str):
    if isinstance(genres_str, str):
        if genres_str.lower() == "unknown" or not genres_str.strip():
            return []
        return [g.strip().lower() for g in genres_str.split(',')]
    return []


def clean_movies_df(df: pd.DataFrame) -> pd.DataFrame:
    # Select relevant columns
    selected_columns = [
        "id", "title", "overview", "genres", "keywords", "tagline", "vote_average",
        "vote_count", "release_date", "runtime", "original_language", "poster_path", "popularity"
    ]
    df = df[selected_columns]
    df = df.loc[:, ~df.columns.duplicated()]

    # Filter conditions
    df = df[
        (df["vote_average"] > 5.8) &
        (df["overview"].notnull()) &
        (df["genres"].notnull()) &
        (df["vote_count"] >= 100)
    ]

    # Fill missing data
    df["tagline"] = df["tagline"].fillna('')
    df["genres"] = df["genres"].fillna('unknown')
    df["title"] = df["title"].fillna("Unknown Title")

    # Apply genre cleaning
    df["genres"] = df["genres"].apply(clean_genres)

    return df

# Exported Main Function to dlt

def get_clean_movie_data(as_json: bool = False):
    dataset_path = get_dataset_path()
    df = pd.read_csv(dataset_path)
    cleaned_df = clean_movies_df(df)

    if as_json:
        return cleaned_df.to_dict(orient="records")
    else:
        return cleaned_df


# Optional: Save to file if running directly

if __name__ == "__main__":
    movies = get_clean_movie_data(as_json=True)
    
    import json
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(movies)} cleaned movies to movies.json")
