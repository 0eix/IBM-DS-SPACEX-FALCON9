# 🚀 SpaceX Falcon 9 First Stage Landing Prediction – Predictive Modeling (Machine Learning)

## 📋 Project Background and Context

SpaceX aims to reduce launch costs by reusing the first-stage boosters of its Falcon 9 rockets.
Achieving reliable booster landings is essential to the company’s cost-saving strategy.
This project analyzes launch data to predict landing success and identify key factors influencing outcomes.

## Questions to answer

What are the most important factors determining Falcon 9 first-stage landing success?
Can we accurately predict landing outcomes using features like payload mass, orbit type, or launch site?
How can machine learning and interactive visual analytics improve insight into SpaceX’s operational performance?

## 🎯 Project Objective

The goal of this project is to **predict whether the first stage of the Falcon 9 rocket will successfully land**, based on technical launch data. This prediction helps assess the **economic viability** of the mission, as rocket reusability significantly reduces launch costs.

## Methodology

Data collection :

- Retrieved launch data via SpaceX API
- Completed missing fields through web scraping (Wikipedia)

Data wrangling :

- Cleaned and processed data to handle missing values and standardize formats.
- Merged datasets from different sources to create a unified data frame for analysis.

Exploratory Data Analysis (EDA):

- Explored trends using Seaborn and Matplotlib
- Queried structured data using SQL for deeper insights

Interactive Visual Analytics:

- Built interactive maps with Folium to visualize landing locations
- Created dynamic dashboards with Plotly Dash

Predictive analysis using classification models :

- Trained and evaluated Logistic Regression, SVM, Decision Tree, and KNN.
- Tuned models using GridSearchCV with cross-validation.


## 📊 Data Sources

The dataset was assembled from multiple sources:
- Official APIs (SpaceX, Launch Library)
- Web scraping (Wikipedia)
- The data was cleaned and structured during the initial steps of the project.

## 🧪 Modeling Pipeline

- **Data Preparation**: Standardization, creation of target variable (`Class`), train-test split
- **Model selection and tuning**:
  - Logistic Regression
  - Decision Tree
  - K-Nearest Neighbors (KNN)
  - Support Vector Machines (SVM)
- **Hyperparameter Optimization**:
  - Performed using `GridSearchCV` with 10-fold cross-validation
- **Performance Evaluation**:
  - Test set accuracy
  - Confusion matrix analysis
  - Interpretation of false positives and false negatives

## 📈 Key Metrics

- **Accuracy**
- **Best Parameters** (`best_params_`)
- **Confusion Matrices** for each model

## 🧠 Results

- The **logistic regression model** demonstrated strong generalization performance with few false positives.
- **Feature selection** helped identify the most influential variables for landing success (e.g., mission type, rocket type, launch site).
