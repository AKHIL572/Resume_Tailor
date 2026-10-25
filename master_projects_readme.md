# Project Portfolio

---

# Project 1

## 1. Title

**House Price Analysis & Prediction System (Power BI Dashboard + Machine Learning + Streamlit App)**

## 2. Project Status

**Complete**

## 3. Project Type

- Data Analytics Project
- Machine Learning Project
- Business Intelligence Dashboard
- End-to-End Data Science Project
- Web Application Deployment

## 4. Project Overview

This project focuses on analyzing and predicting house prices using the King County Housing Dataset.

The project combines:
- Exploratory Data Analysis (EDA) for understanding housing market trends
- Machine Learning models for house price prediction
- Power BI dashboard for business insights visualization
- Streamlit web application for interactive user predictions

The system helps users estimate house prices based on property characteristics such as Living area, House grade, Bedrooms, Bathrooms, Location, Renovation status, Nearby neighborhood features.

## 5. Problem Discussed / Solved

### Problem Statement

House prices are influenced by multiple factors including property size, quality, location, and neighborhood conditions.

The goal of this project was to:
- Analyze housing market patterns
- Identify the most important factors affecting house prices
- Build a machine learning model capable of accurately predicting house prices
- Create interactive dashboards and applications for user-friendly analysis

## 6. Dataset Details

| Field | Details |
|--------|---------|
| **Dataset Name** | King County House Sales Dataset |
| **Dataset Type** | Real-world Housing Dataset |
| **Dataset Source** | Kaggle / Public Housing Dataset |
| **Raw Dataset Columns** | id, date, price, bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition, grade, sqft_above, sqft_basement, yr_built, yr_renovated, zipcode, lat, long, sqft_living15, sqft_lot15 |
| **Engineered Features Added** | sale_year, sale_month, total_sqft, basement_ratio, house_age, renovated, years_since_renovation, price_log |

## 7. File Structure

```text
HOUSE-PRICE-PREDICTION-PROJECT
│
├── dataset/
│   ├── kc_house_data.csv
│   └── cleaned_dataset.csv
├── notebooks/
│   ├── 1_data_cleaning_feature_engineering.ipynb
│   ├── 2_exploratory_data_analysis.ipynb
│   └── 3_preprocessing_modeling.ipynb
├── src/
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── train.py
│   └── predict.py
├── models/
│   ├── house_price_pipeline.pkl
│   ├── scaler.pkl
│   └── columns.pkl
├── Results/
│   ├── feature_importance.png
│   ├── residual_plot.png
│   ├── actual_vs_predicted.png
│   └── model_comparison.png
├── dashboard/
│   └── powerbi_dashboard.pbix
├── app.py
├── test_prediction.py
├── requirements.txt
└── README.md
```

## 8. Tools & Technologies Used

### Programming & Analysis
- Python
- Pandas
- NumPy

### Visualization
- Matplotlib
- Seaborn
- Power BI

### Machine Learning
- Scikit-learn

### Models Used
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor

### Deployment & App
- Streamlit

### Version Control
- Git
- GitHub

## 9. Steps Used / Main Work Done

### Step 1 — Data Loading
- Loaded raw housing dataset
- Inspected columns and dataset structure

### Step 2 — Data Cleaning
- Removed unnecessary columns
- Handled missing values
- Fixed inconsistent data types

### Step 3 — Feature Engineering
Created new features such as:
- House Age
- Basement Ratio
- Total Square Footage
- Renovation Status
- Years Since Renovation
- Log-transformed Price

### Step 4 — Exploratory Data Analysis (EDA)
Performed:
- Univariate Analysis
- Bivariate Analysis
- Multivariate Analysis
- Correlation Analysis
- Outlier Analysis
- Geographic Analysis using Latitude & Longitude

Created visualizations including:
- Histograms
- Boxplots
- Scatter plots
- Heatmaps
- Pairplots
- Correlation matrices

### Step 5 — Data Preprocessing
- Train-test split
- Feature scaling
- Zipcode encoding using one-hot encoding

### Step 6 — Model Training
Trained multiple ML models:
- Linear Regression
- Decision Tree
- Random Forest
- Gradient Boosting

### Step 7 — Model Evaluation
Evaluated using:
- RMSE
- MAE
- R² Score
- Cross-validation

### Step 8 — Hyperparameter Tuning
Used RandomizedSearchCV to improve:
- Random Forest
- Gradient Boosting

### Step 9 — Final Model Selection
Selected the best-performing model based on:
- Lowest RMSE
- Highest R² Score

**Final Model:** Gradient Boosting Regressor

### Step 10 — Model Saving
Saved:
- Trained pipeline
- Feature columns
- Scaler

Using:
- Joblib
- Pickle

### Step 11 — Streamlit Application
Built an interactive web app where users can:
- Enter house details
- Predict house prices
- View house location on a map
- See prediction ranges
- Understand feature importance

### Step 12 — Power BI Dashboard
Created an interactive dashboard for housing market analysis.

## 10. Methodology (Workflow Used)

```text
Data Collection
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Exploratory Data Analysis
      ↓
Preprocessing
      ↓
Model Training
      ↓
Hyperparameter Tuning
      ↓
Evaluation
      ↓
Deployment
```

## 11. Model Building & Performance Evaluation

### a. Baseline Model Performance (Using `price_log` Target)

To identify the most suitable regression algorithm for house price prediction, multiple machine learning models were trained and evaluated using the log-transformed target variable (`price_log`).

#### Baseline Results

| Model | MAE | RMSE | R² Score | 5-Fold CV R² |
|---------------------------|------|------|--------|------------|
| Random Forest Regressor | 0.1230 | 0.1736 | 0.8912 | 0.8847 |
| Gradient Boosting Regressor | 0.1344 | 0.1817 | 0.8807 | 0.8809 |
| Linear Regression | 0.1345 | 0.1843 | 0.8773 | 0.8785 |
| Decision Tree Regressor | 0.1765 | 0.2436 | 0.7857 | 0.7627 |

#### Key Observations
- **Random Forest Regressor** achieved the lowest RMSE and highest baseline R² score.
- **Gradient Boosting Regressor** showed competitive performance and strong cross-validation consistency.
- **Linear Regression** performed reasonably well but could not capture complex nonlinear relationships.
- **Decision Tree Regressor** showed signs of overfitting and delivered the weakest performance.

### b. Hyperparameter Tuning

To further improve prediction accuracy, hyperparameter optimization was performed using RandomizedSearchCV on the top-performing baseline models:
- Random Forest Regressor
- Gradient Boosting Regressor

#### Tuned Model Results

| Model | MAE | RMSE | R² Score |
|-----------------------------------|------|------|--------|
| Gradient Boosting Regressor (Tuned) | 0.1145 | 0.1596 | 0.9080 |
| Random Forest Regressor (Tuned) | 0.1270 | 0.1784 | 0.8851 |

#### Tuning Outcome
The Tuned Gradient Boosting Regressor significantly improved performance.
It achieved the lowest error values and the highest R² score among all tested models.
Tuned Random Forest did not outperform its baseline version.

### c. Best Model Selection

**Final Selected Model:** Gradient Boosting Regressor (Tuned)

#### Best Hyperparameters

```python
{
 'subsample': 0.8,
 'n_estimators': 300,
 'max_depth': 5,
 'learning_rate': 0.1
}
```

#### Why This Model Was Selected?
- Highest prediction accuracy.
- Lowest RMSE and MAE.
- Best ability to capture nonlinear relationships in housing data.
- Strong generalization performance on unseen data.

### d. Final Performance on Actual House Prices

Since the target variable was log-transformed during training, predictions were converted back to actual house prices using:

```python
np.expm1(predictions)
```

#### Final Evaluation Metrics

| Metric | Value |
|------------------------------|-----------|
| Mean Absolute Error (MAE) | $61,613.97 |
| Root Mean Squared Error (RMSE) | $105,889.17 |
| R² Score | 0.9103 |

#### Interpretation
On average, the model's predictions differ from the actual house prices by approximately **$61,614**.
The model explains **91.03% of the variation** in housing prices.
The low prediction error and high R² score indicate that the model is highly effective for estimating house prices.

## 12. Key Insights & Results

### Key Insights
- Living area strongly influences house price
- Higher house grades significantly increase price
- Waterfront properties are generally more expensive
- Renovated houses show higher average prices
- Geographic location plays a major role in pricing

### Final Model Performance

**Gradient Boosting Regressor**

| Metric | Score |
|----------|-------|
| RMSE | ~0.16 |
| R² Score | ~0.91 |

The model achieved strong prediction performance on unseen data.

## 13. Dashboard Details

### KPI Cards
- total houses
- average price
- max price
- median price

### Filters
- zipcode
- sale year
- bedrooms

### Charts
a. distribution of house price
b. geographical distribution of house price
c. average price by number of bedrooms
d. living area vs house price
e. average price by house grade
f. average price by renovation
g. house age vs price

## 14. Deployment & Links

**GitHub Repository:** https://github.com/AKHIL572/house-price-prediction

## 15. Complexity Level

**Intermediate to Advanced Level Project**

## 16. Why the Complexity Level?

Because the project includes:
- End-to-end machine learning workflow
- Feature engineering
- Multiple model comparison
- Hyperparameter tuning
- Interactive Streamlit deployment
- Power BI dashboard creation
- Real-world business analysis

## 17. Additional Things Included in the Project

### Model Interpretability
- Feature importance analysis

### Geographic Analysis
- Latitude & Longitude mapping

### Residual Analysis
- Residual plots for error checking

### Prediction Uncertainty
- Estimated prediction ranges shown in Streamlit app

### User-Friendly Deployment
- Interactive prediction system for non-technical users

## 18. Skills Demonstrated

### Technical Skills
- Data Cleaning
- Feature Engineering
- Exploratory Data Analysis
- Machine Learning
- Model Evaluation
- Hyperparameter Tuning
- Data Visualization
- Dashboard Development
- Web App Deployment

## 19. Data Pipeline / Workflow Note

> This project follows a standard ML data pipeline: raw data ingestion → data cleaning → feature engineering → EDA → preprocessing (train/test split, scaling, encoding) → model training (Linear Regression, Decision Tree, Random Forest, Gradient Boosting) → hyperparameter tuning → evaluation → model persistence (Joblib/Pickle) → deployment. Automation/deployment is handled via a **Streamlit app** (`app.py`) and modular **Python scripts** in `src/` (`data_loader.py`, `preprocessor.py`, `train.py`, `predict.py`).

---

# Project 2

## 1. Title

AI Job Market Intelligence & Smart Recommendation System

## 2. Project Status

Complete

## 3. Project Type

- Machine Learning Project
- Recommendation System
- NLP-Based Skill Matching System
- End-to-End Data Science Project
- Streamlit Web Application

## 4. Project Overview

Developed an end-to-end AI-powered job market intelligence system that predicts suitable salaries for users and recommends the most relevant jobs based on skills, experience, salary expectations, and preferred location.

The system combines:
- Salary Prediction using Machine Learning
- Skill-Based Job Recommendation Engine
- TF-IDF NLP Skill Similarity
- Explainable AI Recommendation Scores
- Interactive Streamlit Deployment

Users can enter their: Skills, Experience, Preferred city

Then system:
- Predicts expected salary
- Recommends top matching jobs
- Shows skill match %, salary match %, and experience match %
- Identifies missing skills to learn

## 5. Problem Discussed / Solved

### Problem Statement
Job seekers often struggle to:
- Identify suitable jobs based on their skills
- Understand expected salary ranges
- Know which skills are missing for better opportunities
- Find personalized job recommendations

Traditional job portals provide generic recommendations without intelligent matching or salary prediction.

### Solution Provided
Built an AI-driven hybrid recommendation system that:
- Predicts market salary using ML models
- Matches jobs using NLP-based skill similarity
- Considers salary compatibility
- Considers experience level
- Considers preferred city
- Provides explainable recommendations and skill gap analysis

## 6. Dataset Details

- **Dataset Name:** Naukri Job Listings Dataset
- **Source:** Collected from Naukri job postings dataset
- **Dataset Size:**
  - ~22,000+ raw job records
  - ~7,500 cleaned salary-disclosed records used for modeling
- **Main Features Used:** Job Title, Industry, Role, Salary, Experience, Location
- **Additional Engineered Datasets:** analytics_jobs.csv, naukri_dashboard_ready.csv, naukri_skills_mapping.csv
- **Target Variable:** salary_avg, Log-transformed salary (log_salary)

## 7. File Structure

```text
AI_Job_Market_Intelligence/
│
├── dataset/
│   ├── naukri_cleaned.csv
│   ├── analytics_jobs.csv
│   ├── X_train.pkl
│   ├── X_test.pkl
│   ├── y_train.pkl
│   ├── y_test.pkl
│   └── tfidf_vectorizer.pkl
├── models/
│   ├── salary_model.pkl
│   ├── scaler.pkl
│   ├── medians.pkl
│   └── tfidf_vectorizer.pkl
├── notebooks/
│   ├── 1_data_cleaning.ipynb
│   ├── 2_eda.ipynb
│   ├── 3_feature_engineering.ipynb
│   ├── 4_salary_prediction_model.ipynb
│   └── 5_job_recommendation_engine.ipynb
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 8. Tools & Technologies Used

- **Programming & Development:** Python, Jupyter Notebook
- **Data Processing:** Pandas, NumPy, Regex
- **Machine Learning:** Scikit-learn, XGBoost
- **NLP / Recommendation:** TF-IDF Vectorization, Cosine Similarity
- **Model Persistence:** Joblib
- **Visualization:** Matplotlib, Seaborn
- **Deployment & Version Control:** Git, GitHub, Streamlit Cloud

## 9. Steps Used / Main Work Done

**Step 1. Data Cleaning & Preprocessing**
- Removed duplicate job postings
- Cleaned salary formats
- Extracted salary ranges
- Standardized city names
- Processed missing values
- Cleaned skill text data

**Step 2. Exploratory Data Analysis (EDA)**
- Analyzed salary distributions
- Identified top industries and cities
- Studied experience vs salary relationship
- Analyzed skill frequency trends

**Step 3. Feature Engineering**
- Created: Experience buckets, Interaction features, Industry-role combinations, City grouping
- Applied: Log transformation on salary, TF-IDF vectorization on skills, One-hot encoding for categorical variables

**Step 4. Model Development**
- Trained and evaluated: Linear Regression, Random Forest Regressor, XGBoost Regressor
- Used: RMSE, MAE and R² Score for model evaluation

**Step 5. Hyperparameter Tuning**
- Applied: RandomizedSearchCV and Cross Validation to optimize XGBoost performance

**Step 6. Recommendation System**
- Built a hybrid recommendation engine using:
  - Skill similarity
  - Salary matching
  - Experience matching
  - City preference matching
- Used cosine similarity for NLP-based skill recommendations

**Step 7. Explainable AI Features**
- Displayed: Skill Match %, Salary Match %, Experience Match %, Missing skills to learn

**Step 8. Web Application Development**
- Built a fully interactive Streamlit application where users can: Enter skills, Select experience, Choose preferred city, Get salary prediction, Receive personalized job recommendations

## 10. Methodology (Machine Learning Workflow)

```text
Data Cleaning: Structured raw job data and handled missing values.
      ↓
Feature Engineering: Created meaningful numerical, categorical, and NLP-based features.
      ↓
Model Training: Trained multiple regression models.
      ↓
Hyperparameter Optimization: Improved model performance using RandomizedSearchCV.
      ↓
Recommendation System: Combined TF-IDF similarity, Salary compatibility, Experience score,
City preference into a weighted hybrid scoring model.
      ↓
Deployment: Integrated models into a production-ready Streamlit application.
```

## 11. Key Insights & Results

- **Best Performing Model:** XGBoost Regressor
- **Final Performance:**
  - Test R² Score: 0.67
  - RMSE: 0.396
  - Real Salary RMSE: ~₹270K
- **Major Insights:**
  - Skills strongly influence salary prediction
  - Experience has a non-linear salary relationship
  - City and industry significantly affect salary trends
  - NLP-based skill similarity improves recommendation relevance
- **Recommendation System Features:**
  - Personalized job recommendations
  - Explainable scoring system
  - Skill gap analysis
  - Real-time salary estimation

## 12. Dashboard Details

No dashboard is created.

**Reason:** The project was intentionally focused on Machine Learning, Recommendation System Design, NLP-Based Matching, and Deployment instead of business intelligence reporting.

## 13. Deployment / GitHub / Live App

- **GitHub Repository:** https://github.com/AKHIL572/AI-Job-Market-Intelligence-Smart-Recommender
- **Live Streamlit App:** https://ai-job-market-intelligence-smart-recommender-hnxcrubwj7pvreg3e.streamlit.app/

## 14. Complexity Level

Advanced Level Project

## 15. Why Advanced?

Because the project includes:
- End-to-end ML pipeline
- NLP-based recommendation engine
- Feature engineering
- Hyperparameter tuning
- Explainable AI
- Deployment
- Hybrid recommendation scoring
- Real-world noisy dataset handling

## 16. Additional Important Points

### Real-World Challenges Handled
- Incomplete salary disclosure
- Noisy skill text
- Imbalanced categories
- High-cardinality features
- Real-world unstructured job data

### Production-Level Features
- Model persistence using Joblib
- Cached loading for Streamlit optimization
- Modular workflow
- Reusable recommendation engine
- Scalable architecture

## 17. Data Pipeline / Workflow Note

> This project follows a standard ML data pipeline: data cleaning → feature engineering (including NLP/TF-IDF) → model training (Linear Regression, Random Forest, XGBoost) → hyperparameter tuning → hybrid recommendation scoring → deployment. Automation/deployment is handled via a **Streamlit app** (`app.py`) deployed on **Streamlit Cloud**, with the ML/NLP pipeline built through Jupyter notebooks and persisted model artifacts (Joblib).

---

# Project 3

## 1. Title

Restaurant Rating Prediction & Business Intelligence System

## 2. Project Status

Completed

## 3. Project Type

- Machine Learning Project
- Data Analytics Project
- Business Intelligence Dashboard
- End-to-End Data Science Project
- Streamlit Deployment Project

## 4. Project Overview

This project is an end-to-end restaurant analytics and rating prediction system developed using Python, Machine Learning, Power BI, and Streamlit, built against a formal business requirements and software requirements specification before any technical work began.

The project analyzes restaurant business data to:
- understand which factors genuinely drive restaurant ratings, backed by statistical hypothesis testing rather than visual impression,
- build a machine learning model that estimates a restaurant's likely rating before it opens, using only pre-launch-available attributes,
- visualize business performance and segmentation through a 3-page interactive Power BI dashboard,
- deploy the prediction model through a Streamlit web application.

The system helps restaurant businesses understand pricing strategy, cuisine positioning, service offerings, and geographic factors that impact restaurant success.

## 5. Problem Discussed / Solved

Restaurants receive ratings based on multiple business factors such as cuisine type, price range, delivery availability, table booking, location, and cost positioning.

The project solves:
- Which features genuinely, statistically influence restaurant ratings?
- Can a restaurant's rating be estimated before it opens, using only attributes known in advance?
- What business insights, quantified and evidence-based, can help improve restaurant performance?
- Which cuisines and pricing categories dominate the market?

Business problems addressed:
- Evidence-based pricing and positioning strategy
- Identifying high-performing restaurant categories
- Rating estimation for new, pre-launch restaurant concepts
- Market segmentation analysis
- Service-offering (delivery/booking) impact analysis

## 6. Dataset Details

- **Dataset Source:** Zomato Restaurant Dataset (Zomato API extract, 2018–2019 snapshot)
- **Dataset Type:** CSV
- **Dataset Files Used:**
  - Res_dataset.csv → Raw dataset
  - cleaned_dataset.csv → Cleaned, currency-normalized dataset
  - model_ready_dataset.csv → Feature-engineered, model-ready dataset
- **Dataset Size:**
  - Original records: 9,551 rows
  - Rated records used for modeling: 7,403 rows
- **Features after preprocessing:** 180 engineered features
- **Important Columns:** Restaurant Name, City, Country, Cuisines, Aggregate Rating, Price Range, Average Cost for Two (currency-normalized to USD), Online Delivery, Table Booking, Latitude & Longitude

## 7. File Structure

```text
Restaurant-Rating-Prediction/
│
├── docs/
│   ├── 01_problem_statement.md
│   ├── 02_business_requirements.md
│   ├── 03_software_requirements.md
│   ├── 04_user_stories.md
│   ├── 05_data_dictionary.md
│   ├── 06_assumptions_and_limitations.md
│   ├── 07_model_card.md
│   └── 08_architecture_overview.md
├── Dataset/
│   ├── Res_dataset.csv
│   ├── cleaned_dataset.csv
│   └── model_ready_dataset.csv
├── notebook/
│   ├── 01_data_understanding_and_cleaning.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_modeling_and_validation.ipynb
│   └── 04_business_insights.ipynb
├── dashboard/
│   ├── restaurant_dashboard.pbix
│   └── dashboard_screenshots/
├── model/
│   ├── restaurant_rating_model.pkl
│   ├── feature_columns.pkl
│   └── model_metadata.pkl
├── streamlit_app/
│   ├── app.py
│   └── predict_utils.py
├── tests/
│   ├── conftest.py
│   ├── test_data_integrity.py
│   ├── test_model_artifacts.py
│   └── test_app_logic.py
├── Screenshots/
├── pytest.ini
├── README.md
├── requirements.txt
└── .gitignore
```

## 8. Tools & Technologies Used

- **Programming Language:** Python
- **Python Libraries:** pandas, numpy, scipy, statsmodels, matplotlib, seaborn, scikit-learn, joblib
- **Machine Learning Models:** Linear Regression, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor
- **Visualization & Dashboard:** Power BI
- **Deployment:** Streamlit
- **Testing:** pytest
- **Version Control:** Git, GitHub

## 9. Steps Used / Main Work Done

**Step 1 — Business Framing**
- Defined problem statement, business requirements, software requirements, and user stories in writing

**Step 2 — Data Collection**
- Imported the restaurant dataset and loaded it into Python

**Step 3 — Data Cleaning**
- Removed duplicates and constant columns
- Handled missing values
- Normalized cost data to a common USD baseline across all 15 currencies represented in the dataset
- Ran outlier review and data validation assertions
- Excluded zero-rated (unreviewed) restaurants from modeling

**Step 4 — Exploratory Data Analysis (EDA)**
- Univariate Analysis: rating distribution, price range distribution, votes distribution, top cities, top cuisines
- Bivariate Analysis, backed by statistical tests: rating vs. price range (ANOVA), rating vs. online delivery (t-test), rating vs. table booking (t-test), votes vs. rating (correlation)
- Multivariate Analysis: correlation heatmap, VIF multicollinearity check, sample-size-aware country segmentation

**Step 5 — Feature Engineering**
- Created: Cuisine_Count, Log_Average_Cost_USD, top-20 cuisine binary features
- Vote count is intentionally excluded from the feature set, since the model is designed to estimate ratings for restaurants prior to launch, before any votes exist

**Step 6 — Data Preprocessing**
- One-hot encoding of categorical features
- Removal of leakage and redundant columns
- Stratified train/test split (India vs. non-India) to ensure representative evaluation

**Step 7 — Model Building**
- Built and compared: Linear Regression, Decision Tree, Random Forest, Gradient Boosting

**Step 8 — Hyperparameter Tuning**
- Used RandomizedSearchCV with cross-validation on Random Forest and Gradient Boosting

**Step 9 — Model Evaluation**
- Evaluated using MAE, MSE, RMSE, R², with dedicated segment-level evaluation split by India / non-India

**Step 10 — Dashboard Development**
- Built a 3-page interactive Power BI dashboard

**Step 11 — Deployment**
- Built a Streamlit web app for rating estimation, with a dedicated tested prediction module

**Step 12 — Automated Testing**
- Built a 31-test automated suite covering data integrity, model artifacts, and app logic

## 10. Model Building & Performance Evaluation

### a. Model Evaluation & Comparison

Several regression models were trained to estimate restaurant ratings. The dataset was split into 80% training and 20% testing, stratified by India/non-India representation. Two best-performing models (Random Forest and Gradient Boosting) were further optimized using RandomizedSearchCV with 3-fold cross-validation.

**Model Comparison:**

| Model | MSE | MAE | RMSE | R² Score | Status |
|-------------------------------------|--------|--------|--------|----------|----------------------|
| Decision Tree Regressor | 0.2342 | 0.3688 | 0.4839 | 0.2487 | Baseline |
| Gradient Boosting Regressor | 0.1715 | 0.3243 | 0.4141 | 0.4498 | Baseline |
| Random Forest Regressor | 0.1673 | 0.3155 | 0.4090 | 0.4632 | Baseline |
| Linear Regression (Scaled) | 0.1635 | 0.3129 | 0.4044 | 0.4753 | Baseline |
| Random Forest Regressor (Tuned) | 0.1583 | 0.3075 | 0.3979 | 0.4919 | Hyperparameter Tuned |
| Gradient Boosting Regressor (Tuned) | 0.1544 | 0.3053 | 0.3930 | 0.5045 | Selected Final Model |

**Performance Analysis:**
- Decision Tree Regressor produced the lowest performance, showing limited generalization.
- Linear Regression provided a strong baseline, indicating several restaurant attributes carry meaningful linear signal.
- Random Forest achieved the strongest untuned baseline.
- Gradient Boosting responded best to hyperparameter optimization, ultimately outperforming all other models across every metric after tuning.

### b. Hyperparameter Tuning

Optimization was performed using RandomizedSearchCV with 3-fold cross-validation.

**Best Hyperparameters (Gradient Boosting):**

```python
{
 'subsample': 0.9,
 'n_estimators': 250,
 'max_depth': 4,
 'learning_rate': 0.1
}
```

**Tuning Outcome:** the tuned Gradient Boosting model achieved lower prediction error, better generalization, and the highest R² across every model evaluated.

### c. Final Selected Model

**Model:** Tuned Gradient Boosting Regressor

**Final Evaluation Metrics (Overall Test Set):**

| Metric | Value |
|--------------------------------|-------------|
| Mean Squared Error (MSE) | 0.1544 |
| Mean Absolute Error (MAE) | 0.3053 |
| Root Mean Squared Error (RMSE) | 0.3930 |
| R² Score | 0.5045 |

**Segment-Level Evaluation:**

| Metric | India | Non-India |
|----------|--------|-----------|
| MAE | 0.3070 | 0.2931 |
| RMSE | 0.3913 | 0.4050 |
| R² Score | 0.4078 | 0.2747 |

**Interpretation:** the model's average prediction error is approximately 0.31 rating points overall. The model explains 50.45% of rating variance overall, with segment-level reporting confirming performance for both the India-majority population and the smaller non-India population, rather than relying on a single blended figure.

### d. Feature Importance Analysis

Feature importance was extracted from the final Gradient Boosting model.

**Most Important Features:**
- Average Cost for Two (currency-normalized, log-transformed) — the strongest predictor of restaurant rating.
- Country (India vs. rest of world) — restaurants in India show a distinct rating profile compared to other countries.
- City — Gurgaon, Noida, and New Delhi carry meaningful city-level signal.
- Price Range — higher price tiers are associated with materially higher ratings.
- Cuisine Profile — cuisine count and specific cuisine categories (Chinese, Cafe, North Indian, Desserts, Continental, Italian) contribute meaningfully.
- Table Booking Availability — associated with higher ratings.
- Online Delivery Availability — contributes to the model, with its effect varying by price tier.

Note: customer vote count is intentionally excluded from the feature set, since this model is designed to estimate ratings for restaurants prior to launch, before any votes exist.


## 11. Methodology (ML Workflow)

```text
Raw Data
  ↓
Data Cleaning & Currency Normalization
  ↓
EDA & Statistical Testing
  ↓
Feature Engineering
  ↓
Preprocessing (Stratified Split)
  ↓
Model Training
  ↓
Hyperparameter Tuning
  ↓
Segment-Aware Evaluation
  ↓
Business Insights
  ↓
Deployment
```

## 12. Key Insights & Results

- **Best Model:** Tuned Gradient Boosting Regressor
- **Final Accuracy:** R² ≈ 0.50 overall (0.41 India, 0.27 non-India)
- **Important Insights:**
  - Price tier is the strongest driver of rating (ANOVA F=522.9, p<0.001, η²=0.175) — Low tier averages 3.24/5, Premium averages 3.89/5
  - Table booking availability shows a real, moderate positive association with rating (Cohen's d=0.32, p=1.58e-22)
  - Online delivery's effect on rating depends on price tier — there is no single universal directional effect
  - Currency-normalized cost is the single strongest predictor in the model
  - Cuisine diversity and specific cuisine categories meaningfully influence predicted rating
  - Top 5 cuisines (North Indian, Chinese, Fast Food, Mughlai, Italian) account for 50.9% of all restaurants
  - Most Important Features: Log_Average_Cost_USD, Country (India), City, Price Range, Cuisine Categories, Table Booking, Online Delivery

## 13. Dashboard Details (Power BI)

**Page 1 — Performance Overview:**
- KPI cards: total restaurants, average rating, average cost for two (USD), total votes, % unrated restaurants
- Filters: country, city, price tier, cuisine
- Charts: distribution of restaurant rating, geographical distribution of restaurants, top 10 cities by restaurant count, restaurants by price tier

**Page 2 — Rating Drivers & Segmentation:**
- KPI cards: average rating, table booking adoption %, online delivery adoption %
- Charts: average rating by price tier, table booking vs. average rating, online delivery effect by price tier, top 10 cuisines by restaurant count, average rating by country (sample-size aware)

**Page 3 — Key Findings & Recommendations:**
- KPI cards: recommendations issued, high-impact items, retracted findings
- Executive summary, evidence-based retraction callout on the delivery/price-tier finding, effort/impact recommendation prioritization quadrant, quantified recommendations table, data reliability & limitations callout, page-navigation across all 3 pages

## 14. Deployment / GitHub / Live App

- **GitHub Repository:** https://github.com/AKHIL572/Restaurant-Rating-Prediction
- **Live Streamlit App:** https://restaurant-rating-prediction-mcmebtyfca3mf9xm5ucui3.streamlit.app/

## 15. Complexity Level

Advanced Level

## 16. Why this complexity level?

- Formal business and software requirements driving the technical build
- Statistical hypothesis testing (t-tests, ANOVA, chi-square, VIF) underpinning every EDA finding
- Leakage-safe feature engineering scoped to a specific, defined use case
- Segment-aware model validation (India vs. non-India), not a single blended metric
- Hyperparameter tuning across multiple models
- Multi-page, segmented, currency-normalized Power BI dashboard
- Tested Streamlit deployment with a dedicated prediction module
- 31-test automated suite covering data, model, and application logic
- Fully version-controlled delivery via Git/GitHub

## 17. Data Pipeline / Workflow Note

> This project follows a standard ML data pipeline: data cleaning & currency normalization → EDA & statistical testing → feature engineering → preprocessing (stratified split) → model training (Linear Regression, Decision Tree, Random Forest, Gradient Boosting) → hyperparameter tuning → segment-aware evaluation → business insights → deployment. Automation/deployment is handled via a **Streamlit app** (`streamlit_app/app.py`) plus a dedicated `predict_utils.py` module, with an automated **pytest** test suite for pipeline reliability.

---

# Project 4

## 1. Title

Telecom Customer Churn Prediction & Business Intelligence Dashboard

## 2. Project Status

Completed
- End-to-end machine learning project
- Business intelligence dashboard completed
- Streamlit web application completed
- Documentation completed
- Testing completed
- Ready for portfolio and GitHub

## 3. Project Type

End-to-End Data Analytics + Machine Learning + Business Intelligence Project

**Project Categories:**
- Data Cleaning & Preprocessing
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Machine Learning
- Model Evaluation
- Business Intelligence Dashboard
- Streamlit Web Application
- Software Engineering (Modular Python Pipeline)
- Documentation

## 4. Project Overview

Customer churn is one of the biggest business challenges faced by subscription-based companies. Losing existing customers is significantly more expensive than retaining them.

The objective of this project was to develop an end-to-end churn prediction system capable of identifying customers who are likely to leave the telecom company before they actually churn.

The project combines business understanding, exploratory data analysis, machine learning, model evaluation, deployment, and interactive business dashboards into one complete solution.

Unlike many churn prediction projects that focus only on model accuracy, this project was intentionally designed around a real business objective: missing a customer who is going to churn costs the company much more than unnecessarily targeting a customer with a retention offer.

Therefore, the entire modeling pipeline was optimized for **high Recall** instead of maximum Accuracy.

## 5. Problem Discussed / Solved

The project solves multiple business problems:

**Business Problems:**
- High customer churn
- Revenue loss due to customer attrition
- Inability to identify high-risk customers early
- Lack of customer segmentation
- Poor visibility into churn patterns
- Difficulty targeting retention campaigns

**Technical Problems Solved:**
- Missing values
- Incorrect data types
- Feature engineering
- Multicollinearity
- Data leakage
- Model selection bias
- Threshold optimization
- Deployment consistency
- Training–Inference mismatch

## 6. Dataset Details

- **Dataset:** IBM Telco Customer Churn Dataset
- **Number of Records:** 7043 Customers
- **Number of Features:** 21 Original Columns
- **Target Variable:** Churn (Yes, No) — Converted into Yes → 1 and No → 0
- **Important Variables:** customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn
- **Dataset Quality:**
  - Duplicate Rows: 0
  - Missing Values: Only one issue existed. TotalCharges contained 11 blank string values. These belonged to customers having tenure = 0. Instead of filling with the median, they were replaced with 0 because these customers had never received a bill.

## 7. File Structure

```text
Telecom_Churn/
│
├── Dataset/
│     ├── churn_dataset.csv
│     └── cleaned_dataset.csv
├── Notebook/
│     ├── 1_data_understanding.ipynb
│     ├── 2_EDA.ipynb
│     └── 3_preprocessing_and_modeling.ipynb
├── src/
│     ├── data_loader.py
│     ├── preprocessing.py
│     ├── feature_engineering.py
│     ├── train.py
│     └── predict.py
├── Models/
│     ├── best_model.pkl
│     ├── decision_threshold.pkl
│     ├── high_charges_threshold.pkl
│     └── model_features.pkl
├── Power_BI/
│     ├── telecom_dashboard.pbix
│     └── telecom_dashboard.pdf
├── tests/
│     └── test_pipeline.py
├── docs/
│     ├── executive_summary.md
│     ├── data_dictionary.md
│     └── model_card.md
├── app.py
├── requirements.txt
└── README.md
```


## 8. Tools & Technologies Used

- **Programming:** Python
- **Libraries:** Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, Joblib
- **Dashboard:** Microsoft Power BI
- **Deployment:** Streamlit
- **Development:** Jupyter Notebook, VS Code
- **Version Control:** Git, GitHub

## 9. Steps Used (Main Work Done)

**Phase 1 — Business Understanding**
- Defined project objective
- Defined business problem
- Identified success metrics

**Phase 2 — Data Understanding**
- Loaded dataset
- Checked shape
- Examined data types
- Checked duplicates
- Checked missing values
- Investigated blank TotalCharges

**Phase 3 — Data Cleaning**
- Removed customerID
- Converted TotalCharges to numeric
- Filled TotalCharges with 0
- Converted Churn to binary

**Phase 4 — Exploratory Data Analysis Performed**
- Univariate Analysis: Distribution plots, Count plots, Histograms
- Bivariate Analysis: Churn vs Contract, Churn vs Internet, Churn vs Payment Method, Churn vs Tenure, Churn vs Charges
- Multivariate Analysis: Correlation Matrix, Heatmap, Business Insights

**Phase 5 — Feature Engineering**
- Created: tenure_group, AutoPayment, HighRiskSegment, HighCharges

**Phase 6 — Data Preprocessing**
- Train-Test Split
- Standard Scaling
- One Hot Encoding

**Phase 7 — Model Building**
- Compared Logistic Regression, Random Forest, Gradient Boosting

**Phase 8 — Hyperparameter Tuning**
- Used GridSearchCV

**Phase 9 — Threshold Optimization**
- Used cross_val_predict()
- Selected Threshold = 0.25
- Business Driven

**Phase 10 — Model Evaluation**
- Measured: Accuracy, Precision, Recall, F1 Score, ROC AUC, Confusion Matrix, ROC Curve

**Phase 11 — Interpretability**
- Feature Coefficients
- Business Interpretation

**Phase 12 — Model Saving**
- Saved: best_model.pkl, model_features.pkl, decision_threshold.pkl, high_charges_threshold.pkl

**Phase 13 — Deployment**
- Built Streamlit Application

**Phase 14 — Dashboard Development**
- Created Interactive Power BI Dashboard

**Phase 15 — Documentation**
- Created: README, Executive Summary, Data Dictionary, Model Card

## 10. Methodology

```text
Business Understanding
    ↓
Data Collection
    ↓
Data Understanding
    ↓
Data Cleaning
    ↓
EDA
    ↓
Feature Engineering
    ↓
Train Test Split
    ↓
Encoding & Scaling
    ↓
Baseline Model
    ↓
Model Comparison
    ↓
Hyperparameter Tuning
    ↓
Cross Validation
    ↓
Threshold Optimization
    ↓
Model Evaluation
    ↓
Interpretability
    ↓
Model Saving
    ↓
Power BI Dashboard
    ↓
Streamlit Deployment
    ↓
Documentation
```

## 11. Key Insights & Results

**Important EDA Findings:**
- Month-to-Month customers churned the most.
- Fiber Optic users had significantly higher churn.
- Electronic Check customers had the highest churn rate.
- Customers with longer tenure were much less likely to churn.
- Two-year contracts greatly reduced churn.
- MonthlyCharges showed a positive relationship with churn during EDA.

**Machine Learning Results:**
- Selected Model: Logistic Regression
- Reason: Highest Cross Validated Recall, CV Recall (0.7967)
- Final Threshold: 0.25
- Final Test Results: Accuracy (62.4%), Recall (94.1%), Precision (40.9%), F1 Score (0.57), ROC AUC (0.840)

**Business Result:**
The model successfully identifies approximately **94% of customers who are likely to churn**, allowing the business to proactively target at-risk customers with retention campaigns. Although the model produces more false positives due to the recall-first strategy, this trade-off aligns with the business objective of minimizing customer loss.

## 12. Dashboard Details

The project includes a two-page interactive Power BI dashboard.

**Dashboard Page 1 – Executive Overview**
- Displays:
  - Total Customers KPI
  - Churned Customers KPI
  - Churn Rate KPI
  - Monthly Revenue KPI
  - Estimated Monthly Revenue at Risk KPI
  - Churn by Contract Type
  - Churn by Internet Service
  - Churn by Payment Method
  - Customer Distribution by Tenure Group
  - Interactive slicers for Gender, Contract, and Internet Service

**Dashboard Page 2 – Customer Risk Analysis**
- Displays:
  - High-Risk Customer Segments
  - Churn by Senior Citizen
  - Churn by Partner Status
  - Churn by Dependents
  - Churn by Monthly Charges
  - Churn by Tenure
  - Customer Segmentation visuals
  - Drill-down analysis
  - Interactive filtering for business users

The dashboard enables stakeholders to monitor churn patterns, identify high-risk customer groups, estimate revenue impact, and support retention decision-making through interactive visual analysis.

## 13. Deployment, GitHub & Live Application

- **GitHub Repository:** https://github.com/AKHIL572/Telecom-Customer-Churn-Analysis-Prediction
- **Live Demo:** https://telecom-customer-churn-analysis-prediction-9tkvwovbgw9tquteei8.streamlit.app/

## 14. Project Complexity Level

Advanced Level

## 15. Why this complexity level?

The project goes beyond a standard churn prediction notebook by including:
- Complete business problem framing
- End-to-end machine learning workflow
- Extensive EDA with business interpretation
- Multiple engineered features
- Data leakage detection and correction
- Feature engineering consistency between training and inference
- Baseline model comparison
- Hyperparameter tuning with GridSearchCV
- Cross-validation-based model selection
- Decision threshold optimization using out-of-fold predictions
- Model interpretability using Logistic Regression coefficients
- Overfitting analysis
- Modular Python pipeline (`src/`)
- Streamlit deployment
- Interactive Power BI dashboard
- Professional project documentation
- Automated testing
- Git version control and structured commit history

## 16. Additional Project Details (Items Not Covered Above)

- Business objective prioritized **Recall over Accuracy**, reflecting real-world retention costs.
- Identified and fixed **three important issues**:
  - `HighCharges` feature leakage by computing the median only on the training data.
  - Model selection leakage by choosing the final model based on cross-validated recall instead of the test set.
  - Threshold selection leakage by using out-of-fold training predictions instead of the test set.
- Fixed a subtle `pd.cut()` issue by setting `include_lowest=True`, ensuring customers with `tenure = 0` were correctly assigned to a tenure group.
- Removed `TotalCharges` from modeling to avoid multicollinearity with `tenure` and `MonthlyCharges`.
- Established a **majority-class Dummy Classifier** baseline, demonstrating that high accuracy alone (73.46%) is misleading because it achieves 0% recall.
- Verified model stability through 5-fold cross-validation, with low standard deviations (0.01–0.03) across recall, precision, accuracy, and ROC-AUC.
- Performed a train-versus-test comparison, confirming negligible metric differences (all below 0.01), indicating the model generalizes well without overfitting.
- Used Logistic Regression instead of Random Forest due to its slightly higher cross-validated recall and superior interpretability through feature coefficients.
- Interpreted standardized coefficients to explain the influence of features such as tenure, contract type, fiber optic service, and monthly charges on churn risk.
- Saved all required deployment artifacts (`best_model.pkl`, `model_features.pkl`, `high_charges_threshold.pkl`, and `decision_threshold.pkl`) to ensure training and inference remain synchronized.
- Centralized feature engineering into a single reusable module (`feature_engineering.py`) so both training and prediction pipelines generate identical features.
- Developed modular Python scripts (`data_loader.py`, `preprocessing.py`, `feature_engineering.py`, `train.py`, and `predict.py`) for maintainability and reproducibility.
- Included project documentation (`README.md`, `executive_summary.md`, `data_dictionary.md`, and `model_card.md`) describing business context, dataset, methodology, assumptions, limitations, and deployment guidance.
- Added automated tests for pipeline and prediction logic to improve reliability.
- Produced a complete portfolio-ready project combining data analysis, machine learning, software engineering, business intelligence, deployment, documentation, and reproducible workflows.

## 17. Data Pipeline / Workflow Note

> This project follows a standard ML data pipeline: business understanding → data collection → data understanding → data cleaning → EDA → feature engineering → train/test split → encoding & scaling → baseline model → model comparison → hyperparameter tuning (GridSearchCV) → cross validation → threshold optimization → model evaluation → interpretability → model saving → dashboard → deployment → documentation. Automation/deployment is handled via a **Streamlit app** (`app.py`) and modular **Python scripts** in `src/` (`data_loader.py`, `preprocessing.py`, `feature_engineering.py`, `train.py`, `predict.py`).

---

# Project 5

## 1. Title

Customer Lifetime Value (CLV) Prediction for Online Retail (Predicting 6-Month Forward Customer Revenue Using Behavioral Purchase Data)

## 2. Project Status

Complete

All three notebooks, the modular `src/` pipeline, the Streamlit application, and the Power BI dashboard are built, tested, and functioning end-to-end. The trained model's performance — including the fact that it does not yet outperform a naive baseline — is fully documented rather than hidden, which is itself treated as a completed, honest deliverable rather than an unfinished one. Known limitations and future improvement paths are listed explicitly in Section 15.

## 3. Project Type

End-to-end **Data Science / Machine Learning project** combining:
- Exploratory data analysis and customer segmentation (unsupervised learning)
- Predictive modeling (supervised regression)
- Production-style software engineering (modular pipeline, testing, logging)
- Business Intelligence reporting (Power BI)
- Interactive deployment (Streamlit web application)

Domain: Retail / Customer Analytics

## 4. Project Overview

This project builds a complete pipeline to predict how much revenue an individual customer will generate over the next 6 months, using only their historical purchase behavior.

It's built on a real UK-based online retailer's transaction data (Dec 2010–Dec 2011) and takes that raw data through the full lifecycle of a production data science project: rigorous data cleaning with a full audit trail, exploratory analysis with real customer segmentation, a leakage-safe modeling pipeline with proper baseline comparison and cross-validated model selection, a modular and tested codebase, an interactive prediction app, and a business-facing BI dashboard — all of which are kept consistent with each other through a single shared configuration and a shared set of model artifacts (segment thresholds, model card).

## 5. Problem Discussed / Solved

Online retailers acquire and retain customers at a cost, but not all customers are equally valuable going forward. Marketing and CRM teams need a forward-looking estimate of customer value — not just historical spend — to:
- Prioritize retention campaigns toward customers likely to generate the most future revenue
- Identify at-risk or low-engagement customers before they churn
- Justify acquisition spend against expected long-term return rather than first-purchase revenue alone

This project solves that by framing CLV as a supervised regression problem: using a strict cutoff date, it builds behavioral features from a customer's purchase history *before* the cutoff, and predicts their revenue in the 6 months after it — with the target window explicitly bounded to prevent data leakage.

## 6. Dataset Details

- **Source:** "Online Retail" transactional dataset — a UK-based, non-store online retailer specializing in all-occasion gifts (originally distributed via the UCI Machine Learning Repository)
- **Raw size:** 541,909 transaction line items
- **Time period:** 1 December 2010 to 9 December 2011 (~12.3 months)
- **Raw columns:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`
- **After cleaning:** 391,150 transaction rows, 0 missing values, 0 duplicates (full audit trail of every row removed and why is preserved in `data_cleaning_audit_log.csv`)
- **Unique customers (full history):** 4,334
- **Customers in the modeling population** (had purchase activity before the cutoff date and therefore have valid features): 2,791
- **Currency:** GBP (£) throughout — enforced consistently across notebooks, scripts, app, and dashboard

## 7. File Structure

```text
ONLINE_RETAIL/
│
├── Dataset/
│   ├── OnlineRetail.csv                          (raw)
│   ├── cleaned_online_retail_transactions.csv    (cleaned, audit-tracked)
│   ├── cancelled_orders.csv                      (preserved separately, not discarded)
│   ├── data_cleaning_audit_log.csv                (before/after row counts per cleaning step)
│   ├── customer_level_eda_summary.csv             (full-history RFM + K-Means segments)
│   ├── segment_profile_summary.csv                (segment-level profile table)
│   └── clv_predictions.csv                        (per-customer model output + segment)
│
├── Models/
│   ├── clv_model.pkl
│   ├── clv_features.pkl
│   ├── segment_thresholds.json                    (single source of truth for Low/Medium/High cutoffs)
│   └── model_card.json                            (training metadata, metrics, baseline comparison, limitations)
│
├── Notebook/
│   ├── 1_data_understanding.ipynb
│   ├── 2_eda.ipynb
│   └── 3_preprocessing_and_modeling.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py                                  (shared paths, features, thresholds — single source of truth)
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── train.py
│   └── predict.py
│
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py                           (6 unit tests, including a leakage-bug regression test)
│
├── Power_BI_dashboard/
│   └── power_BI_Dashboard.pbix                     (3 pages: Overview, Product Insights, Customer Value)
│
├── app.py                                          (Streamlit — 4 tabs)
└── requirements.txt
```

## 8. Tools & Technologies Used

- **Language:** Python 3.12
- **Data manipulation:** pandas, numpy
- **Modeling:** scikit-learn (Linear Regression, Decision Tree, Random Forest, Gradient Boosting), XGBoost
- **Visualization:** matplotlib, seaborn
- **Testing:** pytest
- **Deployment / App:** Streamlit
- **Business Intelligence:** Power BI (DAX, Power Query / M)
- **Environment:** Jupyter Notebook
- **Version control:** Git / GitHub
- **Serialization:** joblib (model artifacts), JSON (model card, segment thresholds)

## 9. Steps Used (Main Work Done)

**Data Understanding & Cleaning**
- Investigated (not blindly removed) every data quality issue before acting: duplicate rows, missing `CustomerID`, cancelled orders (`InvoiceNo` starting with 'C'), non-product `StockCode` values (postage, bank charges, adjustments), residual invalid quantity/price rows
- Preserved cancellations in a separate `cancelled_orders.csv` instead of discarding them, for future returns-behavior feature work
- Built a full before/after audit trail (`data_cleaning_audit_log.csv`) quantifying rows and revenue removed at every step
- Documented every cleaning decision with a written business rationale, plus explicit assumptions and limitations sections

**Exploratory Data Analysis**
- Quantified revenue concentration (Pareto analysis), one-time vs. repeat customer behavior, purchase interval and basket-size patterns, time-of-day/day-of-week ordering patterns
- Investigated IQR-flagged outliers and made a documented decision to keep them (legitimate wholesale transactions) and handle skew via log-transform instead of deletion
- Built genuine customer segmentation via **K-Means clustering** on RFM features, with elbow-method selection and business-friendly segment naming (Champions, Loyal Mid-Value, New/Low Engagement, At Risk/Lapsed)

**Feature Engineering & Modeling**
- Fixed a target-window definition bug (originally unbounded, silently correct only by coincidence) — now explicitly bounded to prevent data leakage
- Expanded the feature set from basic RFM (4 features) to 8 behavioral features: Recency, Frequency, Monetary, TotalQuantity, AvgOrderValue, AvgBasketSize, AvgPurchaseIntervalDays, TenureDays
- Computed two baselines — a mean-prediction baseline and a stronger, domain-realistic "past spend = future spend" baseline — and evaluated the model against both, rather than reporting metrics in isolation
- Ran cross-validated comparison across 5 candidate models (Linear Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost) and selected a champion based on evidence, not a hardcoded assumption
- Tuned the champion model via `RandomizedSearchCV`
- Cross-validated the model's predictions against the independently-derived K-Means segments as a business sanity check
- Saved a full model card (training date, features, hyperparameters, metrics, baseline comparison, known limitations) alongside the model itself

**Engineering / Productionization**
- Refactored all logic out of notebooks into a modular, tested `src/` package
- Added a centralized `config.py` so paths, feature lists, and segmentation thresholds cannot drift out of sync across notebooks, scripts, and the app
- Added `logging` throughout (replacing print statements), CLI arguments for retraining, and explicit input validation with clear error messages
- Added a `tests/` suite with real unit tests, including a regression test that specifically catches the original target-leakage bug

**Deployment**
- Rebuilt the Streamlit app from a single manual-entry form into a 4-tab application: Customer Lookup (real customer data), What-If Scenario (manual input with auto-derived fields), Batch Upload (CSV scoring), and Model Info (transparent performance/limitations display)
- Verified the app end-to-end using Streamlit's `AppTest` framework (not just a visual check) — confirmed zero runtime exceptions across all tabs

**Business Intelligence**
- Rebuilt the Power BI dashboard from a 2-page, disconnected sales report into a 3-page dashboard where the third page (Customer Value & CLV) directly surfaces the model's output, segments, and honest performance metrics to a business audience
- Fixed data lineage so every visual is traceable to the cleaned/audited data rather than the raw file
- Fixed formatting, currency labeling, and cross-page metric consistency issues found during review

## 10. Methodology

The project follows a structured, leakage-aware data science methodology:

1. **Business Understanding** — define the problem as predicting forward-looking customer value to support retention/marketing prioritization
2. **Data Cleaning** — investigate before acting; document every decision; preserve rather than silently discard ambiguous data (cancellations)
3. **Exploratory Analysis** — quantify business-relevant patterns; build unsupervised segments independent of the eventual model, to use as a later sanity check
4. **Leakage-Safe Feature Engineering** — a single cutoff date strictly separates the feature window (history used to build behavioral features) from the target window (future revenue being predicted); target window is explicitly bounded
5. **Baseline-First Evaluation** — establish what "no model" and "a simple heuristic" would achieve *before* judging any ML model's performance
6. **Evidence-Based Model Selection** — compare multiple candidate models via cross-validation rather than assuming one algorithm in advance
7. **Hyperparameter Tuning** — randomized search on the selected champion model only, using the validated methodology
8. **Business Validation** — cross-check model output against independently-derived customer segments, not just statistical metrics
9. **Deployment** — expose the model through both a self-service prediction app and a business-facing dashboard, both drawing from the same trained artifacts

## 11. Key Insights & Results

**Business findings (from EDA):**
- The top 20% of customers by spend generate **~74.6%** of total revenue
- **34.7%** of customers are one-time buyers, but they account for only **~7.2%** of total revenue
- Four behaviorally distinct customer segments identified via clustering: **Champions** (15.8% of customers), **Loyal Mid-Value** (27.2%), **New/Low Engagement** (19.3%), **At Risk/Lapsed** (37.7%)
- Median time between repeat purchases: **22 days**
- Ordering activity concentrates in weekday business hours, consistent with a wholesaler-leaning customer base

**Model results (honestly reported):**
- Champion model: **Gradient Boosting Regressor**
- Test set MAE: **£899.76** (58.7% of mean CLV)
- Test set R²: **0.381**
- Naive "past spend = future spend" baseline MAE: **£794.10**
- **The tuned model does not currently outperform this naive baseline** (-13.3%) — disclosed explicitly in the model card, the Streamlit app's Model Info tab, and the Power BI dashboard's Customer Value page, rather than omitted
- 30.5% of customers in the training population have a true 6-month CLV of £0, which places a structural ceiling on achievable model accuracy independent of model quality
- Despite not beating the naive baseline numerically, the model's predictions correctly rank the independently-derived customer segments in the expected order (Champions highest, At Risk/Lapsed lowest), confirming it has learned genuine behavioral signal even where it hasn't yet beaten the simple heuristic on raw error

## 12. Dashboard — What It Shows

The Power BI dashboard has **3 pages**, all built on the cleaned/audited data and consistent with each other:

**Page 1 — Executive Sales Dashboard:** Total Orders, Total Revenue, Total Quantity, AOV; revenue trend over time; order status distribution (completed vs. cancelled, built from a properly documented combined table rather than raw data); top revenue countries; revenue distribution map; peak ordering hours.

**Page 2 — Product & Customer Intelligence:** Unique Customers, Total Orders, Total Revenue, Cancellation Rate %; weekly sales pattern; customer distribution by country; top products by revenue; product revenue vs. quantity scatter analysis; a customer detail table that bridges into the ML output (Recency, Predicted_CLV, CLV_Segment alongside transaction totals).

**Page 3 — Customer Value & CLV (new):** Total Predicted CLV, Average Predicted CLV, High Value Customer %, One-Time Customer Revenue %, Top 20% Revenue Share; customer segment breakdown (count and average value by segment); a Frequency-vs-Monetary scatter colored by CLV segment; a Top 20 Customers by Predicted CLV table; and a Model Performance & Limitations panel that surfaces the honest baseline comparison directly to business users, including an explicit note that CLV figures should be treated as directional rather than precise.

## 13. Deployment

- **GitHub repository:** https://github.com/AKHIL572/Customer-Lifetime-Value-CLV-Prediction-Segmentation
- **Streamlit application:** https://customer-lifetime-value-clv-prediction-segmentation.streamlit.app/

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 14. Complexity Level

**Intermediate to Advanced**

This goes beyond an entry-level or internship-style project in several concrete ways: leakage-safe, cutoff-date-based target construction; evidence-based model selection via cross-validation across multiple algorithms rather than a single assumed model; mandatory baseline comparison (including a domain-realistic baseline, not just a trivial mean); a modular, tested, logged production codebase rather than notebook-only code; a single shared configuration preventing drift between notebooks, scripts, app, and dashboard; and full-stack delivery spanning ML, a deployed application, and a BI layer that are all kept consistent with each other. It stops short of "expert/production-grade at scale" primarily because of one honestly-disclosed limitation: the model does not yet outperform its baseline, and validation was limited to a single time-based split due to dataset length (see Section 15).

## 15. Anything Missed Above

A few things worth stating explicitly, since they don't fit neatly into the other sections but matter for anyone evaluating this project:

- **The model does not currently beat a naive baseline.** This is disclosed everywhere (model card, app, dashboard) rather than hidden, but it means the modeling work should be read as rigorous and honest rather than as a finished, deployment-ready predictive model. Next steps to address this would include richer features (e.g., product-category diversity, discount/return behavior) or a longer transaction history to enable proper multi-period walk-forward validation.
- **No true walk-forward validation was possible** — the dataset's ~12.3-month span only allows one non-overlapping 6-month feature/target split. This is a data constraint, documented as a limitation rather than worked around artificially.
- **Cold-start customers are not handled.** Brand-new customers with zero purchase history cannot receive RFM-based features and therefore cannot be scored by this model — a separate rule-based approach would be needed for that segment in a real production deployment.
- **The dataset is heavily UK-dominant**; model performance for other countries should be treated as lower-confidence until validated on more geographically diverse data.
- **`clv_predictions.csv` reflects a single training run's snapshot.** If the model is retrained, this file (and anything in the app/dashboard reading from it, like the Customer Lookup tab) needs to be regenerated to stay current — this isn't currently automated as part of `train.py`.
- Every honesty-first design choice in this project (disclosing the baseline comparison, quantifying the structural floor from one-time buyers, documenting cleaning decisions instead of hiding them) was intentional — the goal throughout was to build something that would hold up under real scrutiny, not to optimize for how impressive the numbers look at first glance.

## 16. Data Pipeline / Workflow Note

> This project follows a standard ML data pipeline: business understanding → data cleaning (with audit trail) → EDA & customer segmentation (K-Means) → leakage-safe feature engineering → baseline-first evaluation → evidence-based model selection (cross-validation across 5 models) → hyperparameter tuning → business validation → deployment. Automation/deployment is handled via a **Streamlit app** (`app.py`, 4 tabs, tested with `AppTest`) and modular **Python scripts** in `src/` (`config.py`, `data_loader.py`, `feature_engineering.py`, `train.py`, `predict.py`), with an automated **pytest** suite.

---

# Project 6

## 1. Title

Credit Risk Prediction & Analysis System

## 2. Project Status

Completed

## 3. Project Type

End-to-End Machine Learning Project with Business Intelligence Dashboard and Deployed Web Application

## 4. Project Overview

A full-scale credit risk prediction system built on LendingClub's real-world lending dataset of 2.26 million loan records.

The project covers the complete data science lifecycle — from raw data ingestion and exploratory analysis, through leakage-safe feature engineering and machine learning modeling, to a deployed Streamlit web application and a two-page interactive Power BI business dashboard connected directly to the trained model's output.

The system trains two separate models for two distinct use cases and produces both a binary prediction and a calibrated probability score.

## 5. Problem Discussed / Solved

**Problem:**
- Financial institutions face significant losses due to loan defaults.
- Identifying high-risk borrowers before loan approval, and assessing risk on already-listed loans, are both critical for reducing credit losses — but they are different decisions requiring different inputs.

**Solution:**
- Two binary classification models, each scoped to a specific persona — an Underwriting Screening Model (borrower-only attributes, for screening a new applicant who has not yet been priced) and an Investor Risk Model (full feature set including LendingClub's own grade and interest rate, for scoring an already-listed loan).
- This split exists because grade and interest rate are themselves outputs of LendingClub's own risk assessment and are not available before a lending decision is made — a single combined model conflates these two decisions.
- The project also quantifies how much of the Investor Model's predictive power comes from LendingClub's own institution-assigned risk indicators versus genuine borrower-level signal.

## 6. Dataset Details

- **Data Source:** LendingClub Loan Dataset (publicly available)
- **Size:** 2,260,701 rows × 151 columns
- **Target Variable:** loan_status → mapped to binary (0 = Fully Paid, 1 = Charged Off / Default)
- **Resolved loans used for modeling:** ~1.35 million (Current, Late, In Grace Period loans excluded to avoid label ambiguity; legacy "does not meet the credit policy" loans mapped to their underlying resolved outcome)
- **Overall default rate:** ~19.96% (class imbalance handled via class_weight="balanced")
- **Key features used:** loan amount, interest rate, grade/sub-grade, FICO score, DTI, annual income, revolving utilization, delinquencies, purpose, employment length, home ownership, and 7 engineered features
- **Known data quality issues identified and corrected:** a -1 sentinel placeholder value in the DTI field (converted to missing rather than treated as a real value), and extreme outlier values in annual income and derived income ratios (addressed via percentile-based capping)

## 7. File Structure

```text
credit_risk_prediction/
│
├── app/
│   └── app.py
├── dashboard/
│   └── credit_risk_dashboard.pbix
├── data/
│   ├── metadata/
│   │   └── column_summary.csv
│   ├── processed/
│   │   ├── dashboard_data.csv
│   │   ├── dashboard_risk_by_grade.csv
│   │   ├── dashboard_risk_by_income.csv
│   │   ├── dashboard_risk_by_purpose.csv
│   │   ├── dashboard_risk_by_term.csv
│   │   └── final_model_data.csv
│   └── raw/
│       └── dataset.csv
├── models/
│   ├── credit_risk_model_investor.joblib
│   ├── credit_risk_model_underwriting.joblib
│   ├── expected_features_investor.joblib
│   ├── expected_features_underwriting.joblib
│   ├── feature_caps.joblib
│   └── model_metrics.json
├── notebooks/
│   ├── 1_data_understanding.ipynb
│   ├── 2_eda.ipynb
│   ├── 3_data_preprocessing.ipynb
│   ├── 4_modeling.ipynb
│   └── 5_business_insights.ipynb
├── reports/
│   └── credit_risk_dashboard.pdf
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── evaluate.py
│   ├── feature_engineering.py
│   ├── predict.py
│   ├── preprocessing.py
│   └── train.py
├── .gitignore
├── config.yaml
├── README.md
├── requirements.txt
└── sample_input.csv
```

## 8. Tools & Technologies Used

| Category | Tools |
|--------------------------|---------------------------|
| Language | Python 3.13 |
| Data Processing | Pandas, NumPy |
| Visualization (EDA) | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Statistical Testing | SciPy (chi-square tests) |
| Model Persistence | Joblib |
| Configuration | PyYAML |
| Web Application | Streamlit |
| Dashboard | Power BI |
| Interactive Charts (App) | Plotly |
| Development Environment | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |

## 9. Steps Used (Main Work Done)

**Step 1 — Data Understanding (1_data_understanding.ipynb)**
- Loaded the 2.26M row dataset using a memory-safe chunked loader with automatic retry on constrained machines, explored shape, dtypes, and duplicates
- Analyzed missing values across all 151 columns and categorized them by cause (identifier column scrubbed for privacy, sparse hardship/settlement program fields, low-rate core predictors)
- Investigated and confirmed two raw data quality issues directly from the summary statistics: a -1 sentinel value in DTI and an extreme outlier in annual income
- Studied target variable distribution across all loan status categories, including legacy credit-policy-exception statuses, and made an explicit, documented decision on how to map them
- Ran a leakage-risk column audit with evidence (comparing a candidate leaking column's values across loan outcomes), rather than assuming which columns to exclude
- Checked the dataset's time coverage to support a chronological train/test split later in the pipeline
- Saved column-level metadata for reference in later notebooks

**Step 2 — Exploratory Data Analysis (2_eda.ipynb)**
- Chunk-based, memory-safe loading of the full dataset for exploration
- Visualized loan amount, interest rate, term, and grade distributions, plus home ownership, verification status, and employment length — with default rate broken out by each
- Analyzed interest rate and DTI vs loan outcome using boxplots
- Crosstab analysis of loan status by grade (stacked bar)
- Quantified the significance of key categorical predictors using chi-square tests, rather than relying on visual inspection alone
- Correlation heatmap on a curated set of numeric features, explicitly documented as not a leakage audit (the leakage audit lives in notebook 1)
- Default rate by loan purpose, with written interpretation
- Time-trend analysis of loan volume and default rate by issue year, to evaluate the case for a chronological (rather than random) train/test split

**Step 3 — Data Preprocessing (3_data_preprocessing.ipynb)**
- Chunk-based ingestion filtering to resolved loan statuses only, with legacy credit-policy-exception loans mapped to their underlying outcome
- Data type corrections for int_rate and revol_util
- Applied the raw-data fixes identified in notebook 1: converted the DTI sentinel value to missing, and winsorized annual income at the 1st/99th percentile
- Feature engineering (7 new features):
  - annual_inc_capped — winsorized annual income
  - loan_to_income — affordability ratio, capped at the 99th percentile
  - fico_avg — average of FICO range
  - loan_term_numeric — term as a 36/60 integer
  - installment_to_income — monthly payment burden, capped at the 99th percentile
  - dti_capped — DTI clipped at 100, computed after the sentinel-value fix
  - emp_length_numeric — employment length encoded as a numeric ordinal (0–10) rather than one-hot, to preserve the ordering
- Data validation assertions, including checks for the sentinel value being resolved and no duplicate rows introduced
- Saved a single canonical processed dataset for modeling

**Step 4 — Modeling (4_modeling.ipynb)**
- Loaded processed data and defined two feature sets: a full "Investor" set (including grade/sub-grade and interest rate) and a borrower-only "Underwriting" set
- Sorted by issue date and applied a chronological (out-of-time) 80/20 train/test split, rather than a random split, given the dataset spans more than a decade of different economic conditions
- Established two baselines before evaluating any model: a majority-class baseline and a baseline using LendingClub's own sub-grade alone
- sklearn Pipeline with ColumnTransformer for numeric and categorical preprocessing, fit only on the training split
- Cross-validation (TimeSeriesSplit) comparing Logistic Regression, Decision Tree, and Random Forest
- Model selection made by an explicit rule — the simplest model is chosen unless a more complex model beats it by a stated margin, verified with a paired t-test across CV folds — rather than assumed
- RandomizedSearchCV hyperparameter tuning on the selected model
- Reported train and out-of-time test performance together to check for overfitting
- Added a calibration check (Brier score, reliability curve) alongside ROC-AUC
- Computed a business-driven decision threshold that minimizes total expected cost, rather than defaulting to a 0.5 cutoff
- Feature importance via both impurity-based and permutation importance
- Two-model training: Investor Model (full features) vs Underwriting Model (borrower-only), to directly measure how much predictive power comes from institution-assigned features
- Both models, their expected feature lists, and the fitted preprocessing caps saved as joblib files

**Step 5 — Business Insights (5_business_insights.ipynb)**
- Loads the already-processed, cleaned dataset (not the raw file) and both trained models
- Scores the full resolved population with both models to produce predicted default probabilities
- Builds data-driven risk tiers (quartile-based) and validates that actual default rate increases monotonically across them
- Computes expected loss by segment (predicted probability × loan amount × loss-given-default assumption), by grade and by purpose
- Quantifies model lift: Investor Model vs the sub-grade-alone baseline, and Investor Model vs the Underwriting Model, to isolate the contribution of institution-assigned features
- Generates risk aggregation tables by grade, term, purpose, and income bracket (quantile-based, not fixed dollar bins), each including both actual and model-predicted default rate
- Includes a written executive summary, key findings, recommendations, and a stated limitations section
- Saves dashboard-ready CSVs for Power BI, including the model's predictions, risk tier, and expected loss

## 10. Methodology

- **Problem Type:** Binary Classification (two models, two personas)
- **Imbalance Handling:** class_weight="balanced" across all candidate models
- **Data Leakage Prevention:** Evidence-based leakage audit conducted in notebook 1 and applied at the data-loading stage in notebook 3 (post-outcome columns never loaded, not filtered after the fact); grade, sub_grade, and int_rate are explicitly scoped to the Investor Model only, since they are institution-assigned and unavailable before a lending decision is made
- **Validation Strategy:** Chronological (out-of-time) train/test split, given the multi-year span of the data
- **Evaluation Strategy:** ROC-AUC as the primary ranking metric, alongside calibration (Brier score) and a cost-based decision threshold — not accuracy alone
- **Memory Management:** Chunk-based CSV ingestion with automatic retry at a smaller chunk size on memory-constrained machines
- **Pipeline Architecture:** Full sklearn Pipeline with ColumnTransformer, fit only on the training split, ensuring no leakage between train and test sets

**Model Results:**

| Model | CV ROC-AUC |
|---------------------|------------|
| Logistic Regression | 0.7095 |
| Random Forest | 0.7031 |
| Decision Tree | 0.7001 |

## 11. Model Building & Performance Evaluation

### A. Dataset Overview

| Property | Value |
|-------------------|----------------------------------------------------|
| Raw Dataset Size | 2,260,701 rows × 151 columns |
| Duplicate Records | 0 |
| Target Variable | loan_status |
| Problem Type | Binary Classification |
| Good Loans | ~80% |
| Defaulted Loans | ~20% |
| Test Set Size | 269,620 records (chronological, out-of-time split) |

**Target Definition:**
Only completed loan outcomes were considered:
- Fully Paid → Good Loan (Class 0)
- Charged Off / Default → Bad Loan (Class 1)
- Current, Late, In Grace Period → Excluded

This ensures the model learns from known outcomes rather than uncertain, in-progress loans.

### B. Baseline Comparison

Before evaluating any trained model, two baselines were established: a majority-class baseline (accuracy 0.7822) and a baseline using LendingClub's own sub-grade alone (ROC-AUC 0.6797). Both trained models are evaluated against these, not in isolation.

Three candidate models were compared using 3-fold time-series cross-validation on the training split. Since the dataset is imbalanced, ROC-AUC was the primary comparison metric, and all models used class_weight="balanced".

**Cross-Validation Performance:**

| Model | CV ROC-AUC | Standard Deviation |
|---------------------|------------|--------------------|
| Logistic Regression | 0.7095 | ± 0.0009 |
| Random Forest | 0.7031 | ± 0.0012 |
| Decision Tree | 0.7001 | ± 0.0011 |

Model selection was made using an explicit rule: a more complex model must beat the simplest model by more than a stated margin (verified with a paired t-test) to be selected. No model exceeded Logistic Regression by that margin, so Logistic Regression was selected as the final model type — chosen on its own merits under a predefined rule, not by default.

### C. Hyperparameter Tuning

RandomizedSearchCV was applied to the selected Logistic Regression model.

**Best Hyperparameters:**

```python
{
   'classifier__C': 0.01
}
```

### D. Final Selected Model (Investor Model)

- **Model:** Logistic Regression (regularization tuned via RandomizedSearchCV)

**Test Set Performance (out-of-time):**

| Metric | Value |
|----------------------------|---------------------------------------------------------------|
| Train ROC-AUC | 0.7129 |
| Test ROC-AUC | 0.6968 |
| Train/Test Gap | 0.0161 (within a healthy range — no meaningful overfitting) |
| Brier Score (calibration) | 0.2198 |
| Optimal Decision Threshold | 0.40 (cost-minimizing, not a default 0.5 cutoff) |

**Classification Report (at 0.5 threshold):**
- Good Loan (Class 0): Precision 0.87, Recall 0.63, F1 0.73
- Default Loan (Class 1): Precision 0.33, Recall 0.65, F1 0.44
- Overall Accuracy: 0.64

### E. Investor Model vs Underwriting Model

To evaluate the contribution of institution-assigned credit features, two model variants were trained and compared.

**Model Comparison:**

| Model Variant | Test ROC-AUC |
|---|---|
| Investor Model (includes sub_grade, int_rate) | 0.6968 |
| Underwriting Model (borrower-only features) | 0.6877 |
| sub_grade-alone baseline (no modeling) | 0.6797 |

**Insights:**
- The Investor Model improves on LendingClub's own sub-grade used alone by 0.0171 AUC.
- Of that, 0.0091 AUC is attributable specifically to including sub_grade/interest rate as model inputs.
- Borrower-provided information alone, without any institution-assigned risk indicators, retains the large majority of the model's overall predictive capability.
- This confirms the two-model split was the correct design choice: the Underwriting Model is a legitimate, nearly-as-strong option for screening new applicants who don't yet have an assigned grade.

### F. Business Impact & Insights

**Why Recall Matters?**
In credit risk prediction:
- False Negative: A risky borrower is incorrectly approved.
- False Positive: A good borrower is incorrectly flagged as risky.

Missing a defaulting borrower typically results in direct financial loss, making default recall an important metric alongside precision.

## 12. Key Findings

- The Investor Model identifies approximately 65% of defaulting loans at the default 0.5 threshold; the cost-optimized threshold of 0.40 shifts this trade-off deliberately based on estimated financial impact rather than a default assumption.
- ROC-AUC of ~0.70 indicates reasonable discrimination between good and bad borrowers, and the model beats both a naive baseline and LendingClub's own existing risk grade.
- Institution-assigned risk indicators provide a real but modest improvement over borrower attributes alone — most of the achievable predictive signal is already present in borrower-level data.
- The calibration check (Brier score 0.2198) and chronological validation approach were included specifically so that reported probabilities and performance figures can be trusted to generalize to genuinely new, future loans rather than only to the historical sample.

## 13. Key Result

The project developed a two-model Credit Risk Prediction System:
- an Investor Model (test ROC-AUC 0.6968) for scoring already-listed loans
- an Underwriting Model (test ROC-AUC 0.6877) for screening new applicants without requiring institution-assigned inputs
- Both outperform a naive baseline and LendingClub's own risk grade used alone
- Model selection, validation strategy, calibration, and decision threshold were each determined by an explicit, stated method rather than a default assumption, and the gap between the two models quantifies exactly how much of the achievable signal comes from borrower attributes versus institutional pricing

## 14. Dashboard (Power BI)

A two-page interactive Power BI dashboard titled "Credit Risk Prediction & Analysis," built directly on the model's output rather than historical aggregation alone:

**Page 1 — Executive Summary & Risk Drivers**
- KPI: Total Resolved Loans, Actual Default Rate, Average Loan Amount, Average Interest Rate
- Filters: grade, purpose, term
- Charts:
  - loan volume and default rate by grade
  - default rate by purpose
  - default rate by term
  - default rate by FICO score
- Includes a written executive summary and top-line finding

**Page 2 — Model-Driven Risk**
- KPI: Investor Model AUC, Underwriting Model AUC, sub-grade baseline AUC, average expected loss per loan
- Filters: grade, risk tier
- Charts:
  - actual vs model-predicted default rate by risk tier
  - total expected loss by grade
  - predicted risk tier distribution

## 15. Deployment & GitHub

- **GitHub:** https://github.com/AKHIL572/Credit-Risk-Prediction-System-using-Machine-Learning
- **Streamlit App:** https://credit-risk-prediction-system-using-machine-learning.streamlit.app/

## 16. Complexity Level

Advanced Level

## 17. Why this complexity level?

- 2.26 million row real-world dataset requiring memory-optimized, self-healing chunk-based processing
- Modular, production-style codebase (src/ package with separate, notebook-consistent modules)
- Full sklearn Pipeline architecture preventing data leakage, fit only on the training split
- Chronological (out-of-time) validation strategy, appropriate for a dataset spanning over a decade
- Explicit, statistically-verified model selection rather than an assumed choice
- Two-model architecture addressing a real conceptual problem — institution-assigned features being unavailable before the decision they're meant to inform
- Calibration checking and a cost-based decision threshold, not just ranking metrics
- Feature engineering with domain-specific financial ratios and documented outlier/data-quality handling
- Hyperparameter tuning with cross-validation
- Deployed Streamlit web application supporting both models, batch and single-applicant scoring
- Power BI dashboard connected directly to the trained model's predictions
- End-to-end project from raw data to deployment, with centralized configuration and a documented, tested pipeline

## 18. Additional Things Worth Mentioning

- Sample input file (sample_input.csv) included for easy app testing
- model_metrics.json saved automatically after training, including both models' metrics, baselines, calibration, and the selected decision threshold
- config.yaml used for centralized configuration — data/model paths, split parameters, and cost assumptions — read directly by the training pipeline rather than duplicated across files
- Feature engineering caps (winsorization thresholds) computed once on training data and persisted, so batch and single-record predictions at inference time reuse the same thresholds rather than recomputing them
- Documented limitations section covering selection bias in the underlying data and the illustrative nature of the cost assumptions used for threshold optimization

## 19. Data Pipeline / Workflow Note

> This project follows a standard ML data pipeline: chunked/memory-safe data ingestion → leakage-risk audit → EDA (with statistical testing) → data preprocessing & feature engineering → chronological (out-of-time) train/test split → baseline comparison → model training (Logistic Regression, Decision Tree, Random Forest) with explicit selection rule → hyperparameter tuning → calibration & cost-based threshold → business insights → deployment. Automation/deployment is handled via a **Streamlit app** (`app/app.py`) and modular **Python scripts** in `src/` (`data_loader.py`, `evaluate.py`, `feature_engineering.py`, `predict.py`, `preprocessing.py`, `train.py`), driven by a centralized `config.yaml`.

---

# Project 7

## 1. Title

Predictive Maintenance — Remaining Useful Life (RUL) Estimator for Turbofan Engines

## 2. Project Status

Completed

## 3. Project Type

Machine Learning | Regression | Time-Series Sensor Data | Deployed Web Application

## 4. Project Overview

An end-to-end predictive maintenance system that monitors turbofan engine health using real sensor data and predicts how many operational cycles remain before the engine fails.

The system ingests raw multi-variate sensor readings, engineers features, trains a Random Forest regression model, and serves predictions through an interactive Streamlit dashboard — allowing operators to inspect any engine at any point in its lifecycle.

## 5. Problem Discussed / Solved

- **Problem:** Unplanned engine failures in industrial and aerospace settings are costly and dangerous. Traditional time-based maintenance schedules either over-maintain (wasting resources) or under-maintain (risking failure).
- **Solution:** A data-driven model that continuously estimates the RUL of each engine from its sensor readings — enabling condition-based maintenance. Operators are alerted at Warning (≤40 cycles) and Critical (≤10 cycles) thresholds before failure occurs.

## 6. Dataset Details

| Property | Detail |
|---------------------|---------------------------------------------------------|
| Name | NASA CMAPSS — FD001 subset |
| Source | NASA Prognostics Data Repository |
| Rows | 20,631 |
| Columns | 27 (engine_id, cycle, 3 op settings, 21 sensors, RUL) |
| Engines | 100 (all run to failure) |
| Lifecycle | 128 to 362 cycles per engine (mean ~206) |
| Operating condition | Single (FD001) |
| Fault mode | Single |
| Missing values | None |
| Target variable | RUL (Remaining Useful Life) — regression |
| RUL range | 0 (failure) to 361 cycles |

**Key dataset characteristics discovered:**
- 7 sensors with near-zero variance (sensor_1, 5, 6, 10, 16, 18, 19) — dropped as non-informative
- op_setting_3 constant at 100.0 across all rows — dropped explicitly
- op_setting_1 and op_setting_2 retained despite small variance — genuine signal

## 7. File Structure

```text
PREDICTIVE_MAINTENANCE/
│
├── app/
│   └── app.py                  # Streamlit dashboard
├── data/
│   ├── train_FD001.txt         # Raw NASA data
│   └── train_FD001.csv         # Processed CSV with RUL column
├── models/
│   ├── rf_rul_model.pkl        # Trained Random Forest model
│   └── feature_columns.pkl     # Saved feature list for inference
├── notebooks/
│   ├── 1_data_understanding.ipynb
│   ├── 2_eda.ipynb
│   └── 3_preprocessing_and_modeling.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Data loading & schema validation
│   ├── preprocessor.py         # Feature engineering & RUL pipeline
│   ├── train.py                # Model training & evaluation
│   └── predict.py              # Inference pipeline
├── README.md
└── requirements.txt
```

## 8. Tools & Technologies Used

| Category | Tools |
|----------------------|------------------------------------------------------------------------------------------------------------|
| Language | Python 3 |
| Data handling | Pandas, NumPy |
| Modeling | Scikit-learn (RandomForestRegressor, LinearRegression, Ridge, Lasso, GridSearchCV, GroupKFold, Pipeline) |
| Visualization | Matplotlib, Seaborn |
| App / Dashboard | Streamlit |
| Model persistence | Joblib |
| Notebook environment | Jupyter Notebook |
| Version control | Git, GitHub |
| Deployment | Streamlit Community Cloud |

## 9. Steps Used (Main Work Done)

**Step 1 — Data Understanding (notebook 1)**
- Loaded raw space-delimited .txt file, assigned column names, saved as .csv
- Verified engine cycles all start at 1, no duplicates, zero missing values
- Computed RUL using max_cycle - current_cycle per engine
- Performed IQR-based outlier detection — identified that high outlier counts in sensor_9/14 are real degradation signals, not noise

**Step 2 — Exploratory Data Analysis (notebook 2)**
- Plotted engine lifecycle distribution (128–362 cycles)
- Identified dead sensors via standard deviation threshold (std < 0.01)
- Visualized sensor degradation trends over time for engines 1–3
- Plotted RUL distribution and correlation of each sensor with RUL
- Used invert_xaxis on sensor vs RUL plots to show degradation trajectory naturally
- Identified top 3 RUL-correlated sensors via absolute correlation ranking
- Checked operating condition effects on sensors

**Step 3 — Preprocessing & Modeling (notebook 3)**
- Applied RUL capping at 125 (piecewise linear approach) — removes noise from early healthy-engine cycles
- Dropped low-variance sensors programmatically and op_setting_3 explicitly
- Engine-wise train/test split (80/20 on engine IDs, not rows) — prevents data leakage
- Benchmarked Linear Regression, Ridge, Lasso as baselines
- Trained Random Forest (baseline: 100 trees, max_depth=10)
- Applied GroupKFold cross-validation (5-fold, grouped by engine_id) in both CV and GridSearchCV
- Hyperparameter tuning via GridSearchCV (n_estimators, max_depth, min_samples_split)
- Evaluated tuned model, plotted predicted vs actual RUL, feature importances
- Saved model and feature list to .pkl

**Step 4 — Production Code (src/)**
- data_loader.py — schema validation, dtype enforcement, clean error messages
- preprocessor.py — unified training/inference pipeline, transform("max") for RUL, explicit inference column alignment
- train.py — engine-wise split, GroupKFold CV, test evaluation on uncapped true RUL, n_jobs conflict handling
- predict.py — lazy model loading, smoke-test on mid-life engine row

**Step 5 — Dashboard (app.py)**
- Built full Streamlit app with engine selector, cycle slider, status classification, trajectory plot, sensor trend plot, and downloadable predictions

## 10. Methodology

- **Target Engineering:** RUL computed as max_cycle − current_cycle; capped at 125 during training (piecewise linear RUL) to focus the model on the degradation region
- **Feature Selection:** Variance-based filtering for sensors; explicit name-based removal for constant operational settings
- **Leakage Prevention:** Train/test split and cross-validation both performed at the engine level using GroupKFold — rows from the same engine never appear in both train and validation sets
- **Evaluation Honesty:** Test set evaluated against true uncapped RUL — metrics reflect real-world error, not the training approximation
- **Model Choice:** Random Forest chosen for its ability to capture non-linear sensor interactions without scaling, and for native feature importance output

## 11. Model Evaluation & Comparison

Multiple regression models were trained and evaluated to determine the most effective approach for predicting engine remaining life.

### A. Model Comparison Summary

| Model Category | Performance |
|--------------------------------|----------------------------|
| Linear Regression Models | Lower predictive accuracy |
| Random Forest Regressor | Strong performance |
| Tuned Random Forest Regressor | Best Overall Model |

### B. Key Findings

- Random Forest significantly outperformed traditional linear models.
- The model successfully captured the complex nonlinear relationships between engine sensor readings and degradation patterns.
- Compared with linear approaches, Random Forest achieved:
  - Approximately 17% improvement in RMSE
  - Approximately 25% improvement in MAE
- This demonstrates the advantage of ensemble learning methods for predictive maintenance applications.

### C. Hyperparameter Tuning

To further optimize model performance, hyperparameter tuning was performed on the Random Forest Regressor.

**Tuning Outcome:**

| Metric | Baseline RF | Tuned RF |
|--------|-------------|----------|
| RMSE | 17.016 | 16.999 |

**Analysis:**
- Hyperparameter optimization produced a small but measurable improvement.
- The baseline Random Forest was already performing near its optimal level.
- The tuned model was selected as the final production model due to its superior overall performance.

### D. Final Selected Model

- **Model:** Tuned Random Forest Regressor

**Final Performance Metrics:**

| Metric | Value |
|----------|--------|
| RMSE | 16.999 |
| MAE | 12.400 |
| R² Score | 0.8339 |

**Interpretation:**
- The model's predictions differ from the actual RUL values by approximately 12.4 cycles on average.
- An RMSE of approximately 17 cycles indicates strong predictive accuracy across the test dataset.
- The model explains 83.39% of the variance in engine remaining life, demonstrating a high level of reliability.

### E. Cross-Validation Performance

To evaluate generalization capability and prevent data leakage between engines, GroupKFold Cross-Validation was used.

**Cross-Validation Results:**

| Metric | Value |
|--------------------|--------|
| Mean RMSE | 19.01 |
| Standard Deviation | ± 1.27 |

**Why GroupKFold?**
- Multiple records belong to the same engine throughout its lifecycle.
- GroupKFold ensures that data from the same engine does not appear in both training and validation sets.
- This provides a more realistic estimate of real-world deployment performance.

**Cross-Validation Insight:**
- The low variation across folds indicates stable model performance.
- Results confirm that the model generalizes well to unseen engines.
- The validation RMSE remains close to the test-set RMSE, suggesting minimal overfitting.

### F. Business Impact & Insights

**Operational Benefits:**
The predictive maintenance system enables organizations to:
- Detect engine degradation early.
- Schedule maintenance proactively.
- Reduce unexpected equipment failures.
- Minimize maintenance costs and operational downtime.
- Improve fleet reliability and asset utilization.

**Engineering Insights:**
- Sensor data contains strong predictive signals related to engine wear and degradation.
- Ensemble models such as Random Forest effectively capture nonlinear failure patterns.
- Accurate RUL estimation supports condition-based maintenance rather than fixed maintenance schedules.

### G. Key Result

The project successfully developed a Remaining Useful Life (RUL) Prediction System for turbofan engines using a Tuned Random Forest Regressor.

The model achieved an RMSE of 16.999, MAE of 12.400, and R² Score of 0.8339, explaining over 83% of the variance in engine life.

Cross-validation results (19.01 ± 1.27 RMSE) further confirmed strong generalization capability, making the solution suitable for predictive maintenance and reliability engineering applications.

## 12. Key Insights & Results

- 7 of 21 sensors carry no useful signal — removing them reduces noise and model complexity
- RUL capping at 125 significantly improves model focus on the critical degradation window
- sensor_7, sensor_9, sensor_12 are the strongest degradation indicators with clear monotonic trends toward failure
- sensor_4 is highly important to the model but follows a non-linear, non-monotonic pattern — exploited through RF's tree splits
- Linear models establish a reasonable baseline but RF substantially outperforms them due to non-linear sensor interactions
- GroupKFold CV ensures reported metrics genuinely reflect performance on unseen engines, not unseen rows from known engines

## 13. Dashboard — What It Shows

Built with Streamlit, the dashboard includes:
- Engine selector — dropdown to choose any of the 100 engines
- Cycle slider — inspect predicted RUL at any point in the engine's lifecycle (defaults to 75% of lifecycle)
- 4 metric cards — Predicted RUL, Actual RUL with delta, Selected Cycle, Engine Status
- Status alert banner — color-coded HEALTHY / WARNING / CRITICAL with contextual message
- RUL Trajectory plot — predicted vs actual RUL across all cycles, with selected cycle marker, warning/critical threshold lines, and training cap line
- Sensor degradation trend plot — individual sensor readings over time with selected cycle marker
- Sensor insight panel — contextual explanation of the selected sensor's behavior
- Sensor readings table — all important sensor values at the selected cycle with predicted RUL
- CSV download button — download sensor values + predicted RUL for the selected cycle

## 14. Deployment & GitHub

- **GitHub:** https://github.com/AKHIL572/Predictive-Maintenance-System-Using-Sensor-Data-RUL-Prediction-
- **Live Streamlit App:** https://akhil572-predictive-maintenance-system-using-sensor--app-7n8j7k.streamlit.app/

## 15. Complexity Level

Advanced Level

## 16. Data Pipeline / Workflow Note

> This project follows a standard ML data pipeline: raw sensor data ingestion → data understanding → EDA (sensor variance & correlation analysis) → preprocessing & feature engineering (RUL capping, low-variance sensor removal) → engine-wise (leakage-safe) train/test split → model training (Linear Regression, Ridge, Lasso, Random Forest) → GroupKFold cross-validation → hyperparameter tuning (GridSearchCV) → evaluation on uncapped true RUL → deployment. Automation/deployment is handled via a **Streamlit app** (`app/app.py`) deployed on **Streamlit Community Cloud**, and modular **Python scripts** in `src/` (`data_loader.py`, `preprocessor.py`, `train.py`, `predict.py`).

---


# Project 8: Flipkart Product Pricing & Discount Analysis | End-to-End Data Analytics Project

## 1. Project Title
Flipkart Product Pricing & Discount Analysis | End-to-End Data Analytics Project

## 2. Project Status
Completed

## 3. Project Type
End-to-End Data Analytics Project

- Domain: E-Commerce Analytics
- Focus Areas:
  - Data Cleaning
  - Exploratory Data Analysis (EDA)
  - Feature Engineering
  - Business Analytics
  - Dashboard Development
  - Business Reporting
  - Data Visualization

## 4. Project Overview
- This project analyzes Flipkart's product catalogue to understand pricing strategies, discount patterns, category distribution, and catalogue quality.
- The project follows an end-to-end data analytics workflow, beginning with raw data preprocessing in Python, followed by Exploratory Data Analysis (EDA), feature engineering, business insight generation, and finally the development of an interactive Power BI dashboard.
- The analysis focuses on identifying pricing trends, discount behaviour across categories and price segments, product distribution, brand presence, and data quality issues.
- The final deliverables include detailed technical documentation, business reports, and an interactive dashboard designed to support business decision-making.

## 5. Problem Discussed / Solved
- The project addresses the following business problem:
  - How can Flipkart optimize product pricing, discount strategies, and catalogue quality to improve product positioning and support better business decisions?
- The analysis answers several business questions:
  - Which product categories dominate the catalogue?
  - Which categories contain the highest-priced products?
  - How are products distributed across different price ranges?
  - Which price segments receive the highest discounts?
  - Do expensive products receive larger discounts?
  - Which brands have the largest catalogue presence?
  - How reliable is the available brand and rating information?
  - What catalogue quality issues could affect business analysis?
  - The project provides business recommendations based on these findings.

## 6. Dataset Details
- Dataset Name: Flipkart Product Catalogue Dataset
- Source: Public Flipkart Product Dataset (2015–2016)
- Original Records: 20,000 product listings
- Cleaned Dataset: 15,827 product listings
- Original Features: Brand, Product Name, Product Category Tree, Product Rating, Retail Price, Discounted Price, Product URL, Product Specifications, Image, PID, Unique ID, Overall Rating, Crawl Timestamp, FK Advantage Indicator
- Features Used: Brand, Product Name, Product Category Tree, Product Rating, Retail Price, Discounted Price
- Engineered Features: Discount Percentage, Main Category, Sub Category, Price Bucket

## 7. File Structure
```
Flipkart_Product_Analysis/
│
├── data/
│   ├── flipkart_dataset.csv
│   └── cleaned_flipkart_dataset.csv
├── notebooks/
│   ├── 01_Data_Understanding_&_Cleaning.ipynb
│   ├── 02_Exploratory_Data_Analysis.ipynb
│   ├── 03_PowerBI_Dashboard_Preparation.ipynb
│   └── 04_Business_Recommendations_&_Executive_Summary.ipynb
├── dashboard/
│   ├── Flipkart_Dashboard.pbix
│   └── Flipkart_Dashboard.pdf
├── reports/
│   ├── 01_Business_Requirement_Document.md
│   ├── 02_Data_Cleaning_Report.md
│   ├── 03_EDA_Report.md
│   ├── 04_Business_Insights_Report.md
│   ├── 05_Dashboard_Documentation.md
│   ├── 06_Executive_Summary.md
│   ├── 07_Final_Project_Report.md
│   └── 08_Data_Dictionary.md
├── README.md
├── requirements.txt
└── LICENSE
```

## 8. Tools & Technologies Used
- Programming Language: Python
- Python Libraries: Pandas, NumPy, Matplotlib, Seaborn
- Business Intelligence: Power BI, DAX
- Development Tools: Jupyter Notebook, Git, GitHub
- Documentation: Markdown

## 9. Steps Used (Main Work Done)

### Phase 1 — Business Understanding
- Defined business problem
- Identified project objectives
- Selected relevant dataset
- Identified analytical scope

### Phase 2 — Data Understanding
- Imported dataset
- Selected relevant columns
- Examined dataset structure
- Checked data types
- Performed descriptive statistics
- Identified missing values
- Identified duplicate records

### Phase 3 — Data Cleaning
- Removed duplicate records
- Removed records with missing price values
- Converted product ratings to numeric
- Replaced missing brand values with "Unknown"
- Removed unnecessary columns
- Validated cleaned dataset

### Phase 4 — Feature Engineering
- Created new analytical features: Discount Percentage, Main Category, Sub Category, Price Bucket
- Prepared a dashboard-ready dataset for Power BI.

### Phase 5 — Exploratory Data Analysis
- Performed analysis on:
  - Product categories
  - Product pricing
  - Discount distribution
  - Price distribution
  - Brand distribution
  - Category-wise pricing
  - Category-wise discounts
  - Brand-wise discounts
  - Price buckets
  - Product ratings
  - Data quality
  - Relationship between retail price and discount percentage

### Phase 6 — Business Insight Generation
- Generated actionable business insights based on:
  - Catalogue composition
  - Pricing behavior
  - Discount strategy
  - Product segmentation
  - Brand presence
  - Data completeness

### Phase 7 — Dashboard Development
- Designed an interactive Power BI dashboard featuring:
  - KPI Cards
  - Interactive filters
  - Category analysis
  - Brand analysis
  - Pricing analysis
  - Discount analysis
  - Data quality indicators
  - Business insights
  - Business recommendations

### Phase 8 — Documentation
- Prepared comprehensive project documentation including:
  - Business Requirement Document
  - Data Cleaning Report
  - EDA Report
  - Business Insights Report
  - Dashboard Documentation
  - Executive Summary
  - Final Project Report
  - Data Dictionary
  - README

## 10. Methodology
```
Business Understanding
        ↓
Data Collection
        ↓
Data Understanding
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis
        ↓
Business Insight Generation
        ↓
Dashboard Development
        ↓
Business Recommendations
        ↓
Project Documentation
```

## 11. Key Insights & Results
- Cleaned dataset contains 15,827 products across 251 product categories.
- Average product discount is 39.41%.
- Clothing is the largest category, accounting for approximately 31% of product listings, indicating high competition and price sensitivity.
- Furniture has the highest average retail price among all categories.
- Nearly 47% of products are priced below ₹500, highlighting a strong mass-market focus.
- Lower-priced products generally receive higher average discounts than premium products.
- Approximately 29% of products have missing brand information, reducing the reliability of brand-level analysis.
- Only about 10% of products contain rating information, limiting meaningful customer satisfaction analysis.
- Discount percentages remain relatively consistent across most product categories, suggesting a broadly uniform pricing strategy.

## 12. Dashboard Created
- Yes — Interactive Power BI Dashboard
- Dashboard Includes
  - KPI Cards: Total Products, Average Discount (%), Average Retail Price, Total Identified Brands
  - Data Quality Indicators: Unknown Brand Percentage, Products with Rating Percentage, Total Categories
  - Interactive Filters: Main Category, Price Bucket, Brand
  - Charts:
    - Top Product Categories by Product Count
    - Average Retail Price by Category
    - Product Distribution Across Price Segments
    - Top 10 Brands by Product Count
    - Average Discount (%) by Main Category
    - Average Discount (%) by Price Bucket
    - Retail Price vs Discount Percentage (Scatter Plot)
    - Business Insight Panel
  - Highlights key analytical findings directly on the dashboard.
  - Business Recommendation Panel
  - Provides actionable recommendations derived from the analysis.

## 13. Deployment
- GitHub Link: https://github.com/AKHIL572/flipkart-pricing-discount-analysis

## 14. Complexity Level
Intermediate

## 15. Why Intermediate level?
- This project demonstrates competencies beyond basic data analysis by incorporating:
  - End-to-end analytics workflow
  - Data preprocessing
  - Feature engineering
  - Business-oriented exploratory analysis
  - Dashboard development using Power BI
  - DAX measures
  - Business recommendations
  - Comprehensive project documentation
  - GitHub repository organization

## 16. Additional Information

### Business Deliverables
- Business Requirement Document
- Data Cleaning Report
- Exploratory Data Analysis Report
- Business Insights Report
- Dashboard Documentation
- Executive Summary
- Final Project Report
- Data Dictionary

### Skills Demonstrated
- Business Understanding
- Data Cleaning
- Data Wrangling
- Feature Engineering
- Exploratory Data Analysis (EDA)
- Data Visualization
- Dashboard Design
- Business Intelligence
- DAX Calculations
- Analytical Thinking
- Business Recommendation Development
- Technical Documentation
- Git Version Control
- GitHub Project Management

### Project Limitations
- The dataset represents a static product catalogue (2015–2016) and does not include transactional data such as sales, orders, revenue, or customer interactions.
- Product ratings are available for only about 10% of listings, limiting customer sentiment analysis.
- Missing brand information (~29%) affects the completeness of brand-level insights.
- Time-series analysis, sales forecasting, and customer behavior analysis are not possible due to the nature of the dataset.


# Project 9: Supermarket Sales Analysis — End to End Excel Project

## 1. Title
Supermarket Sales Analysis — End to End Excel Project

## 2. Project Status
Completed

## 3. Project Type
Data Analysis & Interactive Dashboard — Microsoft Excel

## 4. Project Overview
- An end to end data analysis project performed entirely in Microsoft Excel on a real world supermarket sales dataset containing 1000 transactions across three branches in Myanmar.
- The project covers the complete data analytics workflow from raw data cleaning through exploratory analysis using pivot tables to a fully interactive business dashboard with KPI cards and slicers.

## 5. Problem Discussed & Solved
- Business Problem: As a supermarket chain operating across three cities, which product lines, branches, and customer segments are driving profitability and customer satisfaction — and how can the management optimise sales strategy based on data?
- Questions answered:
  - Which city branch generates the highest revenue?
  - Which product line drives the most gross income and customer satisfaction?
  - Do members contribute more revenue than normal customers?
  - Which time of day generates the highest sales?
  - Which payment method is most preferred by customers?
  - When does revenue peak across months?

## 6. Dataset Details
- Source: Kaggle — Supermarket Sales Dataset by Aungpyaeap
- Link: kaggle.com/datasets/aungpyaeap/supermarket-sales
- Size: 1000 rows, 17 columns
- Time Period: January 2019 to March 2019
- Branches: Three cities — Naypyitaw, Yangon, Mandalay
- Key columns: Invoice ID, Branch, City, Customer Type, Gender, Product Line, Unit Price, Quantity, Tax, Total, Date, Time, Payment, COGS, Gross Margin %, Gross Income, Rating

## 7. File Structure
```
supermarket_sales_analysis.xlsx
│
├── RawData          → Original dataset with added helper columns
├── Sheet1           → Pivot: Gross Income by City
├── Sheet2           → Pivot: Revenue by Customer Type
├── Sheet3           → Pivot: Product Line Performance
├── Sheet4           → Pivot: Monthly Revenue Trend
├── Sheet5           → Pivot: Payment Method Analysis
├── Sheet6           → Pivot: Time Period Sales Analysis
└── Dashboard        → Final interactive dashboard
```

## 8. Tools & Technologies Used
- Microsoft Excel — sole tool used end to end
- Pivot Tables & Pivot Charts
- Excel Slicers & Report Connections
- Excel Formulas — SUM, AVERAGE, COUNT, TEXT, MONTH, SUBTOTAL
- Chart types — Combo chart, Donut chart, Line chart, Bar chart, Column chart
- Cell formatting — Currency, Number formatting, Merge & Center
- KPI Card design using merged cells and formatting

## 9. Steps Used

### Step 1 — Data Understanding
- Loaded raw CSV into Excel and converted to structured table
- Understood all 17 columns and their business meaning
- Identified key metrics: gross income, rating, total, COGS

### Step 2 — Data Cleaning
- Checked for duplicates and removed them
- Verified data types — dates, numbers, text
- Extracted Month from date column for time based analysis
- Extracted Time Period (Morning, Afternoon, Evening) from time column
- Standardized formatting across columns

### Step 3 — Exploratory Analysis via Pivot Tables
- Created 6 separate pivot tables each answering a specific business question
- Used SUM, AVERAGE, COUNT aggregations across different dimensions

### Step 4 — Data Visualisation
- Created charts from each pivot table
- Built combo chart with secondary axis for product line performance
- Used donut chart for customer type distribution
- Used line chart for monthly trend
- Used horizontal bar chart for city revenue comparison

### Step 5 — Dashboard Creation
- Created dedicated dashboard sheet
- Designed KPI cards showing Total Customers, Total Sales, Gross Income, Average Rating
- Assembled all charts into a single professional layout
- Added four slicers — Month, Customer Type, City, Payment Method
- Connected slicers to pivot tables via Report Connections
- Added Key Insights panel with written business findings
- Applied consistent colour theme and professional formatting

## 10. Key Insights & Results
- Naypyitaw branch generates the highest gross income among all three cities
- Food and Beverages is the top performing product line — highest revenue AND highest customer rating of 7.15, making it the star category
- Member and Normal customers contribute almost equally to revenue (501 vs 499 customers) suggesting the membership program needs stronger incentives to differentiate value
- Afternoon is the peak sales period generating ₹148,023 — nearly double morning sales of ₹61,799
- January recorded the highest monthly revenue at ₹5,537, with a dip in February and recovery in March
- Ewallet is the most preferred payment method, followed closely by Cash and Credit Card
- Customer ratings are consistently between 6.7 and 7.15 across all product lines — indicating uniformly decent but not exceptional customer satisfaction

## 11. Dashboard Contains
- KPI cards: total customers, total sales, gross income, average rating
- Filters: month, customer type, city, payment
- Charts:
  - Revenue by city
  - Revenue by customer type
  - Product line performance
  - Monthly revenue trend
  - Sales by time period
  - Product profitability analysis

## 12. Deployment
- GitHub: https://github.com/AKHIL572/excel-sales-analytics-dashboard

## 13. Complexity Level
Intermediate Level

## 14. Why this complexity level?
- Goes beyond basic Excel usage into pivot tables, combo charts, secondary axis, and slicers
- Covers complete end to end workflow not just analysis
- Involves real business problem framing and insight generation
- Interactive dashboard with connected slicers shows practical Excel proficiency
- Not advanced because it doesn't use Power Query, macros, VBA, or complex DAX


# Project 10: Brazilian E-Commerce End-to-End Data Analysis using SQL and Power BI

## 1. Title
Brazilian E-Commerce End-to-End Data Analysis using SQL and Power BI

## 2. Project Status
Completed

## 3. Project Type
- Personal Portfolio Project
- Domain: E-Commerce / Retail Analytics
- Type: End-to-End Data Analytics Project

## 4. Project Overview
- A complete data analytics project analyzing **100,000+ orders** from **Olist** — Brazil's largest e-commerce marketplace that connects small and medium businesses to customers across all 27 Brazilian states through a single contract.
- Between 2016 and 2018, Olist experienced rapid growth — order volume grew from 329 orders in 2016 to over 54,000 orders in 2018, serving over 96,000 unique customers across the country.
- The project covers the entire data analytics pipeline from raw data import, cleaning, relational modeling, advanced SQL analysis to an interactive 4-page Power BI dashboard. The goal was to extract meaningful business insights about revenue, delivery performance, customer behavior and product performance — and provide actionable recommendations to address three critical business challenges identified during analysis.

## 5. Business Context & Problem Statement

### Business Context
Olist is Brazil's largest e-commerce marketplace connecting small businesses to customers nationwide. Despite strong revenue growth of R$13.59 Million, the business faces three critical challenges that require immediate attention:

### Critical Business Problems Identified

**Problem 1 — Declining Delivery Performance**
- On-time delivery rate dropped significantly:
  - 2016: 98.53% on time
  - 2017: 93.37% on time
  - 2018: 90.63% on time
- As order volume grew 300%, logistics quality declined. 7,827 orders were delivered late — directly impacting customer satisfaction and review scores.

**Problem 2 — Zero Customer Retention**
- Analysis reveals nearly 0% repeat customer rate. Every month the business depends entirely on acquiring new customers to generate revenue — making growth expensive and unsustainable long term.

**Problem 3 — Geographic Delivery Inequality**
- Customers in northern Brazilian states (AP, RR, AM) wait up to 29 days for delivery compared to the national average of 12.5 days — creating an unfair customer experience based on location.

### Business Questions Answered

| Problem | Analysis Done |
|---|---|
| Which states generate most revenue? | Geographic revenue analysis |
| Which product categories perform best? | Category revenue and sales analysis |
| How is delivery performance? | Late vs on-time delivery by state |
| What payment methods do customers prefer? | Payment distribution analysis |
| Which months have highest sales? | Monthly revenue trend analysis |
| Are customers returning? | Repeat customer rate analysis |
| Which sellers perform best? | Seller revenue ranking |
| What affects customer satisfaction? | Review score vs delivery analysis |

### Data Engineering Problems Solved
- Wrong datatypes at import causing data loss
- Decimal values truncated due to INT columns
- Date columns stored as TEXT
- Duplicate rows in geolocation data (1M → 19K)
- NULL and missing values across multiple tables
- Encoding issues in Portuguese city names
- Missing referential integrity between tables
- No indexes causing potential slow queries

## 6. Dataset Details

| Detail | Information |
|---|---|
| Source | Kaggle — Brazilian E-Commerce Public Dataset by Olist |
| Dataset Link | kaggle.com/datasets/olistbr/brazilian-ecommerce |
| Total Tables | 9 CSV files |
| Total Orders | 99,441 |
| Total Customers | 96,096 unique customers |
| Total Products | 32,951 |
| Total Sellers | 3,095 |
| Total Reviews | 99,224 |
| Time Period | September 2016 — August 2018 |
| Total Revenue | R$ 13.59 Million |
| Geography | Brazil — 27 states |

### Tables in Dataset

| Table | Rows | Description |
|---|---|---|
| `customers_raw` | 99,441 | Customer details and location |
| `orders_raw` | 99,441 | Order status and timestamps |
| `order_items` | 112,650 | Items within each order |
| `order_payments` | 103,886 | Payment details |
| `order_reviews_raw` | 99,224 | Customer reviews and scores |
| `products_raw` | 32,951 | Product specifications |
| `sellers_raw` | 3,095 | Seller details |
| `geolocation_raw` | 1,000,163 | ZIP code coordinates |
| `product_name_raw` | 71 | Portuguese to English translations |

## 7. File Structure
```
olist-ecommerce-sql-analysis/
│
├── sql/
│   ├── 1_create_table.sql
│   ├── 2_datatype_conversion.sql
│   ├── 3_data_cleaning.sql
│   ├── 4_table_relationship.sql
│   ├── 5_analysis_queries.sql
│   ├── 6_create_views.sql
│   ├── 7_statistical_analysis.sql
│   └── 8_rfm_analysis.sql
│
├── csv_exports/
│   ├── sales_summary.csv
│   ├── delivery_analysis.csv
│   ├── customer_analysis.csv
│   ├── product_analysis.csv
│   ├── payment_analysis.csv
│   └── customer_payment_analysis.csv
│
├── powerbi/
│   └── olist_dashboard.pbix
│
├── docs/
│   ├── DATA_DICTIONARY.md
│   ├── DATA_QUALITY_REPORT.md
│   ├── STATISTICAL_ANALYSIS.md
│   ├── KPI_FRAMEWORK.md
│   └── RFM_ANALYSIS.md
│
└── README.md
```

## 8. Tools & Technologies Used

| Tool | Version | Purpose |
|---|---|---|
| MySQL | 8.0 | Database creation, data storage |
| MySQL Workbench | 8.0 | Database management and query execution |
| Power BI Desktop | Latest | Dashboard and visualization |
| GitHub | — | Version control and portfolio hosting |

### SQL Concepts Used

| Concept | Where Used |
|---|---|
| DDL — CREATE, ALTER, DROP | Phase 1, 3 |
| DML — INSERT, UPDATE, DELETE | Phase 1, 2 |
| SELECT, WHERE, GROUP BY, ORDER BY | All phases |
| INNER JOIN, LEFT JOIN | Level 2+ |
| HAVING | Level 3+ |
| Subqueries in WHERE, FROM, SELECT | Level 4 |
| EXISTS, NOT EXISTS | Level 4 |
| CASE WHEN | Multiple phases |
| DATEDIFF, YEAR, MONTH, STR_TO_DATE | Phase 1+ |
| NULLIF, COALESCE | Phase 1-2 |
| RANK, ROW_NUMBER, DENSE_RANK | Level 5 |
| LAG, LEAD | Level 5 |
| Running Totals, Moving Averages | Level 5 |
| PARTITION BY | Level 5 |
| PRIMARY KEY, FOREIGN KEY | Phase 3 |
| CREATE INDEX | Phase 3 |
| CREATE VIEW | Phase 5 |
| ON DELETE RESTRICT, ON UPDATE CASCADE | Phase 3 |

## 9. Steps Used

### Phase 1 — Data Import & Datatype Correction
- What was done:
  - Created MySQL database `olist_ecommerce`
  - Created 9 tables with initial datatypes
  - Imported all 9 CSV files using `LOAD DATA LOCAL INFILE`
  - Identified datatype issues after import
  - Fixed DECIMAL columns — `price`, `freight_value`, `payment_value`
  - Fixed coordinate columns — `geolocation_lat`, `geolocation_lng` to DOUBLE
  - Re-imported 3 tables that lost decimal data due to INT columns
  - Converted 8 date/time TEXT columns to DATETIME using STR_TO_DATE()
  - Handled empty strings with NULLIF() during conversion
  - Optimized INT columns to TINYINT and SMALLINT UNSIGNED
  - Converted TEXT columns to proper VARCHAR with correct lengths
  - Checked MAX lengths before deciding VARCHAR sizes
- Key learning: Always define correct datatypes BEFORE importing data!

### Phase 2 — Data Quality Checks
- What was done:
  - Duplicate Check — Grouped all columns together to find true duplicates
  - Found `geolocation_raw` had 1,000,163 rows but only 19,015 unique zip codes
  - Created `geolocation_clean` table with averaged coordinates per zip code
  - NULL Check — Used SUM(CASE WHEN IS NULL) pattern for all 9 tables
  - Found `orders_raw` has expected NULLs in delivery date columns
  - Found `order_reviews_raw` has expected NULLs in comment columns
  - Found `products_raw` has 610 missing categories → labeled as 'unknown'
  - Verified 1,603 orders were placed for 'unknown' category products
  - Encoding Issues — Investigated UTF-8 encoding problems in city names
  - Documented as known Kaggle dataset limitation with mixed encoding
  - Unexpected Values — Checked all categorical columns for invalid entries
  - Found 3 orders with `not_defined` payment type → documented
  - Found 2 orders with 0 installments → documented
  - Found 31 coordinates outside Brazil's geographic boundaries → deleted
  - Recreated `geolocation_clean` after boundary cleanup
  - Referential Integrity — Used LEFT JOIN to verify all foreign relationships
  - All 5 key relationships verified — zero orphan records
  - Business Logic — Verified no impossible date combinations existed
  - Statistical Outliers — Checked extreme values in price, freight, weight
- Data Quality Report produced: 9 issues identified, 7 resolved, 2 documented as source data limitations. Overall data quality score: 82/100.

### Phase 3 — Relational Modeling
- What was done:
  - Identified Snowflake Schema structure across 9 tables
  - Added Primary Keys to all 9 tables
  - Used composite PKs for `order_items` and `order_payments`
  - Added auto-increment ID to `order_reviews_raw` due to duplicate review_ids
  - Added Foreign Keys with proper cascade rules:
    - `ON DELETE RESTRICT` — prevents accidental parent deletion
    - `ON UPDATE CASCADE` — automatically updates child references
  - Created 13 performance indexes on:
    - All foreign key columns
    - Frequently filtered columns (order_status, timestamps, review_score)
    - Geographic columns (customer_state, seller_state)
  - Tested all constraints:
    - DELETE test → correctly blocked by RESTRICT
    - INSERT test → correctly blocked invalid foreign key
    - Normal operations → verified all data intact
  - Added missing categories to `product_name_raw` for foreign key compliance

### Phase 4 — SQL Business Analysis
- Level 1 — Single Table Queries (22 queries):
  - Order status distribution
  - Monthly order trends
  - Late delivery count
  - Average delivery time
  - Total revenue
  - Payment method distribution
  - Review score distribution
  - Average review score
  - Product category sizes
  - Seller distribution by state
  - And 12 more queries
- Level 2 — JOIN Queries (17 queries):
  - Revenue by customer state
  - Orders by city
  - Revenue by payment type
  - Average payment by order status
  - Review score by order status
  - Best selling categories
  - Revenue by product category
  - Top sellers by revenue
  - Average delivery time by state
  - Late deliveries by category
  - And 7 more queries
- Level 3 — GROUP BY & Aggregations (15 queries):
  - Monthly revenue trends
  - Revenue growth rates
  - On-time delivery percentage by state
  - Revenue percentage by category
  - Seller percentage by state
  - Review score percentage distribution
  - Categories below average review score
  - Average freight by state
  - And 7 more queries
- Level 4 — Subqueries (12 queries):
  - Products above average price
  - Customers with more orders than average
  - Sellers above average revenue
  - Highest priced product per category
  - Customer with most orders per state
  - Categories with above average price AND review score
  - Revenue comparison score 5 vs score 1
  - States with above average customers AND sellers
  - And 4 more queries
- Level 5 — Window Functions (12 queries):
  - Seller revenue ranking using RANK()
  - Top 3 products per category using ROW_NUMBER()
  - Month over month revenue using LAG()
  - Running cumulative revenue using SUM() OVER()
  - Running revenue percentage
  - 3-month moving average
  - Sellers with spike months using AVG() OVER()
  - Best and worst month per state
  - And 4 more queries
- Additional Analysis
  - Statistical Analysis — Correlation analysis, distribution analysis, Pareto principle, percentile analysis and seasonal patterns
  - RFM Analysis — Customer segmentation using Recency, Frequency and Monetary scores producing 11 customer segments with marketing action recommendations

### Phase 5 — View Creation & Dashboard
- SQL Views Created:

| View | Purpose | Rows |
|---|---|---|
| `sales_summary` | Main revenue and sales dataset | 112,647 |
| `delivery_analysis` | Delivery performance with calculated fields | 96,476 |
| `customer_analysis` | Customer behavior metrics | 98,666 |
| `product_analysis` | Product and category performance | 32,951 |
| `payment_analysis` | Payment trends and installments | 103,886 |
| `customer_payment_analysis` | Combined customer and payment data | ~112,000 |

- Power BI Dashboard Built:
  - Imported 6 CSV exports
  - Created DAX measures for KPIs
  - Built 4 interactive pages with cross-filtering
  - Added slicers for Year, State, Category, Payment Type, Order Status

## 10. Methodology
```
Raw CSV Data (Kaggle)
        ↓
MySQL Database Creation
        ↓
Data Import (LOAD DATA LOCAL INFILE)
        ↓
Phase 1: Datatype Correction & Optimization
        ↓
Phase 2: Data Quality Checks & Cleaning
        ↓
Phase 3: Relational Modeling (PK, FK, Indexes)
        ↓
Phase 4: Business Analysis (SQL Levels 1-5)
        +  Statistical Analysis
        +  RFM Customer Segmentation
        ↓
Phase 5: SQL Views Creation
        ↓
CSV Export from Views
        ↓
Power BI Dashboard (4 pages)
        ↓
GitHub Upload + Documentation
```

## 11. Key Insights & Business Recommendations

### Revenue Insights

| Insight | Value |
|---|---|
| Total Revenue | R$ 13.59 Million |
| Best Month | November 2017 (Black Friday) — R$ 1.01M |
| Top Revenue State | São Paulo — R$ 5.20M (38%) |
| Top Revenue Category | Health & Beauty — R$ 1.26M |
| Top Seller Revenue | R$ 229,472 |
| Average Order Value | R$ 137.45 |

### Order & Delivery Insights

| Insight | Value |
|---|---|
| Total Orders | 99,441 |
| Delivery Success Rate | 97% |
| Average Delivery Time | 12.5 days |
| Late Deliveries | 8.11% (7,827 orders) |
| Worst Delivery State | Alagoas (AL) — 76.07% on time |
| Best Delivery State | Rondônia (RO) — 97.12% on time |
| Delivery Trend | 2016: 98.53% → 2017: 93.37% → 2018: 90.63% |

### Customer Insights

| Insight | Value |
|---|---|
| Total Unique Customers | 96,096 |
| Top Customer City | São Paulo — 15,540 customers |
| Repeat Customer Rate | Nearly 0% — major business challenge |
| Average Customer Spend | R$ 148.90 |
| Most Customers State | São Paulo — 43% of all customers |

### Product Insights

| Insight | Value |
|---|---|
| Most Sold Category | Bed/Bath/Table — 11,115 items |
| Highest Revenue Category | Health & Beauty — R$ 1.26M |
| Most Expensive Category | Computers — avg R$ 1,098 |
| Average Review Score | 4.09 / 5 |
| 5-Star Reviews | 57.78% of all reviews |
| Products with No Category | 610 (labeled unknown) |

### Payment Insights

| Insight | Value |
|---|---|
| Most Used Payment | Credit Card — 74% |
| Credit Card Revenue | R$ 10.97M (80% of total) |
| Average Installments | 2.85 |
| Most Orders Single Payment | 52,546 orders (1 installment) |
| Not Defined Payments | 3 orders (data quality issue) |

### Statistical Insights

| Finding | Value |
|---|---|
| Delay vs Review Correlation | -0.42 (moderate negative) |
| Fast delivery avg score | 4.52 stars |
| Critical delivery avg score | 2.87 stars |
| Top 20% sellers revenue share | 82.7% (Pareto confirmed) |
| Price distribution | Right skewed — median R$74.99 vs mean R$120.65 |
| Black Friday growth | November 2017 +52.1% spike |

### Key Business Recommendations

**Critical Priority:**
1. Fix delivery in northern states — Partner with regional carriers in AP, RR, AM to reduce 29-day average to under 15 days
2. Launch customer loyalty program — Even 5% repeat rate = R$679,582 additional annual revenue
3. Product recommendation at checkout — Increase items per order from 1.13 to 1.5 = 32% more revenue without new customers

**High Priority:**
4. Recruit sellers in North/Northeast Brazil — Reduce geographic concentration and improve delivery times
5. Promote high-margin categories — Watches/Gifts generates R$1.20M at rank #7 in volume — significant upside with promotion

**RFM Segment Actions:**
6. Win back At Risk customers — Good customers who are becoming inactive — personalized win-back campaign
7. Nurture Recent Customers — Convert first purchase to second within 60 days — after 2 purchases, 60% more likely to buy again

## 12. Dashboard Details

### Page 1 — Brazilian E-Commerce Executive Overview
- Subtitle: Sales Performance & Business KPI Summary (2016-2018)
- KPI Cards: Total Revenue, Total Orders, Total Customers, Average Order Value
- Filters: Year, Customer State, Product Category, Payment Type, Order Status
- Charts:
  - Monthly Revenue Trend (Line chart — 2016/2017/2018)
  - Top 10 Revenue Generating States (Bar chart)
  - Top 10 Product Categories by Revenue (Bar chart)
  - Order Status Distribution (Donut chart)

### Page 2 — Product Performance & Category Insights
- Subtitle: Product Revenue, Sales Volume & Customer Satisfaction Analysis
- KPI Cards: Total Product Revenue, Total Products Sold, Average Product Rating, Average Product Price
- Filters: Product Category, Review Score, Product Price
- Charts:
  - Top 10 Product Categories by Revenue (Bar chart)
  - Highest Rated Product Categories (Column chart)
  - Most Sold Product Categories (Treemap)
  - Most Expensive Product Categories (Bar chart)
  - Revenue vs Customer Satisfaction (Scatter plot)
  - Categories with Highest Freight Cost (Bar chart)

### Page 3 — Delivery Performance & Logistics Analysis
- Subtitle: Delivery Speed, Delay Trends & Customer Fulfillment Insights
- KPI Cards: Average Delivery Days, Late Delivery %, On-Time Delivery %, Average Delay Days
- Filters: Year, Customer State, Delivery Status, Actual Delivery Days
- Charts:
  - Average Delivery Days Trend (Line chart)
  - Delivery Status Distribution (Donut chart)
  - States with Slowest Deliveries (Clustered bar chart)
  - States with Highest Delivery Delays (Bar chart)
  - Estimated vs Actual Delivery Days (Combo chart)
  - Yearly Delivery Performance (100% Stacked bar)

### Page 4 — Customer & Payment Insights Analysis
- Subtitle: Customer Behavior, Payment Trends & Purchase Patterns
- KPI Cards: Total Customers, Average Customer Spend, Total Payment Value (incl. Freight), Average Installments
- Filters: Year, Customer State, Payment Type, Payment Installments, Total Spend
- Charts:
  - Payment Method Distribution (Donut chart)
  - Customer Acquisition Trend (Line chart)
  - Top Revenue Generating States (Bar chart)
  - Installment Usage Distribution (Column chart)
  - Top 10 Customers by Total Spending (Bar chart)
  - Revenue Contribution by Payment Type (100% Stacked column)

## 13. Documentation

| Document | Description |
|---|---|
| [README.md](README.md) | Main project overview and navigation |
| [Data Dictionary](docs/DATA_DICTIONARY.md) | Detailed description of all 9 tables, 6 views, column definitions and data quality notes |
| [Data Quality Report](docs/DATA_QUALITY_REPORT.md) | Complete assessment of 9 data issues found, resolutions applied and remaining limitations |
| [Statistical Analysis](docs/STATISTICAL_ANALYSIS.md) | Correlation analysis, distribution analysis, Pareto principle and seasonal patterns |
| [KPI Framework](docs/KPI_FRAMEWORK.md) | 32 business KPIs across 7 areas with current values, targets, gaps and monitoring frequency |
| [RFM Analysis](docs/RFM_ANALYSIS.md) | Customer segmentation using RFM methodology with 11 segments and marketing recommendations |

## 14. Deployment
- GitHub Repository: https://github.com/AKHIL572/olist-ecommerce-sql-analysis

## 15. Complexity Level
Advanced

## 16. Why Advanced Level?
- 9 table relational database design with Snowflake Schema
- Full data engineering pipeline from raw CSV to dashboard
- 78 SQL queries across 5 complexity levels
- Window functions with PARTITION BY, LAG, LEAD, Moving Averages
- Referential integrity with cascade rules
- 13 performance indexes
- Statistical analysis including correlation and Pareto analysis
- RFM customer segmentation with 11 segments
- Multi-page interactive Power BI dashboard
- Comprehensive documentation suite (6 documents)
- Real world dataset with real data quality issues


# Project 11: Spotify User Behavior Analysis | End-to-End Data Analytics Project

## 1. Project Title
Spotify User Behavior Analysis | End-to-End Data Analytics Project

## 2. Project Status
Completed
- End-to-end analytics workflow completed
- GitHub repository updated with the final version
- Power BI dashboard completed
- Excel analysis workbook completed
- Documentation (README) completed

## 3. Project Type
End-to-End Data Analytics Project
- Domain: Music Streaming / Product Analytics
- Category: Data Cleaning, Data Analysis, Business Intelligence, Product Analytics, Customer Analytics, Dashboard Development

## 4. Project Overview
- This project simulates a real-world Product/Growth Analytics scenario using a synthetic Spotify user dataset.
- The analysis begins with a raw dataset containing intentional data quality issues and follows the complete analytics lifecycle—from data quality assessment and cleaning to feature engineering, statistical validation, business analysis, and interactive dashboard development.
- The objective was to transform raw user behavior data into meaningful business insights related to user engagement, customer retention, subscription conversion, listening behavior, and product preferences while documenting every analytical decision.

## 5. Problem Discussed / Solved
The project addresses the following business problems:
- Identify customer churn patterns and retention opportunities.
- Analyze user engagement across demographics and subscription plans.
- Measure Premium subscription adoption.
- Evaluate advertisement conversion performance.
- Understand listening behavior across different user segments.
- Identify the most preferred Spotify features.
- Analyze user requests for future product features.
- Validate analytical findings using statistical significance testing.
- Build executive-level dashboards for business reporting.

## 6. Dataset Details
- Dataset Name: Raw Spotify User Dataset
- Dataset Type: Synthetic dataset designed to simulate real-world Spotify user behavior.
- Original Dataset
  - Total Records: 50,050
  - Total Columns: 18
- Data Types:
  - The dataset contains: Numerical columns, Categorical columns, Binary columns, Date column, Identifier column
- Original Columns: user_id, country, age, signup_date, subscription_type, subscription_status, months_inactive, inactive_3_months_flag, ad_interaction, ad_conversion_to_subscription, music_suggestion_rating_1_to_5, avg_listening_hours_per_week, favorite_genre, most_liked_feature, desired_future_feature, primary_device, playlists_created, avg_skips_per_day
- Data Quality Issues Identified:
  - Missing values
  - Duplicate records
  - Duplicate user IDs
  - Invalid age values
  - Future signup dates
  - Negative listening hours
  - Negative playlist counts
  - Inconsistent country names
  - Inconsistent device names
  - Outliers
  - Optional user feedback fields with missing responses
- Cleaning Outcome:
  - Final Records: 50,020
  - Duplicate Rows Removed: 30
  - Feature-engineered columns added
  - Clean analytical dataset generated

## 7. File Structure
```
Spotify User Behavior Analysis/
│
├── data/
│   ├── raw_spotify_dataset.csv
│   └── cleaned_spotify_dataset.csv
├── notebooks/
│   └── 01_data_cleaning.ipynb
├── excel/
│   └── cleaned_spotify_dataset.xlsx
├── dashboard/
│   ├── Spotify Analysis.pbix
│   └── Spotify Analysis.pdf
├── screenshots/
│   ├── page1_executive_overview.png
│   ├── page2_churn_retention.png
│   ├── page3_subscription_conversion.png
│   ├── page4_user_engagement.png
│   └── page5_product_insights.png
├── README.md
└── .gitignore
```

## 8. Tools & Technologies Used
- Programming: Python
- Python Libraries: Pandas, NumPy, SciPy
- Development Environment: Jupyter Notebook, VS Code
- Data Analysis: Microsoft Excel
- Dashboard: Power BI Desktop
- Version Control: Git, GitHub

## 9. Steps Used (Main Work Performed)

### Phase 1 – Data Understanding
- Imported raw dataset
- Performed initial inspection
- Reviewed dataset structure
- Generated descriptive statistics
- Identified missing values
- Detected duplicate records
- Checked data types

### Phase 2 – Data Quality Assessment
- Missing value analysis
- Duplicate detection
- Invalid value detection
- Timeline validation
- Outlier identification
- Inconsistent categorical value detection

### Phase 3 – Data Cleaning
- Removed duplicate rows
- Standardized categorical values
- Preserved meaningful missing values where appropriate
- Corrected inconsistent text formatting
- Flagged invalid signup dates
- Created indicator columns for missing values and outliers

### Phase 4 – Feature Engineering
- Created analytical helper columns including:
  - Age Group
  - Playlist Creator Category
  - Premium User Flag
  - Churn Flag
  - Conversion Flag
  - Missing Rating Flag
  - Invalid Signup Flag
  - Outlier Flags

### Phase 5 – Statistical Analysis
- Performed hypothesis testing using: Chi-Square Test, One-Way ANOVA
- Validated whether observed differences across segments were statistically significant.

### Phase 6 – Excel Analysis
- Created an Excel workbook containing:
  - Executive Summary
  - Cleaned Dataset
  - Cleaning Summary
  - Metric Definitions
  - Business Questions
  - Pivot Tables
  - Business Insights

### Phase 7 – Dashboard Development
- Built a multi-page interactive Power BI dashboard.

### Phase 8 – Documentation
- Created professional README
- Added dashboard screenshots
- Organized repository structure
- Updated GitHub repository
- Maintained project version history using Git

## 10. Methodology
```
Data Understanding
        ↓
Data Quality Assessment
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Statistical Validation
        ↓
Business Question Analysis
        ↓
Pivot Table Analysis
        ↓
KPI Development
        ↓
Dashboard Development
        ↓
Documentation
        ↓
Git Version Control
```

## 11. Key Insights & Results
- Total Users: 50K
- Active Users: 39K
- Inactive Users: 11K
- Overall Churn Rate: 22.25%
- Premium Users: 27K
- Premium Adoption Rate: 54.95%
- Advertisement Conversion Rate: 8.70%
- Average Weekly Listening Hours: 9.99
- Average Recommendation Rating: 3.64
- Average Playlists per User: 8
- Total Playlists Created: 400K
- User engagement remained relatively consistent across demographic segments.
- Statistical testing indicated that several observed visual differences were not statistically significant, emphasizing evidence-based interpretation over visual assumptions.
- Approximately 40% of users did not provide future feature requests, so feature-related conclusions represent responding users only.

## 12. Dashboard Details
A 5-page interactive Power BI dashboard was developed.

### Page 1 – Executive Overview
- KPI cards: Total Users, Active Users, Churn Rate %, Average Listening Hours, Ad Conversion Rate %
- Filters: Country, Age Group, Subscription Type, Favorite Gnere, Year
- Charts:
  - User Signup Trend over time
  - Subscription Distribution
  - Active vs Inactive Users by subscription
  - Top Countries
  - Average weekly Listening Hours by Age Group

### Page 2 – Customer Churn & Retention Analysis
- KPI Cards: Total Users, Inactive Users, Chrun Rate %, Avg Months Inactive, Retention Rate %
- Filters: Country, Age Group, Subscription Type, Favorite Genre, Year
- Charts:
  - Churn Rate by Age Group
  - Churn Rate by Subscription Type
  - Churn Rate by Country
  - Distribution of users by Months of Inactivity
  - Active vs Inactive Users by Age Group
  - Inactive Users by Favorite Genre

### Page 3 – Subscription & Conversion Analysis
- KPI Cards: Total Subscribers, Premium Users, Free Users, Premium Adoption Rate %, Ad Conversion Rate %
- Filters: Country, Age Group, Subscription Type, Favorite Genre, Year
- Charts:
  - Subscription Plan Distribution
  - Premium Adoption by Age Group
  - Ad Conversion Rate by Age Group
  - Subscription Conversion Funnel
  - Premium Adoption by Country
  - Active vs Inactive Users by Subscription Type

### Page 4 – User Engagement Analysis
- KPI cards: Avg Weekly Listening Hours, Avg Daily Skips, Total Playlist Created, Avg Playlists per User, Avg Recommendation Rating
- Filters: Country, Age Group, Subscription Type, Favorite Genre, Playlist Creator
- Charts:
  - Average Listening Hours by Age Group
  - Average Listening Hours by Subscript6ion Type
  - Average Daily Skips by Favorite Genre
  - Playlist Creator Categories Distribution
  - Average Weekly Listening Hours vs Average Playlist Created
  - Average Recommendation Rating by Genre

### Page 5 – Product Insights & Recommendations
- KPI Cards: Avg Recommendation Rating, Unique Music Genre, Most Popular Genre, Avaliable Spotify Features, Total Feature Preferences
- Filters: Country, Age Group, Subscription Type, Favorite Genre, Playlist Creator
- Charts:
  - Top Favorite Music Genres
  - Average Recommendation Ratings by Genre
  - Most Preferred Spotify Features
  - Most Requested Future Features
  - Feature Preferences by Subscription Type
  - Average Recommendation Ratings across Age Groups

## 13. Deployment / GitHub
- GitHub Repository: https://github.com/AKHIL572/spotify-user-insights-powerbi

## 14. Complexity Level
Intermediate → Advanced Data Analytics Project
- This project demonstrates:
  - Data Quality Assessment
  - Data Cleaning
  - Feature Engineering
  - Statistical Analysis
  - Business Intelligence Reporting
  - Excel Analytics
  - Power BI Dashboard Development
  - Business Storytelling
  - Git Version Control
  - Professional Project Documentation

It goes beyond a basic dashboard project by documenting the complete analytical workflow and validating findings using statistical tests.

## 15. Additional Information
- The project follows an end-to-end analytics pipeline from raw data to executive reporting.
- All cleaning decisions are documented with business justification rather than applying blanket transformations.
- Statistical significance testing was incorporated to distinguish supported findings from visually observed patterns.
- The Excel workbook serves as a complete business reporting document, including cleaning summaries, KPI definitions, business questions, pivot tables, and executive insights.
- The Power BI dashboard was rebuilt using the cleaned dataset to ensure consistency across all reported metrics.
- Git and GitHub were used throughout the project to manage updates, replace earlier project artifacts, and maintain a structured version history.
- The repository documentation, folder organization, and dashboard screenshots were finalized to make the project portfolio-ready and easy for recruiters or hiring managers to review.


# Project 12: Netflix Content Catalog Analysis & Discoverability Enhancement

## 1. Project Title
Netflix Content Catalog Analysis & Discoverability Enhancement

## 2. Project Status
Completed

## 3. Project Type
Business Analytics & Data Analytics Project (Exploratory Data Analysis + Power BI Dashboard + Business Analysis Documentation)
- This project combines:
  - Business Analysis (BA)
  - Data Analysis
  - Exploratory Data Analysis (EDA)
  - Dashboard Development
  - Business Documentation

## 4. Project Overview
- This project analyzes Netflix's content catalog to understand content distribution, growth trends, genre preferences, country-wise availability, ratings, duration patterns, and catalog composition.
- The project begins with analyzing the raw Netflix dataset, assessing data quality, performing exploratory data analysis, generating business insights, preparing optimized datasets for Power BI, and finally developing an interactive two-page Power BI dashboard.
- Apart from analytics, a complete Business Analyst documentation set was created, including Business Case, Project Charter, BRD, Stakeholder Analysis, User Stories, Process Maps, SRS, and UAT, making the project closely resemble an industry-style Business Analysis project.

## 5. Problem Discussed / Solved
- The project focuses on understanding Netflix's content catalog and identifying opportunities to improve content discoverability and support business decisions.
- The analysis addresses business questions such as:
  - How has Netflix's content library grown over time?
  - Does Netflix contain more Movies or TV Shows?
  - Which countries contribute the most content?
  - Which genres dominate the catalog?
  - What ratings are most common?
  - What are the movie duration and TV season distributions?
  - How has content been added over the years and months?
  - How can content distribution insights support acquisition and regional content strategy?
  - How can an interactive dashboard improve self-service analytics for business stakeholders?
- The BA documentation further frames these questions into business requirements, functional requirements, user stories, and acceptance criteria based on structured interviews with four Netflix subscribers.

## 6. Dataset Details
- Dataset Name: Netflix Movies and TV Shows
- Source: Kaggle
- Dataset Type: Structured CSV dataset
- Records: 8,807
- Columns: 12
- Memory Usage: Approximately 7.79 MB
- Features: show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description
- Target Variable: None
- Problem Type: Business Analytics / Exploratory Data Analysis
- Date Range:
  - Earliest content added: 2008-01-01
  - Latest content added: 2021-09-25

## 7. File Structure
```
Netflix/
│
├── BA-Documentation/
│    ├── Business Requirement Document (BRD)
│    ├── Business Case & Project Charter
│    ├── Process Maps (As-Is & To-Be)
│    ├── Stakeholder Analysis
│    ├── User Stories
│    ├── System Requirement Specification (SRS)
│    └── User Acceptance Testing (UAT)
├── dashboard/
│    └── netflix_dashboard.pbix
├── data/
│    ├── raw/
│    │     └── netflix_titles.csv
│    └── processed/
│          ├── netflix_dashboard.csv
│          ├── netflix_eda.csv
│          ├── country_table.csv
│          └── genre_table.csv
├── notebooks/
│    ├── 1_data_understanding.ipynb
│    ├── 2_data_quality_assessment.ipynb
│    ├── 3_exploratory_data_analysis.ipynb
│    ├── 4_business_insights.ipynb
│    └── 5_dashboard_data_preparation.ipynb
├── reports/
│    └── Netflix_dashboard.pdf
└── README.md
```

## 8. Tools & Technologies Used
- Programming: Python
- Libraries: Pandas, NumPy, Matplotlib, Seaborn, pathlib
- Visualization: Power BI
- Documentation: Microsoft Word, Microsoft Excel
- Version Control: Git, GitHub

## 9. Steps Used (Main Work Performed)

### Phase 1 – Business Analysis
- Defined project objectives
- Created Business Case
- Prepared Project Charter
- Identified stakeholders
- Conducted structured stakeholder interviews (4 Netflix subscribers)
- Created User Stories
- Prepared Business Requirement Document (BRD)
- Designed As-Is and To-Be Process Maps
- Created System Requirement Specification (SRS)
- Prepared User Acceptance Testing (UAT) document

### Phase 2 – Data Understanding
- Loaded raw dataset
- Studied dataset structure
- Analyzed columns
- Checked unique values
- Reviewed data types
- Performed summary statistics
- Checked duplicates
- Converted date fields
- Generated data quality report
- Identified missing values

### Phase 3 – Data Quality Assessment
- Visualized missing values
- Investigated missing-value patterns
- Analyzed director and country missingness
- Checked rating inconsistencies
- Identified mixed duration formats
- Investigated multi-value columns
- Defined cleaning strategy

### Phase 4 – Exploratory Data Analysis
- Content type analysis
- Rating distribution analysis
- Release year analysis
- Content added by year
- Content added by month
- Country distribution analysis
- Genre distribution analysis
- Movie duration analysis
- TV show season analysis
- Content type vs rating comparison

### Phase 5 – Business Insights
- Summarized findings
- Generated business insights
- Identified business impacts
- Proposed recommendations
- Documented project limitations
- Prepared final conclusions

### Phase 6 – Dashboard Data Preparation
- Handled missing values
- Created movie duration feature
- Created TV season feature
- Generated normalized country table
- Generated normalized genre table
- Created dashboard-ready dataset
- Exported processed datasets for Power BI

### Phase 7 – Dashboard Development
- Built two-page Power BI dashboard
- Created KPI cards
- Added interactive slicers
- Built charts
- Added navigation
- Published dashboard report (PDF export)

## 10. Methodology
1. Business Requirement Gathering
2. Stakeholder Analysis
3. Business Documentation
4. Data Understanding
5. Data Quality Assessment
6. Data Cleaning Strategy
7. Exploratory Data Analysis
8. Business Insight Generation
9. Dashboard Dataset Preparation
10. Power BI Dashboard Development
11. User Acceptance Testing
12. Final Documentation

## 11. Key Insights & Results
- Total titles analyzed: 8,807
- Movies: 6,131
- TV Shows: 2,676
- Movies dominate the Netflix catalog.
- Content additions increased significantly after 2015.
- The United States contributes the largest number of titles.
- TV-MA is the most common content rating.
- International Movies and Dramas are the most represented genres.
- Most movies have durations between 80–120 minutes.
- Most TV Shows consist of one season.
- Missing values are concentrated primarily in the director column (29.91%), while country and cast have around 9% missing values.
- The dataset contains no duplicate records.
- Multi-country and multi-genre fields were normalized for dashboard reporting.

## 12. Dashboard Created (What It Shows)
- Dashboard: Yes (Power BI)
- Pages: 2

### Page 1: Executive Overview
- KPI Cards: Total Titles, Movies, TV Shows, Total Countries, Total Genres
- Filters: Content Type, Rating, Year Added, Country, Genre
- Charts:
  - Movie vs TV Shows
  - Content Rating distribution
  - Content added over Time
  - Content added by months
  - Top 10 countries
  - Release year distribution
- Switches:
  - Executive Overview
  - Content Insights

### Page 2: Content Insights
- Title: Netflix Content Insights
- KPI Cards: Average Movie Duration, Average TV Seasons, Most Common Rating
- Filters: Content Type, Rating, Year Added, Country, Genre
- Charts:
  - Top 10 genres
  - Movie duration distribution
  - TV season distribution
  - Rating by content type
  - Country-wise content comparison
  - Country Distribution

## 13. Deployment / GitHub / Live Application
- GitHub Repository: https://github.com/AKHIL572/netflix-content-analysis-powerbi

## 14. Complexity Level
Intermediate Level

## 15. Reason for this complexity level
- End-to-end EDA workflow
- Data quality assessment
- Feature engineering for reporting
- Normalized dashboard data preparation
- Two-page interactive Power BI dashboard
- Complete Business Analysis documentation (Business Case, Project Charter, BRD, SRS, User Stories, Process Maps, UAT)
- Business requirement traceability from stakeholder interviews through dashboard implementation

## 15. Additional Project Details (Not Covered Above)
- A comprehensive Business Analysis lifecycle was documented, including Business Case, Project Charter, Stakeholder Analysis, User Stories, BRD, SRS, Process Maps, and UAT.
- Requirements were derived from structured interviews with four real Netflix subscribers and mapped through Business Requirements, Functional Requirements, System Requirements, and User Stories to maintain end-to-end traceability.
- Separate normalized country and genre tables were created by splitting multi-value fields, improving the Power BI data model and enabling more flexible filtering.
- Missing values were intentionally retained during the EDA stage for transparency and handled only during dashboard preparation by replacing selected fields with "Unknown".
- The dashboard was validated through 8 UAT test scenarios, with 7 fully passing and 1 partially meeting the intended hierarchical filtering behavior, which was documented as a future enhancement rather than being hidden.


# Project 13: Student Enrollment and Learning Management System

## 1. Project Overview

**Project Name:** Student Enrollment and Learning Management System
**Project Domain:** EdTech / E-Learning & Training Management
**Project Type:** Full-Stack Development Project + Independent QA Testing Cycle (Mixed: Full Stack Web Application + End-to-End Enterprise QA Project)
**Project Status:** Complete — Development functional; full STLC QA cycle executed, 4 defects found and fixed, regression-verified, automated
**My Role(s):** Developer (built the system) and QA Engineer (independently tested it end-to-end)
**Development Status:** All Node.js/Express REST APIs, Angular Standalone frontend components, MongoDB schemas, database seed scripts, and defect resolutions DEF-001 through DEF-004 are fully built, integrated, and verified.
**QA Status:** Complete Software Testing Life Cycle (STLC) executed — Requirement Analysis, Test Plan, Risk Matrix, RTM, Test Cases, Automated Postman Regression Suite, Defect Retesting, QA Metrics Dashboard, Test Summary Report, and Test Closure Sign-off.

### Abstract
The Student Enrollment System is an enterprise-grade client-server application designed to streamline training course management and student learning workflows. Built using a decoupled architecture with a Node.js/Express REST API backend, MongoDB (Mongoose) database, and an Angular 17+ dark glassmorphism single-page frontend, the system enforces Role-Based Access Control (RBAC) across three distinct user personas: Admin, Employee/Trainer, and Student.

The platform supports course discovery, real-time seat limitation handling, multi-method payment simulation (PayPal, Credit Card, UPI ID, Net Banking), step-by-step module completion tracking, and trainer assignment workflows. The project also demonstrates high software reliability through resolved production defect fixes (preventing seat loss, negative seat bounds, unpaid completion jumps, and database error leaks) validated by a complete QA suite and automated API test collection.

The application serves educational institutes and corporate training providers by digitizing student course discovery, seat-limited enrollments, fee payment processing, module-based learning progress tracking, and administrative instructor/course management. It covers the full lifecycle of course discovery, enrollment, simulated payment, content delivery, and progress tracking across the three user roles.

## 2. Tech Stack & Tools
- **Tech Stack:** Node.js, Express.js, MongoDB, Mongoose, JWT, Bcrypt, Angular (Standalone Components), RxJS
- **Testing Tools:** Postman, Newman (CLI automation), MongoDB Compass, Excel/Power BI-style dashboarding

## 3. Architecture & Methodology
- **Architecture:** Decoupled Client-Server REST API & Single Page Application (SPA)
- **Software Development Methodology:** Agile / Iterative Development with defect-driven refactoring
- **Testing Methodology:** Hybrid QA Approach combining Black-box Functional Testing, API Integration Testing, Boundary Value Analysis (BVA), Equivalence Partitioning (EP), Security/RBAC Verification, and Automated API Regression Testing

## 4. Core Modules / Features

### 4.1 Core Modules (system-level)
- Authentication and Role-Based Access Control — JWT-based auth with per-route role authorization (`protect` + `authorizeRoles` middleware)
- Course Management — Admin CRUD for courses, seat capacity, trainer assignment
- Employee Approval Workflow — self-registration with admin approval gate before login is permitted
- Enrollment and Payment — seat-limited enrollment, simulated multi-method payment (PayPal, Credit Card, UPI ID, Net Banking), atomic seat allocation
- Module and Progress Tracking — course content delivery gated by enrollment status, auto-completion at 100% progress
- Dashboards — separate aggregate views for Student, Employee, and Admin roles
- Course Roster — instructor/admin view of enrolled students with live progress and status

### 4.2 Student Portal Features
- Course Catalog Discovery — browse courses filtered by technology, with real-time seat availability and fee details
- Seat-Limited Checkout — enforces seat quotas during registration; prevents over-enrollment
- Multi-Method Simulated Payment — process course fees via PayPal, Credit Card, UPI, or Net Banking
- Interactive Learning Viewer — access module content, track atomic module completion, view automatic course progress percentages
- Profile management and enrolled-courses view with progress
- Enrollment + payment modal flow
- Change password

### 4.3 Employee / Trainer Portal Features
- Assigned Course Roster — view courses assigned by administrators and active student enrolments
- Student Mastery Progress — track progress percentages, mark student course completions, or cancel enrollments
- Instructor Profile & Security — manage trainer profile data and perform secure password updates
- Registration held in "pending" status until admin approval; login blocked until approved
- List of all employees

### 4.4 Admin Management Portal Features
- Full Course Lifecycle — create, edit course details, update seat limits, assign/reassign trainers, delete courses
- Module Management — create, structure, and order course learning modules
- Trainer Registration Approval — review and approve pending trainer registration requests; list pending employees
- Analytics & Reporting Dashboard — overview of system metrics (total students, active enrollments, completion rates)
- Admin registration is secret-key gated
- Change password

## 5. Project Structure
```
student_enrollment_system/
│
├── backend/
│   ├── config/
│   │   └── db.js                          # MongoDB connection via Mongoose
│   ├── controllers/
│   │   ├── adminController.js             # Admin auth, employee approval
│   │   ├── courseController.js            # Course CRUD & roster logic
│   │   ├── dashboardController.js         # Student/Employee/Admin dashboard aggregation
│   │   ├── employeeController.js          # Employee auth & profile management
│   │   ├── enrollmentController.js        # Enrollment & status management
│   │   ├── moduleController.js            # Learning module CRUD
│   │   ├── paymentController.js           # Payment processing & seat reservation
│   │   ├── progressController.js          # Module completion & progress calculation
│   │   └── studentController.js           # Student registration & login
│   ├── middleware/
│   │   └── authMiddleware.js              # protect + authorizeRoles
│   ├── models/
│   │   ├── adminModel.js
│   │   ├── courseModel.js
│   │   ├── employeeModel.js
│   │   ├── enrollmentModel.js
│   │   ├── moduleModel.js
│   │   ├── paymentModel.js
│   │   ├── progressModel.js
│   │   └── studentModel.js
│   ├── routes/
│   │   ├── adminRoutes.js
│   │   ├── courseRoutes.js
│   │   ├── dashboardRoutes.js
│   │   ├── employeeRoutes.js
│   │   ├── enrollmentRoutes.js
│   │   ├── moduleRoutes.js
│   │   ├── paymentRoutes.js
│   │   ├── progressRoutes.js
│   │   └── studentRoutes.js
│   ├── seed/
│   │   └── seed.js                        # Test data seed script (added during QA cycle)
│   ├── .env
│   ├── package.json
│   ├── server.js
│   └── start_server.bat
│
├── frontend/student-enrollment/            # Angular, standalone components
│   └── src/app/
│       ├── app.ts, app.html, app.routes.ts, app.config.ts
│       ├── components/
│       │   ├── admin-dashboard/
│       │   ├── employee-dashboard/
│       │   ├── student-dashboard/
│       │   ├── login/
│       │   └── course-roster/
│       ├── features/auth/register/
│       │   └── register.ts
│       ├── guards/
│       │   └── auth-guard.ts
│       └── services/
│           ├── auth.service.ts
│           └── enrollment.service.ts
│
├── qa-artifacts/                           # Full QA documentation suite
│   ├── Requirement Analysis.docx
│   ├── Test Plan Document.docx
│   ├── Risk_Matrix.xlsx
│   ├── Test_Case_Sheet_and_RTM.xlsx
│   ├── Defect_Log.xlsx
│   ├── Student_Enrollment_Regression_Suite.postman_collection.json
│   ├── Test_Summary_Report.docx
│   ├── QA_Metrics_Dashboard.xlsx
│   └── Test_Closure_Report.docx
│
└── README.md
```

## 6. Backend Detail

### 6.1 Models (Mongoose Schemas)

| Model | Key Fields / Rules |
|---|---|
| Student | name, email (unique), password (bcrypt pre-save hook), phone, age, gender, address, district, state, highestQualification, role (default 'student') |
| Employee | name, email (unique), password (bcrypt pre-save hook), qualification, specialization, experienceYears, skills[], status (enum: pending/approved, default pending), role (default 'employee') |
| Admin | name, email (unique), password (hashed manually in controller), phone, department, role (default 'admin') |
| Course | title, description, duration, fee, technology, startDate, seatsAvailable, assignedEmployee (ref Employee), createdBy (ref Admin) |
| Enrollment | student (ref), course (ref), status (enum: pending_payment/enrolled/completed/cancelled), unique compound index on {student, course} |
| Payment | student, course, enrollment (refs), amount, paymentMethod (enum: PayPal/Credit Card/UPI ID/Net Banking), transactionId, status |
| Module | course (ref), title, description, order, contentUrl, duration; unique compound index on {course, order} |
| Progress | student, course (refs), completedModules[] (ref Module), lastOpenedModule, completionPercentage, lastAccessedAt |

### 6.2 Controllers and Responsibilities
- `studentController.js` — register, login, get/update profile, change password
- `employeeController.js` — register (pending approval), login (blocked until approved), get profile, change password, list all employees
- `adminController.js` — register (secret-key gated), login, get profile, change password, approve employee, list pending employees
- `courseController.js` — create/get/update/delete course, get course roster (with employee-assignment check)
- `enrollmentController.js` — enroll in course, get my courses, get all enrollments, update enrollment status (with state-transition guard added during QA)
- `paymentController.js` — process simulated payment, atomic seat decrement (with payment-method pre-validation added during QA)
- `moduleController.js` — create/get/update/delete modules (with clean duplicate-order error handling added during QA)
- `progressController.js` — mark module complete, auto-update enrollment to 'completed' at 100%, get course progress
- `dashboardController.js` — student/employee/admin dashboard aggregation (MongoDB aggregation pipelines for enrollment status counts and monthly trends)

### 6.3 Routes and Middleware
- 9 route files map directly to the 9 controllers, mounted under `/api/students`, `/api/employees`, `/api/admin`, `/api/courses`, `/api/modules`, `/api/enrollments`, `/api/payments`, `/api/progress`, `/api/dashboard`
- `authMiddleware.js` exports `protect` (verifies JWT, attaches req.user based on role) and `authorizeRoles(...roles)` (blocks access if req.user.role is not in the allowed list) — applied per-route, e.g. `authorizeRoles('admin')` or `authorizeRoles('admin','employee')`
- `server.js` wires CORS (locked to `http://localhost:4200`), JSON body parsing, all 9 routers, and a 404 handler

## 7. Frontend Detail (Angular, Standalone Components)
- `auth.service.ts` — handles login/register per role, stores JWT in localStorage, decodes role via jwt-decode, builds Authorization headers for all authenticated requests
- `enrollment.service.ts` — dashboard data fetch helpers for student/employee/admin
- `auth-guard.ts` — route guard checking `isLoggedIn()` and matching the route's required role against the decoded token's role before allowing navigation
- `login.ts` / `register.ts` — role-selectable (student/employee/admin) forms; admin registration includes the admin secret field
- `student-dashboard.ts` — profile, enrolled courses with progress, course catalog browsing, enrollment + payment modal flow, course/module viewer with progress marking
- `employee-dashboard.ts` — profile, assigned courses with student status counts
- `admin-dashboard.ts` — platform stats, pending employee approvals, course CRUD (create/edit/delete), module creation, trainer assignment
- `course-roster.ts` — per-course student roster view with status update/cancel actions (admin/employee)
- `app.routes.ts` — route table gating each dashboard behind authGuard with a required role in route data
- Frontend design: custom vanilla CSS glassmorphic aesthetics (dark theme, curated HSL gradients, responsive cards, micro-animations) without relying on heavyweight third-party CSS utilities

## 8. How It Works — Frontend-Backend-Database Integration Flow
1. **Authentication & Access** — Users register as Students, Employees (Trainers), or Admins. JWT tokens containing role metadata are issued upon login and attached via `Authorization: Bearer <token>` headers to all REST requests. Route middleware (`protect`, `authorizeRoles`) guards backend endpoints.
2. **Course Enrollment & Seat Control** — A student selects a course; the backend creates an enrollment record with status `pending_payment`. Seat count is not permanently decremented until payment succeeds.
3. **Payment & Seat Allocation** — The student submits a valid payment method (PayPal, Credit Card, UPI ID, Net Banking). `paymentController.makePayment` validates input, checks ownership, atomically decrements `Course.seatsAvailable` via Mongoose (`findOneAndUpdate`), creates a Payment document, and updates the Enrollment status to `enrolled`. If Payment creation or the enrollment save fails after the seat is taken, compensating rollback logic (`$inc seatsAvailable: +1`) restores the seat.
4. **Learning & Progress Tracking** — Students access modules for enrolled courses. Completing a module triggers `completeModule`, which recalculates the completion percentage (`completedModules / totalModules * 100`). Upon reaching 100%, the enrollment status automatically transitions to `completed`.
5. **Response Handling** — The response flows back through Express to the Angular service's Observable subscriber, which updates component state (signals) and closes the payment modal.
6. **Admin & Trainer Governance** — Instructors monitor course rosters and student progress percentages; admins oversee trainer approvals, course content structure, seat counts, and system metrics.
7. **Persistence** — MongoDB persists all changes via Mongoose models, enforced by schema-level rules (enums, unique indexes) in parallel with controller-level validation.

Example concrete trace: Angular component `student-dashboard.ts` calls `HttpClient.post()` with the JWT attached via `AuthService.getAuthHeaders()` → request hits Express `server.js`, routed via `paymentRoutes.js` to `paymentController.js` → `authMiddleware.protect` verifies the JWT and attaches req.user; `authorizeRoles('student')` confirms the role → controller logic executes as above → response returns to Angular → MongoDB persists the changes.

## 9. QA Testing Cycle — Complete Details
An independent, full Software Testing Life Cycle (STLC) was executed against the completed application, treating it as a black-box + code-reviewed system under test — separate from the development effort.

### 9.1 QA Methodology / Phases Followed
- Requirement Analysis — formal requirement document (REQ-001 to REQ-040) derived from system behavior, with a Clarification Log documenting ambiguities and assumptions before test design began; deconstructs system scope into testable functional modules (Auth, Courses, Payments, Progress) and defines acceptance criteria
- Test Planning — scope, strategy, entry/exit criteria, roles, schedule; in-scope/out-of-scope boundaries; test environment setups; testing types (Functional, API, Security, Regression); milestone schedule
- Risk Assessment — modules scored by Impact x Likelihood, driving test coverage depth per module; analyzes system vulnerabilities (e.g., payment seat race conditions, unauthorized status jumps), assigns Probability and Impact ratings, and defines risk mitigation strategies
- Test Case Design — 93 test cases designed (Positive, Negative, Boundary, RBAC Security), each traced to a requirement via a live Requirement Traceability Matrix (RTM)
- Test Environment and Data Setup — isolated test database, repeatable seed script (Node.js/Mongoose)
- Test Execution (Manual) — 65 test cases executed directly against the running application via Postman
- Defect Logging — formal defect log with severity, root cause (code-level), and fix recommendation
- Defect Resolution — all 4 confirmed defects fixed in the actual codebase
- Regression Testing — each fix manually re-verified against a clean reseed before being marked closed
- Test Automation — self-contained Postman/Newman regression suite built and executed
- Reporting and Closure — Test Summary Report, QA Metrics Dashboard, Test Closure Report

### 9.2 QA Artifacts Produced

| File | Format | Purpose |
|---|---|---|
| Requirement Analysis.docx | Word | 40 formal requirements (REQ-001–040) + Clarification Log of ambiguities/assumptions; functional & non-functional requirements breakdown |
| Test Plan Document.docx | Word | Master QA test strategy: scope, entry/exit criteria, environment, schedule, testing risks |
| Risk_Matrix.xlsx | Excel | Module-level risk scoring (Impact x Likelihood) driving test coverage depth |
| Test_Case_Sheet_and_RTM.xlsx | Excel | 93 test cases with full execution results + live Requirement Traceability Matrix |
| Defect_Log.xlsx | Excel | 4 defects: root cause, severity, reproduction steps, fix recommendation, verification status (all Closed/Fixed) |
| Student_Enrollment_Regression_Suite.postman_collection.json | JSON | 22-request automated Postman/Newman regression suite, 37 assertions, with dynamic pre-request data generators |
| Test_Summary_Report.docx | Word | Execution stats, per-module results, defect summary, coverage, recommendation |
| QA_Metrics_Dashboard.xlsx | Excel | Visual dashboard: KPIs, test status by module, defect severity distribution, defect density, release readiness indicators |
| Test_Closure_Report.docx | Word | Formal sign-off: exit criteria verification, deliverables list, key findings, lessons learned, residual risk mitigation, production release recommendation |

### 9.3 Test Execution Results

| Metric | Value |
|---|---|
| Total test cases designed | 93 |
| Test cases executed | 65 |
| Pass (final, post-fix) | 65 / 65 (100%) |
| Open failures at closure | 0 |
| Requirements covered (RTM) | 40 / 40 (100%) |
| Test cases deferred (documented, not executed) | 28 — exploratory/concurrency sessions, DB-index checks, and 2 NFR sweep cases |
| Defects found | 4 (2 Critical, 1 High, 1 Low) |
| Defects fixed and regression-verified | 4 / 4 (100%) |
| Automated regression suite result | 22 / 22 requests passed, 37 / 37 assertions passed |

### 9.4 Defects Found — Full Detail

**DEF-001 (Critical) — Seat Permanently Consumed on Failed Payment**
- Where found: Manual API testing of the payment endpoint with an invalid paymentMethod value
- Root cause: `paymentController.js` decremented the course seat count (atomic `findOneAndUpdate`) BEFORE validating `paymentMethod` against the schema enum. If validation failed afterward, the seat was already gone with no rollback.
- Impact: Any failed payment attempt (invalid method, or any later step failing) permanently destroyed a seat with no recovery path — a real revenue/inventory-integrity bug.
- Fix: Reordered logic to validate `paymentMethod` before the seat decrement; added a try/catch with a compensating rollback (`$inc seatsAvailable: +1`) if `Payment.create()` or the enrollment save ever fails after the seat is taken.
- Verification: Reseeded test DB, retested invalid payment (seat count unchanged), then valid payment (seat correctly decremented by exactly 1). Confirmed fixed.

**DEF-002 (High) — Negative Seat Count Allowed on Course Update**
- Where found: Manual test of `PUT /api/courses/:id` with `seatsAvailable: -3`
- Root cause: `createCourse` validated `seatsAvailable >= 0`, but `updateCourse` had no equivalent check — a validation-parity gap between two code paths for the same field.
- Impact: Admin could push any course into a nonsensical negative seat count, corrupting displayed data and any logic assuming non-negative seats.
- Fix: Added the same 'seatsAvailable < 0' guard to `updateCourse` before saving.
- Verification: Retested PUT with negative seats post-fix — correctly rejected with 400 'Seats cannot be negative'.

**DEF-003 (Critical) — Enrollment Could Jump to 'Completed' Without Payment**
- Where found: Manual test of `PUT /api/enrollments/:id` setting status directly to 'completed' on a pending_payment (unpaid) enrollment
- Root cause: `updateEnrollmentStatus` only blocked manually setting status to 'enrolled' — it never validated the enrollment's CURRENT status before allowing a transition to 'completed', so `pending_payment → completed` succeeded unconditionally.
- Impact: An enrollment could show 'completed' despite the student never paying — a serious business-integrity gap, traced back to an ambiguity flagged during Requirement Analysis before any test was written.
- Fix: Added a state-transition guard — 'completed' is now only reachable when the enrollment's current status is 'enrolled'.
- Verification: Reseeded, retested on a fresh unpaid enrollment — correctly rejected with a clear payment-required message. Confirmed fixed.

**DEF-004 (Low) — Raw MongoDB Errors Leaked to API Clients**
- Where found: Manual test of duplicate module order (unique index collision)
- Root cause: Generic `catch(error)` blocks across multiple controllers returned raw `error.message` directly to the client, including full MongoDB duplicate-key text exposing internal database/collection/index names.
- Impact: Minor information disclosure; also poor API design (clients see internal implementation details instead of clean, actionable messages).
- Fix: Catch blocks updated across `moduleController.js`, `enrollmentController.js`, `studentController.js`, and `employeeController.js` to specifically detect `error.code === 11000` (duplicate key) and `error.name === 'CastError'` (invalid ID), returning clean, user-friendly messages; generic 500s reserved for genuinely unexpected errors.
- Verification: Retested duplicate module creation — clean message returned, no raw database text. Confirmed fixed.

### 9.5 Automated Regression Suite Detail
A self-contained Postman collection (importable, runnable via Newman CLI) with 22 requests across 5 folders: Auth and RBAC, Course Management, Enrollment and Payment, Enrollment Status, and Module Management. It registers its own fresh test data each run (dynamic timestamps), so it can be re-executed indefinitely without manual reseeding. Three folders are explicitly labeled as regression checks tied to DEF-001, DEF-003, and DEF-004, permanently locking in verification that these specific bugs cannot silently reappear. Final run: 22/22 requests passed, 37/37 assertions passed, 0 failures, ~3 second total execution time.

### 9.6 Key QA Findings / Lessons Learned
- Risk-based test design was validated in practice: both Critical defects (DEF-001, DEF-003) were found in the two modules ranked highest-risk during the Risk Assessment phase, before a single test case was written.
- One defect (DEF-003) traced directly back to an ambiguity raised during Requirement Analysis (documented in the Clarification Log) — proving that early requirement scrutiny genuinely catches real defects later.
- Automating regression checks immediately after each fix (rather than deferring all automation to the end) meant every fix had a permanent, repeatable verification the same day it was made.
- A reject-employee workflow gap was identified and deliberately treated as a product/requirements question for stakeholders, not logged as a defect — correctly distinguishing 'missing feature' from 'bug'.

## 10. Deployment & Setup
**Database Baseline Seed Script:** Located at `backend/seed/seed.js`. Running `node seed/seed.js` inside `backend/` creates a fresh test dataset populated with approved/pending trainers, student accounts, courses, modules, and enrollments without affecting production data.

**CLI Automated Test Execution:** The Postman regression suite in `qa-artifacts/` can be executed automatically via Newman in any CI/CD pipeline using:
```
newman run qa-artifacts/Student_Suite.postman_collection.json
```
## 11. Github
- repo : https://github.com/AKHIL572/student-enrollment-system

## 12. Additional Information

### Resume-Ready Summary
Suggested resume bullet points:
- Built a full-stack, role-based Learning Management System (Node.js, Express, MongoDB, Angular) supporting Student, Employee, and Admin workflows with JWT-based authentication and role-based access control.
- Independently executed a complete STLC QA cycle on the application: designed 93 test cases with 100% requirement traceability (40/40 requirements), risk-based coverage prioritization, and formal test planning documentation.
- Identified, root-caused, and fixed 4 defects (2 Critical, 1 High, 1 Low) through manual API testing, including a critical seat-integrity bug caused by non-atomic payment logic and a business-logic gap allowing unpaid enrollments to be marked complete.
- Built a self-contained, automated Postman/Newman regression suite (22 requests, 37 assertions) with dedicated regression checks for each confirmed defect, achieving a 100% pass rate on final execution.
- Produced a complete QA documentation suite — Requirement Analysis, Test Plan, Risk Matrix, Defect Log, Test Summary Report, QA Metrics Dashboard, and Test Closure Report — demonstrating end-to-end QA process ownership from planning through sign-off.

### One-line project summary for interviews
"I built a role-based enrollment platform, then stepped into a QA engineer role to independently test it end-to-end — designing risk-prioritized test cases, finding and fixing 4 real defects including a critical payment/seat-integrity bug, and automating regression checks so those fixes can never silently break again."


# Project 14: Smart AI Assistant

## 1. Project Overview
A multi-feature, AI-powered web application built with Streamlit and Google's Gemini API that provides intelligent assistance across multiple domains including general chat, food nutrition analysis, YouTube video summarization, and PDF document analysis.

**Project Status:** Completed

| Milestone | Status |
|---|---|
| Core application development | Complete |
| Chat with AI feature | Complete |
| Food Image Analyzer feature | Complete |
| YouTube Summarizer feature | Complete |
| PDF Document Chat feature | Complete |
| Bug fixes (PDF Unicode crash, JSON error handling) | Complete |
| Performance optimization (expanded context limits) | Complete |
| UI/UX enhancements (modern CSS styling) | Complete |
| Deployment readiness | Ready for deployment |

### Project Goal / Objective
The primary objective of this project is to develop a unified, intelligent AI assistant that consolidates multiple AI-powered utilities into a single, user-friendly web application. The specific goals include:
- Provide a conversational AI interface that maintains multi-turn context for general-purpose assistance.
- Enable nutritional analysis from food images using computer vision, with the ability to export detailed reports in PDF, Excel, and CSV formats.
- Summarize YouTube video content by extracting transcripts and generating concise, AI-powered summaries of key topics and takeaways.
- Enable intelligent document analysis from uploaded PDF files, with the ability to answer user questions by searching the document content and falling back to Google Search when necessary.
- Deliver a modern, responsive, and visually appealing UI that provides a premium user experience.

### Abstract
The Smart AI Assistant is a Streamlit-based web application that integrates Google's Gemini 2.5 Flash Lite generative AI model to deliver four distinct intelligent features within a single platform. The application leverages multimodal AI capabilities — including text generation, image understanding, and search grounding — to provide users with a versatile digital assistant.

The system accepts diverse inputs such as natural language text, food photographs, YouTube video URLs, and PDF documents. It processes these inputs through the Gemini API and returns structured, actionable outputs including conversational responses, nutritional breakdowns with downloadable reports, video content summaries, and document-grounded answers with web search fallback.

The application is built entirely in Python using the Streamlit framework for the frontend, with supporting libraries for PDF parsing (PyPDF2), YouTube transcript extraction (youtube-transcript-api), image processing (Pillow), and report generation (fpdf, pandas, openpyxl). The architecture follows a modular design with dedicated helper functions for each feature, centralized error handling, and retry logic for API resilience.

## 2. Tech Stack & Tools

### Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python-based web UI framework) |
| AI/ML Backend | Google Gemini 2.5 Flash Lite (Generative AI) |
| Image Processing | Pillow (PIL) |
| Document Parsing | PyPDF2 |
| Video Processing | youtube-transcript-api |
| Report Generation | fpdf (PDF), pandas + openpyxl (Excel/CSV) |
| Configuration | python-dotenv (.env files) |
| Version Control | Git + GitHub |

### Dependencies (requirements.txt)

| Package | Purpose |
|---|---|
| streamlit | Web application framework and UI |
| google-generativeai | Google Gemini API client SDK |
| python-dotenv | Environment variable management |
| pillow | Image processing and manipulation |
| PyPDF2 | PDF text extraction |
| youtube-transcript-api | YouTube video transcript extraction |
| fpdf | PDF report generation |
| pandas | Data manipulation for Excel/CSV exports |
| openpyxl | Excel file (.xlsx) writing engine |

## 3. Architecture & Methodology

### Development Approach
The project follows a modular, feature-driven development approach where each AI feature is implemented as an independent module within a single Streamlit application, sharing common utilities and configuration.

### Architecture
```
User Input (Text / Image / URL / PDF)
        ↓
┌─────────────────────┐
│   Streamlit UI      │  ← Frontend (sidebar navigation, file uploaders, chat)
│   (app.py)          │
└────────┬────────────┘
        ↓
┌─────────────────────┐
│  Helper Functions   │  ← Input preprocessing (transcript extraction, PDF parsing, image loading)
└────────┬────────────┘
        ↓
┌─────────────────────┐
│  Google Gemini API  │  ← AI processing (text generation, image understanding, search grounding)
│ (gemini-2.5-flash)  │
└────────┬────────────┘
        ↓
┌─────────────────────┐
│  Output Formatting  │  ← Response display, PDF/Excel/CSV report generation, metrics cards
└─────────────────────┘
```

### Error Handling Strategy
- **API Resilience:** `safe_generate_content()` implements retry logic with configurable max retries and delay.
- **Input Validation:** Environment variables are validated at startup; file types are restricted via Streamlit uploaders.
- **Graceful Degradation:** Each feature catches specific exceptions (e.g., TranscriptsDisabled, JSONDecodeError) and displays informative error messages rather than crashing.
- **Memory Protection:** PDF extraction enforces page and character limits to prevent excessive memory usage.

## 4. Project Functions and Features

### Feature 1: Chat with AI
- **Description:** A general-purpose conversational AI chatbot.
- **Input:** Natural language text via chat input.
- **Output:** AI-generated responses with full conversation context.
- **Key Implementation Details:**
  - Maintains multi-turn conversation history using st.session_state.
  - Uses Gemini's start_chat() API to pass conversation history for contextual responses.
  - Displays messages in a familiar chat interface with user/model message bubbles.

### Feature 2: Food Image Analyzer
- **Description:** Upload a food photo to receive a detailed nutritional breakdown with downloadable reports.
- **Input:** Food image (JPG/PNG/JPEG).
- **Output:**
  - Detailed per-item nutritional analysis (displayed on screen).
  - Summary metrics cards (Calories, Protein, Carbs, Fats, Health Score).
  - Downloadable reports in 3 formats: PDF, Excel (.xlsx), and CSV.
- **Key Implementation Details:**
  - Uses Gemini's multimodal capability (text + image input).
  - Makes two API calls: one for detailed human-readable analysis, one for structured JSON data.
  - The clean_for_pdf() function handles Unicode-to-Latin-1 encoding for safe PDF generation.
  - create_nutrition_pdf() generates a professional PDF report with food image, detailed analysis, and summary table.
  - create_nutrition_excel() generates a multi-sheet Excel workbook with auto-adjusted column widths.
  - create_nutrition_csv() generates a flat CSV file with all nutritional data.

### Feature 3: YouTube Summarizer
- **Description:** Paste a YouTube video URL to receive an AI-generated summary of the video content.
- **Input:** YouTube video URL (supports youtube.com/watch, youtu.be, and youtube.com/shorts formats).
- **Output:** Comprehensive summary with key points, main topics, and takeaways.
- **Key Implementation Details:**
  - Extracts video ID using regex patterns supporting multiple URL formats.
  - Uses the YouTubeTranscriptApi to fetch video transcripts (captions).
  - Supports up to 150,000 characters of transcript context for summarization.
  - Displays a progress bar during extraction and summarization phases.
  - Handles specific error cases: disabled transcripts, missing captions, unavailable/private videos.

### Feature 4: PDF Document Chat
- **Description:** Upload one or more PDF documents and ask questions. The AI searches the documents first, then falls back to Google Search if needed.
- **Input:** One or more PDF files + a natural language question.
- **Output:** AI-generated answer prefixed with [Document Search] or [Web Search Fallback] depending on the source.
- **Key Implementation Details:**
  - Supports multi-file upload with consolidated text extraction.
  - Extracts up to 150,000 characters per PDF and 300,000 characters consolidated.
  - Uses a search-grounded Gemini model (google_search_retrieval tool) for web fallback.
  - Memory-protected extraction with page and character limits to prevent overflow.

### Helper Functions

| Function | Purpose |
|---|---|
| safe_generate_content() | Wrapper for Gemini API with retry logic (2 retries, 1s delay) |
| extract_transcript_details() | YouTube transcript extraction with multi-format URL parsing |
| extract_pdf_text() | PDF text extraction with page/character limits |
| clean_for_pdf() | Unicode-to-Latin-1 text sanitization for FPDF compatibility |
| create_nutrition_pdf() | Professional PDF report generation |
| create_nutrition_excel() | Multi-sheet Excel workbook generation |
| create_nutrition_csv() | Flat CSV file generation |
| get_base64_of_bin_file() | Base64 encoding for embedding the logo in HTML |

## 5. Project Structure
```
AI_Assistant_Project/
│
├── app.py                 # Main application file (681 lines)
│                          # Contains all UI, logic, and feature implementations
│
├── requirements.txt       # Python package dependencies (9 packages)
│
├── .env                   # Environment variables (GOOGLE_API_KEY)
│
├── project_logo.png       # Custom application logo (~1.4 MB)
│
├── .gitignore             # Git ignore rules for env, venv, cache, OS files
│
├── venv/                  # Python virtual environment (local only)
│
└── __pycache__/           # Python bytecode cache (auto-generated)
```

## 6. Conclusion and Results
The Smart AI Assistant project has been successfully developed and tested as a fully functional, multi-feature AI-powered web application. The project achieves all of its stated objectives:

### Results Achieved
- **Conversational AI** — The chat feature provides contextual, multi-turn conversations powered by Gemini, maintaining full conversation history within a session.
- **Food Nutrition Analysis** — The image analyzer accurately identifies food items from photographs, provides detailed per-item nutritional breakdowns, and generates downloadable reports in three formats (PDF, Excel, CSV) without any encoding errors.
- **YouTube Video Summarization** — The summarizer successfully extracts and processes video transcripts (up to 150,000 characters) and delivers comprehensive AI-generated summaries with key takeaways.
- **Intelligent Document Analysis** — The PDF chat feature processes multi-file uploads (up to 300,000 characters consolidated), answers questions from document content, and intelligently falls back to Google Search when documents lack sufficient information.

### Key Technical Achievements
- **Multimodal AI Integration:** Successfully leveraged Gemini's text, image, and search-grounded capabilities within a single application.
- **Robust Error Handling:** Implemented retry logic, specific exception handling, and graceful degradation across all features.
- **Unicode-Safe Report Generation:** Resolved FPDF Latin-1 encoding limitations with a comprehensive text sanitization pipeline.
- **Scalable Context Windows:** Optimized input limits to take full advantage of Gemini's large context window capacity.

## 7. Deployment & Setup

**GitHub Repository:** https://github.com/AKHIL572/Smart-AI-Assistant
**Language:** Python
**Framework:** Streamlit

### How to Run Locally
1. Clone the repository
```
git clone https://github.com/AKHIL572/Smart-AI-Assistant.git
cd Smart-AI-Assistant
```
2. Create and activate virtual environment
```
python -m venv venv
.venv\Scripts\activate        # Windows
# source venv/bin/activate     # macOS/Linux
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Set up environment variables

Create a .env file with:
```
GOOGLE_API_KEY=your_google_api_key_here
```
5. Run the application
```
streamlit run app.py
```


# Project 15: Clinic Appointment Booking System — An End-to-End QA Automation Project

## 1. Project Overview

**Status:** Completed (QA cycle closed — v1.0 → v1.1)
**Role:** QA Analyst (also built the application under test)
**Type:** Manual + API Testing, Defect Lifecycle Management, Agile QA Process

### Purpose
This project demonstrates a complete, independent Software Testing Life Cycle (STLC) on a real, purpose-built application — not a public demo site — so that every requirement, test case, defect, and fix reflects genuine hands-on QA work.

A small Flask app (patient/doctor/admin roles, slot booking, cancellation, prescription upload) built specifically to be QA'd end-to-end — not a public demo site, so every bug found is genuinely yours to document.

### Goal / Objective
- Design and execute a full manual + API test cycle across a multi-role application (Patient / Doctor / Admin)
- Practice Agile QA workflow using Jira: Epics, Tasks, Bugs, Releases
- Find genuine defects through exploratory and structured testing, and carry each through a full defect lifecycle (Open → Fixed → Retest → Closed)
- Produce professional QA documentation: Test Strategy, Test Plan, RTM, Test Case Repository, Test Closure Report
- Build a reusable UI + API test automation framework skeleton (BDD, Selenium, Postman/Newman, CI)

### Problem Statement
Clinics need a system for patients to discover doctors by specialization, view available appointment slots, and book or cancel appointments — while doctors need visibility into their schedules, and admins need to onboard doctors and manage slot availability. This mirrors the domain of a prior Business Analyst project (BRD/SRS for an Ayurvedic clinic), giving continuity between requirements-gathering and hands-on QA work.

## 2. Tech Stack & Tools

| Category | Tools |
|---|---|
| Application | Python, Flask, Flask-SQLAlchemy, Flask-Login, SQLite, Jinja2, HTML/CSS |
| Test Management | Jira Cloud (Scrum Space, Epics/Tasks/Bugs, Releases, Labels) |
| Test Documentation | Microsoft Word (Test Strategy & Plan, Test Closure Report), Excel (RTM + Test Case Repository, formula-driven) |
| API Testing | Postman collection with scripted assertions, Newman (CLI runner) |
| UI Automation (framework built) | Selenium WebDriver, pytest-bdd (Gherkin), Page Object Model, Faker |
| Reporting / CI (framework built) | Allure reporting, GitHub Actions with an enforced pass-rate quality gate |
| Debugging / Diagnostics | Browser DevTools (DOM inspection), custom Python scripts for direct database inspection |

## 3. Methodology
1. Built the application (Flask + SQLite) with three roles, modeled on a real clinic-booking domain
2. Authored the Test Strategy & Test Plan (scope, approach, entry/exit criteria, defect severity/priority matrix, risks)
3. Set up Jira (Scrum-template Space), including Releases (v1.0 Baseline, v1.1 Post-Redesign Fixes) and Labels (in place of Components, which team-managed Spaces don't support)
4. Created 5 Epics — Authentication, Slot Booking, Doctor Dashboard, Admin Panel, API Layer
5. Created 3 Tasks per Epic (Design test cases, Set up test environment, Execute test cases) — 15 Tasks total
6. Performed exploratory black-box functional testing across all modules
7. Designed 41 formal test cases and built the RTM
8. Found and logged 3 genuine defects in Jira, each with steps to reproduce, severity, and priority
9. Investigated two suspected issues and ruled them out with direct evidence, documenting the reasoning rather than filing false tickets
10. Fixed all 3 confirmed defects, retested each, and closed the tickets
11. Released v1.1 in Jira once all linked defects were verified closed
12. Authored the Test Closure Report, evaluating exit criteria honestly — including what was *not* fully completed

## 4. Application Features

### Patient
- Register and log in
- Search doctors by specialization
- View a doctor's available appointment slots
- Book and cancel appointments
- Upload a prescription file against an appointment

### Doctor
- View assigned appointments
- Mark an appointment as complete

### Admin
- Create new doctor profiles
- Allocate appointment slots (date, time, capacity) per doctor
- View all doctors, their slots, and all system-wide appointments

### REST API
- All core actions (register, login, search, book, cancel) available as JSON endpoints with correct status codes, independently testable via Postman/curl

## 5. Project Structure
```
clinic-app/
├── README.md                      # This file — project reference document
├── run.py                         # Flask entry point
├── seed_data.py                   # Seeds admin/doctor/patient test accounts + sample slots
├── requirements.txt
├── app/
│   ├── __init__.py                 # App factory, blueprint registration
│   ├── models.py                   # User, DoctorProfile, Slot, Appointment (SQLAlchemy)
│   ├── routes/
│   │   ├── auth.py                 # Register, login, logout
│   │   ├── patient.py              # Search, book, cancel, upload prescription
│   │   ├── doctor.py               # View schedule, mark appointment complete
│   │   ├── admin.py                # Add doctor, add slot, view dashboards
│   │   └── api.py                  # JSON REST API mirroring the UI actions
│   └── templates/                  # Jinja2 HTML templates (one per page/role)
├── inspect_db.py                   # Diagnostic script — dumps raw Slot table
├── inspect_users.py                # Diagnostic script — dumps raw User table
└── docs/                           # All QA documentation deliverables
    ├── Test_Strategy_and_Test_Plan.docx
    ├── QA_Test_Cases_and_RTM.xlsx    # 41 test cases + RTM + Defect ID cross-references
    └── Test_Closure_Report.docx
```

**Note on defect tracking:** there is no separate "defect log" file. All 3 defects (CQA-1, CQA-2, CQA-3) are tracked as the source of truth in **Jira**, and cross-referenced in the `Defect ID` column of `QA_Test_Cases_and_RTM.xlsx` and summarized in `Test_Closure_Report.docx`. See the Jira Workflow Evidence section below for screenshots of the actual tickets.

## 6. QA Testing Cycle

### What Was Actually Tested and Done
- Exploratory, black-box functional testing across all modules by hand, before formal test case design
- 41 formal manual/API test cases designed and executed, tracked in a Requirement Traceability Matrix (RTM) with live formulas
- Full authentication testing: valid/invalid login, weak passwords, duplicate emails, role-based redirection, logout/session handling
- Full booking-logic testing: valid booking, full-capacity slots, past-date slots, duplicate bookings by the same patient, cancellation, and re-booking after cancellation
- Doctor dashboard testing: appointment visibility, marking appointments complete
- Admin panel testing: doctor creation, slot allocation, duplicate-email handling
- REST API testing: status codes and validation across register/login/list/book/cancel endpoints, plus role-boundary enforcement (a patient cannot reach admin-only routes)
- Two suspected issues were investigated and ruled out using direct evidence — browser DevTools DOM inspection, and a custom database-inspection script — rather than being assumed to be defects
- 3 genuine defects were found, root-caused, fixed, retested, and formally closed
- A post-redesign regression check was performed and caught a real regression (duplicated "Dr." title) before closure

**Explicitly not covered this cycle:** payment processing, performance/load testing, security/penetration testing, and email/SMS notifications (mocked out) — see Known Limitations below.

### Defects Found, Fixed, and Closed

| Defect ID | Summary | Severity | Status |
|---|---|---|---|
| CQA-1 | Duplicate booking attempt on a full-capacity slot returned a misleading "slot is fully booked" error instead of "you already have a booking" | Medium | Closed |
| CQA-2 | Admin dashboard did not display existing slots per doctor, only a link to add new ones | Medium | Closed |
| CQA-3 | Doctor name displayed with a duplicated "Dr." prefix after a UI redesign (regression) | Low | Closed |

### Deliverables Produced
- [Test Strategy & Test Plan](docs/Test_Strategy_and_Test_Plan.docx)
- [Requirement Traceability Matrix + 41 Test Cases](docs/QA_Test_Cases_and_RTM.xlsx) (Excel, formula-driven)
- Jira project: 5 Epics, 15 Tasks, 3 Bugs (all closed), 2 Releases
- [Test Closure Report](docs/Test_Closure_Report.docx)
- The application itself (this repository)
- A UI + API test automation framework skeleton (BDD, Selenium, Postman/Newman, CI pipeline)

### Jira Workflow Evidence
*Screenshots below — since the Jira site itself is private, these serve as proof of the workflow instead of a live link.*
- **Backlog/Board:** all 5 Epics with 15 Tasks nested, marked Done — [Board](docs/screenshots/board.png)
- **Sample Bug ticket (CQA-1):** description, severity, steps to reproduce, status — [Bug CQA-1](docs/screenshots/cqa-1.png)
- **Releases page:** v1.0 and v1.1, both marked Released — [Releases](docs/screenshots/releases.png)

### Key Skills Demonstrated
- STLC / Agile QA process ownership from requirement analysis through closure
- Manual black-box and exploratory testing
- Test case design, RTM construction, defect severity/priority triage
- Defect lifecycle management in Jira (Open → Fixed → Retest → Closed)
- API testing with status-code-level assertions
- Root-cause investigation using DevTools and direct database inspection — distinguishing genuine defects from environmental/data issues
- Regression testing awareness (catching a defect introduced by a later UI change)
- Professional QA documentation aligned to real-world formats

## 7. Known Limitations
- Slot creation time fields lack format validation (no AM/PM, no HH:MM enforcement) — identified and documented, not fixed this cycle
- Prescription-upload and doctor-cross-boundary test cases were designed but not executed this cycle
- The automation framework has not yet been re-targeted from its original reference site to this application's own UI/API and verified running in CI

## 8. Status Summary
Complete through Test Closure and ready to present as a finished, closed QA cycle.

## 9. Deployment & Setup

### Setup
```bash
pip install -r requirements.txt
python seed_data.py     # creates clinic.db with sample doctors/slots
python run.py            # serves on http://127.0.0.1:5000
```

### Seeded Test Accounts

| Role | Email | Password |
|---|---|---|
| Admin | admin@clinic.test | AdminPass123 |
| Doctor | anjali@clinic.test | DoctorPass123 |
| Patient | patient@clinic.test | PatientPass123 |

### Links
GitHub Repo: https://github.com/AKHIL572/clinic-appointment-booking-qa
