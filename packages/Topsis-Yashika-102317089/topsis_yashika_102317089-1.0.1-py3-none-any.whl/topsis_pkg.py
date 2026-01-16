import pandas as pd
import sys
import os
import numpy as np

def main():
    # 1. Parameter check (Input, Weights, Impacts, Output) [cite: 37, 40]
    if len(sys.argv) != 5:
        print("Error: Usage: python 102317089.py <InputDataFile> <Weights> <Impacts> <ResultFileName>") [cite: 37]
        return

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    result_file = sys.argv[4]

    # 2. File Not Found Handling [cite: 42]
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    try:
        # Load file
        df = pd.read_csv(input_file)
        
        # 3. Column count check (3 or more) [cite: 29, 44]
        if len(df.columns) < 3:
            print("Error: Input file must have 3 or more columns.")
            return

        # 4. Numeric check (2nd column to last) [cite: 31, 45]
        data = df.iloc[:, 1:].values
        if not np.issubdtype(data.dtype, np.number):
            print("Error: Columns from 2nd to last must contain numeric values only.")
            return

        # 5. Weights and Impacts parsing [cite: 47]
        weights = [float(w) for w in weights_str.split(',')]
        impacts = impacts_str.split(',')

        # 6. Length consistency check 
        if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
            print("Error: Number of weights/impacts must match numeric columns.")
            return

        # 7. Impact value check (+ or -) [cite: 46, 68]
        if not all(i in ['+', '-'] for i in impacts):
            print("Error: Impacts must be '+' or '-'.")
            return

        # --- TOPSIS Calculation [cite: 3, 21] ---
        
        # Step A: Normalization
        norm_data = data / np.sqrt((data**2).sum(axis=0))
        
        # Step B: Apply Weights
        weighted_data = norm_data * weights
        
        # Step C: Ideal Best/Worst
        ideal_best = []
        ideal_worst = []
        for i in range(len(impacts)):
            if impacts[i] == '+':
                ideal_best.append(max(weighted_data[:, i]))
                ideal_worst.append(min(weighted_data[:, i]))
            else:
                ideal_best.append(min(weighted_data[:, i]))
                ideal_worst.append(max(weighted_data[:, i]))

        # Step D: Distance Calculation
        dist_best = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
        dist_worst = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))

        # Step E: Topsis Score and Rank [cite: 34]
        df['Topsis Score'] = dist_worst / (dist_best + dist_worst)
        df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

        # 8. Save Result [cite: 34, 35]
        df.to_csv(result_file, index=False)
        print(f"Success: Results saved to {result_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()