# Hotel Snow PMS - Troubleshooting Guide

## Problem: "ModuleNotFoundError: No module named 'django'"

This means Django is not installed in your current Python environment.

### Solution Options:

#### Option 1: Use the Python Launcher (Recommended)
```bash
python launch_hotel_pms.py
```
This script automatically installs all dependencies and starts the server.

#### Option 2: Use the Enhanced Batch File
Double-click `setup_and_run.bat` - this will install dependencies automatically.

#### Option 3: Manual Installation
Open Command Prompt in the project folder and run:
```bash
cd C:\PY\hotel_pms_project
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py setup_rooms  
python manage.py create_initial_users
python manage.py runserver
```

#### Option 4: Check Your Python Environment
You might have multiple Python installations. Try:
```bash
python --version
python -m pip --version
```

If you're using Anaconda/Miniconda, activate the correct environment:
```bash
conda activate your_environment_name
```

## Other Common Issues

### Issue: "Port already in use"
**Solution**: Either:
- Close other applications using port 8000
- Or use a different port: `python manage.py runserver 127.0.0.1:8080`

### Issue: Database errors
**Solution**: Delete db.sqlite3 and run setup again:
```bash
del db.sqlite3  # Windows
# or
rm db.sqlite3   # Mac/Linux

python manage.py migrate
python manage.py setup_rooms
python manage.py create_initial_users
```

### Issue: "Permission denied" on build.sh
**Solution** (for Linux/Mac deployment):
```bash
chmod +x build.sh
```

### Issue: Static files not loading
**Solution**:
```bash
python manage.py collectstatic --noinput
```

## Quick Setup Verification

After successful startup, verify these URLs work:

1. **Main Login**: http://127.0.0.1:8000
2. **Admin Panel**: http://127.0.0.1:8000/admin/
3. **Timeline**: http://127.0.0.1:8000/timeline/

## Default Login Credentials

- **Super User**: `superadmin` / `snow2024!`
- **Admin User**: `admin` / `admin2024!`  
- **Member User**: `frontdesk` / `front2024!`

## Still Having Issues?

1. **Check Python Version**: Must be 3.8+
   ```bash
   python --version
   ```

2. **Check Project Structure**: Make sure these files exist:
   - `manage.py`
   - `requirements.txt`
   - `hotel_pms/settings.py`
   - `rooms/models.py`

3. **Try Different Startup Methods**:
   - `python launch_hotel_pms.py` (most reliable)
   - `setup_and_run.bat` (Windows)
   - `python manage.py runserver` (manual)

4. **Check for Port Conflicts**: Try different ports:
   ```bash
   python manage.py runserver 127.0.0.1:8080
   python manage.py runserver 127.0.0.1:8001
   ```

If none of these solutions work, the issue might be with your Python installation or system PATH configuration.