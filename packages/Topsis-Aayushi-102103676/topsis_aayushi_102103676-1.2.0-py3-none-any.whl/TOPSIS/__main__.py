# File: TOPSIS/__main__.py

import pandas as pd
import numpy as np
import sys

def topsis(data, weights, impacts):
    # --- Validations ---
    if len(data.columns) < 3:
        raise ValueError("Input file must contain three or more columns.")
    
    # Check for numeric values in criteria columns
    try:
        data.iloc[:, 1:] = data.iloc[:, 1:].astype(float)
    except ValueError:
        raise ValueError("Columns from 2nd to last must contain numeric values only.")

    num_criteria = len(data.columns) - 1
    if len(weights) != num_criteria or len(impacts) != num_criteria:
        raise ValueError(f"Number of weights and impacts must match the number of criteria ({num_criteria}).")
    
    if not all(i in ['+', '-'] for i in impacts):
        raise ValueError("Impacts must be a comma-separated list of '+' or '-'.")

    # --- Calculations ---
    # 1. Create a numeric-only dataframe for calculations
    df_numeric = data.iloc[:, 1:].values

    # 2. Normalize the data (Vector Normalization)
    rss = np.linalg.norm(df_numeric, axis=0)
    normalized_data = df_numeric / rss

    # 3. Apply weights
    weighted_normalized_data = normalized_data * weights

    # 4. Determine ideal best and ideal worst solutions
    ideal_best = np.zeros(num_criteria)
    ideal_worst = np.zeros(num_criteria)

    for i in range(num_criteria):
        if impacts[i] == '+':
            ideal_best[i] = weighted_normalized_data[:, i].max()
            ideal_worst[i] = weighted_normalized_data[:, i].min()
        else: # impact is '-'
            ideal_best[i] = weighted_normalized_data[:, i].min()
            ideal_worst[i] = weighted_normalized_data[:, i].max()

    # 5. Calculate Euclidean distance from ideal best and worst
    dist_best = np.linalg.norm(weighted_normalized_data - ideal_best, axis=1)
    dist_worst = np.linalg.norm(weighted_normalized_data - ideal_worst, axis=1)
    
    # 6. Calculate TOPSIS Score (add epsilon to avoid division by zero)
    topsis_score = dist_worst / (dist_best + dist_worst + 1e-8)

    return topsis_score

def main():
    if len(sys.argv) != 5:
        print("Usage: topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        print("Example: topsis data.csv \"1,1,1,1\" \"-,-,+,+\" result.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    result_file = sys.argv[4]

    try:
        # Load data and parse arguments
        dataset = pd.read_csv(input_file)
        weights = [float(w) for w in weights_str.split(',')]
        impacts = impacts_str.split(',')

        # Perform TOPSIS calculation
        topsis_score = topsis(dataset.copy(), weights, impacts)

        # Add results to the original dataframe and save
        dataset['Topsis Score'] = topsis_score
        dataset['Rank'] = dataset['Topsis Score'].rank(ascending=False).astype(int)
        dataset.to_csv(result_file, index=False)

        print(f"Successfully generated TOPSIS results in '{result_file}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()