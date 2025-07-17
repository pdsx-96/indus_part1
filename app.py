from flask import Flask, request, jsonify
from flasgger import Swagger
import sqlite3
from uuid import uuid4
import os

app = Flask(__name__)
swagger = Swagger(app)

# config
DATABASE = 'records.db'
API_KEY = "my_secure_api_key"  # TODO: move to env vars later

def init_db():
    """set up the database table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def require_api_key():
    key = request.headers.get('x-api-key')
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/records', methods=['POST'])
def add_record():
    """
    Add a new record
    ---
    parameters:
      - in: header
        name: x-api-key
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          id: Record
          required:
            - name
            - status
          properties:
            name:
              type: string
            status:
              type: string
    responses:
      200:
        description: Record added
      400:
        description: Bad request
      401:
        description: Unauthorized
    """
    auth = require_api_key()
    if auth: return auth

    try:
        data = request.json
        if not data or 'name' not in data or 'status' not in data:
            return jsonify({"error": "Missing required fields: name, status"}), 400

        record_id = str(uuid4())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO records (id, name, status) VALUES (?, ?, ?)',
            (record_id, data['name'], data['status'])
        )
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Record added", "id": record_id}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/records', methods=['GET'])
def get_records():
    """
    Get all records or filter by status
    ---
    parameters:
      - in: header
        name: x-api-key
        required: true
        type: string
      - in: query
        name: status
        required: false
        type: string
    responses:
      200:
        description: List of records
      401:
        description: Unauthorized
    """
    auth = require_api_key()
    if auth: return auth

    try:
        status = request.args.get('status')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM records WHERE status = ?', (status,))
        else:
            cursor.execute('SELECT * FROM records')
        
        records = cursor.fetchall()
        conn.close()
        
        # convert to dict format
        records_dict = {}
        for record in records:
            records_dict[record['id']] = {
                'name': record['name'],
                'status': record['status'],
                'created_at': record['created_at']
            }
        
        return jsonify(records_dict), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/records/<record_id>', methods=['PUT'])
def update_record(record_id):
    """
    Update a record
    ---
    parameters:
      - in: header
        name: x-api-key
        required: true
        type: string
      - in: path
        name: record_id
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          properties:
            name:
              type: string
            status:
              type: string
    responses:
      200:
        description: Record updated
      404:
        description: Record not found
      401:
        description: Unauthorized
    """
    auth = require_api_key()
    if auth: return auth

    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # check if exists
        cursor.execute('SELECT id FROM records WHERE id = ?', (record_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Record not found"}), 404
        
        # build update query
        update_fields = []
        values = []
        
        if 'name' in data:
            update_fields.append('name = ?')
            values.append(data['name'])
        
        if 'status' in data:
            update_fields.append('status = ?')
            values.append(data['status'])
        
        if not update_fields:
            conn.close()
            return jsonify({"error": "No valid fields to update"}), 400
        
        values.append(record_id)
        query = f'UPDATE records SET {", ".join(update_fields)} WHERE id = ?'
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Record updated"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """
    Delete a record
    ---
    parameters:
      - in: header
        name: x-api-key
        required: true
        type: string
      - in: path
        name: record_id
        required: true
        type: string
    responses:
      200:
        description: Record deleted
      404:
        description: Record not found
      401:
        description: Unauthorized
    """
    auth = require_api_key()
    if auth: return auth

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Record not found"}), 404
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Record deleted"}), 200
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/')
def home():
    return "API is running! Check /apidocs for docs"

if __name__ == '__main__':
    init_db()
    # Get port from environment variable (for cloud deployment) or use 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
