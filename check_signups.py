#!/usr/bin/env python3
"""
Quick script to check signup database
Usage: python check_signups.py
"""

from database import SignupDatabase
import sys

def main():
    print("🏥 MediBuddy Signup Database")
    print("=" * 40)
    
    try:
        db = SignupDatabase()
        
        # Get basic stats
        total = db.get_signup_count()
        print(f"📊 Total Signups: {total}")
        
        if total == 0:
            print("📭 No signups yet!")
            return
        
        print("\n📧 Recent Signups:")
        print("-" * 40)
        
        # Get all signups
        signups = db.get_all_signups()
        
        # Display in a nice format
        for i, signup in enumerate(signups[:10], 1):  # Show last 10
            print(f"{i:2d}. {signup['email']:<30} | {signup['signup_date']}")
        
        if len(signups) > 10:
            print(f"\n... and {len(signups) - 10} more signups")
        
        print(f"\n💾 Database file: signups.db")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 