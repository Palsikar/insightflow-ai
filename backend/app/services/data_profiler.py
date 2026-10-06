import pandas as pd


def detect_column_type(series: pd.Series) -> str:

    # Numeric columns
    if pd.api.types.is_numeric_dtype(series):

        # Detect binary columns such as 0/1
        unique_values = series.dropna().unique()

        if len(unique_values) == 2 and set(unique_values).issubset({0, 1}):
            return "binary"

        return "numeric"

    # Already converted datetime columns
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"

    # String/text columns
    if pd.api.types.is_string_dtype(series):

        # Try detecting dates
        try:
            converted = pd.to_datetime(
                series,
                errors="coerce",
                dayfirst=True
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.8:
                return "date"

        except Exception:
            pass

        # Detect categorical text
        unique_ratio = series.nunique() / max(len(series), 1)

        if unique_ratio <= 0.05:
            return "categorical"

        return "text"

    return "unknown"


def profile_dataset(df: pd.DataFrame):

    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_details": []
    }

    for column in df.columns:

        column_data = df[column]

        detected_type = detect_column_type(column_data)

        column_info = {
            "name": column,
            "data_type": str(column_data.dtype),
            "semantic_type": detected_type,
            "missing_values": int(column_data.isnull().sum()),
            "missing_percentage": round(
                (column_data.isnull().sum() / len(df)) * 100,
                2
            ),
            "unique_values": int(column_data.nunique()),
            "sample_values": column_data.dropna()
            .head(5)
            .tolist()
        }

        # Add statistics for numeric columns
        if pd.api.types.is_numeric_dtype(column_data):

            column_info["statistics"] = {
                "mean": round(float(column_data.mean()), 2),
                "minimum": float(column_data.min()),
                "maximum": float(column_data.max()),
                "median": round(float(column_data.median()), 2),
                "standard_deviation": round(
                    float(column_data.std()), 2
                )
            }

        profile["column_details"].append(column_info)

    return profile