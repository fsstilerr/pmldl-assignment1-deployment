# PMLDL Assignment 1: Deployment

This project implements an automated MLOps pipeline for penguin species classification.

The pipeline consists of three main parts:

1. Data Engineering
2. Model Engineering
3. Deployment

The complete pipeline is scheduled to run automatically every 5 minutes.

## Dataset

The project uses the Palmer Penguins dataset.

The target variable is `species` with three classes:

- Adelie
- Chinstrap
- Gentoo

The model uses the following input features:

- island
- bill length
- bill depth
- flipper length
- body mass
- sex

## Project Structure

```text
.
├── code
│   ├── datasets
│   │   └── prepare_data.py
│   ├── models
│   │   └── train_model.py
│   └── deployment
│       ├── api
│       │   ├── main.py
│       │   ├── Dockerfile
│       │   └── requirements.txt
│       ├── app
│       │   ├── app.py
│       │   ├── Dockerfile
│       │   └── requirements.txt
│       └── docker-compose.yml
├── data
│   ├── raw
│   │   └── penguins.csv
│   └── processed
├── metrics
├── models
├── scripts
│   └── run_pipeline.sh
├── dvc.yaml
├── dvc.lock
├── requirements.txt
└── README.md
```

## Data Engineering

Data processing is implemented in `code/datasets/prepare_data.py`.

The script:

- loads the raw CSV dataset
- removes duplicated rows
- handles missing values
- normalizes categorical values
- checks and removes numerical outliers using the IQR method
- splits the dataset into training and testing data

The split is:

- 80% training data
- 20% testing data

The processed files are saved to:

```text
data/processed/train.csv
data/processed/test.csv
```

This stage is managed by DVC.

## Model Engineering

Model training is implemented in `code/models/train_model.py`.

Numerical features are transformed using `StandardScaler`.

Categorical features are transformed using `OneHotEncoder`.

The preprocessing and classifier are combined into a Scikit-learn `Pipeline`.

The model used is Logistic Regression.

The model is evaluated using:

- Accuracy
- Macro F1-score

Current test results:

```text
Accuracy: 1.0000
Macro F1-score: 1.0000
```

The trained model is saved to:

```text
models/model.joblib
```

The evaluation metrics are saved to:

```text
metrics/metrics.json
```

MLflow is used to log model parameters, metrics, and artifacts.

## DVC Pipeline

The DVC pipeline contains two connected stages:

```text
prepare_data
     |
     v
train_model
```

The pipeline can be executed with:

```bash
dvc repro
```

DVC tracks dependencies and only reruns stages when their inputs or code have changed.

## Deployment

The trained model is deployed using two separate Docker containers.

### FastAPI

FastAPI provides the model prediction API.

The API contains the following endpoints:

```text
GET  /
GET  /health
POST /predict
```

The API is available at:

```text
http://localhost:8000
```

Swagger documentation is available at:

```text
http://localhost:8000/docs
```

### Streamlit

Streamlit provides the web interface.

The user can enter penguin characteristics, click the prediction button, and receive the predicted species and class probabilities.

The application is available at:

```text
http://localhost:8501
```

The Streamlit container communicates with the FastAPI container using:

```text
http://api:8000
```

## Docker

Build the Docker images:

```bash
docker compose -f code/deployment/docker-compose.yml build
```

Start the containers:

```bash
docker compose -f code/deployment/docker-compose.yml up -d
```

Check the running containers:

```bash
docker compose -f code/deployment/docker-compose.yml ps
```

Stop the containers:

```bash
docker compose -f code/deployment/docker-compose.yml down
```

## Complete Pipeline

The complete pipeline is executed by:

```text
scripts/run_pipeline.sh
```

It performs the following sequence:

```text
DVC pipeline
    ↓
data processing
    ↓
model training and evaluation
    ↓
Docker image build
    ↓
FastAPI and Streamlit deployment
```

Run the complete pipeline manually with:

```bash
./scripts/run_pipeline.sh
```

## Automatic Execution

The pipeline is scheduled using cron and runs every 5 minutes.

The cron job executes `scripts/run_pipeline.sh` and saves the output to:

```text
logs/pipeline.log
```

Example schedule:

```text
*/5 * * * *
```

The log can be checked using:

```bash
cat logs/pipeline.log
```

## Setup

Python 3.12 is used for the project.

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the complete pipeline:

```bash
./scripts/run_pipeline.sh
```

After the pipeline starts successfully:

- FastAPI documentation: `http://localhost:8000/docs`
- Streamlit application: `http://localhost:8501`

## Technologies

- Python 3.12
- Pandas
- Scikit-learn
- DVC
- MLflow
- FastAPI
- Streamlit
- Docker
- Docker Compose
- cron