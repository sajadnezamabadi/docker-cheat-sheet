#!/usr/bin/env python3
"""
Redis Demo Application
A simple Python application demonstrating Redis usage
"""
import redis
import time
import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Redis connection
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redis Docker Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 700px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #dc3545;
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            background: #28a745;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        .info-box strong {
            color: #dc3545;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #dc3545;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #c82333;
        }
        .counter {
            font-size: 3em;
            color: #dc3545;
            text-align: center;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <span class="status">✓ Running</span>
        <h1>Redis Docker Demo</h1>
        <p style="font-size: 1.2em; color: #333; margin-bottom: 30px;">
            Welcome to Redis running in Docker! 
        </p>
        
        <div class="info-box">
            <strong>Redis Host:</strong> {{ redis_host }}<br>
            <strong>Redis Port:</strong> {{ redis_port }}<br>
            <strong>Status:</strong> {{ status }}<br>
            <strong>Counter Value:</strong>
        </div>
        
        <div class="counter">{{ counter }}</div>
        
        <a href="/api/" class="btn">View API Info</a>
        <a href="/api/increment" class="btn" style="margin-left: 10px; background: #c82333;">Increment Counter</a>
        <a href="/api/reset" class="btn" style="margin-left: 10px; background: #6c757d;">Reset Counter</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with Redis info"""
    try:
        counter = redis_client.get('counter') or '0'
        status = 'Connected'
    except Exception as e:
        counter = '0'
        status = f'Error: {str(e)}'
    
    return render_template_string(
        HTML_TEMPLATE,
        redis_host=os.environ.get('REDIS_HOST', 'redis'),
        redis_port=os.environ.get('REDIS_PORT', 6379),
        status=status,
        counter=counter
    )

@app.route('/api/')
def api_info():
    """API information"""
    try:
        redis_client.ping()
        status = 'connected'
        info = redis_client.info()
    except Exception as e:
        status = 'error'
        info = {'error': str(e)}
    
    return jsonify({
        'status': 'success',
        'redis': {
            'host': os.environ.get('REDIS_HOST', 'redis'),
            'port': os.environ.get('REDIS_PORT', 6379),
            'connection_status': status,
            'info': info if status == 'connected' else None
        },
        'endpoints': {
            'home': '/',
            'api_info': '/api/',
            'increment': '/api/increment',
            'get_counter': '/api/counter',
            'reset': '/api/reset',
            'set_value': 'POST /api/set?value=<number>'
        }
    })

@app.route('/api/increment')
def increment():
    """Increment counter"""
    try:
        value = redis_client.incr('counter')
        return jsonify({
            'status': 'success',
            'message': 'Counter incremented',
            'value': value
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/counter')
def get_counter():
    """Get counter value"""
    try:
        value = redis_client.get('counter') or '0'
        return jsonify({
            'status': 'success',
            'value': int(value)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/reset')
def reset():
    """Reset counter"""
    try:
        redis_client.set('counter', 0)
        return jsonify({
            'status': 'success',
            'message': 'Counter reset',
            'value': 0
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/set', methods=['POST'])
def set_value():
    """Set counter value"""
    from flask import request
    try:
        value = request.args.get('value', '0')
        redis_client.set('counter', int(value))
        return jsonify({
            'status': 'success',
            'message': 'Counter set',
            'value': int(value)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

