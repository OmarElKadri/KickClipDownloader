from flask import Flask, render_template, request, send_file, jsonify, session
import yt_dlp
import os
import secrets
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', secrets.token_hex(16))

DOWNLOAD_FOLDER = 'downloads'
Path(DOWNLOAD_FOLDER).mkdir(exist_ok=True)

def download_kick_clip(url, output_path="kick_clip"):
    """
    Downloads a Kick.com clip using yt-dlp.
    
    Args:
        url (str): Kick clip URL
        output_path (str): Output filename template
    
    Returns:
        dict: Result with success status and filename or error message
    """
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'compat_opts': ['filename'],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith('.mp4'):
                filename = filename.rsplit('.', 1)[0] + '.mp4'
        return {'success': True, 'filename': filename}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'error': 'Please provide a URL'}), 400
    
    if 'kick.com' not in url:
        return jsonify({'success': False, 'error': 'Please provide a valid Kick.com URL'}), 400
    
    output_path = os.path.join(DOWNLOAD_FOLDER, f'kick_clip_{secrets.token_hex(8)}.%(ext)s')
    
    result = download_kick_clip(url, output_path)
    
    if result['success']:
        filename = os.path.basename(result['filename'])
        session['last_download'] = filename
        return jsonify({
            'success': True, 
            'message': 'Download completed successfully!',
            'filename': filename
        })
    else:
        return jsonify({'success': False, 'error': result['error']}), 500

@app.route('/get-file/<filename>')
def get_file(filename):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
