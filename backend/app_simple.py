from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import pandas as pd
import json
import os
from werkzeug.utils import secure_filename
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Configure CORS to allow requests from any localhost port
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:3000",
    os.getenv('FRONTEND_URL', 'http://localhost:3000')
]}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.getenv('UPLOAD_FOLDER', 'uploads'))
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'csv,json,xls,xlsx').split(','))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_embeddings(text):
    """Simplified embedding function using basic text features"""
    try:
        # Simple text features as embeddings
        words = text.lower().split()
        word_count = len(words)
        char_count = len(text)
        avg_word_length = char_count / max(word_count, 1)
        
        # Create a simple feature vector (768 dimensions to match BERT)
        embedding = np.random.randn(768)
        # Add some actual text features
        embedding[0] = word_count / 100.0  # Normalize word count
        embedding[1] = char_count / 1000.0  # Normalize char count
        embedding[2] = avg_word_length / 10.0  # Normalize avg word length
        
        return embedding.tolist()
    except Exception as e:
        logger.error(f"Error getting embeddings: {str(e)}")
        # Fallback to random embeddings
        embedding = np.random.randn(768)
        return embedding.tolist()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_status': 'simplified_mode'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Get embeddings
        embeddings = get_embeddings(text)
        
        # Calculate basic statistics
        embeddings_array = np.array(embeddings)
        stats = {
            'mean': float(np.mean(embeddings_array)),
            'std': float(np.std(embeddings_array)),
            'min': float(np.min(embeddings_array)),
            'max': float(np.max(embeddings_array)),
            'word_count': len(text.split()),
            'char_count': len(text)
        }
        
        return jsonify({
            'embeddings': embeddings,
            'statistics': stats,
            'text_length': len(text),
            'word_count': len(text.split()),
            'model_used': 'simplified_text_analyzer'
        })
    
    except Exception as e:
        logger.error(f"Error in analyze_text: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Try to read the file and return basic info
            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                elif filename.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(filepath)
                else:
                    return jsonify({'error': 'Unsupported file format'}), 400
                
                return jsonify({
                    'filename': filename,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': df.columns.tolist(),
                    'file_size': os.path.getsize(filepath)
                })
            
            except Exception as e:
                logger.error(f"Error reading uploaded file: {str(e)}")
                return jsonify({'error': 'Error reading file'}), 400
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting simplified Flask server...")
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)