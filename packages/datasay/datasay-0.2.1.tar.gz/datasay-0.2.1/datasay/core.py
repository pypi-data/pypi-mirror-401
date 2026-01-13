import pandas as pd
from pathlib import Path


def _analyze_series(series, drop_threshold=0.25):
    data = series.dropna().tolist()

    if len(data) < 2:
        return "not enough data"

    start, end = data[0], data[-1]
    peak, trough = max(data), min(data)

    events = []

    if end > start:
        events.append("ended higher than it started")
    elif end < start:
        events.append("ended lower than it started")
    else:
        events.append("ended at the same value it started")

    if peak != start and peak != end:
        events.insert(0, f"rose to a peak of {peak}")

    sharp_drops = []
    for i in range(1, len(data)):
        change = (data[i] - data[i - 1]) / max(abs(data[i - 1]), 1)
        if change <= -drop_threshold:
            sharp_drops.append(data[i])

    if sharp_drops:
        events.append(f"dropped sharply to {min(sharp_drops)}")

    sentence = "Data " + ", ".join(events[:-1])
    if len(events) > 1:
        sentence += ", and " + events[-1]
    else:
        sentence += events[0]

    return sentence.capitalize() + "."


def _load_data(path):
    ext = Path(path).suffix.lower()

    if ext == ".csv":
        return pd.read_csv(path)

    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(path)

    elif ext == ".json":
        return pd.read_json(path)

    elif ext in (".tsv", ".txt"):
        return pd.read_csv(path, sep="\t")

    elif ext == ".parquet":
        return pd.read_parquet(path)

    else:
        raise ValueError(
            f"Unsupported file format: {ext}. "
            "Supported formats: csv, xlsx, xls, json, tsv, parquet"
        )


def explain(data):
    # Accept file path OR DataFrame
    if isinstance(data, str):
        data = _load_data(data)

    insights = []

    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            insight = _analyze_series(data[col])
            insights.append(f"{col}: {insight}")
        else:
            insights.append(f"{col}: {data[col].nunique()} unique values")

    return "\n".join(insights)

