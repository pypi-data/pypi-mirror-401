import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 5:
        print("Usage: topsis <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        print("Example: topsis data.csv \"1,1,1,2\" \"+,+,-,+\" result.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]
    
    try:
        data = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: File not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    if data.shape[1] < 3:
        print("Error: Input file must have at least three columns")
        sys.exit(1)
    
    criteria_data = data.iloc[:, 1:]
    
    for col in criteria_data.columns:
        if not pd.api.types.is_numeric_dtype(criteria_data[col]):
            print(f"Error: Column '{col}' contains non-numeric values")
            sys.exit(1)
    
    try:
        weights = [float(w.strip()) for w in weights_str.split(',')]
    except ValueError:
        print("Error: Weights must be numeric values separated by commas")
        sys.exit(1)
    
    impacts = [i.strip() for i in impacts_str.split(',')]
    
    num_criteria = criteria_data.shape[1]
    
    if len(weights) != num_criteria:
        print(f"Error: Number of weights ({len(weights)}) must equal number of criteria ({num_criteria})")
        sys.exit(1)
    
    if len(impacts) != num_criteria:
        print(f"Error: Number of impacts ({len(impacts)}) must equal number of criteria ({num_criteria})")
        sys.exit(1)
    
    for impact in impacts:
        if impact not in ['+', '-']:
            print(f"Error: Impact '{impact}' is invalid. Impacts must be either '+' or '-'")
            sys.exit(1)
    
    normalized = criteria_data / np.sqrt((criteria_data ** 2).sum(axis=0))
    
    weighted = normalized * weights
    
    ideal_best = []
    ideal_worst = []
    
    for i, impact in enumerate(impacts):
        if impact == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())
    
    distance_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))
    
    topsis_score = distance_worst / (distance_best + distance_worst)
    
    data['Topsis Score'] = topsis_score
    data['Rank'] = topsis_score.rank(ascending=False).astype(int)
    
    try:
        data.to_csv(output_file, index=False)
        print(f"Success: Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
