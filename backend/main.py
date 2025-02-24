#!/usr/bin/env python3
"""
Google Calendar Event Generator from Images
This script processes images containing event information using OpenAI's GPT-4 Vision
and creates events in Google Calendar using the Google Calendar API via LangChain.
"""

import os
import json
import base64
import logging
import re
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def setup_google_credentials() -> Credentials:
    """
    Set up and return Google Calendar API credentials.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def encode_image(image_path: str) -> str:
    """
    Encode an image file to base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_event_details(image_path: str) -> Dict[str, Any]:
    """
    Extract event details from an image using OpenAI's GPT-4o.
    """
    try:
        # Read the default timezone from the environment variable, defaulting to "America/Los_Angeles" if not provided.
        default_timezone = os.getenv("DEFAULT_TIMEZONE", "Europe/Madrid")
        
        client = OpenAI()
        
        # Encode the image to base64
        base64_image = encode_image(image_path)
        
        # Prepare the prompt for GPT-4o using the default timezone from .env
        prompt = f"""Please analyze this image and extract event details. 
        Return the information in the following JSON format:
        {{
            "summary": "Event title",
            "start": {{"dateTime": "YYYY-MM-DDTHH:MM:SS", "timeZone": "{default_timezone}"}},
            "end": {{"dateTime": "YYYY-MM-DDTHH:MM:SS", "timeZone": "{default_timezone}"}},
            "location": "Event location",
            "description": "Event description"
        }}
        Ensure all dates and times are in ISO format with timezone information."""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        # Extract and parse the JSON response
        content = response.choices[0].message.content
        logger.info(f"Response: {content}")
        
        pattern = r"```(?:json)?\s*(\{.*\})\s*```"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = match.group(1)
        
        logger.info(f"Response cleaned: {content}")
        
        return json.loads(content)
    
    except Exception as e:
        logger.error(f"Error extracting event details: {str(e)}")
        raise

def validate_event_details(event_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and format the extracted event details.
    """
    required_fields = ['summary', 'start', 'end']
    for field in required_fields:
        if field not in event_details:
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure start and end times are properly formatted
    for time_field in ['start', 'end']:
        if 'dateTime' not in event_details[time_field]:
            raise ValueError(f"Missing dateTime in {time_field}")
        
        # Validate datetime format
        try:
            datetime.fromisoformat(event_details[time_field]['dateTime'].replace('Z', '+00:00'))
        except ValueError as e:
            raise ValueError(f"Invalid datetime format in {time_field}: {str(e)}")
    
    return event_details

def create_calendar_event(credentials: Credentials, event_details: Dict[str, Any]) -> str:
    """
    Create a new event in Google Calendar using the provided details.
    """
    try:
        service = build('calendar', 'v3', credentials=credentials)
        event = service.events().insert(calendarId='primary', body=event_details).execute()
        return event.get('htmlLink')
    except Exception as e:
        logger.error(f"Error creating calendar event: {str(e)}")
        raise

def main(image_path: str):
    """
    Main function to process the image and create a calendar event.
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Validate image file
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Extract event details from image
        logger.info("Extracting event details from image...")
        event_details = extract_event_details(image_path)
        
        # Validate extracted details
        logger.info("Validating event details...")
        validated_details = validate_event_details(event_details)
        
        # Setup Google Calendar credentials
        logger.info("Setting up Google Calendar credentials...")
        credentials = setup_google_credentials()
        
        # Create calendar event
        logger.info("Creating calendar event...")
        event_link = create_calendar_event(credentials, validated_details)
        
        logger.info(f"Event created successfully! View it here: {event_link}")
        return event_link
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create Google Calendar events from images")
    parser.add_argument("image_path", help="Path to the image containing event details")
    args = parser.parse_args()
    
    main(args.image_path)