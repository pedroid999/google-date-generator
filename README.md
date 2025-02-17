# Google Calendar Event Generator from Images

This application uses OpenAI's GPT-4o multi-modal model to extract event details from images and automatically creates events in Google Calendar using the Google Calendar API via LangChain.


## Prerequisites

- Python 3.11 or higher
- OpenAI API key with GPT-4o
- Google Cloud Project with Calendar API enabled
- Google OAuth 2.0 credentials

## Setup Instructions

1. Clone this repository:
```bash
git clone <repository-url>
cd google-date-generator
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
   - Create a `.env` file in the project root with the following:
```
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (defaults to "America/Los_Angeles" if not set)
DEFAULT_TIMEZONE=America/Los_Angeles
```

5. Set up Google Calendar API:
   - Go to the [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials:
     1. Go to "Credentials" section
     2. Click "Create Credentials" > "OAuth client ID"
     3. Select "Desktop application" as application type
     4. Download the credentials and save them as `credentials.json` in the project root

## Usage

1. Prepare your image:
   - The image should contain clear event information (title, date, time, location, etc.)
   - Supported formats: JPEG, PNG, WebP, HEIF
   - Make sure the text in the image is readable

2. Run the script:
```bash
python main.py path/to/your/image.jpg
```

3. First-time setup:
   - A browser window will open for Google OAuth authentication
   - Sign in with your Google account
   - Authorize the application to access your calendar
   - The authentication tokens will be saved locally as `token.json`

4. The script will:
   - Analyze the image using GPT-4o 
   - Extract event details including:
     * Event title
     * Start date and time
     * End date and time
     * Location (if available)
     * Description (if available)
   - Create the event in your Google Calendar
   - Provide a link to view the created event

## Error Handling

The application includes comprehensive error handling for:
- Invalid image files or unsupported formats
- OpenAI API issues (invalid key, rate limits, etc.)
- Google Calendar API authentication problems
- Network connectivity issues
- Invalid date/time formats
- Missing required event information

## File Structure

- `main.py`: Main application script
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (create this file)
- `.env.template`: Template for environment variables
- `credentials.json`: Google OAuth credentials (download from Google Cloud Console)
- `token.json`: OAuth tokens (automatically generated)
- `.gitignore`: Git ignore rules for sensitive files

## Security Notes

- Never commit your `.env` file or credentials
- Keep your OAuth credentials secure
- The application stores authentication tokens locally in `token.json`
- The `.gitignore` file is configured to prevent accidental commits of sensitive files

## Troubleshooting

1. **OpenAI API Issues**:
   - Ensure your API key is valid and has access to GPT-4o
   - Check your API usage and limits

2. **Google Calendar API Issues**:
   - Verify that the Calendar API is enabled in your Google Cloud Project
   - Ensure `credentials.json` is properly configured
   - If authentication fails, delete `token.json` and try again

3. **Image Processing Issues**:
   - Ensure the image is in a supported format
   - Check that the image contains clear, readable text
   - Verify the image file exists and is accessible

## Contributing

Feel free to submit issues and enhancement requests!

## Upcoming Features

- **Ollama Local LLMs Support**:  
  We are working on integrating support for running large language models locally via Ollama. This enhancement will allow:
  - Offline processing of image-based event extraction.
  - Reduced dependency on cloud APIs.
  - Enhanced customization and potentially improved response times in environments with limited connectivity. 