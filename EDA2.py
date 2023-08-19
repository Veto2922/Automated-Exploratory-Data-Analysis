import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
import seaborn as sns





#--------------------Load the data into df-------------------------------------------------------------------------------------

def load_data(data_source):
    if data_source.endswith('.csv'):
        df = pd.read_csv(data_source)
        return df
    elif data_source.endswith('.xlsx') or data_source.endswith('.xls'):
        df = pd.read_excel(data_source)
        return df
    elif data_source.endswith('.sql'):
        df = pd.read_sql(data_source)
        return df
    else:
        raise ValueError("Unsupported data source")
    
#------------------------------------------------------------------------------------------------------------------------------


def explore_data(data):
    """
    Explore the given DataFrame and provide basic insights.
    
    Args:
        data (pd.DataFrame): The DataFrame to explore.
    """
    # Basic information
    print("Basic Information:")
    print("Number of rows:", data.shape[0])
    print("Number of columns:", data.shape[1])
    
    # Data types
    print("\nData Types:")
    print(data.dtypes)
    
    # Summary statistics for numerical columns
    numerical_columns = data.select_dtypes(include=['int64', 'float64'])
    if not numerical_columns.empty:
        print("\nSummary Statistics for Numerical Columns:")
        print(numerical_columns.describe())
    else:
        print("\nNo numerical columns found.")
    
    # Unique values in categorical columns
    categorical_columns = data.select_dtypes(include=['object'])
    if not categorical_columns.empty:
        print("\nUnique Values in Categorical Columns:")
        for column in categorical_columns.columns:
            unique_values = data[column].nunique()
            print(f"{column}: {unique_values} unique values")
    else:
        print("\nNo categorical columns found.")
    
    # Number and percentage of null values in each column
    null_counts = data.isnull().sum()
    total_cells = data.shape[0]
    print("\nMissing Values:")
    for column, null_count in null_counts.items():
        if null_count > 0:
            percentage = (null_count / total_cells) * 100
            print(f"{column}: {null_count} missing ({percentage:.2f}%)")










#--------------------------------------------preprocess_data-------------------------------------------------------------------
def preprocess_data(data):
   print('*' * 100)
   print('Go to preprocessing data-------------------')
   print('*' * 100)
   for column in data.columns:
    if data[column].dtype == "object":
        # Handle categorical columns
        if args.missing_strategy == "remove":
            data[column] = data[column].dropna()
        elif args.missing_strategy == "mean":
            data[column] = data[column].fillna(data[column].mode()[0])  # Filling with mode for categorical data
        elif args.missing_strategy == "median":
            data[column] = data[column].fillna(data[column].mode()[0])  # Filling with mode for categorical data
    elif data[column].dtype in ["int64", "float64"]:
        # Handle numerical columns
        if args.missing_strategy == "remove":
            data[column] = data[column].dropna()
        elif args.missing_strategy == "mean":
            data[column] = data[column].fillna(data[column].mean())
        elif args.missing_strategy == "median":
            data[column] = data[column].fillna(data[column].median())

        if args.scaling == "minmax":
            data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
        elif args.scaling == "standard":
            data[column] = (data[column] - data[column].mean()) / data[column].std()

#======================================================================================================================================================

#======================================================================================================================================================

def visualizations(data):
    # Visualization
    print('Displaying graphics-------------------')
    if args.visualize:
        # Generate visualizations for each column
        for column in data.columns:
            if data[column].dtype == "object":
                plt.figure(figsize=(15, 10))
                sns.countplot(data=data, x=column)
                plt.title(f"Countplot of {column}")
                plt.xticks(rotation=45)
                plt.show()
            elif data[column].dtype in ["int64", "float64"]:
                plt.figure(figsize=(15, 10))
                sns.histplot(data[column], kde=True)
                plt.title(f"Histogram of {column}")
                plt.show()
                # fig = px.box(data, y=column, title=f"Box Plot of {column}")
                plt.show()

    

#############################################################################################################################################


def main(data_source):
    df =  load_data(args.data_source)

    # Call the explore_data function
    explore_data(df)

    preprocess_data(df)
    print('*' * 100)
    print('preprocessing is done :)')
        # Number and percentage of null values in each column
        
    print("\nMissing Values:")
    print(df.isnull().sum())
    print('*' * 100)

    visualizations(df)

    print('*******************************************END**************************************************')
    print('Thank you for use my tool')

if __name__ == '__main__':
#---------------------Get data from the user----------------------------------------------------------------------------------

    parser = argparse.ArgumentParser(description='Automated EDA Tool')
    parser.add_argument('data_source', type=str, help='Path to data source (CSV, Excel, or SQL connection)')
    parser.add_argument("--missing_strategy", choices=["remove", "mean", "median"], default="mean", help="Missing value strategy")
    parser.add_argument("--scaling", choices=["minmax", "standard"], default="minmax", help="Feature scaling strategy")
    parser.add_argument("--visualize", action="store_true", help="Generate visualizations")
    args = parser.parse_args()
    print(args.data_source)
    main(args.data_source)

#------------------------------------------------------------------------------------------------------------------------------
    
    
