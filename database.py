import sqlite3
import datetime
from typing import List, Dict
import os

class SignupDatabase:
    def __init__(self, db_path: str = "signups.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_signup(self, email: str, ip_address: str = None, user_agent: str = None) -> bool:
        """Add a new email signup"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO signups (email, ip_address, user_agent)
                VALUES (?, ?, ?)
            ''', (email.lower().strip(), ip_address, user_agent))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Email already exists
            return False
        except Exception as e:
            print(f"Error adding signup: {e}")
            return False
    
    def get_all_signups(self) -> List[Dict]:
        """Get all signups"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, signup_date, ip_address, status
            FROM signups
            ORDER BY signup_date DESC
        ''')
        
        signups = []
        for row in cursor.fetchall():
            signups.append({
                'id': row[0],
                'email': row[1],
                'signup_date': row[2],
                'ip_address': row[3],
                'status': row[4]
            })
        
        conn.close()
        return signups
    
    def get_signup_count(self) -> int:
        """Get total number of signups"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM signups')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM signups WHERE email = ?', (email.lower().strip(),))
        exists = cursor.fetchone()[0] > 0
        
        conn.close()
        return exists
    
    def delete_signup(self, signup_id: int) -> bool:
        """Delete a signup by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM signups WHERE id = ?', (signup_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting signup: {e}")
            return False
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export signups to CSV file"""
        if filename is None:
            filename = f"signups_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        import csv
        signups = self.get_all_signups()
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'email', 'signup_date', 'ip_address', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for signup in signups:
                writer.writerow(signup)
        
        return filename

# Utility functions
def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None 