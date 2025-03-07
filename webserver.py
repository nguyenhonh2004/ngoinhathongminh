from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit  # Thêm SocketIO
import joblib
import numpy as np

# Load model và scaler
binary_model = joblib.load('binary_model.pkl')
scaler = joblib.load('scaler.pkl')

app = Flask(__name__)
socketio = SocketIO(app)  # Khởi tạo SocketIO

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    sample = np.array(data['sensor_values']).reshape(1, -1)
    scaled_sample = scaler.transform(sample)
    prediction = binary_model.predict(scaled_sample)[0]

    # Xác định các chỉ số bất thường
    abnormal_indicators = []
    if not (20 <= data['sensor_values'][0] <= 35):
        abnormal_indicators.append('temperature')
    if not (30 <= data['sensor_values'][1] <= 70):
        abnormal_indicators.append('humidity')
    if not (200 <= data['sensor_values'][2] <= 600):
        abnormal_indicators.append('gas')
    if not (30 <= data['sensor_values'][3] <= 80):
        abnormal_indicators.append('sound')
    if not (300 <= data['sensor_values'][4] <= 800):
        abnormal_indicators.append('light')

    response = {
        'sensor_values': data['sensor_values'],
        'prediction': int(prediction),
        'abnormal_indicators': abnormal_indicators
    }

    # Gửi dữ liệu tới client qua SocketIO
    socketio.emit('update_data', response)
    return jsonify(response)

if __name__ == '__main__':
    socketio.run(app, debug=True)
