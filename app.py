import pandas as pd
from flask import Flask, request, render_template
import pickle
import traceback

app = Flask(__name__)

# Load data and model at startup
try:
    df_1 = pd.read_csv("first_telc.csv")
    model = pickle.load(open("model.sav", "rb"))
    expected_features = model.feature_names_in_
except Exception as e:
    print(f"Error loading data or model: {str(e)}")
    raise

def validate_and_convert_input(form_data):
    """Validate and convert form inputs to proper types with error handling"""
    validated = {}
    errors = []
    
    # Define field specifications
    field_specs = {
        'SeniorCitizen': {'type': 'int', 'default': 0, 'required': False},
        'MonthlyCharges': {'type': 'float', 'default': 0.0, 'required': True},
        'TotalCharges': {'type': 'float', 'default': 0.0, 'required': True},
        'tenure': {'type': 'int', 'default': 0, 'required': True},
        # Categorical fields
        'gender': {'type': 'str', 'default': '', 'required': True},
        'Partner': {'type': 'str', 'default': '', 'required': True},
        'Dependents': {'type': 'str', 'default': '', 'required': True},
        'PhoneService': {'type': 'str', 'default': '', 'required': True},
        'MultipleLines': {'type': 'str', 'default': '', 'required': True},
        'InternetService': {'type': 'str', 'default': '', 'required': True},
        'OnlineSecurity': {'type': 'str', 'default': '', 'required': True},
        'OnlineBackup': {'type': 'str', 'default': '', 'required': True},
        'DeviceProtection': {'type': 'str', 'default': '', 'required': True},
        'TechSupport': {'type': 'str', 'default': '', 'required': True},
        'StreamingTV': {'type': 'str', 'default': '', 'required': True},
        'StreamingMovies': {'type': 'str', 'default': '', 'required': True},
        'Contract': {'type': 'str', 'default': '', 'required': True},
        'PaperlessBilling': {'type': 'str', 'default': '', 'required': True},
        'PaymentMethod': {'type': 'str', 'default': '', 'required': True}
    }
    
    for field, spec in field_specs.items():
        value = form_data.get(field, '').strip()
        
        # Check for required fields
        if spec['required'] and not value:
            errors.append(f"{field} is required")
            validated[field] = spec['default']
            continue
            
        # Convert based on type
        try:
            if spec['type'] == 'int':
                validated[field] = int(value) if value else spec['default']
            elif spec['type'] == 'float':
                validated[field] = float(value) if value else spec['default']
            else:  # string
                validated[field] = value if value else spec['default']
        except ValueError:
            errors.append(f"Invalid value for {field}")
            validated[field] = spec['default']
    
    return validated, errors

def preprocess_input(validated_data, expected_features):
    """Preprocess the input data to match model requirements"""
    # Create DataFrame
    new_df = pd.DataFrame([validated_data.values()], columns=validated_data.keys())
    
    # Combine with existing data
    df_2 = pd.concat([df_1, new_df], ignore_index=True)
    
    # Process tenure into groups
    labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
    df_2['tenure_group'] = pd.cut(df_2.tenure.astype(int), 
                                 range(1, 80, 12), 
                                 right=False, 
                                 labels=labels)
    
    # Create dummy variables
    categorical_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
                      'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                      'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                      'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure_group']
    
    df_processed = pd.get_dummies(df_2, columns=categorical_cols)
    
    # Align with expected features
    for feature in expected_features:
        if feature not in df_processed.columns:
            df_processed[feature] = 0
    
    return df_processed[expected_features].tail(1)

@app.route("/")
def loadPage():
    return render_template('home.html', query="")

@app.route("/", methods=['POST'])
def predict():
    try:
        # Collect form data
        raw_form_data = {
            'SeniorCitizen': request.form.get('query1', ''),
            'MonthlyCharges': request.form.get('query2', ''),
            'TotalCharges': request.form.get('query3', ''),
            'gender': request.form.get('query4', ''),
            'Partner': request.form.get('query5', ''),
            'Dependents': request.form.get('query6', ''),
            'PhoneService': request.form.get('query7', ''),
            'MultipleLines': request.form.get('query8', ''),
            'InternetService': request.form.get('query9', ''),
            'OnlineSecurity': request.form.get('query10', ''),
            'OnlineBackup': request.form.get('query11', ''),
            'DeviceProtection': request.form.get('query12', ''),
            'TechSupport': request.form.get('query13', ''),
            'StreamingTV': request.form.get('query14', ''),
            'StreamingMovies': request.form.get('query15', ''),
            'Contract': request.form.get('query16', ''),
            'PaperlessBilling': request.form.get('query17', ''),
            'PaymentMethod': request.form.get('query18', ''),
            'tenure': request.form.get('query19', '')
        }
        
        # Validate and convert inputs
        validated_data, errors = validate_and_convert_input(raw_form_data)
        
        if errors:
            return render_template('home.html',
                                output1="Please fix these errors: " + ", ".join(errors),
                                output2="",
                                **{f'query{i}': raw_form_data.get(col, '') 
                                 for i, col in enumerate(raw_form_data, 1)})
        
        # Preprocess and predict
        prediction_data = preprocess_input(validated_data, expected_features)
        prediction = model.predict(prediction_data)
        probability = model.predict_proba(prediction_data)[:,1]
        
        # Prepare results
        if prediction[0] == 1:
            result = {
                'output1': "This customer is likely to be churned!!",
                'output2': f"Confidence: {probability[0]*100:.2f}%"
            }
        else:
            result = {
                'output1': "This customer is likely to continue!!",
                'output2': f"Confidence: {probability[0]*100:.2f}%"
            }
        
        return render_template('home.html', 
                            **result,
                            **{f'query{i}': raw_form_data.get(col, '') 
                             for i, col in enumerate(raw_form_data, 1)})
        
    except Exception as e:
        traceback.print_exc()
        return render_template('home.html',
                            output1=f"System error: {str(e)}",
                            output2="Please try again",
                            **{f'query{i}': '' for i in range(1, 20)})

if __name__ == "__main__":
    app.run(debug=True)