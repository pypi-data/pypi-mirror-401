import sys
import pandas as pd
import numpy as np
import os

def check_numeric(df):
    data = df.iloc[:, 1:]
    try:
        data.astype(float)
        return True
    except ValueError:
        return False

def main():
    if len(sys.argv) != 5:
        print("ERROR: Incorrect number of parameters.")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        print('Example: python topsis.py data.xlsx "1,1,1,1" "+,+,-,+" result.xlsx')
        return

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    if not os.path.exists(input_file):
        print("ERROR: File not found.")
        return

    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.xlsx'):
            df = pd.read_excel(input_file)
        else:
            print("ERROR: Unsupported file format. Please use .csv or .xlsx")
            return
    except Exception as e:
        print(f"ERROR: Could not read file. {e}")
        return

    if df.shape[1] < 3:
        print("ERROR: Input file must contain three or more columns.")
        return

    if not check_numeric(df):
        print("ERROR: From 2nd to last columns must contain numeric values only.")
        return
    
    data = df.iloc[:, 1:].values.astype(float)
    
    try:
        weights = [float(w) for w in weights_str.split(',')]
        impacts = impacts_str.split(',')
    except ValueError:
        print("ERROR: Weights must be numeric and separated by commas.")
        return

    num_cols = data.shape[1]
    
    if len(weights) != num_cols or len(impacts) != num_cols:
        print("\n--------------------------------------------------")
        print("❌ ERROR: Mismatch between Data and Inputs")
        print("--------------------------------------------------")
        print(f"1. Your file '{input_file}' has {num_cols} numeric columns.")
        print(f"   (Columns detected: {df.columns[1:].tolist()})")
        print(f"2. You provided {len(weights)} weights.")
        print(f"3. You provided {len(impacts)} impacts.")
        print("--------------------------------------------------")
        print(f"👉 SOLUTION: You need exactly {num_cols} weights and {num_cols} impacts.")
        print("--------------------------------------------------\n")
        return

    if not all(i in ['+', '-'] for i in impacts):
        print("ERROR: Impacts must be either +ve or -ve.")
        return

    rss = np.sqrt(np.sum(data**2, axis=0))
    normalized_data = data / rss
    weighted_data = normalized_data * weights

    ideal_best = []
    ideal_worst = []

    for i in range(num_cols):
        col = weighted_data[:, i]
        if impacts[i] == '+':
            ideal_best.append(np.max(col))
            ideal_worst.append(np.min(col))
        else:
            ideal_best.append(np.min(col)) 
            ideal_worst.append(np.max(col)) 

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    s_plus = np.sqrt(np.sum((weighted_data - ideal_best)**2, axis=1))
    s_minus = np.sqrt(np.sum((weighted_data - ideal_worst)**2, axis=1))

    total_dist = s_plus + s_minus
    topsis_score = np.divide(s_minus, total_dist, out=np.zeros_like(s_minus), where=total_dist!=0)
    
    df['Topsis Score'] = topsis_score
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    elif output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)
    else:
        df.to_csv(output_file + ".csv", index=False)
        
    print(f"SUCCESS: File saved to {output_file}")

if __name__ == "__main__":
    main()