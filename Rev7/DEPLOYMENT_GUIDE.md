# Hotel Snow PMS - Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Setup Steps

1. **Navigate to project directory**:
   ```bash
   cd hotel_pms_project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database and initial data**:
   ```bash
   python manage.py migrate
   python manage.py setup_rooms
   python manage.py create_initial_users
   ```

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
   
   Or simply double-click `start_local.bat` on Windows.

5. **Access the application**:
   - Open your browser to http://127.0.0.1:8000
   - Login with any of these accounts:
     - **Super User**: `superadmin` / `snow2024!`
     - **Admin User**: `admin` / `admin2024!`
     - **Member User**: `frontdesk` / `front2024!`

## Render.com Deployment

### Account Setup
- **URL**: https://render.com
- **Email**: con4cros@gmail.com
- **Password**: 1971!Kendocho

### Deployment Steps

1. **Login to Render Dashboard**
   - Go to https://dashboard.render.com
   - Sign in with the provided credentials

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your Git repository
   - Choose the repository containing this code

3. **Configure Web Service**
   - **Name**: `hotel-snow-pms`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn hotel_pms.wsgi:application`

4. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - **Name**: `hotel-snow-pms-db`
   - **Database Name**: `hotel_pms`
   - **User**: `hotel_pms_user`

5. **Set Environment Variables**
   In the web service settings, add these environment variables:
   - `DATABASE_URL`: (automatically set when you connect the database)
   - `SECRET_KEY`: Generate a secure secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`

6. **Connect Database to Web Service**
   - In web service settings, go to "Environment"
   - Add DATABASE_URL from your PostgreSQL service
   - Format: `postgres://username:password@hostname:port/database`

7. **Deploy**
   - Click "Deploy Latest Commit"
   - Wait for build to complete
   - Your app will be available at `https://your-app-name.onrender.com`

### Post-Deployment Setup

1. **Access Django Admin**:
   - Go to `https://your-app-name.onrender.com/admin/`
   - Login with `superadmin` / `snow2024!`

2. **Verify Room Setup**:
   - Check that all 40+ rooms are created
   - Verify room types and rates are set

3. **Test Functionality**:
   - Create a test booking
   - Check timeline visualization
   - Test user permissions

## Environment Variables Reference

### Development (.env file)
```
SECRET_KEY=django-insecure-6^)i)k=*-1!jz5$1cj#l1cwaebcgfmag7xsz%6$low1h(5#zyf
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (Render.com)
```
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgres://user:pass@hostname:port/dbname
```

## Troubleshooting

### Common Issues

1. **Migration Errors**:
   ```bash
   python manage.py migrate --fake-initial
   ```

2. **Static Files Not Loading**:
   ```bash
   python manage.py collectstatic --no-input
   ```

3. **Database Connection Issues**:
   - Verify DATABASE_URL format
   - Check database service is running
   - Ensure database user has proper permissions

4. **Build Fails on Render**:
   - Check build.sh has execute permissions
   - Verify all dependencies in requirements.txt
   - Check Python version compatibility

### Performance Optimization

1. **Enable Database Connection Pooling**:
   - Already configured in settings.py

2. **Static File Compression**:
   - WhiteNoise automatically compresses static files

3. **Browser Caching**:
   - Configured for static assets

## Security Checklist

- ✅ SECRET_KEY is properly set in production
- ✅ DEBUG is False in production
- ✅ ALLOWED_HOSTS is configured correctly
- ✅ Database credentials are secure
- ✅ CSRF protection is enabled
- ✅ User passwords are encrypted
- ✅ Session security is configured

## Backup and Maintenance

### Database Backup (Render)
- Use Render's automatic PostgreSQL backups
- Manual backup via pg_dump is also available

### Regular Maintenance
- Update dependencies monthly
- Monitor error logs
- Review user accounts quarterly
- Update room rates as needed

### Monitoring
- Check application logs in Render dashboard
- Monitor database performance
- Track user activity

## Support

For technical issues:
1. Check Render service logs
2. Review Django error logs
3. Verify environment variables
4. Test with local development setup

The system includes comprehensive logging and error handling for production reliability.