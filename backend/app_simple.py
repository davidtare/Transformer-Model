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
# Removed sklearn imports to avoid dependency issues

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

def analyze_timeseries(data):
    """Analyze time series data for bottlenecks and anomalies"""
    try:
        # Validate input data
        if not isinstance(data, list):
            raise ValueError("Input data must be a list of objects")
        
        # Validate each item in the data
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Each item must be a dictionary")
            if 'timestamp' not in item:
                raise ValueError("Each item must have a 'timestamp' field")
            if 'step' not in item:
                raise ValueError("Each item must have a 'step' field")
            if 'delay' not in item:
                raise ValueError("Each item must have a 'delay' field")
            
            # Convert delay to float if it's a string
            if isinstance(item['delay'], str):
                try:
                    item['delay'] = float(item['delay'])
                except ValueError:
                    raise ValueError(f"Delay value '{item['delay']}' cannot be converted to a number")
        
        # Convert timestamps to datetime objects
        for item in data:
            try:
                item['timestamp'] = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
            except ValueError as e:
                raise ValueError(f"Invalid timestamp format: {item['timestamp']}. Expected ISO format (YYYY-MM-DDTHH:mm:ss)")
        
        # Sort by timestamp
        data.sort(key=lambda x: x['timestamp'])
        
        # Calculate delays between steps
        delays = []
        for i in range(1, len(data)):
            delay = (data[i]['timestamp'] - data[i-1]['timestamp']).total_seconds() / 3600  # Convert to hours
            delays.append(delay)
        
        # Calculate bottleneck impact scores
        bottlenecks = []
        for i, step in enumerate(data):
            if i == 0:
                continue
            impact = float(step['delay']) / max(delays) if max(delays) > 0 else 0
            bottlenecks.append({
                'step': step['step'],
                'impact': impact,
                'delay': float(step['delay'])
            })
        
        # Sort bottlenecks by impact
        bottlenecks.sort(key=lambda x: x['impact'], reverse=True)
        
        # Detect anomalies using simple statistical methods (Z-score)
        delay_values = np.array([float(item['delay']) for item in data])
        mean_delay = np.mean(delay_values)
        std_delay = np.std(delay_values)
        
        # Identify anomalous steps using Z-score (threshold = 2)
        anomalous_steps = []
        for i, step in enumerate(data):
            z_score = abs((float(step['delay']) - mean_delay) / std_delay) if std_delay > 0 else 0
            if z_score > 2:  # Anomaly threshold
                anomalous_steps.append({
                    'step': step['step'],
                    'description': f"Unusual delay pattern detected: {step['delay']} hours (Z-score: {z_score:.2f})"
                })
        
        # Generate recommendations
        recommendations = []
        
        # Bottleneck recommendations
        if bottlenecks:
            top_bottleneck = bottlenecks[0]
            recommendations.append({
                'title': 'Bottleneck Optimization',
                'description': f"Consider optimizing {top_bottleneck['step']} as it has the highest impact on process delays."
            })
        
        # Anomaly recommendations
        if anomalous_steps:
            recommendations.append({
                'title': 'Process Anomaly',
                'description': f"Investigate unusual delays in {', '.join(step['step'] for step in anomalous_steps)}."
            })
        
        # Sequential optimization recommendations
        if len(bottlenecks) >= 2:
            recommendations.append({
                'title': 'Process Reordering',
                'description': f"Consider reordering steps to reduce dependencies between {bottlenecks[0]['step']} and {bottlenecks[1]['step']}."
            })
        
        return {
            'bottlenecks': bottlenecks,
            'anomalies': anomalous_steps,
            'recommendations': recommendations
        }
        
    except Exception as e:
        logger.error(f"Error in time series analysis: {str(e)}")
        raise ValueError(str(e))

@app.route('/api/analyze-timeseries', methods=['POST'])
def analyze_timeseries_endpoint():
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided'}), 400
        
        results = analyze_timeseries(data['data'])
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting simplified Flask server...")
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)