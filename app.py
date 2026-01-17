#!/usr/bin/env python3
from flask import Flask, render_template, send_file, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
KARAOKE_DIR = "/media/breno/External/Karaoke"
QUEUE_FILE = "/tmp/karaoke_queue.json"

def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_queue(queue):
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f)

# Site público - para adicionar músicas na fila
@app.route('/')
def index():
    return render_template('public.html')

# Site do DJ - para tocar as músicas
@app.route('/dj')
def dj():
    return render_template('dj.html')

@app.route('/api/songs')
def get_songs():
    query = request.args.get('q', '').lower()
    files = sorted([f for f in os.listdir(KARAOKE_DIR) if f.endswith('.mp4')])
    
    if query:
        files = [f for f in files if query in f.lower()]
    
    return jsonify(files)

@app.route('/api/queue', methods=['GET'])
def get_queue():
    return jsonify(load_queue())

@app.route('/api/queue/add', methods=['POST'])
def add_to_queue():
    data = request.json
    queue = load_queue()
    queue.append({
        'song': data['song'],
        'addedAt': datetime.now().isoformat(),
        'id': len(queue)
    })
    save_queue(queue)
    return jsonify({'success': True})

@app.route('/api/queue/remove/<int:idx>', methods=['DELETE'])
def remove_from_queue(idx):
    queue = load_queue()
    if 0 <= idx < len(queue):
        queue.pop(idx)
        save_queue(queue)
    return jsonify({'success': True})

@app.route('/api/queue/clear', methods=['POST'])
def clear_queue():
    save_queue([])
    return jsonify({'success': True})

@app.route('/video/<path:filename>')
def video(filename):
    return send_file(os.path.join(KARAOKE_DIR, filename), mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
