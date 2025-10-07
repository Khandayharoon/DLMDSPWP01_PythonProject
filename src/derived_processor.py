import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .base_processor import DataProcessorBase


class DerivedDataProcessor(DataProcessorBase):
    """
    Derived class to classify test data against best-fit ideal functions
    and generate multiple visualizations.
    """

    def __init__(self, train_table, ideal_table, test_table, database_url):
        super().__init__(train_table, ideal_table, test_table, database_url)
        self.normalized_train_data = None
        self.normalized_ideal_data = None
        self.normalized_test_data = None
        self.best_fit_indices = None

    # ======================================================================
    # CLASSIFY TEST DATA
    # ======================================================================
    def classify_test_data(self):
        """
        Classify each test row to closest ideal function,
        only if deviation <= max training deviation * sqrt(2).
        Works with any number of Y-columns in test data.
        """
        labels, deviations = [], []
        test_y_columns = self.normalized_test_data.columns[1:]

        for _, test_row in self.normalized_test_data.iterrows():
            min_dists = []

            num_columns = min(len(test_y_columns), len(self.best_fit_indices))
            for i in range(num_columns):
                ideal_idx = self.best_fit_indices[i]
                ideal_col = self.normalized_ideal_data.iloc[:, ideal_idx]

                test_val = test_row[test_y_columns[i]]
                dist = self.calculate_min_distance(ideal_col, test_val)
                min_dists.append(dist)

            if min_dists:
                min_distance = min(min_dists)
                best_idx = np.argmin(min_dists)

                # compute allowed max deviation for that Y-column
                train_dev = np.max(np.abs(
                    self.normalized_train_data.iloc[:, best_idx + 1]
                    - self.normalized_ideal_data.iloc[:, self.best_fit_indices[best_idx]]
                ))

                if min_distance <= train_dev * np.sqrt(2):
                    labels.append(f"Y{self.best_fit_indices[best_idx]}")
                    deviations.append(round(min_distance, 3))
                else:
                    labels.append("Unassigned")
                    deviations.append(round(min_distance, 3))
            else:
                labels.append("Unassigned")
                deviations.append(None)

        return labels, deviations

    # ======================================================================
    # PLOTS & VISUALIZATIONS
    # ======================================================================
    def plot_all_visualizations(self, x_axis_range):
        """
        Generate multiple types of plots:
        line, scatter, residuals, histogram, boxplot, overlay, area, bar,
        violin, and heatmap.
        """
        num_cols = len(self.best_fit_indices)

        # Line plots
        for i in range(num_cols):
            plt.figure(figsize=(8, 5))
            plt.plot(
                x_axis_range,
                self.normalized_ideal_data.iloc[:, self.best_fit_indices[i]],
                "b-o",
                label="Ideal",
            )
            plt.plot(
                x_axis_range,
                self.normalized_train_data.iloc[:, i + 1],
                "r--",
                label="Train",
            )
            plt.title(f"Line Plot: Train Y{i+1} vs Ideal Y{self.best_fit_indices[i]}")
            plt.xlabel("X")
            plt.ylabel("Normalized Value")
            plt.legend()
            plt.grid(True)
            plt.show()

        # Scatter plots
        for i in range(num_cols):
            plt.figure(figsize=(6, 6))
            plt.scatter(
                self.normalized_ideal_data.iloc[:, self.best_fit_indices[i]],
                self.normalized_train_data.iloc[:, i + 1],
                alpha=0.7,
            )
            plt.plot([-3, 3], [-3, 3], "r--")
            plt.title(f"Scatter Plot: Train Y{i+1} vs Ideal Y{self.best_fit_indices[i]}")
            plt.xlabel("Ideal")
            plt.ylabel("Train")
            plt.grid(True)
            plt.show()

        # Residual plots
        for i in range(num_cols):
            residuals = (
                self.normalized_train_data.iloc[:, i + 1]
                - self.normalized_ideal_data.iloc[:, self.best_fit_indices[i]]
            )
            plt.figure(figsize=(8, 5))
            plt.stem(x_axis_range, residuals)
            plt.title(f"Residuals: Train Y{i+1} - Ideal Y{self.best_fit_indices[i]}")
            plt.xlabel("X")
            plt.ylabel("Residual")
            plt.grid(True)
            plt.show()

        # Histogram of deviations
        all_devs = []
        for i in range(num_cols):
            all_devs.extend(
                (
                    self.normalized_train_data.iloc[:, i + 1]
                    - self.normalized_ideal_data.iloc[:, self.best_fit_indices[i]]
                ).values
            )
        plt.figure(figsize=(8, 5))
        plt.hist(all_devs, bins=10, color="skyblue", edgecolor="black")
        plt.title("Histogram of Deviations")
        plt.xlabel("Deviation")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()

        # Boxplot
        plt.figure(figsize=(10, 6))
        combined_data = pd.DataFrame()
        for i in range(num_cols):
            combined_data[f"Train_Y{i+1}"] = self.normalized_train_data.iloc[:, i + 1]
            combined_data[f"Ideal_Y{self.best_fit_indices[i]}"] = self.normalized_ideal_data.iloc[
                :, self.best_fit_indices[i]
            ]
        combined_data.boxplot()
        plt.title("Boxplot: Train vs Ideal")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

        # Combined overlay
        plt.figure(figsize=(10, 6))
        for i in range(num_cols):
            plt.plot(
                x_axis_range,
                self.normalized_train_data.iloc[:, i + 1],
                "--",
                label=f"Train Y{i+1}",
            )
            plt.plot(
                x_axis_range,
                self.normalized_ideal_data.iloc[:, self.best_fit_indices[i]],
                "-o",
                label=f"Ideal Y{self.best_fit_indices[i]}",
            )
        plt.title("Combined Overlay")
        plt.xlabel("X")
        plt.ylabel("Normalized Value")
        plt.legend()
        plt.grid(True)
        plt.show()

        # Area plot
        plt.figure(figsize=(10, 6))
        for i in range(num_cols):
            plt.fill_between(
                x_axis_range,
                self.normalized_train_data.iloc[:, i + 1],
                alpha=0.3,
                label=f"Train Y{i+1}",
            )
            plt.fill_between(
                x_axis_range,
                self.normalized_ideal_data.iloc[:, self.best_fit_indices[i]],
                alpha=0.2,
                label=f"Ideal Y{self.best_fit_indices[i]}",
            )
        plt.title("Area Plot")
        plt.legend()
        plt.grid(True)
        plt.show()

        # Bar plot (mean values)
        means = pd.DataFrame(
            {
                "Train": self.normalized_train_data.iloc[:, 1 : num_cols + 1].mean(),
                "Ideal": self.normalized_ideal_data.iloc[:, self.best_fit_indices].mean(),
            }
        )
        means.plot(kind="bar", figsize=(10, 6))
        plt.title("Bar Plot of Mean Values")
        plt.show()

        # Violin plot
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=combined_data)
        plt.title("Violin Plot: Train vs Ideal")
        plt.xticks(rotation=45)
        plt.show()

        # Heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(combined_data.corr(), annot=True, cmap="coolwarm")
        plt.title("Heatmap of Correlations")
        plt.show()

    # ======================================================================
    # MAIN PIPELINE
    # ======================================================================
    def main(self):
        """Full workflow: normalization, best-fit selection, visualization, test classification."""
        # Normalize
        self.normalized_train_data = self.preprocess_data(self.train_data)
        self.normalized_ideal_data = self.preprocess_data(self.ideal_data)
        self.normalized_test_data = self.preprocess_data(self.test_data)

        # Find best fits
        self.best_fit_indices = self.find_best_fit_columns(
            self.normalized_train_data, self.normalized_ideal_data
        )

        # Visualize
        x_axis_range = range(len(self.normalized_train_data))
        self.plot_all_visualizations(x_axis_range)

        # Classify test data
        labels, deviations = self.classify_test_data()

        # Combine with original test data
        final_test_data = self.test_data.copy()
        final_test_data["No. of ideal func"] = labels
        final_test_data["Delta Y (test func)"] = deviations

        return final_test_data
