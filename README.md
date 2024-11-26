# submission-dicoding-data-analysis

## Description
This is a submission project on the "Belajar Analisis Data dengan Python" course at dicoding.com.

## Project Structure
- `dashboard/`: This directory contains dashboard.py and CSV file which is used to create dashboards on Streamlit for data analysis results.
- `data/`: Directory containing the raw CSV data files.
- `notebook.ipynb`: This file contains the full code for analyzing the e-commerce public dataset, which starts with data wrangling, EDA, visualization & Explanatory, and conclusion.
- `requirements.txt`: This file contains library that needs to run this project.
- `readme.md`: This documentation file.

## Installation
1. Clone this repo to your local machine:
   ```
   git clone https://github.com/RozyRangkuti/submission-dicoding-data-analysis.git
   ```
2. Go to the project directory:
   ```
   cd submission-dicoding-data-analysis
   ```
3. Install the required Python packages by running:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Data Wrangling: The notebook.ipynb file includes scripts designed to prepare and clean the data.

2. Exploratory Data Analysis (EDA): Analyze and explore the data using the available Python scripts. Insights from EDA can help you better understand patterns in e-commerce public data.

3. Visualization: Run the Streamlit dashboard to interactively explore the data.
   ```
   cd submission-dicoding-data-analysis
   streamlit run dashboard.py
   ```
Access the dashboard in your web browser at `https://e-commerce-submission-analysis.streamlit.app/`.
