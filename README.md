# Impact Analysis Agent (Test Calibre POC)

## Run locally
Prereqs: Python 3.11+, Docker Desktop, Git

```
git clone <repo-url>
cd impact-analysis-agent
git checkout develop
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env         # Mac/Linux: cp .env.example .env
docker compose up -d
python -m scripts.setup_db
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs