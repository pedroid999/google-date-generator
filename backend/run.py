import uvicorn
import argparse
from dotenv import load_dotenv

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the FastAPI backend server")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv("config/.env")
    
    # Configure uvicorn settings
    config = {
        "app": "app:app",
        "host": args.host,
        "port": args.port,
        "reload": True,  # Enable auto-reload
        "log_level": "debug" if args.debug else "info",
    }

    if args.debug:
        config.update({
            "reload_dirs": ["./"],  # Watch current directory for changes
            "workers": 1,  # Use single worker in debug mode
            "timeout_keep_alive": 0,  # Disable keep-alive timeout
        })
    
    # Run the server
    uvicorn.run(**config)

if __name__ == "__main__":
    main() 