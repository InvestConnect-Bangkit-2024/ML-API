from flask import Flask, request, jsonify
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np

# Inisialisasi Flask
app = Flask(__name__)

# Load model dan scaler
try:
    model = tf.keras.models.load_model('model_company_recommendation.h5')
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

try:
    with open('scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
except FileNotFoundError:
    scaler = None

# Load dataset untuk referensi
try:
    data = pd.read_csv('data_company_cleaned.csv')
except Exception as e:
    raise RuntimeError(f"Error loading dataset: {e}")

# Validasi input JSON
required_fields = ['Industry/Sector', 'Stage', 'Business Model', 'Loyal Customer']

def validate_input(user_input):
    for field in required_fields:
        if field not in user_input:
            raise ValueError(f"Missing required field: {field}")
    return True

# Endpoint untuk mendapatkan rekomendasi perusahaan
@app.route('/recommend', methods=['POST'])
def recommend_company():
    try:
        # Ambil inputan dari request
        user_input = request.get_json()
        
        # Validasi input
        validate_input(user_input)

        # Data input dari user
        input_data = pd.DataFrame({
            'Industry/Sector': [user_input['Industry/Sector']],
            'Stage': [user_input['Stage']],
            'Business Model': [user_input['Business Model']],
            'Loyal Customer': [float(user_input['Loyal Customer'])]  # Pastikan numeric
        })

        # Jika ada preprocessing tambahan seperti encoding, tambahkan di sini
        # Contoh encoding kategori (jika perlu)
        # input_data_encoded = encode_features(input_data)

        # Skalakan data jika scaler tersedia
        if scaler:
            numeric_features = ['Loyal Customer']
            input_data[numeric_features] = scaler.transform(input_data[numeric_features])

        # Melakukan prediksi dengan model
        prediction = model.predict(input_data)

        # Ambil top-5 rekomendasi berdasarkan hasil prediksi
        top_companies_idx = np.argsort(prediction[0])[-5:][::-1]  # Sort descending
        top_companies = data.iloc[top_companies_idx]

        # Format hasil rekomendasi
        response = top_companies[['Company Name', 'Industry/Sector', 'Stage', 'Business Model']].to_dict(orient='records')

        return jsonify({'recommendations': response}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f"Internal server error: {e}"}), 500

# Run aplikasi Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
