# 🧠 DLMDSPWP01 – Programming with Python  
### Advanced Data Processing & Visualization Project

---

## 📘 Overview

This project is part of the **IU Internationale Hochschule** module  
**DLMDSPWP01 – Programming with Python**.

It demonstrates **Object-Oriented Programming (OOP)** principles in Python applied to a real-world data analysis pipeline using:
- 🧮 **Pandas** & **NumPy** for data manipulation  
- 📊 **Matplotlib** & **Seaborn** for visualizations  
- 💾 **SQLite** & **SQLAlchemy** for database operations  

The program:
1. Loads and normalizes **training**, **ideal**, and **test** datasets  
2. Finds the **best-fit ideal functions** for each training function  
3. Classifies **test data** points based on deviation criteria  
4. Generates **10 types of plots** for visualization  
5. Saves all processed results into an **SQLite database**

---

## 🏗️ Project Structure

DLMDSPWP01_PythonProject/
│
├── data/
│ ├── train.csv
│ ├── ideal.csv
│ └── test.csv
│
├── src/
│ ├── base_processor.py # Base class for loading, normalizing, and DB operations
│ ├── derived_processor.py # Derived class for analysis, classification, visualization
│
├── database.db # SQLite database created by the program
├── main.py # Entry point for the full data processing pipeline
├── requirements.txt # Python dependencies
└── README.md # Project documentation (this file)

yaml
Copy code

---

## ⚙️ Installation & Setup Guide

### 🧩 1. Clone the Repository
Open your terminal or PowerShell, navigate to your desired directory, and run:
```bash
git clone https://github.com/yourusername/DLMDSPWP01_PythonProject.git
cd DLMDSPWP01_PythonProject
🔹 (If you haven’t installed Git yet, download it from git-scm.com)

🧮 2. Create a Virtual Environment (Recommended)
Creating a virtual environment keeps your dependencies isolated from system Python.

🪟 On Windows:
bash
Copy code
python -m venv venv
venv\Scripts\activate
🍎 On macOS / 🐧 Linux:
bash
Copy code
python3 -m venv venv
source venv/bin/activate
📦 3. Install Required Packages
Once the virtual environment is activated:

bash
Copy code
pip install -r requirements.txt
If you don’t have a requirements.txt yet, create one with:

nginx
Copy code
pandas
numpy
matplotlib
seaborn
sqlalchemy
📂 4. Add Your Data Files
Make sure your train, ideal, and test CSV files are placed inside the /data folder:

kotlin
Copy code
data/
├── train.csv
├── ideal.csv
└── test.csv
All files must contain:

a common X-column

one or more Y-columns (Y1, Y2, Y3, ...)

▶️ Running the Program
Once everything is set up, simply run:

bash
Copy code
python main.py
✅ The program will:

Load and normalize the datasets

Find best-fit ideal functions

Classify test data points

Generate and display plots

Save results into database.db

📊 Output Example
X	Y (test)	No. of ideal func	ΔY (test func)
1.23	2.45	Y12	0.067
2.13	1.09	Unassigned	0.532
...	...	...	...

📈 Visualizations
The script generates 10 types of plots:

Line Plot – Train vs Ideal

Scatter Plot – Test vs Ideal

Residual Plot

Histogram

Boxplot

Bar Plot

Violin Plot

Area Plot

Combined Overlay Plot

Correlation Heatmap

All plots are shown interactively using Matplotlib and Seaborn.

🗃️ Database Output
The processed data is stored in database.db (SQLite) with these tables:

Table Name	Description
train_data	Normalized training data
ideal_data	Ideal function reference data
test_data	Test data used for classification
result	Final output with classifications & deviations

You can view it using any SQLite browser (e.g., DB Browser for SQLite).

🧮 Classification Logic
For each test point:

Calculate deviation from every ideal function.

Select the minimum deviation.

deviation≤(max_train_deviation×√2)
assign that ideal function; otherwise mark as “Unassigned”.

🧠 Learning Outcomes
This project demonstrates:

✅ Class inheritance and modular code design (OOP)

✅ Data normalization and transformation techniques

✅ Database persistence with SQLAlchemy + SQLite

✅ Advanced visualization using Matplotlib & Seaborn

✅ Real-world data pipeline implementation in Python

🧩 Troubleshooting
Issue	Cause	Solution
ModuleNotFoundError	Missing package	Run pip install -r requirements.txt
TypeError: cannot unpack NoneType	classify_test_data() not returning correctly	Ensure it returns labels, deviations
ValueError: Length mismatch	DataFrame size vs result list mismatch	Check that CSVs have same number of X-values
Plots not showing	Non-interactive terminal	Run inside VSCode, Jupyter, or enable %matplotlib inline

👨‍💻 Author Information
Name: Haroon Nissar Haroon Nissar
Course: DLMDSPWP01 – Programming with Python
University: IU Internationale Hochschule
Year: 2025
Language: Python 3.13#
