import pandas as pd
import numpy as np
from sqlalchemy import create_engine, inspect

class DataProcessorBase:
    """Handles loading, saving, and preprocessing of data."""
    def __init__(self, train_table, ideal_table, test_table, database_url):
        self.engine = create_engine(database_url)
        self.train_table = train_table
        self.ideal_table = ideal_table
        self.test_table = test_table
        self.database_url = database_url

        # Load CSVs → SQL → DataFrames
        for file, table in zip(["train.csv", "ideal.csv", "test.csv"],
                               [train_table, ideal_table, test_table]):
            self.load_csv_to_sql(file, table)

        self.train_data = self.load_data_from_sql(train_table)
        self.ideal_data = self.load_data_from_sql(ideal_table)
        self.test_data = self.load_data_from_sql(test_table)

    def load_csv_to_sql(self, csv_file, table_name):
        df = pd.read_csv(f"data/{csv_file}")
        df.to_sql(table_name, self.engine, index=False, if_exists="replace")

    def load_data_from_sql(self, table_name):
        inspector = inspect(self.engine)
        if table_name not in inspector.get_table_names():
            raise ValueError(f"Table '{table_name}' not found.")
        with self.engine.connect() as conn:
            return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    def preprocess_data(self, df):
        df = df.dropna()
        return (df - df.mean()) / df.std()

    def calculate_squared_errors(self, col1, col2):
        if len(col1) != len(col2):
            raise ValueError("Columns must have same length.")
        return np.sum((np.array(col1) - np.array(col2))**2)

    def find_best_fit_columns(self, normalized_train, normalized_ideal):
        best_fit = []
        for i in range(1, len(normalized_train.columns)):
            train_col = normalized_train.iloc[:, i]
            errors = [
                self.calculate_squared_errors(train_col, normalized_ideal.iloc[:, j])
                for j in range(1, len(normalized_ideal.columns))
            ]
            best_fit.append(np.argmin(errors) + 1)
        return best_fit

    def calculate_min_distance(self, array_a, value_b):
        return np.min(np.abs(array_a - value_b))
