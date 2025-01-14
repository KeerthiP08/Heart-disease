# Heart Disease Prediction Using Machine Learning

## Overview

This project aims to provide a web-based tool for predicting heart disease using machine learning techniques. It evaluates various ML models to assist doctors in early detection and decision-making, potentially reducing severe medical consequences.

## Features

- **Prediction Models:** Logistic Regression, SVM, KNN, and Decision Tree.
- **Web-based Interface:** User-friendly platform for prediction results.
- **Data Analysis:** Utilizes patient data with 14 key attributes for prediction.

## Technologies Used

- **Front-End:** HTML, CSS
- **Back-End:** Python (Django), MySQL

## Dataset

The dataset is present in the media folder. It contains patient information, including attributes such as:

- Age
- Sex
- Chest pain type
- Resting blood pressure
- Serum cholesterol
- Fasting blood sugar
And more...

Target values:

- '1' - Presence of heart disease
- '0' - Absence of heart disease

## Project Structure

admin/
assets/
heart/
media/
users/
db.sqlite3
manage.py

## How to Run the Project  
1. Clone this repository:  
   ```bash
   git clone <repository-url>
2. Navigate to the project directory:
   cd <project-folder>
3. Install the required dependencies:
   pip install -r requirements.txt
4. Apply migrations:
   python manage.py migrate
5. Run the server:
   python manage.py runserver
6. Open the application in your browser:
   http://127.0.0.1:8000
   
## Output Screens

**Home Page:** Interface for entering patient details.
**Prediction Page:** Displays the prediction result (e.g., "Heart Disease Detected" or "No Heart Disease Detected").
**Accuracy Comparison:** Graph or table showing accuracy metrics for the ML models used.
**Admin Panel:** Example of the admin interface for managing users and data.

## Results

- Achieved **85% prediction accuracy**, with Logistic Regression being the best-performing model.
- Early prediction facilitates timely interventions and improved treatment outcomes.

## Future Enhancements
- Train on diverse datasets for better generalization.
- Predict different types of cardiovascular diseases.
- Provide personalized health recommendations.
- Integrate advanced machine learning models.
