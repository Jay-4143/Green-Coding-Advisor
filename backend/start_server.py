#!/usr/bin/env python
"""Start the FastAPI server with proper error handling"""
import sys
import os
import traceback

def check_environment():
    """Verify that we are running in the expected environment"""
    try:
        import uvicorn
        return True
    except ImportError:
        print("\n" + "!" * 60)
        print("ERROR: Could not find 'uvicorn' module.")
        print("-" * 60)
        print(f"Current Python: {sys.executable}")
        print(f"Path searching in: {sys.path}")
        print("-" * 60)
        print("\nPOSSIBLE FIXES:")
        print("1. Run the server using the batch script: start_server.bat")
        print("2. Activate your virtual environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("!" * 60 + "\n")
        return False

def main():
    if not check_environment():
        sys.exit(1)
        
    import uvicorn
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

