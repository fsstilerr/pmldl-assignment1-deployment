from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field


MODEL_PATH = Path("models/model.joblib")

model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Penguin Species Prediction API",
    version="1.0",
)


class PenguinFeatures(BaseModel):
    island: Literal["Biscoe", "Dream", "Torgersen"]
    bill_length_mm: float = Field(gt=0)
    bill_depth_mm: float = Field(gt=0)
    flipper_length_mm: float = Field(gt=0)
    body_mass_g: float = Field(gt=0)
    sex: Literal["MALE", "FEMALE"]


@app.get("/")
def root():
    return {"message": "Penguin prediction API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: PenguinFeatures):
    input_df = pd.DataFrame([data.model_dump()])

    prediction = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]
    classes = model.named_steps["model"].classes_

    probability_dict = {
        class_name: round(float(probability), 4)
        for class_name, probability in zip(classes, probabilities)
    }

    return {
        "prediction": prediction,
        "probabilities": probability_dict,
    }