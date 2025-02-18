# Google Calendar Event Generator

This application uses OpenAI's GPT-4 Vision model to extract event details from images and automatically creates events in Google Calendar. It consists of a Python FastAPI backend and a Next.js frontend with TypeScript and Tailwind CSS.

## Project Structure

```
.
├── backend/
│   ├── config/
│   │   ├── credentials.json
│   │   └── .env
│   ├── app.py
│   ├── main.py
│   ├── debug.py
│   ├── requirements.txt
│   └── run.py
└── frontend/
    ├── src/
    │   └── app/
    │       ├── page.tsx
    │       ├── layout.tsx
    │       └── globals.css
    ├── package.json
    └── tailwind.config.js
```

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- OpenAI API key with GPT-4 Vision access
- Google Cloud Project with Calendar API enabled
- Google OAuth 2.0 credentials
- VS Code (recommended for debugging)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
## On macOS/Linux:
source venv/bin/activate
## On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the `backend/config` directory with:
```
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_TIMEZONE=America/Los_Angeles  # Optional, defaults to America/Los_Angeles
```

5. Set up Google Calendar API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials:
     1. Go to "Credentials" section
     2. Click "Create Credentials" > "OAuth client ID"
     3. Select "Desktop application" as application type
     4. Download the credentials and save them as `credentials.json` in the `backend/config` directory

6. Run the backend server:

   **Normal mode:**
   ```bash
   python run.py
   ```

   **Debug mode:**
   ```bash
   python run.py --debug
   ```

   Additional options:
   ```bash
   python run.py --debug --host localhost --port 8000
   ```

The backend server will start at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend application will start at `http://localhost:3000`.

## Debug Mode Features

The application includes comprehensive debugging capabilities that can be enabled in several ways:

### 1. Using VS Code (Recommended)

1. Open VS Code in the project root
2. Go to the Debug panel (Ctrl/Cmd + Shift + D)
3. Select "Python: FastAPI Backend" from the dropdown
4. Press F5 or click the play button

The VS Code launch configuration includes:
- Integrated terminal output
- Source maps for better stack traces
- Automatic Python path configuration
- Support for breakpoints and variable inspection

### 2. Command Line Debug Mode

Run the backend with debug flags:
```bash
python run.py --debug [--host HOST] [--port PORT]
```

Debug mode enables:
- Detailed request/response logging
- Function entry/exit tracking
- Execution time measurements
- Enhanced error reporting
- Auto-reload on code changes

### 3. Debug Features

The debug mode includes:

- **Request Logging:**
  - HTTP method and URL
  - Request headers
  - Response status codes
  - Execution timing

- **Function Tracking:**
  - Entry and exit points
  - Arguments and return values
  - Execution time measurements
  - Exception details

- **File Logging:**
  - Console output (stdout)
  - File logging (`backend/app.log`)
  - Formatted timestamps
  - Source file and line numbers

- **Development Features:**
  - Hot reload enabled
  - Single worker mode
  - Unlimited keep-alive timeout
  - Watch mode for file changes

### 4. Debug Utilities

The `debug.py` module provides:

- `@debug_log` decorator for function logging
- `log_debug()` function for custom debug messages
- Automatic logging configuration
- Support for both sync and async functions

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload an image containing event information
3. The application will:
   - Process the image using GPT-4 Vision
   - Extract event details
   - Create an event in your Google Calendar
   - Provide a link to view the created event

## API Endpoints

### Backend API

- `POST /api/process-image`: Process an image and create a calendar event
  - Request: Multipart form data with an image file
  - Response: JSON with event link
```json
{
  "success": true,
  "event_link": "https://calendar.google.com/..."
}
```

- `GET /api/health`: Health check endpoint
  - Response: JSON with status
```json
{
  "status": "healthy"
}
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid image files or unsupported formats
- OpenAI API issues
- Google Calendar API authentication problems
- Network connectivity issues
- Invalid date/time formats
- Missing required event information

## Security Notes

- Never commit sensitive files (`.env`, `credentials.json`, `token.json`)
- Keep your OAuth credentials and API keys secure
- The backend stores authentication tokens locally
- The `.gitignore` file is configured to prevent accidental commits of sensitive files

## Contributing

Feel free to submit issues and enhancement requests!

## Follow Us
Stay connected and join the conversation:
- Follow us on [Twitter (@Pedrete666)](https://twitter.com/Pedrete666)
- Follow us on [Bluesky (@pedroid999.bsky.social)](https://bsky.app/profile/pedroid999.bsky.social)

## Upcoming Features

- **Ollama Local LLMs Support**:  
  We are working on integrating support for running large language models locally via Ollama. This enhancement will allow:
  - Offline processing of image-based event extraction.
  - Reduced dependency on cloud APIs.
  - Enhanced customization and potentially improved response times in environments with limited connectivity. 