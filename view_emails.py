#!/usr/bin/env python3
"""
Email Viewer for MedDoc Assistant Signups
==========================================
Simple script to view, search, and export signup emails from the database.
"""

from database import SignupDatabase
import sys
from datetime import datetime

def main():
    """Main function to display signup emails"""
    db = SignupDatabase()
    
    print("=" * 60)
    print("📧 MEDOC ASSISTANT - SIGNUP EMAILS")
    print("=" * 60)
    
    # Get all signups
    signups = db.get_all_signups()
    total_count = db.get_signup_count()
    
    print(f"Total Signups: {total_count}\n")
    
    if not signups:
        print("No signups found in the database.")
        return
    
    # Display all signups
    print("📋 ALL SIGNUPS:")
    print("-" * 60)
    print(f"{'#':<3} {'Email':<35} {'Date':<20} {'Status':<10}")
    print("-" * 60)
    
    for i, signup in enumerate(signups, 1):
        email = signup['email']
        date = signup['signup_date'][:16]  # Show date without seconds
        status = signup['status']
        print(f"{i:<3} {email:<35} {date:<20} {status:<10}")
    
    print("-" * 60)
    print(f"Total: {total_count} signups\n")
    
    # Export option
    print("📤 EXPORT OPTIONS:")
    export = input("Would you like to export to CSV? (y/n): ").strip().lower()
    
    if export == 'y':
        filename = db.export_to_csv()
        print(f"✅ Exported to: {filename}")
    
    # Search option
    print("\n🔍 SEARCH:")
    search_term = input("Enter email to search (or press Enter to skip): ").strip()
    
    if search_term:
        found = [s for s in signups if search_term.lower() in s['email'].lower()]
        if found:
            print(f"\n Found {len(found)} matching email(s):")
            for signup in found:
                print(f"  - {signup['email']} ({signup['signup_date'][:16]})")
        else:
            print("  No matching emails found.")

def list_emails_only():
    """Simple function to just list emails"""
    db = SignupDatabase()
    signups = db.get_all_signups()
    
    print("Email List:")
    print("-" * 40)
    for signup in signups:
        print(signup['email'])

def get_recent_signups(days=7):
    """Get signups from the last N days"""
    db = SignupDatabase()
    signups = db.get_all_signups()
    
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    
    recent = []
    for signup in signups:
        signup_date = datetime.strptime(signup['signup_date'], '%Y-%m-%d %H:%M:%S')
        if signup_date >= cutoff_date:
            recent.append(signup)
    
    print(f"Recent signups (last {days} days): {len(recent)}")
    for signup in recent:
        print(f"  - {signup['email']} ({signup['signup_date'][:16]})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_emails_only()
        elif sys.argv[1] == "--recent":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            get_recent_signups(days)
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python view_emails.py          # Interactive view")
            print("  python view_emails.py --list   # Just list emails")
            print("  python view_emails.py --recent [days]  # Recent signups")
            print("  python view_emails.py --help   # Show this help")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        main() 