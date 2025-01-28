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
|-- admin/           
|-- assets/             
|-- heart/                
|-- media/              
|-- users/           
|-- db.sqlite3                 
|-- manage.py                    

## Project Workflow

1. Data Collection and Processing
   - Dataset preprocessing to clean and format data.
   - Splitting the data into training (70%) and testing (30%) sets.
2. Model Training
   - Training ML models: Logistic Regression, SVM, KNN, and Decision Tree.
3. Model Evaluation
   - Evaluating accuracy for each model.

## How to Run the Project  
1. Clone this repository:  
   ```bash
   git clone <https://github.com/KeerthiP08/Heart-disease>
2. Navigate to the project directory:
   ```bash
   cd <project-folder>
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Apply migrations:
   ```bash
   python manage.py migrate
5. Run the server:
   ```bash
   python manage.py runserver
6. Open the application in your browser:
   http://127.0.0.1:8000

## Results

- Achieved **85% prediction accuracy**, with Logistic Regression being the best-performing model.
- Early prediction facilitates timely interventions and improved treatment outcomes.

## Future Enhancements
- Train on diverse datasets for better generalization.
- Predict different types of cardiovascular diseases.
- Provide personalized health recommendations.
- Integrate advanced machine learning models.

## Contributing

Contributions are welcome!
To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
4. Push the changes:
   ```bash
   git push origin feature-name
5. Create a pull request.

## Contact

For any inquiries or suggestions, feel free to reach out:

Email: keerthireddy0508@gmail.com
