#!/usr/bin/env python3
"""
Quick setup script - creates DB and a default admin user.
Run this after installing requirements.
"""

import os
import sys
import subprocess

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def run(cmd):
    print(f">> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    print("=== Team Task Manager Setup ===\n")

    run("python manage.py migrate")

    print("\n--- Creating superuser for Django admin panel ---")
    run("python manage.py createsuperuser")

    print("\n✅ Setup complete! Run: python manage.py runserver")
