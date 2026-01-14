import argparse
import sys
import pandas as pd
import numpy as np

def main():
    parser= argparse.ArgumentParser(description="TOPSIS Calculator BY Rehnoor Aulakh")
    parser.add_argument('input_file', help='Input File Path/Name')
    parser.add_argument('weights',help="Weights (comma-separated)")
    parser.add_argument('impacts',help="Impacts (comma-separated)")
    parser.add_argument('output',help="Output File Name")

    args= parser.parse_args()
    #Check1: If the file is valid
    try:
        data= pd.read_csv(args.input_file)
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' cannot be found")
        sys.exit(1)
    #Check if 3 or more columns are available
    if len(data.columns)-1<3:
        print("At least 3 Numeric columns must be there")
        sys.exit(1)
    #Check for 2nd to last column must be numeric
    for col in data.columns[1:]:
        if not np.issubdtype(data[col].dtype,np.number):
            print(f"Error: Column '{col}' must contain numeric data only")
            sys.exit(1)
    #Check2: If the arguments are valid
    #2a. Check for correct number of arguments
    #2b. the weights must be numberic
    try:
        weights = [float(w) for w in args.weights.split(',')]
    except ValueError:
        print("Error: Weights must be numeric, separated by commas")
        sys.exit(1)
    #2c. the impact must be + or -
    impacts= args.impacts.split(',')
    for impact in impacts:
        if impact not in ['+','-']:
            print("Error: Impacts must be either + or -")
            sys.exit(1)
    #2d. check for column count from 2 to last, must be same as number of weights and impacts
    num_criteria= len(data.columns)-1
    if(len(weights)!=num_criteria):
        print("Error: Number of weights are incorrect")
        sys.exit(1)
    if(len(impacts)!= num_criteria):
        print("Error: Number of impacts are incorrect")
        sys.exit(1)
    
    #Normalizing the values
    for col in data.columns[1:]:
        sum_of_squares=(data[col]**2).sum()
        divisor= np.sqrt(sum_of_squares)
        data[col]=data[col]/divisor

    #Applying the weights
    i=0
    for col in data.columns[1:]:
        data[col]*=weights[i]
        i+=1

    #Calculating the best and worst values for every column
    best_values=[]
    worst_values=[]
    #Iterate the data frame column to find the best and worst values
    i=0
    for col in data.columns[1:]:
        if(impacts[i]=='+'):
            best_values.append(data[col].max())
            worst_values.append(data[col].min())
        else:
            best_values.append(data[col].min())
            worst_values.append(data[col].max())
        i+=1

    #Calculate the Euclidean distance from each alternative to: Ideal best (S+) Ideal worst (S-)
        
    S_plus=[]
    S_minus=[]

    #index of the row of data
    for index,row in data.iterrows():
        #reset sum for each row
        sum_best=0
        sum_worst=0
        #i is the counter to iterable, and col is column of dataframe from 1 to last
        i=0
        for col in (data.columns[1:]):
            sum_best+=(row[col]-best_values[i])**2
            sum_worst+=(row[col]-worst_values[i])**2
            i+=1
        S_plus.append(np.sqrt(sum_best))
        S_minus.append(np.sqrt(sum_worst))

    # Calculate the performace score
    #Formula: S-/S-+S+

    performance=[]
    for i in range(len(S_plus)):
        performance.append(S_minus[i]/(S_plus[i]+S_minus[i]))
    data["Topsis Score"]=performance
    data["Rank"]= data["Topsis Score"].rank(ascending=True).astype(int)

    data.to_csv(args.output,index=False)
    
if __name__=='__main__':
    main()