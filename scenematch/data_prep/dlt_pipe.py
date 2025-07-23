# dlt_pipe.py - SIMPLIFIED VERSION
import dlt
import os
import pandas as pd
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

def clean_list_column(text):
    """Convert comma-separated text to list"""
    if isinstance(text, str) and text.strip() and text.strip().lower() != "unknown":
        return [item.strip().lower() for item in text.split(',')]
    return []

@dlt.resource
def clean_movies():
    """Clean movie data from CSV"""
    dataset_path = os.path.expanduser(os.getenv("DATASET_PATH"))
    
    print("📖 Reading CSV data...")
    df = pd.read_csv(dataset_path)
    
    # Select columns
    columns = ["id", "title", "overview", "genres", "keywords", "tagline",
              "vote_average", "vote_count", "release_date", "runtime", 
              "original_language", "popularity"]
    df = df[columns]
    
    # Filter quality movies
    df = df[
        (df["vote_average"] > 5.8) &
        (df["vote_count"] >= 100) &
        (df["overview"].notnull()) &
        (df["genres"].notnull())
    ]
    
    # Clean data
    df["tagline"] = df["tagline"].fillna('')
    df["title"] = df["title"].fillna('Unknown Title')
    df["genres"] = df["genres"].fillna('unknown').apply(clean_list_column)
    df["keywords"] = df["keywords"].fillna('unknown').apply(clean_list_column)
    
    # Remove empty genres/keywords
    df = df[(df["genres"].str.len() > 0) & (df["keywords"].str.len() > 0)]
    
    # Add UUID
    df["uuid"] = [str(uuid.uuid4()) for _ in range(len(df))]
    
    print(f"✅ Cleaned {len(df)} movies")
    
    for record in df.to_dict('records'):
        yield record

def run_dlt_pipeline():
    """Run the complete pipeline"""
    
    print("🚀 STARTING PIPELINE")
    print("=" * 40)
    
    # Setup paths
    dlt_output = os.path.abspath("./dlt_output")
    cleaned_path = os.path.expanduser(os.getenv("CLEANED_DATA_PATH"))
    
    # Handle directory path
    if not cleaned_path.endswith('.json'):
        cleaned_path = os.path.join(cleaned_path, "cleaned_movies.json")
    
    # Create directories
    os.makedirs(dlt_output, exist_ok=True)
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    
    print(f"📁 DLT output: {dlt_output}")
    print(f"📄 JSON output: {cleaned_path}")
    print()
    
    # Configure and run DLT pipeline
    os.environ["DESTINATION__FILESYSTEM__BUCKET_URL"] = dlt_output
    
    pipeline = dlt.pipeline(
        pipeline_name="movie_preparation",
        destination="filesystem", 
        dataset_name="cleaned_movies"
    )
    
    print("⚙️  RUNNING DLT PIPELINE")
    print("-" * 30)
    
    info = pipeline.run(clean_movies(), write_disposition="replace")
    
    print("✅ DLT pipeline completed")
    print()
    
    # Save to JSON
    print("💾 SAVING JSON FILE")
    print("-" * 20)
    
    movies = list(clean_movies())
    
    with open(cleaned_path, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(movies)} movies")
    print()
    
    print("🎉 PIPELINE COMPLETE")
    print("=" * 40)
    print(f"📁 DLT artifacts: {dlt_output}")
    print(f"📄 Clean JSON: {cleaned_path}")
    
    return info, cleaned_path

if __name__ == "__main__":
    run_dlt_pipeline()
