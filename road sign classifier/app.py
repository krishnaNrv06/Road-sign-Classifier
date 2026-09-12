from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model('traffic_sign_model_43class_FINAL.h5')

gtsrb_names = {
    0: 'Speed limit 20km/h', 1: 'Speed limit 30km/h', 2: 'Speed limit 50km/h',
    3: 'Speed limit 60km/h', 4: 'Speed limit 70km/h', 5: 'Speed limit 80km/h',
    6: 'End of speed limit 80km/h', 7: 'Speed limit 100km/h', 8: 'Speed limit 120km/h',
    9: 'No passing', 10: 'No passing for vehicles over 3.5t', 11: 'Right of way at next intersection',
    12: 'Priority road', 13: 'Yield', 14: 'Stop', 15: 'No vehicles',
    16: 'Vehicles over 3.5t prohibited', 17: 'No entry', 18: 'General caution',
    19: 'Dangerous curve left', 20: 'Dangerous curve right', 21: 'Double curve',
    22: 'Bumpy road', 23: 'Slippery road', 24: 'Road narrows on right', 25: 'Road work',
    26: 'Traffic signals', 27: 'Pedestrians', 28: 'Children crossing', 29: 'Bicycles crossing',
    30: 'Beware of ice/snow', 31: 'Wild animals crossing', 32: 'End of all speed/passing limits',
    33: 'Turn right ahead', 34: 'Turn left ahead', 35: 'Ahead only', 36: 'Go straight or right',
    37: 'Go straight or left', 38: 'Keep right', 39: 'Keep left', 40: 'Roundabout mandatory',
    41: 'End of no passing', 42: 'End of no passing for vehicles over 3.5t'
}

def predict_image(image_path):
    img = Image.open(image_path).convert('RGB').resize((30, 30))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    pred = model.predict(img_array, verbose=0)
    pred_class = np.argmax(pred)
    confidence = np.max(pred) * 100
    return gtsrb_names[pred_class], confidence

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            prediction, confidence = predict_image(filepath)
            is_critical = prediction in ['Stop', 'Yield', 'No entry']
            return render_template('index.html',
                                   prediction=prediction,
                                   confidence=f"{confidence:.2f}",
                                   image_path=filepath,
                                   is_critical=is_critical)
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)