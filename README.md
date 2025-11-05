# Mr. Trash Wheel 🗑️

An AI-powered waste classification web application that uses deep learning to identify and categorize different types of waste materials. Help make waste management easier and more efficient!

## Features

- **6 Waste Categories**: Classifies waste into cardboard, glass, metal, paper, plastic, and trash
- **Real-time Prediction**: Upload an image and get instant classification results
- **Confidence Scores**: View prediction confidence and probability distribution
- **User-friendly Interface**: Clean, responsive design with easy image upload
- **Production Ready**: Includes error handling, logging, and security features

## How It Works

Mr. Trash Wheel uses a Convolutional Neural Network (CNN) trained on waste images to identify and classify different types of waste materials. The model processes uploaded images and provides accurate predictions to help with proper waste segregation.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd trashwheel
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload an image of waste material and get instant classification!

## Deployment

### Heroku

1. Create a Heroku app:
```bash
heroku create your-app-name
```

2. Push to Heroku:
```bash
git push heroku main
```

3. Open your deployed app:
```bash
heroku open
```

### Environment Variables

- `FLASK_DEBUG`: Set to `true` for development mode (default: `false`)
- `PORT`: Port number for the application (default: `5000`)

## API Endpoints

- `GET /`: Main application page
- `POST /predict`: Upload image for classification
- `GET /health`: Health check endpoint

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- Maximum file size: 16MB

## Project Structure

```
trashwheel/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Heroku deployment config
├── templates/             # HTML templates
│   └── index.html
├── static/                # Static assets (CSS, JS, images)
└── trashwheelgpubackup/  # Trained model files
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **ML Framework**: TensorFlow/Keras
- **Computer Vision**: OpenCV
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Heroku-ready with Gunicorn

## Model Information

The waste classification model uses a CNN architecture trained on labeled waste images to identify:
- Cardboard
- Glass
- Metal
- Paper
- Plastic
- Trash (general waste)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Contact

For questions or feedback, please reach out through the contact section on the website.

---

Made with ❤️ to help create a cleaner, more sustainable world through better waste management.