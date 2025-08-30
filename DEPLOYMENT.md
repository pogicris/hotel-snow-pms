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