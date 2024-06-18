from flask import Flask, request, render_template, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__, static_folder='static', template_folder='.')
model = load_model('model/card_detector.h5')

class_names = ['clubs', 'diamonds', 'hearts', 'spades']

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def predict_card_shape(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    predictions = model.predict(img_array)
    return class_names[np.argmax(predictions)]

def predict_card_shape_from_array(img_array):
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    return class_names[np.argmax(predictions)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            prediction = predict_card_shape(filepath)
            return render_template('index.html', prediction=prediction, img_path=filename)
    return render_template('index.html', prediction=None, img_path=None)

@app.route('/camera.html')
def camera():
    return render_template('camera.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    img_data = base64.b64decode(data['image'])
    img = Image.open(BytesIO(img_data)).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img)
    prediction = predict_card_shape_from_array(img_array)
    return jsonify({'prediction': prediction})

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
