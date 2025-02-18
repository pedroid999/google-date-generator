from fastapi import FastAPI, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from main import main as process_image
from debug import debug_log, setup_debug_mode, log_debug
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Check if we're in debug mode
DEBUG = "--debug" in sys.argv
if DEBUG:
    setup_debug_mode()
    logger.info("Running in debug mode")

app = FastAPI(
    title="Google Calendar Event Generator API",
    description="API for generating Google Calendar events from images",
    version="1.0.0",
    debug=DEBUG
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests in debug mode"""
    if DEBUG:
        log_debug(f"Request: {request.method} {request.url}")
        log_debug(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    if DEBUG:
        log_debug(f"Response status: {response.status_code}")
    
    return response

@app.post("/api/process-image")
@debug_log
async def process_image_endpoint(file: UploadFile):
    """
    Process an uploaded image and create a Google Calendar event.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Create a temporary file to store the uploaded image
        with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file.flush()
            
            if DEBUG:
                log_debug(f"Processing image: {file.filename}")
                log_debug(f"Temp file created at: {temp_file.name}")
            
            # Process the image and create the calendar event
            event_link = process_image(temp_file.name)
            
            # Clean up the temporary file
            os.unlink(temp_file.name)
            
            if DEBUG:
                log_debug(f"Event created successfully: {event_link}")
            
            return {"success": True, "event_link": event_link}
    
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        if DEBUG:
            log_debug(f"Error details: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
@debug_log
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"} 