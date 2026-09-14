from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


RAW_DATA_PATH = Path("data/raw/penguins.csv")
TRAIN_DATA_PATH = Path("data/processed/train.csv")
TEST_DATA_PATH = Path("data/processed/test.csv")

NUMERIC_COLUMNS = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]

CATEGORICAL_COLUMNS = [
    "island",
    "sex",
]


def remove_outliers_iqr(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)

    for column in columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        column_mask = df[column].between(lower_bound, upper_bound) | df[column].isna()
        mask &= column_mask

    return df[mask].copy()


def main():
    print("Loading raw dataset...")
    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Raw rows: {len(df)}")

    df = df.drop_duplicates()

    df = df.dropna(subset=["species"])

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["sex"] = df["sex"].str.strip().str.upper()

    rows_before_outlier_removal = len(df)

    df = remove_outliers_iqr(df, NUMERIC_COLUMNS)

    removed_outliers = rows_before_outlier_removal - len(df)

    print(f"Removed outlier rows: {removed_outliers}")

    for column in NUMERIC_COLUMNS:
        median_value = df[column].median()
        df[column] = df[column].fillna(median_value)

    for column in CATEGORICAL_COLUMNS:
        mode_value = df[column].mode()[0]
        df[column] = df[column].fillna(mode_value)

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["species"],
    )

    TRAIN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(TRAIN_DATA_PATH, index=False)
    test_df.to_csv(TEST_DATA_PATH, index=False)

    print(f"Clean rows: {len(df)}")
    print(f"Training rows: {len(train_df)}")
    print(f"Testing rows: {len(test_df)}")

    print("Missing values after cleaning:")
    print(df.isna().sum())

    print("Data engineering stage completed.")


if __name__ == "__main__":
    main()