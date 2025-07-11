# import all necessary libraries here
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# 1. Impute Missing Values
def impute_missing_values(data, strategy='mean'):
    """
    Fill missing values in the dataset.
    :param data: pandas DataFrame
    :param strategy: str, imputation method ('mean', 'median', 'mode')
    :return: pandas DataFrame
    """
     # TODO: Fill missing values based on the specified strategy
   
    #pass
    data_copy = data.copy()  # Avoid modifying the original DataFrame
    missing_values_before = data_copy.isnull().sum().sum()  # Count total missing values (first sum(): columns, second sum(): dataframe total)
    print("Before imputation, missing values in the dataset:" , missing_values_before) #check total missing values before
    
    for col in data_copy.columns:
        if data_copy[col].dtype == 'object':
            # Fill categorical columns with mode
            data_copy[col]= data_copy[col].fillna(data_copy[col].mode()[0]) #(ChatGPT, 2025)-used for categorical columns code structure
        else:
            # Fill numerical columns with mean or median
            if strategy == 'median':
                data_copy[col] = data_copy[col].fillna(data_copy[col].median())
            elif strategy == 'mode':
                data_copy[col]= data_copy[col].fillna(data_copy[col].mode()[0])
            elif strategy == 'mean':
                # Default to mean
                data_copy[col] = data_copy[col].fillna(data_copy[col].mean())
            else:
                raise ValueError("Invalid strategy. Use 'mean', 'median', or 'mode'.")
    missing_values_after = data_copy.isnull().sum().sum()  # Count total missing values after imputation
    print("After imputation, missing values in the dataset:" , missing_values_after) #check total missing values after
    return data_copy

# 2. Remove Duplicates
def remove_duplicates(data):
    """
    Remove duplicate rows from the dataset.
    :param data: pandas DataFrame
    :return: pandas DataFrame
    """
    data_copy = data.copy()  # Avoid modifying the original DataFrame
    duplicate_values_before = data_copy.duplicated().sum()  # Count total duplicate rows before
    print("Before removing duplicates, duplicate rows in the dataset:" , duplicate_values_before) #check total duplicate rows before
    print("Before removing duplicates, number of rows and columns in the dataset:", data_copy.shape) #check shape of the dataset before removing duplicates
   
    for col in data_copy.columns: 
        if data_copy[col].dtype == 'object':
            # Convert categorical columns to string type
            data_copy[col] = data_copy[col].astype(str)
            
    # Remove duplicate rows
    data_copy = data_copy.drop_duplicates()
    duplicate_values_after = data_copy.duplicated().sum()  # Count total duplicate rows after
    print("After removing duplicates, duplicate rows in the dataset:" , duplicate_values_after) #check total duplicate rows after
    print("After removing duplicates, number of rows and columns in the dataset:", data_copy.shape) #check shape of the dataset after removing duplicates
    return data_copy
    
   
    # pass
    

# 3. Normalize Numerical Data
def normalize_data(data,method='minmax'):
    """Apply normalization to numerical features.
    :param data: pandas DataFrame
    :param method: str, normalization method ('minmax' (default) or 'standard')
    """
     # TODO: Normalize numerical data using Min-Max or Standard scaling
     #I used AI to help me understand the concepts and code structure (OpenAI, 2025)
     
    data_copy = data.copy()      # Avoid modifying the original DataFrame
    numerical_cols = data_copy.select_dtypes(include=['number']).columns
    
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError("Invalid method. Use 'minmax' or 'standard'.")
    #apply the scaler to the numerical columns
    data_copy[numerical_cols]= scaler.fit_transform(data_copy[numerical_cols])
    
    return data_copy

   
    # pass

# 4. Remove Redundant Features   
def remove_redundant_features(data, threshold=0.9):
    """Remove redundant or duplicate columns.
    :param data: pandas DataFrame
    :param threshold: float, correlation threshold
    :return: pandas DataFrame
    """
     # TODO: Remove redundant features based on the correlation threshold (HINT: you can use the corr() method)
    #I used Google  AI Overview (Google, 2025) to understand the concept and code structure
    
    data_copy = data.copy()  # Avoid modifying the original DataFrame
    print("Before removing redundant features:", data_copy.shape)
    
    #select numerical columns
    numerical_data = data_copy.select_dtypes(include=['number']) 
    
    # Calculate correlation matrix
    corr_matrix = numerical_data.corr().abs() #(Google, 2025)

     # Identify highly correlated features
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)) #(Google, 2025)
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]

     # Remove highly correlated features
    data_copy_filtered = data_copy.drop(to_drop, axis=1)
    
    print("After removing redundant features:", data_copy_filtered.shape)
    print("At threshold = ", threshold, "Removed repundant features:", to_drop)
    
    return data_copy_filtered


   
    # pass

# ---------------------------------------------------

def simple_model(input_data, split_data=True, scale_data=False, print_report=False):
    """
    A simple logistic regression model for target classification.
    Parameters:
    input_data (pd.DataFrame): The input data containing features and the target variable 'target' (assume 'target' is the first column).
    split_data (bool): Whether to split the data into training and testing sets. Default is True.
    scale_data (bool): Whether to scale the features using StandardScaler. Default is False.
    print_report (bool): Whether to print the classification report. Default is False.
    Returns:
    None
    The function performs the following steps:
    1. Removes columns with missing data.
    2. Splits the input data into features and target.
    3. Encodes categorical features using one-hot encoding.
    4. Splits the data into training and testing sets (if split_data is True).
    5. Scales the features using StandardScaler (if scale_data is True).
    6. Instantiates and fits a logistic regression model.
    7. Makes predictions on the test set.
    8. Evaluates the model using accuracy score and classification report.
    9. Prints the accuracy and classification report (if print_report is True).
    """

    # if there's any missing data, remove the columns
    input_data.dropna(inplace=True)

    # split the data into features and target
    target = input_data.copy()[input_data.columns[0]] # y = first column as the label (target variable)
    
    features = input_data.copy()[input_data.columns[1:]] #x = rest of the columns as input features

    # if the column is not numeric, encode it (one-hot)
    for col in features.columns:
        if features[col].dtype == 'object':
            features = pd.concat([features, pd.get_dummies(features[col], prefix=col)], axis=1)
            features.drop(col, axis=1, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, stratify=target, random_state=42)

    if scale_data:
        # scale the data
        X_train = normalize_data(X_train)
        X_test = normalize_data(X_test)
        
    # instantiate and fit the model
    log_reg = LogisticRegression(random_state=42, max_iter=100, solver='liblinear', penalty='l2', C=1.0)
    log_reg.fit(X_train, y_train)

    # make predictions and evaluate the model
    y_pred = log_reg.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f'Accuracy: {accuracy}')
    
    # if specified, print the classification report
    if print_report:
        print('Classification Report:')
        print(report)
        print('Read more about the classification report: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html and https://www.nb-data.com/p/breaking-down-the-classification')
    
    return None