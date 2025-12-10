#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to start the server and capture errors"""
import sys
import traceback

try:
    print("Importing app...")
    from app.main import app
    print("App imported successfully")
    
    print("\nStarting server...")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
except Exception as e:
    print(f"\nError occurred: {e}")
    print(f"\nError type: {type(e).__name__}")
    print(f"\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

