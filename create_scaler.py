import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# Input data yang akan digunakan
data = {
    "Industry/Sector": ["Sustainable Energy"],
    "Stage": ["Growth"],
    "Business Model": ["E-commerce"],
    "Loyal Customer": [15961]
}

# Mengonversi inputan ke DataFrame untuk memproses dengan scaler
input_data = pd.DataFrame(data)

# Encode data kategori menjadi numerik menggunakan LabelEncoder (jika diperlukan)
from sklearn.preprocessing import LabelEncoder

# Menggunakan LabelEncoder untuk kolom kategori (Industry/Sector, Stage, Business Model)
le_industry = LabelEncoder()
le_stage = LabelEncoder()
le_business_model = LabelEncoder()

input_data['Industry/Sector'] = le_industry.fit_transform(input_data['Industry/Sector'])
input_data['Stage'] = le_stage.fit_transform(input_data['Stage'])
input_data['Business Model'] = le_business_model.fit_transform(input_data['Business Model'])

# Membuat dan melatih scaler
scaler = StandardScaler()
scaler.fit(input_data)  # Fit scaler pada data input

# Menyimpan scaler ke file
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

print("Scaler berhasil disimpan ke scaler.pkl")
