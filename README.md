# YouTube Transcript Backend

A Flask-based API service for extracting YouTube video transcripts with multi-language support.

## Features

- Extract transcripts from YouTube videos
- Support for multiple languages (English, Spanish, German, French, Portuguese, Italian)
- Timestamp formatting for transcript entries
- CORS support for cross-origin requests
- Health check endpoint
- Docker containerization for easy deployment

## Requirements

- Python 3.11+
- Flask 3.0.0
- Flask-CORS 4.0.0
- youtube-transcript-api 0.6.2
- Gunicorn 21.2.0

## Installation

### Local Setup

1. Clone the repository:
```bash
cd yt-analyzer-backend
git init
git add .
git commit -m "Initial backend"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python server.py
```

The server will start at `http://localhost:5000`

### Docker Setup

1. Build the Docker image:
```bash
docker build -t youtube-transcript-api .
```

2. Run the container:
```bash
docker run -p 5000:5000 youtube-transcript-api
```

## API Endpoints

### GET/POST `/transcript`

Fetch the transcript of a YouTube video.

**Parameters:**
- `video_id` (optional): YouTube video ID (11 characters)
- `url` (optional): Full YouTube URL

**Supported URL formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- Direct video ID

**Response (Success):**
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "transcript": "[0:00] This is the first line\n[0:05] This is the second line\n..."
}
```

**Response (Error):**
```json
{
  "error": "Invalid video ID"
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Usage Examples

### Using cURL

```bash
# Using video ID
curl "http://localhost:5000/transcript?video_id=dQw4w9WgXcQ"

# Using full URL
curl "http://localhost:5000/transcript?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Using youtu.be shortened URL
curl "http://localhost:5000/transcript?url=https://youtu.be/dQw4w9WgXcQ"

# Health check
curl "http://localhost:5000/health"
```

### Using JavaScript/Fetch

```javascript
// Fetch transcript by video ID
fetch('http://localhost:5000/transcript?video_id=dQw4w9WgXcQ')
  .then(response => response.json())
  .then(data => console.log(data.transcript));

// Fetch transcript by URL
fetch('http://localhost:5000/transcript?url=https://youtu.be/dQw4w9WgXcQ')
  .then(response => response.json())
  .then(data => console.log(data.transcript));
```

## Deployment

### GitHub Setup

1. Create a new repository on GitHub
2. Connect your local repository:
```bash
git remote add origin https://github.com/YOUR_USERNAME/yt-transcript-backend.git
git branch -M main
git push -u origin main
```

### Production Deployment

The application uses Gunicorn as the WSGI server, configured to:
- Bind to all interfaces (`0.0.0.0`)
- Listen on port `5000`
- Support concurrent requests

For production deployment, consider:
- Using a reverse proxy (Nginx, Apache)
- Setting up HTTPS/SSL
- Configuring proper logging
- Using environment variables for configuration
- Implementing rate limiting

## License

MIT

## Contributing

Feel free to submit issues and enhancement requests!
