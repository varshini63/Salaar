from flask import Flask, render_template, request, jsonify, send_file, session
import hashlib
import os
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Challenge configuration
LAYER_1_Y_VALUES = {
    'y1': '3728197',
    'y2': '3728224',
    'y3': '3728269'
}

LAYER_1_SECRET = '3728192'  # a0 value
LAYER_1_FLAG = 'Kh4an54ar_R1s35'

LAYER_2_FLAG = 'Salaar_devaratha_raisaar'
LAYER_2_UNLOCK = 'w4rz0n3_D3v4r4th4'

LAYER_3_FLAG = 'w4rz0n3{Kh4an54ar_3rup3kk3l4}'
LAYER_3_UNLOCK = 'CTF{CRYPTOGRAPHY}'

def check_layer(layer_num):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if f'layer_{layer_num}_unlocked' not in session:
                return jsonify({'error': 'Previous layer not completed'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/layer1')
def layer1():
    session['layer_1_unlocked'] = True
    return render_template('layer1.html')

@app.route('/api/layer1/hashes')
def get_hashes():
    return jsonify({
        'y1': hashlib.md5(LAYER_1_Y_VALUES['y1'].encode()).hexdigest(),
        'y2': hashlib.md5(LAYER_1_Y_VALUES['y2'].encode()).hexdigest(),
        'y3': hashlib.md5(LAYER_1_Y_VALUES['y3'].encode()).hexdigest(),
        'x_values': [1, 2, 3]
    })

@app.route('/api/layer1/submit', methods=['POST'])
def submit_layer1():
    data = request.json
    answer = data.get('answer', '').strip()
    
    if answer == LAYER_1_SECRET:
        session['layer_2_unlocked'] = True
        return jsonify({
            'success': True,
            'message': 'Deva\'s vault opens! The path to Khansaar awaits...',
            'flag': LAYER_1_FLAG,
            'next_layer': '/layer2'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'The vault remains sealed. Check your calculations.'
        })

@app.route('/layer2')
@check_layer(2)
def layer2():
    return render_template('layer2.html')

@app.route('/download/flag_parts.zip')
@check_layer(2)
def download_zip():
    import os
    file_path = os.path.join(os.getcwd(), 'challenges', 'flag_parts.zip')
    return send_file(file_path, as_attachment=True, download_name='flag_parts.zip', mimetype='application/zip')

@app.route('/api/layer2/submit', methods=['POST'])
def submit_layer2():
    if 'layer_2_unlocked' not in session:
        return jsonify({'error': 'Layer not unlocked'}), 403
    
    data = request.json
    answer = data.get('answer', '').strip()
    
    if answer == f'CTF{{{LAYER_2_FLAG}}}':
        session['layer_3_unlocked'] = True
        return jsonify({
            'success': True,
            'message': 'The tribes unite! Devaratha\'s legacy is revealed...',
            'flag': LAYER_2_UNLOCK,
            'next_layer': '/layer3'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'The tribal seals remain unbroken. Try again.'
        })

@app.route('/layer3')
@check_layer(3)
def layer3():
    return render_template('layer3.html')

@app.route('/download/khansaar_transmission.wav')
@check_layer(3)
def download_wav():
    import os
    file_path = os.path.join(os.getcwd(), 'challenges', 'khansaar_transmission.wav')
    return send_file(file_path, as_attachment=True, download_name='khansaar_transmission.wav', mimetype='audio/wav')

@app.route('/api/layer3/submit', methods=['POST'])
def submit_layer3():
    if 'layer_3_unlocked' not in session:
        return jsonify({'error': 'Layer not unlocked'}), 403
    
    data = request.json
    answer = data.get('answer', '').strip()
    
    if answer == LAYER_3_UNLOCK:
        return jsonify({
            'success': True,
            'message': 'Khansaar is yours! The throne of Devaratha acknowledges you!',
            'final_flag': LAYER_3_FLAG
        })
    else:
        return jsonify({
            'success': False,
            'message': 'The final transmission is not decoded. Listen carefully.'
        })

@app.route('/reset')
def reset():
    session.clear()
    return jsonify({'message': 'Session reset'})

if __name__ == '__main__':
    os.makedirs('challenges', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)