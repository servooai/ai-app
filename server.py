from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)
CORS(app)

# ✅ اعمل instance مرة واحدة فقط
ytt_api = YouTubeTranscriptApi()

def extract_video_id(url):
    patterns = [
        r'(?:v=|youtu\.be\/|embed\/|shorts\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route('/transcript', methods=['GET', 'POST'])
def get_transcript():
    video_id = request.args.get('video_id') or request.args.get('url', '')
    
    if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
        video_id = extract_video_id(video_id)
    
    if not video_id:
        return jsonify({'error': 'Invalid video ID'}), 400

    try:
        # ✅ استخدم ytt_api.fetch() مش YouTubeTranscriptApi.fetch()
        transcript = ytt_api.fetch(video_id, languages=['en', 'es', 'de', 'fr', 'pt', 'it'])
        
        formatted = []
        for entry in transcript:
            start = int(entry.start)
            mins = start // 60
            secs = start % 60
            text = entry.text.replace('\n', ' ').strip()
            if text:
                formatted.append(f"[{mins}:{secs:02d}] {text}")

        return jsonify({
            'success': True,
            'video_id': video_id,
            'transcript': '\n'.join(formatted)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
