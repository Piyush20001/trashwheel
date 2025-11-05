import cv2
import os
import logging
import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Load model with error handling
try:
    model = keras.models.load_model("trashwheelgpubackup")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

app = Flask(__name__, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(file_content):
    """Process image file and return preprocessed array"""
    try:
        # Decode image using cv2 (fixed deprecated np.fromstring)
        img_array = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Failed to decode image")

        # Convert color space and resize
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))
        img = image.img_to_array(img, dtype=np.uint8)
        img = np.array(img) / 255.0

        return img
    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        raise

@app.route('/')
def index():
    """Render home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict waste category from uploaded image"""
    try:
        # Validate file presence
        if 'image' not in request.files:
            return render_template('index.html',
                                 error='No file uploaded. Please select an image.')

        file = request.files['image']

        # Validate filename
        if file.filename == '':
            return render_template('index.html',
                                 error='No file selected. Please choose an image.')

        # Validate file type
        if not allowed_file(file.filename):
            return render_template('index.html',
                                 error='Invalid file type. Please upload PNG, JPG, or JPEG.')

        # Process image
        file_content = file.read()
        img = process_image(file_content)

        # Make prediction
        predictions = model.predict(img[np.newaxis, ...], verbose=0)
        predicted_idx = np.argmax(predictions[0])
        predicted_class = labels[predicted_idx]
        confidence = float(predictions[0][predicted_idx]) * 100

        # Get all class probabilities
        all_predictions = {
            labels[i]: float(predictions[0][i] * 100)
            for i in range(len(labels))
        }

        logger.info(f"Prediction: {predicted_class} ({confidence:.2f}%)")

        return render_template('index.html',
                             prediction=predicted_class,
                             confidence=confidence,
                             all_predictions=all_predictions)

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return render_template('index.html',
                             error=f'Error processing image: {str(e)}')
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return render_template('index.html',
                             error='An unexpected error occurred. Please try again.')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    # Use environment variable for debug mode (default: False for production)
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
