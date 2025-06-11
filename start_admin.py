#!/usr/bin/env python3
"""
Quick script to run the admin panel
Usage: python start_admin.py
"""

import subprocess
import sys

def run_admin():
    print("🚀 Starting MediBuddy Admin Panel...")
    print("🌐 Admin panel will be available at: http://localhost:8502")
    print("🔑 Admin password: cavari2024admin")
    print("---")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "admin.py", 
            "--server.port", "8502"
        ])
    except KeyboardInterrupt:
        print("\n👋 Admin panel stopped")

if __name__ == "__main__":
    run_admin() 