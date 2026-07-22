# Student Performance Predictor : End-to-End ML Project

Predicts a student's **math score** from demographic and academic inputs
(gender, ethnicity, parental education, lunch type, test preparation, reading
score, writing score), using a modular training pipeline and a Flask web app
for serving predictions.

## Problem Statement

Given a student's background and their reading/writing scores, can we predict
their math score? The dataset (`notebook/data/stud.csv`) contains 1000 student
records. This is framed as a regression problem, evaluated with R².

## Pipeline Architecture

```
raw CSV (notebook/data/stud.csv)
        │
        ▼
┌─────────────────────┐
│  Data Ingestion      │  reads CSV, splits train/test (80/20)
│  (data_ingestion.py) │  → artifacts/train.csv, artifacts/test.csv
└─────────┬────────────┘
          ▼
┌─────────────────────────┐
│  Data Transformation      │  numeric: median-impute + scale
│  (data_transformation.py) │  categorical: mode-impute + one-hot + scale
└─────────┬──────────────────┘  → artifacts/preprocessor.pkl
          ▼
┌─────────────────────┐
│  Model Training       │  GridSearchCV over 7 regressors
│  (model_trainer.py)   │  (Linear, RF, DT, GBM, XGBoost, CatBoost, AdaBoost)
└─────────┬─────────────┘  → artifacts/model.pkl (best by test R²)
          ▼
┌─────────────────────┐
│  Flask App             │  loads model.pkl + preprocessor.pkl
│  (app.py)              │  serves predictions at /predict
└─────────────────────┘
```

Each stage is a standalone script under `src/components/`. `src/pipeline/train_pipeline.py`
orchestrates all three training stages; `src/pipeline/predict_pipeline.py` handles
loading the saved artifacts and running inference for the Flask app.

## Result

Exploratory model comparison in `notebook/2. MODEL TRAINING.ipynb` found Linear
Regression as a strong baseline, reaching **R² ≈ 0.88 on the test set**. The
production pipeline (`model_trainer.py`) re-runs a GridSearchCV comparison
across 7 models on every training run and automatically saves whichever one
scores highest — so the exact winning model can vary slightly by run.

## Project Structure

```
├── app.py                          # Flask app entry point
├── requirements.txt
├── setup.py
├── notebook/
│   ├── 1 . EDA STUDENT PERFORMANCE.ipynb
│   ├── 2. MODEL TRAINING.ipynb
│   └── data/stud.csv
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── pipeline/
│   │   ├── train_pipeline.py
│   │   └── predict_pipeline.py
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
├── templates/
│   ├── index.html
│   └── predict.html
└── artifacts/                      # generated at train time — gitignored
```

## How to Run Locally

**1. Clone and set up the environment**
```bash
git clone https://github.com/SahilInstinct/End-to-end-MLproject.git
cd End-to-end-MLproject
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

**2. Train the model** (required before the app will run — this generates
`artifacts/model.pkl` and `artifacts/preprocessor.pkl`, which are gitignored
and not shipped in the repo)
```bash
python -m src.pipeline.train_pipeline
```

**3. Run the Flask app**
```bash
python app.py
```
Visit `http://localhost:8080` in your browser, go to the predict page, fill
in the form, and get a predicted math score.

## Tech Stack

Python, pandas, NumPy, scikit-learn, XGBoost, CatBoost, Flask, dill (for
model serialization).

## Future Improvements

- [ ] Add unit tests for `DataTransformation` and `PredictPipeline`
- [ ] Dockerize for deployment
- [ ] Log evaluation metrics (not just the winning R²) to compare model runs over time
