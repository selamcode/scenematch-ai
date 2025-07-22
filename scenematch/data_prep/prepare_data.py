import os
import pandas as pd
import uuid
from dotenv import load_dotenv

load_dotenv()

# Config and Setup
def get_dataset_path():
    return os.getenv("DATASET_PATH")

# Cleaning Helpers
def clean_list_column(text):
    if isinstance(text, str):
        if text.strip().lower() == "unknown" or not text.strip():
            return []
        return [item.strip().lower() for item in text.split(',')]
    return []

def clean_movies_df(df: pd.DataFrame) -> pd.DataFrame:
    selected_columns = [
        "id", "title", "overview", "genres", "keywords", "tagline",
        "vote_average", "vote_count", "release_date", "runtime",
        "original_language", "popularity"
    ]
    df = df[selected_columns]  # 'poster_path' excluded here
    df = df.loc[:, ~df.columns.duplicated()]

    df = df[
        (df["vote_average"] > 5.8) &
        (df["vote_count"] >= 100) &
        (df["overview"].notnull()) &
        (df["genres"].notnull())
    ]

    # Fill missing values
    df["tagline"] = df["tagline"].fillna('')
    df["title"] = df["title"].fillna('Unknown Title')
    df["genres"] = df["genres"].fillna('unknown')
    df["keywords"] = df["keywords"].fillna('unknown')

    df["genres"] = df["genres"].apply(clean_list_column)
    df["keywords"] = df["keywords"].apply(clean_list_column)

    # Remove empty genre or keyword lists
    df = df[df["genres"].str.len() > 0]
    df = df[df["keywords"].str.len() > 0]

    df.insert(0, "uuid", [str(uuid.uuid4()) for _ in range(len(df))])

    return df

# Exported Main Function
def get_clean_movie_data(as_json: bool = False):
    dataset_path = get_dataset_path()
    df = pd.read_csv(dataset_path)
    cleaned_df = clean_movies_df(df)

    if as_json:
        return cleaned_df.to_dict(orient="records")
    return cleaned_df

# Save to JSON if run directly
if __name__ == "__main__":
    movies = get_clean_movie_data(as_json=True)

    import json
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(movies)} cleaned movies to movies.json")
