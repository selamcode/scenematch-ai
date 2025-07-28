# Scenematch-ai

End-to-end, reproducible demo of an **agentic-RAG** movie-recommendation system.

From data prep to hybrid search to an LLM-powered chatbot—plus feedback dashboards for continuous improvement.

---

### Movies data source:

> Download the csv version:

- https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies

<br>

## 1. Main Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OPENAI](https://img.shields.io/badge/OPENAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-5E3EFB?style=for-the-badge&logo=qdrant&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-146f45?style=for-the-badge&logo=postgresql&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PANDAS](https://img.shields.io/badge/PANDAS-150458?style=for-the-badge&logo=pandas&logoColor=white)


| Layer | Tech |
| ----- | ---- |
| Python | Python Interpreter - 3.9.13|
| Large-Language Model | OpenAI `gpt-4o-mini` |
| Embeddings | `jinaai/jina-embeddings-v2-small-en` |
| Vector DB | Qdrant (Docker) |
| Data pipeline | DLT + pandas |
| Web UI | Flask (HTML/CSS) |
| ORM / DB | SQLAlchemy + PostgreSQL |
| Monitoring | Grafana |
| Containerization | Docker & Docker Compose |

<br>

### 2. What should the workspace look like ?

##### After completing `Quick-start` step 1 - 4, you should have a file tree that look like this.

```text

scenematch-ai/                         # ← project root
├── .env                               # environment variables (see step 4 below)
├── README.md
├── requirements.txt
├── venv/                              # Python virtual environment
│
│
├── data/
│   ├── raw/
│   │   └── movies.csv                 # DATASET_PATH
│   ├── processed/                     # CLEANED_DATA_PATH (output of dlt_pipe.py)
│   └── evaluation/
│       ├── ground_truth/
│       │   └── ground_truth_uuids.json# GROUND_TRUTH_PATH
│       └── evaluation_result/         # EVALUATION_RESULT (metrics land here)
│
└── scenematch/
    ├── __init__.py
    │
    ├── clients/
    ├── data_prep/
    ├── evaluation/
    ├── rag/
    ├── web_app/
    │
    └── monitoring/                   # Grafana stack 
        └── grafana-stack/
            ├── docker-compose.yaml
            └── datasources.yaml

```

<br>

## 3. Quick-start (local)


#### 1. Clone repo

<br>

``` bash

git clone https://github.com/selamcode/scenematch-ai.git

```
<br>

``` bash

cd scenematch-ai 

```
<br>

#### 2. Python env
<br>

``` bash
python -m venv venv
source venv/bin/activate # Windows → venv\Scripts\activate
pip install -r requirements.txt
```
<br>

#### 3. Run Qdrant

<br>

```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```
<br>

#### 4. Create .env and Set Variables
<br>

```python
# OpenAI
# Your secret key for GPT calls. Get it from https://platform.openai.com
OPENAI_API_KEY=sk-********************************

# Raw CSV downloaded from Kaggle 
DATASET_PATH=path/to/data/raw/movies.csv              # e.g. /Users/ana/projects/...
# Folder that will hold the cleaned CSV / JSON output
CLEANED_DATA_PATH=/path/to/data/processed

# Ground-truth UUID list for evaluation
GROUND_TRUTH_PATH=/path/to/data/evaluation/ground_truth/ground_truth_uuids.json
# Where evaluation metrics will be written
EVALUATION_RESULT=/path/to/data/evaluation/evaluation_result

# PostgreSQL (feedback storage) 
DATABASE_URL="postgresql://you@localhost:5432/feedback_db"           
```

- Replace `<you>` with your macOS or Linux username (or a Windows absolute path like C:\Users\You\...).

- Keep the variable names exactly as shown—code expects them via `python-dotenv`.

<br>

#### 6. Run the ETL pipeline (DLT) to convert the raw CSV into JSON ready for Qdrant embedding

<br>

``` bash 
python -m scenematch.data_prep.dlt_pipe 
```
<br>

>  - dlt_pipe.py is the main ETL script. 
>  - data_cleaning.ipynb and prepare_data.py exist only for ad-hoc testing and experimentation; you do not need them for normal setup.

<br>

#### 7 Build vector index & embed

<br>

- Toggle `CREATE_NEW_COLLECTION = True` in scenematch/rag/main.py

<br>

```python
# scenematch/rag/main.py
CREATE_NEW_COLLECTION = True in scenematch/rag/main.py
```
<br>

#### 8 Run Chat!

<br>

- ##### a) CLI

<br>

```python
python -m scenematch.rag.main
```
<br>

> Make sure you run `a` before `b`, the indexing and embeding happens in `a`.

<br>

- ##### b) Web
```python
python -m scenematch.web_app.chat_app # open http://127.0.0.1:5000
```

<br>

##### Bonus

#### (Optional) Grafana + Postgres for feedback

```bash 
cd monitoring/grafana-stack
docker compose up -d
```
