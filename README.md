# Salary Predictor (MVC · Flask · scikit-learn)

A production-ready Linear Regression **Salary Predictor** built with a clean **MVC** structure:
- **Model (M):** scikit-learn pipeline (preprocessing + LinearRegression), stored in `artifacts/model.joblib`
- **View (V):** Jinja templates + optional React skeleton in `frontend/`
- **Controller (C):** Flask Blueprints handling routes and APIs

## Features
- Predict salary (INR) using: `years_experience`, `education_level`, `job_title`, `city`, `company_size`, and skills (`python`, `java`, `aws`, `sql`).
- Clean service + controller layers, reusable pipeline, and type-safe request validation.
- Trained on a **synthetic but realistic** dataset (`data/salary_data.csv`) you can retrain on your data.
- Dockerfile + Gunicorn + `docker-compose.yml` for easy deploy.
- Ready for interviews: readable code, comments, tests scaffold, and a simple UI.

## Quickstart (Local)
```bash
# 1) Create virtualenv and install deps
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) (Optional) retrain the model
python train.py

# 3) Run the app
export FLASK_APP=app
flask run  # or: python -m flask --app app run
# open http://127.0.0.1:5000
```

## Run with Gunicorn (prod-ish)
```bash
gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0:5000 wsgi:app
```

## Docker
```bash
docker build -t salary-predictor .
docker run -p 5000:5000 salary-predictor
# open http://localhost:5000
```

Or with compose:
```bash
docker compose up --build
```

## API
- `POST /api/predict`
```json
{
  "years_experience": 3.5,
  "education_level": "Bachelor",
  "job_title": "Data Scientist",
  "city": "Bengaluru",
  "company_size": "Large",
  "skills_python": 1,
  "skills_java": 0,
  "skills_aws": 1,
  "skills_sql": 1
}
```
_Response_
```json
{
  "predicted_salary_inr": 1450000,
  "currency": "INR",
  "model_version": "1.0.0"
}
```

- `POST /api/train` (retrain from `data/salary_data.csv`), returns metrics.

## MVC Mapping
- **Models:** `app/models/regression.py` (pipeline + I/O), `app/models/schemas.py` (request schema)
- **Views:** `app/views/templates/*.html` (Jinja UI), `app/views/static/*`
- **Controllers:** `app/controllers/*` (Flask blueprints and routing)
- **Services:** `app/services/preprocess.py` (feature engineering)

## Tech Choices (Interview Talking Points)
- **scikit-learn Pipeline + ColumnTransformer** keeps preprocessing consistent across train/predict.
- **OneHotEncoder(handle_unknown="ignore")** makes model robust to unseen categories.
- **Joblib artifact** versioned in `artifacts/` and loaded on startup (fast, reproducible).
- **Blueprinted Flask** for clear MVC boundaries; easy swap to FastAPI if needed.
- **Docker + Gunicorn** for deployment parity; compose for local orchestration.
- **Synthetic dataset** avoids privacy issues and keeps the repo self-contained.

## Frontend (Optional React)
A minimal Vite React skeleton is in `frontend/` that can call `/api/predict`. To use:
```bash
cd frontend
npm install
npm run dev
```
Configure `VITE_API_BASE=http://localhost:5000` in `.env` if needed.

## Folder Structure
```
salary-predictor-mvc/
├─ app/
│  ├─ controllers/
│  ├─ models/
│  ├─ services/
│  └─ views/
├─ artifacts/
├─ data/
├─ frontend/   # optional React view
├─ train.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ wsgi.py
```

---

### Step-by-step (what you can walk through in an interview)
1. **Problem framing** → regression target: salary (INR).
2. **Data** → collect/clean; for demo use provided `data/salary_data.csv`.
3. **Features** → numeric, categorical, binary skills.
4. **Pipeline** → `ColumnTransformer` (scaler + OHE) → `LinearRegression`.
5. **Training** → split, fit, metrics (R², MAE), save to `artifacts/model.joblib`.
6. **Serve** → Flask MVC; controller validates request → model predicts.
7. **UI** → Jinja page &/or React form calling `/api/predict`.
8. **Deploy** → Gunicorn + Docker; health endpoint for readiness checks.
9. **Extend** → regularization (Ridge/Lasso), model registry, monitoring, CI/CD.

Flow:

User Input (View - index.html) → Controller (Flask route) → Model (Linear Regression) 
→ Controller (send result) → View (result.html with prediction)

Enjoy!
