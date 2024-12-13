from flask import Flask, request, jsonify
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the model and data
model = tf.keras.models.load_model('model_company_recommendation.h5')
data = pd.read_pickle('data_company_cleaned.pkl')

# Label encoders for categorical features
industry_encoder = LabelEncoder()
stage_encoder = LabelEncoder()
business_model_encoder = LabelEncoder()

# Fit label encoders on the data
industry_encoder.fit(data['Industry/Sector'])
stage_encoder.fit(data['Stage'])
business_model_encoder.fit(data['Business Model'])

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hallo!'

# API route for recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get JSON data from the request
        input_data = request.get_json()

        # Extract user input
        industry = input_data['Industry/Sector']
        stage = input_data['Stage']
        business_model = input_data['Business Model']
        loyal_customer = input_data['Loyal Customer']

        # Encode the categorical inputs
        industry_encoded = industry_encoder.transform([industry])[0]
        stage_encoded = stage_encoder.transform([stage])[0]
        business_model_encoded = business_model_encoder.transform([business_model])[0]

        # Prepare the input data for the model
        input_features = [
            industry_encoded,
            stage_encoded,
            business_model_encoded,
            loyal_customer
        ]
        
        # Convert to the proper shape (batch size, number of features)
        input_features = pd.DataFrame([input_features])

        # Predict the company recommendations
        predictions = model.predict(input_features)
        
        # Post-process predictions (sorting, top-n, etc.)
        recommended_companies = data.iloc[predictions.argsort()[0][:5]]  # Top 5 recommendations

        # Format the response
        response = recommended_companies[['Company Name', 'Industry/Sector', 'Stage', 'Business Model']].to_dict(orient='records')

        return jsonify({'recommendations': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
