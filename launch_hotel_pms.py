#!/usr/bin/env python3
"""
Hotel Snow PMS Launcher
Simple launcher script that ensures all dependencies are installed and starts the server
"""

import sys
import subprocess
import os
from pathlib import Path

def print_banner():
    print("=" * 50)
    print("    🏨 Hotel Snow PMS Launcher")
    print("=" * 50)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], stdout=subprocess.DEVNULL)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def setup_database():
    """Setup database if needed"""
    db_file = Path("db.sqlite3")
    
    if not db_file.exists():
        print("🗄️  Setting up database...")
        try:
            subprocess.check_call([sys.executable, "manage.py", "migrate"])
            subprocess.check_call([sys.executable, "manage.py", "setup_rooms"])
            subprocess.check_call([sys.executable, "manage.py", "create_initial_users"])
            print("✅ Database setup complete!")
            print()
            print("🔑 Login Credentials:")
            print("   - Super User: superadmin / snow2024!")
            print("   - Admin User: admin / admin2024!")
            print("   - Member User: frontdesk / front2024!")
            print()
        except subprocess.CalledProcessError as e:
            print(f"❌ Database setup failed: {e}")
            input("Press Enter to exit...")
            sys.exit(1)
    else:
        print("✅ Database already exists")
        # Run migrations in case there are updates
        subprocess.check_call([sys.executable, "manage.py", "migrate"], 
                            stdout=subprocess.DEVNULL)

def start_server():
    """Start the Django development server"""
    print("🚀 Starting Hotel Snow PMS server...")
    print()
    print("📍 Server URL: http://127.0.0.1:8000")
    print("🔑 Use the login credentials shown above")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.check_call([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        input("Press Enter to exit...")

def main():
    """Main launcher function"""
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if manage.py exists
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found!")
        print("Make sure you're running this from the hotel_pms_project directory")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print_banner()
    check_python_version()
    install_dependencies()
    setup_database()
    start_server()

if __name__ == "__main__":
    main()