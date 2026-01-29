import pandas as pd
import numpy as np
from pathlib import Path

def topsis(input_file, weights_str, impacts_str, output_file):
   

    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError("Input file not found.")

    # Read input file
    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file)
    elif input_file.endswith(".xlsx"):
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Input file must be .csv or .xlsx")

    # At least 3 columns
    if df.shape[1] < 3:
        raise ValueError("Input file must contain at least 3 columns.")

    # Numeric columns from 2nd onward
    try:
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors="raise")
    except ValueError:
        raise ValueError("Non-numeric value found in criteria columns (from 2nd to last column).")

    n_criteria = df.shape[1] - 1

    # Parse weights
    try:
        weights = [float(x.strip()) for x in weights_str.split(",")]
    except ValueError:
        raise ValueError("Weights must be numeric and comma-separated.")

    if len(weights) != n_criteria:
        raise ValueError(f"Number of weights ({len(weights)}) must match number of criteria ({n_criteria}).")

    weights = np.array(weights, dtype=float)
    weights = weights / np.sum(weights)

    # Parse impacts
    impacts = [imp.strip().upper() for imp in impacts_str.split(",")]
    if len(impacts) != n_criteria or not all(imp in ["+", "-"] for imp in impacts):
        raise ValueError("Impacts must be '+' or '-' only, comma-separated, and count must match criteria.")

    # TOPSIS algorithm
    data = df.iloc[:, 1:].values

    # Step 1: normalize
    norm = np.sqrt(np.sum(data ** 2, axis=0))
    r = data / norm

    # Step 2: weighted normalized
    v = r * weights

    # Step 3: ideal best and worst
    ideal_best = np.zeros(n_criteria)
    ideal_worst = np.zeros(n_criteria)
    for j in range(n_criteria):
        if impacts[j] == "+":
            ideal_best[j] = np.max(v[:, j])
            ideal_worst[j] = np.min(v[:, j])
        else:
            ideal_best[j] = np.min(v[:, j])
            ideal_worst[j] = np.max(v[:, j])

    # Step 4: distances
    s_pos = np.sqrt(np.sum((v - ideal_best) ** 2, axis=1))
    s_neg = np.sqrt(np.sum((v - ideal_worst) ** 2, axis=1))

    # Step 5: score and rank
    score = s_neg / (s_pos + s_neg)
    rank = np.argsort(-score) + 1

    # Append and save
    df["Topsis Score"] = np.round(score, 4)
    df["Rank"] = rank.astype(int)
    df.to_csv(output_file, index=False)

    return df 
