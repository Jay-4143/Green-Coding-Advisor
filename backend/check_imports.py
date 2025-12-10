#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check if all imports work correctly"""
import sys
import traceback

print("Checking imports...")
print("=" * 50)

modules_to_check = [
    "app.config",
    "app.database",
    "app.models",
    "app.schemas",
    "app.auth",
    "app.logger",
    "app.ml_predictor",
    "app.badge_service",
    "app.streak_service",
    "app.email_service",
    "app.chatbot_service",
    "app.report_generator",
    "app.error_handlers",
    "app.routers.auth",
    "app.routers.submissions",
    "app.routers.metrics",
    "app.routers.advisor",
    "app.routers.chatbot",
    "app.routers.projects",
    "app.routers.teams",
    "app.routers.badges",
    "app.routers.reports",
    "app.routers.streaks",
    "app.main",
]

errors = []
for module_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"OK: {module_name}")
    except Exception as e:
        print(f"ERROR: {module_name} - {e}")
        errors.append((module_name, e))
        traceback.print_exc()
        print()

print("=" * 50)
if errors:
    print(f"\nFound {len(errors)} errors:")
    for module_name, error in errors:
        print(f"  - {module_name}: {error}")
    sys.exit(1)
else:
    print("\nAll imports successful!")
    print("\nTrying to create app...")
    try:
        from app.main import create_app
        app = create_app()
        print("App created successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR creating app: {e}")
        traceback.print_exc()
        sys.exit(1)

