#!/usr/bin/env python
"""
Seed script to populate MongoDB with test users, submissions, badges, and teams.
Run from the backend directory:  python seed_users.py
"""
import asyncio
import sys
import os
import random
from datetime import datetime, timedelta

# Add the parent directory so app imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.mongo import get_mongo_client, get_next_sequence
from app.config import settings
from app.auth import get_password_hash
from app.badge_service import BadgeService


# ── User definitions ──────────────────────────────────────────────────────────
USERS = [
    {"username": "Khagesh Patel",  "email": "khageshpatel23@gmail.com",  "scores": [74, 68, 76, 71, 73]},
    {"username": "Keyur Patel",    "email": "keyurpatel1@gmail.com",     "scores": [62, 67, 64, 69]},
    {"username": "Heet Ravaliya",  "email": "ravaliyaheet76@gmail.com",  "scores": [81, 75, 78, 80, 76]},
    {"username": "Abhi Patel",     "email": "abhipatel4@gmail.com",      "scores": [55, 60, 58, 61]},
    {"username": "Sanchay Sood",   "email": "ssanchay0@gmail.com",       "scores": [82, 79, 84, 80, 78, 83]},
    {"username": "Subham Kumar",   "email": "subhkumar@gmail.com",       "scores": [70, 66, 72, 68]},
    {"username": "Nevil Savaliya", "email": "nevils890@gmail.com",       "scores": [76, 72, 74, 73, 75]},
    {"username": "Yash Panday",    "email": "yypanday34@gmail.com",      "scores": [59, 64, 62]},
]

# ── Sample code snippets for submissions (varied languages) ───────────────────
SAMPLE_CODES = {
    "python": [
        "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n",
        "result = []\nfor i in range(len(items)):\n    if items[i] > 0:\n        result.append(items[i] * 2)\n",
        "total = 0\nfor num in numbers:\n    total += num\nprint(total)\n",
        "data = [x**2 for x in range(100)]\nfiltered = [x for x in data if x % 2 == 0]\nresult = sum(filtered)\n",
        "import os\ndef read_files(paths):\n    contents = []\n    for path in paths:\n        with open(path) as f:\n            contents.append(f.read())\n    return contents\n",
    ],
    "javascript": [
        "function findMax(arr) {\n  let max = arr[0];\n  for (let i = 1; i < arr.length; i++) {\n    if (arr[i] > max) max = arr[i];\n  }\n  return max;\n}\n",
        "const results = [];\nfor (let i = 0; i < items.length; i++) {\n  results.push(items[i] * 2);\n}\n",
        "async function fetchAll(urls) {\n  const results = await Promise.all(urls.map(url => fetch(url)));\n  return results;\n}\n",
    ],
    "java": [
        "public class Sort {\n  public static void sort(int[] arr) {\n    for (int i = 0; i < arr.length; i++) {\n      for (int j = 0; j < arr.length - 1; j++) {\n        if (arr[j] > arr[j+1]) {\n          int temp = arr[j];\n          arr[j] = arr[j+1];\n          arr[j+1] = temp;\n        }\n      }\n    }\n  }\n}\n",
        "public class Main {\n  public static String concat(List<String> items) {\n    StringBuilder sb = new StringBuilder();\n    for (String s : items) sb.append(s);\n    return sb.toString();\n  }\n}\n",
    ],
    "c": [
        "#include <stdio.h>\n\nint main() {\n    int arr[] = {5, 3, 8, 1, 9};\n    int n = sizeof(arr)/sizeof(arr[0]);\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n-1; j++) {\n            if (arr[j] > arr[j+1]) {\n                int t = arr[j]; arr[j] = arr[j+1]; arr[j+1] = t;\n            }\n        }\n    }\n    return 0;\n}\n",
    ],
}

DEFAULT_PASSWORD = "Test@1234"


async def seed():
    client = get_mongo_client()
    db = client[settings.mongodb_db]
    
    print("=" * 60)
    print("  Green Coding Advisor — Seed Script")
    print("=" * 60)
    
    # Initialize default badges first
    await BadgeService.initialize_default_badges(db)
    print("[OK] Default badges initialized")
    
    # Load badge definitions
    all_badges = await db["badges"].find({}).to_list(length=None)
    badge_map = {b["name"]: b for b in all_badges}
    
    hashed_pw = get_password_hash(DEFAULT_PASSWORD)
    user_ids = {}
    
    # ── Create Users ──────────────────────────────────────────────────────────
    for user_data in USERS:
        existing = await db["users"].find_one({"email": user_data["email"]})
        if existing:
            user_ids[user_data["email"]] = existing["id"]
            print(f"[SKIP] User '{user_data['username']}' already exists (id={existing['id']})")
            continue
        
        user_id = await get_next_sequence(db, "users")
        user_doc = {
            "id": user_id,
            "email": user_data["email"],
            "username": user_data["username"],
            "hashed_password": hashed_pw,
            "role": "developer",
            "is_active": True,
            "is_verified": True,
            "otp": None,
            "otp_expiry": None,
            "email_verification_token": None,
            "password_reset_token": None,
            "password_reset_expires": None,
            "current_streak": random.randint(1, 7),
            "longest_streak": random.randint(5, 15),
            "last_submission_date": None,
            "created_at": datetime.utcnow() - timedelta(days=random.randint(10, 60)),
            "updated_at": datetime.utcnow(),
        }
        await db["users"].insert_one(user_doc)
        user_ids[user_data["email"]] = user_id
        print(f"[OK] Created user '{user_data['username']}' (id={user_id})")
    
    # ── Create Submissions ────────────────────────────────────────────────────
    languages = list(SAMPLE_CODES.keys())
    
    for user_data in USERS:
        uid = user_ids.get(user_data["email"])
        if not uid:
            continue
        
        # Check if user already has submissions
        existing_count = await db["submissions"].count_documents({"user_id": uid, "status": "completed"})
        if existing_count > 0:
            print(f"[SKIP] User '{user_data['username']}' already has {existing_count} submissions")
            continue
        
        for i, score in enumerate(user_data["scores"]):
            lang = random.choice(languages)
            code = random.choice(SAMPLE_CODES[lang])
            code_len = len(code)
            
            # Realistic metrics based on score
            energy = round(random.uniform(0.01, 0.08), 4)
            co2 = round(energy * 0.475 * random.uniform(0.8, 1.3), 4)
            cpu_time = round(random.uniform(0.5, 5.0), 2)
            memory_kb = round(code_len / 1024 + random.uniform(0.2, 1.5), 2)
            complexity = round(random.uniform(2.0, 7.0), 2)
            
            sub_id = await get_next_sequence(db, "submissions")
            created_at = datetime.utcnow() - timedelta(
                days=random.randint(1, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            sub_doc = {
                "id": sub_id,
                "user_id": uid,
                "project_id": None,
                "code_content": code,
                "language": lang,
                "filename": f"code_{i+1}.{lang if lang != 'javascript' else 'js'}",
                "status": "completed",
                "green_score": score,
                "energy_consumption_wh": energy,
                "co2_emissions_g": co2,
                "cpu_time_ms": cpu_time,
                "memory_usage_mb": memory_kb,
                "complexity_score": complexity,
                "analysis_results": {"patterns_found": random.randint(1, 5)},
                "suggestions": [],
                "created_at": created_at,
                "analyzed_at": created_at + timedelta(seconds=random.randint(2, 10)),
            }
            await db["submissions"].insert_one(sub_doc)
        
        print(f"[INFO] Created {len(user_data['scores'])} submissions for '{user_data['username']}'")
    
    # ── Award Badges ──────────────────────────────────────────────────────────
    # Badge assignment based on scores and submission count
    badge_assignments = {
        "khageshpatel23@gmail.com": ["First Steps", "Loop Optimizer", "Async Champion"],
        "keyurpatel1@gmail.com":    ["First Steps"],
        "ravaliyaheet76@gmail.com": ["First Steps", "Loop Optimizer", "Async Champion", "Sustainability Expert"],
        "abhipatel4@gmail.com":     ["First Steps"],
        "ssanchay0@gmail.com":      ["First Steps", "Loop Optimizer", "Async Champion", "Sustainability Expert"],
        "subhkumar@gmail.com":      ["First Steps"],
        "nevils890@gmail.com":      ["First Steps", "Loop Optimizer", "Async Champion"],
        "yypanday34@gmail.com":     ["First Steps"],
    }
    
    for email, badge_names in badge_assignments.items():
        uid = user_ids.get(email)
        if not uid:
            continue
        
        for badge_name in badge_names:
            badge = badge_map.get(badge_name)
            if not badge:
                continue
            
            existing = await db["user_badges"].find_one({"user_id": uid, "badge_id": badge["id"]})
            if existing:
                continue
            
            ub_id = await get_next_sequence(db, "user_badges")
            await db["user_badges"].insert_one({
                "id": ub_id,
                "user_id": uid,
                "badge_id": badge["id"],
                "earned_at": datetime.utcnow() - timedelta(days=random.randint(1, 20)),
            })
        
        print(f"[INFO] Awarded {len(badge_names)} badge(s) to '{email}'")
    
    # ── Create Teams ──────────────────────────────────────────────────────────
    teams_data = [
        {
            "name": "Team Alpha",
            "description": "Frontend and Backend optimization specialists",
            "admin_email": "khageshpatel23@gmail.com",
            "member_emails": ["keyurpatel1@gmail.com", "ravaliyaheet76@gmail.com", "abhipatel4@gmail.com"],
        },
        {
            "name": "Team Beta",
            "description": "Sustainable code research and development",
            "admin_email": "ssanchay0@gmail.com",
            "member_emails": ["subhkumar@gmail.com", "nevils890@gmail.com", "yypanday34@gmail.com"],
        },
    ]
    
    for team_data in teams_data:
        existing_team = await db["teams"].find_one({"name": team_data["name"]})
        if existing_team:
            print(f"[SKIP] Team '{team_data['name']}' already exists")
            continue
        
        admin_uid = user_ids.get(team_data["admin_email"])
        if not admin_uid:
            print(f"[WARN] Admin user not found for team '{team_data['name']}'")
            continue
        
        team_id = await get_next_sequence(db, "teams")
        team_doc = {
            "id": team_id,
            "name": team_data["name"],
            "description": team_data["description"],
            "created_by": admin_uid,
            "created_at": datetime.utcnow() - timedelta(days=random.randint(5, 20)),
        }
        await db["teams"].insert_one(team_doc)
        
        # Add admin as team member
        member_id = await get_next_sequence(db, "team_members")
        await db["team_members"].insert_one({
            "id": member_id,
            "team_id": team_id,
            "user_id": admin_uid,
            "role": "admin",
            "joined_at": datetime.utcnow() - timedelta(days=random.randint(5, 20)),
        })
        
        # Add other members
        for member_email in team_data["member_emails"]:
            member_uid = user_ids.get(member_email)
            if not member_uid:
                continue
            
            member_id = await get_next_sequence(db, "team_members")
            await db["team_members"].insert_one({
                "id": member_id,
                "team_id": team_id,
                "user_id": member_uid,
                "role": "member",
                "joined_at": datetime.utcnow() - timedelta(days=random.randint(1, 15)),
            })
        
        print(f"[INFO] Created team '{team_data['name']}' with {1 + len(team_data['member_emails'])} members")
    
    print()
    print("=" * 60)
    print("  [OK] Seed completed successfully!")
    print(f"  [INFO] All users have password: {DEFAULT_PASSWORD}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(seed())
