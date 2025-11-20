#!/usr/bin/env python3
"""
PostgreSQL Demo Application
A simple Python application demonstrating PostgreSQL usage
"""
import psycopg2
import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'db'),
        database=os.environ.get('POSTGRES_DB', 'mydb'),
        user=os.environ.get('POSTGRES_USER', 'postgres'),
        password=os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        port=os.environ.get('POSTGRES_PORT', 5432)
    )

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PostgreSQL Docker Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #336791 0%, #2a5470 100%);
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
            color: #336791;
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
            border-left: 4px solid #336791;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        .info-box strong {
            color: #336791;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #336791;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #2a5470;
        }
        table {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #336791;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <span class="status">✓ Running</span>
        <h1>PostgreSQL Docker Demo</h1>
        <p style="font-size: 1.2em; color: #333; margin-bottom: 30px;">
            Welcome to PostgreSQL running in Docker! 🚀
        </p>
        
        <div class="info-box">
            <strong>Database:</strong> {{ db_name }}<br>
            <strong>Host:</strong> {{ db_host }}<br>
            <strong>User:</strong> {{ db_user }}<br>
            <strong>Status:</strong> {{ status }}<br>
            <strong>Total Users:</strong> {{ user_count }}
        </div>
        
        <a href="/api/" class="btn">View API Info</a>
        <a href="/api/users" class="btn" style="margin-left: 10px; background: #2a5470;">View Users</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with PostgreSQL info"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users;")
        user_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        status = 'Connected'
    except Exception as e:
        user_count = 0
        status = f'Error: {str(e)}'
    
    return render_template_string(
        HTML_TEMPLATE,
        db_name=os.environ.get('POSTGRES_DB', 'mydb'),
        db_host=os.environ.get('POSTGRES_HOST', 'db'),
        db_user=os.environ.get('POSTGRES_USER', 'postgres'),
        status=status,
        user_count=user_count
    )

@app.route('/api/')
def api_info():
    """API information"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM users;")
        user_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        status = 'connected'
    except Exception as e:
        version = None
        user_count = 0
        status = 'error'
        error_msg = str(e)
    
    return jsonify({
        'status': 'success',
        'postgresql': {
            'host': os.environ.get('POSTGRES_HOST', 'db'),
            'database': os.environ.get('POSTGRES_DB', 'mydb'),
            'user': os.environ.get('POSTGRES_USER', 'postgres'),
            'connection_status': status,
            'version': version if status == 'connected' else None,
            'user_count': user_count
        },
        'endpoints': {
            'home': '/',
            'api_info': '/api/',
            'users': '/api/users',
            'create_user': 'POST /api/users?name=<name>&email=<email>'
        },
        'error': error_msg if status == 'error' else None
    })

@app.route('/api/users')
def get_users():
    """Get all users"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, created_at FROM users ORDER BY id;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        
        users_list = [
            {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'created_at': str(user[3])
            }
            for user in users
        ]
        
        return jsonify({
            'status': 'success',
            'count': len(users_list),
            'users': users_list
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    from flask import request
    try:
        name = request.args.get('name', '')
        email = request.args.get('email', '')
        
        if not name or not email:
            return jsonify({
                'status': 'error',
                'message': 'Name and email are required'
            }), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email, created_at;",
            (name, email)
        )
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'User created',
            'user': {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'created_at': str(user[3])
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

