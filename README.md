# Hotel Snow PMS ❄️

A comprehensive Property Management System for Hotel Snow, built with Django 4.2 and Python 3.10.

## Features

### 🏨 Room Management
- **Multiple Room Types**: Studio A, Studio A Promo, Studio B, Studio Deluxe, Family Rooms, Penthouse, Module House, KTV Rooms
- **Specific Room Numbers**: Pre-configured with exact room numbers for each type
- **Room Availability Tracking**: Real-time availability status

### 💰 Rate Management
- **Dynamic Pricing**: Separate weekday and weekend rates
- **Philippine Holiday Support**: Automatic holiday rate application
- **Bulk Rate Updates**: Update all rooms of the same type simultaneously

### 👥 User Authentication & Access Control
- **Three User Levels**:
  - **Admin**: View logs, delete/cancel bookings, manage schedules
  - **Members**: Standard booking operations (no log access)
  - **Super**: Rate management, system memos, user management

### 📅 Timeline & Scheduling
- **Visual Timeline**: Bar-style schedule display
- **Weekly View**: Scrollable week navigation
- **Color-Coded Status**: 
  - 🟢 Green: Fully Paid
  - 🟡 Yellow: Pencil Booked
  - 🔴 Red: No Show
  - 🟣 Purple: Partial Payment

### 📋 Booking Management
- **Check-in Status Tracking**: Multiple status levels
- **Payment Tracking**: Partial and full payment support
- **Guest Information**: Contact details and notes
- **Booking History**: Complete audit trail

## Room Configuration

### Studio A (15 rooms)
- Rooms: 101, 102, 103, 104, 105, 106, 107, 110, 111, 112, 113, 114, 115, 116, 117

### Studio A Promo (4 rooms)
- Rooms: 108, 109, 118, 119

### Studio B (7 rooms)
- Rooms: 201, 203, 205, 207, 209, 211, 212

### Studio Deluxe (5 rooms)
- Rooms: 202, 204, 206, 208, 210

### Family Room w/o Balcony (2 rooms)
- Rooms: 214, 216

### Family Room w/ Balcony (2 rooms)
- Rooms: 213, 215

### Penthouse (2 rooms)
- Rooms: 301, 302

### Module House (2 rooms)
- Rooms: 401, 402

### KTV Rooms (4 rooms)
- Rooms: 501, 502, 503, 504

## Installation & Setup

### Local Development

1. **Clone and Setup**:
   ```bash
   cd hotel_pms_project
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   ```bash
   python manage.py migrate
   python manage.py setup_rooms
   python manage.py createsuperuser
   ```

3. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the Application**:
   - Open http://localhost:8000
   - Login with your superuser credentials

### Render.com Deployment

1. **Create Render Account**: Sign up at render.com with provided credentials
2. **Connect Repository**: Link your Git repository
3. **Create PostgreSQL Database**: Use the Render dashboard
4. **Deploy Web Service**: Use the render.yaml configuration
5. **Set Environment Variables**:
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app.onrender.com
   - `DATABASE_URL`: Automatically set by Render

## User Roles & Permissions

### Super User
- ✅ Manage room rates
- ✅ Create system memos and popups
- ✅ Delete users and bookings
- ✅ View all logs and reports
- ✅ Access Django admin panel

### Admin User
- ✅ View all logs and booking history
- ✅ Delete and cancel bookings
- ✅ Modify schedules and booking status
- ❌ Cannot change room rates
- ❌ Cannot manage users

### Member User
- ✅ Create and modify bookings
- ✅ View timeline and availability
- ✅ Update payment status
- ❌ Cannot view logs
- ❌ Cannot delete bookings

## Key Features

### Rate Management
- **Weekend Rates**: Apply Friday-Saturday and holidays
- **Holiday Integration**: Philippine holiday calendar
- **Bulk Updates**: Change rates for all rooms of same type

### Timeline Visualization
- **Horizontal Scrolling**: Navigate through different weeks
- **Vertical Scrolling**: Browse all room types
- **Color Coding**: Instant status recognition
- **Click Interactions**: Direct access to booking details

### Booking System
- **Smart Rate Calculation**: Automatic weekday/weekend/holiday pricing
- **Conflict Prevention**: Availability checking
- **Status Tracking**: From pencil booking to check-out
- **Payment Management**: Partial and full payment tracking

### Security Features
- **Encrypted Passwords**: Django's built-in security
- **Session Management**: Secure login/logout
- **Permission-Based Access**: Role-specific functionality
- **CSRF Protection**: Form security

## Technology Stack

- **Backend**: Django 4.2, Python 3.10
- **Database**: PostgreSQL (production), SQLite (development)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment**: Render.com
- **Static Files**: WhiteNoise
- **Date/Time**: Philippine timezone (Asia/Manila)

## Support & Maintenance

The system includes comprehensive error handling, logging, and monitoring capabilities suitable for production use. Regular backups and security updates are recommended.

## Deployment Credentials

**Render.com Account**:
- Email: con4cros@gmail.com
- Password: 1971!Kendocho

## Getting Started

1. Access the login page
2. Use your assigned credentials
3. Navigate through the intuitive interface
4. Create bookings using the timeline view
5. Manage rates (Super users only)
6. Monitor system through dashboard

The system is designed for ease of use while maintaining professional hotel management standards.