# 🏨 Hotel PMS Rev9 - Timeline Management System

**Professional hotel management system with enhanced 2-week timeline view, optimized for Render.com deployment.**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

## 🚀 Quick Deploy to Render.com

### One-Click Deployment
1. Fork this repository to your GitHub
2. Connect to [Render.com](https://render.com)
3. Create new Web Service from your GitHub repo
4. Use these settings:
   - **Root Directory**: `/` (or `/Rev9` if in subdirectory)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn hotel_pms.wsgi:application`

### Database Setup
Render will automatically:
- Create PostgreSQL database
- Run migrations
- Initialize room types and demo data
- Set up admin user

## 🎯 Features

### 📅 Enhanced Timeline View
- **2-Week Display**: Professional booking calendar
- **Room Grouping**: Organized by type (Loft, Single, Double, Triple)
- **Color-coded Bookings**: 
  - 🟢 Green: Pencil bookings
  - 🔵 Blue: Fully paid
  - 🟣 Purple: Partial payment
  - 🔴 Red: No-shows
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Click bookings for details, collapsible room sections

### 🏨 Room Management
- **Room Types**: Loft, Single, Double, Triple, Studio rooms
- **Rate Management**: Weekday/weekend pricing with holiday support
- **Occupancy Tracking**: Real-time availability status

### 👥 User Management  
- **Role-based Access**: Admin, Manager, Staff levels
- **Secure Authentication**: Django's built-in security
- **Activity Logging**: Track all booking changes

## 🖥️ Screenshots

### Timeline View
The main timeline displays a 2-week booking overview with room groupings and color-coded reservations, matching professional hotel management standards.

### Dashboard
Clean dashboard with quick stats, recent bookings, and navigation to all system features.

## 🔧 Local Development

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup
```bash
git clone <your-repo>
cd Rev9

# Install dependencies  
pip install -r requirements.txt

# Setup database
python manage.py migrate
python init_production.py

# Run development server
python manage.py runserver
```

### Default Login
- **Username**: `admin`
- **Password**: `HotelAdmin2024!`

## 📦 Production Deployment

### Environment Variables
```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com
PRODUCTION=True
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@yourhotel.com
ADMIN_PASSWORD=secure-password
```

### Render Configuration
The `render.yaml` file includes complete configuration for:
- PostgreSQL database setup
- Environment variables
- Build and start commands
- Security settings

## 🏗️ Architecture

### Tech Stack
- **Backend**: Django 4.2 (Python)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render.com
- **Static Files**: WhiteNoise

### File Structure
```
Rev9/
├── hotel_pms/           # Django project settings
├── rooms/               # Main application
│   ├── models.py       # Database models
│   ├── views.py        # Business logic
│   └── templates/      # HTML templates
├── static/             # CSS, JS, images
├── build.sh           # Render build script
├── init_production.py # Database initialization
├── requirements.txt   # Python dependencies
└── render.yaml       # Render configuration
```

## 🔐 Security

- ✅ CSRF protection enabled
- ✅ Secure headers configured
- ✅ Environment-based secrets
- ✅ Production-ready settings
- ✅ SQL injection protection
- ✅ XSS protection

## 📱 Mobile Support

Rev9 is fully responsive:
- **Mobile Timeline**: Horizontal scroll with optimized touch controls
- **Tablet Layout**: Balanced view with all features accessible
- **Desktop Experience**: Full-featured timeline with advanced interactions

## 🆘 Support & Updates

### Troubleshooting
- Check Render logs for deployment issues
- Verify environment variables are set
- Ensure PostgreSQL database is connected

### Updates
This system is designed for easy updates:
- Push code changes to GitHub
- Render automatically redeploys
- Database migrations run automatically

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django framework for robust backend
- Render.com for seamless deployment
- Bootstrap for responsive design
- Contributors and testers

---

**🌟 Hotel PMS Rev9 - Professional timeline management for modern hotels**