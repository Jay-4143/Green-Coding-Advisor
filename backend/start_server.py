#!/usr/bin/env python
"""Start the FastAPI server with proper error handling"""
import sys
import uvicorn
import traceback

def main():
    try:
        print("Starting Green Coding Advisor Backend Server...")
        print("=" * 60)
        print("Server will be available at: http://localhost:8000")
        print("API Documentation: http://localhost:8000/docs")
        print("=" * 60)
        print()
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",  # Listen on all interfaces to accept both localhost and 127.0.0.1
            port=8000,
            reload=False,  # Disable reload for more stable startup
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nERROR: Failed to start server: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

