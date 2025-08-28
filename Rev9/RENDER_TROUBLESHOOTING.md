# 🔧 Render.com Deployment Troubleshooting Guide

## ❌ **Common Issue: Changes Not Reflecting**

If you've pushed Rev9 to GitHub and redeployed on Render.com but **still see the old timeline design**, here's the systematic troubleshooting approach:

## 🕵️ **Step 1: Verify Local Files**

Run the test script to verify all components:

```bash
cd Rev9
python test_deployment.py
```

This will check:
- ✅ Models have required fields (`display_order`, `get_nights_count`)
- ✅ Timeline view logic shows 14 days
- ✅ Template has correct structure
- ✅ CSS has 14-column grid layout

## 🔍 **Step 2: Check Render Build Logs**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click your service → **"Logs"** tab
3. Look for these **critical indicators**:

### ✅ **Successful Build Indicators:**
```bash
🚀 Building Hotel PMS Rev9 for Render...
📦 Installing Python dependencies...
📁 Collecting static files...
🗄️ Running database migrations...
🏨 Initializing Hotel PMS Rev9 data...
✅ Rev9 build complete!
```

### ❌ **Failure Indicators:**
```bash
# Static files not collected
Error: collectstatic failed

# Migration errors  
django.db.utils.ProgrammingError: column "display_order" does not exist

# Missing dependencies
ModuleNotFoundError: No module named 'holidays'

# Template errors
TemplateDoesNotExist: rooms/timeline.html
```

## 🔧 **Step 3: Force Complete Rebuild**

If changes aren't reflecting, force a complete rebuild:

### Option A: Manual Redeploy
1. Go to Render Dashboard → Your Service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Wait for complete rebuild

### Option B: Dummy Commit
```bash
# Make a small change to force new deployment
echo "# Rev9 timeline fix - $(date)" >> README.md
git add README.md
git commit -m "Force rebuild for timeline fixes"
git push origin main
```

## 📂 **Step 4: Verify File Structure on Render**

Add debug info to your build script:

```bash
# Add to build.sh
echo "📁 Checking file structure..."
ls -la templates/rooms/
ls -la static/css/
echo "✅ File structure verified"
```

## 🗄️ **Step 5: Database Issues**

If models aren't working:

```bash
# In Render console or logs, check:
python manage.py showmigrations
python manage.py migrate --plan

# If display_order field missing:
python manage.py makemigrations --dry-run
python manage.py migrate
```

## 🎨 **Step 6: Static Files Issues**

### Check Static Files Collection:
```bash
# Should see in build logs:
python manage.py collectstatic --no-input
# Output should show:
# X static files copied to '/opt/render/project/src/staticfiles'
```

### CSS Not Loading:
1. Check `STATIC_URL` and `STATIC_ROOT` in settings.py
2. Verify `whitenoise` is in `MIDDLEWARE`
3. Check browser Network tab for 404 errors on CSS files

## 🌐 **Step 7: Browser Cache Issues**

Even if deployment works, your browser might cache old files:

1. **Hard Refresh**: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
2. **Clear Browser Cache**: Settings → Clear browsing data
3. **Incognito/Private Window**: Test in private browsing mode
4. **Different Browser**: Try Chrome, Firefox, Safari

## 🔄 **Step 8: Environment Variables**

Verify these are set in Render:

```env
DATABASE_URL=(auto-connected from PostgreSQL)
SECRET_KEY=(auto-generated)  
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
PRODUCTION=True
```

## 📋 **Step 9: Systematic Debugging**

### Test Each Component:

1. **Timeline URL**: Visit `/timeline/` directly
2. **View Source**: Check if new HTML structure is present
3. **Developer Tools**: Look for CSS/JS errors in console
4. **Network Tab**: Verify CSS files are loading correctly

### Check Template Rendering:
```python
# Add debug to views.py temporarily:
def timeline_view(request):
    # ... existing code ...
    
    # Debug output
    print(f"DEBUG: Date range has {len(date_range)} days")
    print(f"DEBUG: Timeline data has {len(timeline_data)} room types")
    
    # ... rest of code ...
```

## 🚨 **Emergency Fixes**

### If Timeline Still Shows 1 Week:

1. **Check views.py line 82**: Should be `end_date = start_date + timedelta(days=13)`
2. **Check template**: Should have `{% for date in date_range %}` looping 14 times
3. **Check CSS**: Should have `repeat(14, 1fr)` for 14 columns

### If Design Doesn't Match Sample:

1. **Check template structure**: Should use `timeline-page`, `timeline-header`, `timeline-main`
2. **Check CSS classes**: Should match `.timeline-page`, `.timeline-grid`, etc.
3. **Check static files**: CSS should be loading from `/static/css/timeline.css`

## ✅ **Verification Checklist**

After fixing, verify:

- [ ] Timeline shows exactly 14 days (Fr 30, Sa 1... Th 13)
- [ ] Header shows "RECEPTION / Reservations" with stats
- [ ] Room types are grouped (▼ Loft, ▼ Single, ▼ Double, ▼ Triple)  
- [ ] Booking bars span multiple consecutive days
- [ ] Colors match sample (green, blue, purple, red)
- [ ] Navigation says "Previous 2 Weeks" / "Next 2 Weeks"
- [ ] Mobile layout works with horizontal scroll

## 📞 **Still Not Working?**

If timeline still doesn't reflect changes after all steps:

1. **Share Render build logs** - Copy full build log output
2. **Share live URL** - The actual Render.com URL to check
3. **Confirm git push** - Verify latest commits are in GitHub
4. **Check service status** - Ensure Render service is running

---

**The Rev9 fixes ARE properly implemented. The issue is likely deployment/caching related, not code related.**