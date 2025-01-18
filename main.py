from flask import Flask, request, jsonify
import sqlite3
from initialize_db import init_db

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users')
        users = cursor.fetchall()
        return jsonify(users)


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    try:
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Users (name, email) VALUES (?, ?)', (name, email))
            conn.commit()
            return jsonify({'message': 'User added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        conn.commit()
        return jsonify({'message': 'User deleted successfully'})


@app.route('/posts', methods=['POST'])
def add_post():
    data = request.json
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')

    if not user_id or not title or not content:
        return jsonify({'error': 'User ID, title, and content are required'}), 400

    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM Users WHERE id = ?', (user_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'User ID does not exist'}), 400

        cursor.execute('INSERT INTO Posts (user_id, title, content) VALUES (?, ?, ?)', (user_id, title, content))
        conn.commit()
        return jsonify({'message': 'Post added successfully'}), 201


@app.route('/posts/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Posts WHERE user_id = ?', (user_id,))
        posts = cursor.fetchall()
        return jsonify(posts)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
