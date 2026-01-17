#!/usr/bin/env python3
from flask import Flask, render_template, send_file, request, jsonify
import os
import json
from datetime import datetime
from threading import Thread
from karaoke_agent import process_song_request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
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

@app.route('/api/queue/reorder', methods=['POST'])
def reorder_queue():
    data = request.json
    from_idx = data.get('from')
    to_idx = data.get('to')
    
    queue = load_queue()
    if 0 <= from_idx < len(queue) and 0 <= to_idx < len(queue):
        item = queue.pop(from_idx)
        queue.insert(to_idx, item)
        save_queue(queue)
    
    return jsonify({'success': True})

@app.route('/api/request-song', methods=['POST'])
def request_song():
    data = request.json
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'success': False, 'error': 'Query vazia'})
    
    # Processa em background para não travar a requisição
    def download_async():
        try:
            print(f"[AGENT] Iniciando download para: {query}")
            result = process_song_request(query)
            print(f"[AGENT] Resultado: {result}")
        except Exception as e:
            print(f"[AGENT] ERRO: {e}")
            import traceback
            traceback.print_exc()
    
    Thread(target=download_async, daemon=True).start()
    
    return jsonify({'success': True, 'message': 'Processando pedido'})

@app.route('/manifest.json')
def manifest():
    return send_file('manifest.json', mimetype='application/json')

@app.route('/manifest-dj.json')
def manifest_dj():
    return send_file('manifest-dj.json', mimetype='application/json')

@app.route('/video/<path:filename>')
def video(filename):
    return send_file(os.path.join(KARAOKE_DIR, filename), mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
