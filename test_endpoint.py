#!/usr/bin/env python3
import requests
import json

# Test data for the analyze-timeseries endpoint
test_data = {
    "data": [
        {
            "timestamp": "2024-01-01T10:00:00",
            "step": "Data Collection",
            "delay": 2.5
        },
        {
            "timestamp": "2024-01-01T12:30:00",
            "step": "Data Processing",
            "delay": 1.2
        },
        {
            "timestamp": "2024-01-01T14:00:00",
            "step": "Analysis",
            "delay": 3.8
        },
        {
            "timestamp": "2024-01-01T18:00:00",
            "step": "Report Generation",
            "delay": 0.5
        }
    ]
}

try:
    # Test the analyze-timeseries endpoint
    response = requests.post(
        'http://localhost:5001/api/analyze-timeseries',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the server. Make sure it's running on port 5001.")
except Exception as e:
    print(f"Error: {e}")