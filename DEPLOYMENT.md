# Hotel Snow PMS - Deployment Guide

## Environment Variables for Production (Render.com)

Set these environment variables in your Render dashboard:

### Required Variables:
- `DEBUG=False`
- `SECRET_KEY=your-very-long-random-secret-key-here-at-least-50-characters`
- `DATABASE_URL=postgresql://user:password@host:port/database` (provided by Render)
- `ALLOWED_HOSTS=hotel-snow-pms-docker.onrender.com,yourdomain.com`

### Optional Variables (with defaults):
- `SECURE_SSL_REDIRECT=True` (default: True in production)
- `SECURE_HSTS_SECONDS=31536000` (default: 1 year)

## Database Migration and Setup

The Docker container will automatically:
1. Run database migrations
2. Create initial users (if they don't exist)
3. Setup rooms and room types (if they don't exist)

## Initial Login Credentials

After successful deployment, use these credentials:
- **Super Admin**: `superadmin` / `snow2024!`
- **Admin**: `admin` / `admin2024!`
- **Front Desk**: `frontdesk` / `front2024!`

## Health Check

Visit `/health/` to check if the application is running correctly.

## Common Issues Fixed

1. **Database migrations not running** - Now runs automatically on container start
2. **Missing initial data** - Users and rooms are created automatically
3. **Static files not served** - Properly configured with WhiteNoise
4. **Security warnings** - Production security settings enabled
5. **ALLOWED_HOSTS not configured** - Now includes render domain by default

## Manual Migration (if needed)

If you need to run migrations manually:
```bash
python manage.py migrate
python manage.py create_initial_users
python manage.py setup_rooms
```

## 📊 NEW: Excel Backup System

### Features Added:
- **Automatic Backup**: Every 10 minutes (144 backups stored for 24-hour rotation)
- **Manual Export/Import**: Download current data or import from Excel
- **24-Hour Rotation**: Automatically removes backups older than 24 hours
- **Backup Management**: View, download, and manage all backups

### Additional Environment Variables for Production:
- `REDIS_URL=redis://red-xxxxx:6379` (Add Redis service in Render dashboard)

### Render Configuration Required:
1. **Add Redis Service**: 
   - Go to Render dashboard → Add Service → Redis
   - Copy the Redis URL to `REDIS_URL` environment variable
2. **The startup script automatically handles**:
   - Database migrations
   - Celery worker (processes backup tasks)
   - Celery beat scheduler (triggers 10-minute backups)
   - Gunicorn web server

### How to Use:
1. **Access**: Admin menu → Backup Management (Super User only)
2. **Export Data**: Click "Export Current Data" to download Excel file
3. **Import Data**: Use "Import Data" to upload Excel file with bookings
4. **Manual Backup**: Create backup stored in database
5. **View History**: See all automatic and manual backups with download options

### Backup Schedule:
- **Every 10 minutes**: Automatic backup created
- **Every hour**: Old backup cleanup
- **24-hour retention**: Only keeps last 144 automatic backups (1 day)
- **Manual backups**: Preserved until manually deleted

### Excel Format:
- **Bookings Sheet**: All booking data with guest info, dates, payments
- **Rooms Sheet**: Room configuration and rates
- **Formatted**: Professional styling with headers and auto-sized columns

### Important Notes:
- Backups are stored in PostgreSQL database (binary data)
- Automatic system handles database migrations and data setup
- Manual backups can be deleted, automatic ones are protected
- Import validates data and shows detailed error reports