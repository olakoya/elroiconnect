# ElroiConnect Dating Website - Setup Guide

## Overview
ElroiConnect is a faith-based dating/connection platform built with Python Flask, featuring user registration with video requirements, profile management, matching, messaging, and search functionality.

## Features
- ✅ User registration with mandatory introduction video viewing (like KonnectNow)
- ✅ User authentication and login system
- ✅ Detailed user profiles with photos and bios
- ✅ Profile browsing and search functionality
- ✅ Like system with mutual matching
- ✅ Real-time messaging between matched users
- ✅ Advanced search filters (gender, location, name)
- ✅ Responsive design with modern UI
- ✅ Photo upload capability
- ✅ Faith-focused features (denomination, interests)

## Installation Instructions

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Required Packages

Create a `requirements.txt` file with:

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Project Structure

Create the following directory structure:

```
elroiconnect/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── venv
├── instance
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── intro_videos.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── messages.html
│   ├── conversation.html
│   └── search.html
│
└── static/              # Static files
    ├── logo.svg
    ├── logo-icon.svg    # Icon only
│   ├── logo-text.svg    # Text only
    ├── uploads/         # User uploaded photos
    └── videos/          # Introduction videos
        ├── intro0.mp4
        ├── intro1.mp4
        ├── intro2.mp4
        ├── intro3.mp4
        ├── intro4.mp4
        ├── intro5.mp4
        ├── intro6.mp4
        └── intro7.mp4
```

### 4. Setup Steps

1. **Create the main application file** (`app.py`) with the code from the first artifact

2. **Create the templates folder** and add all HTML template files from the artifacts

3. **Create static folders**:
```bash
mkdir -p static/uploads
mkdir -p static/videos
```

4. **Add introduction videos**: Place 3 short video files (MP4 format) in `static/videos/` named:
   - intro1.mp4 (About the platform)
   - intro2.mp4 (Community guidelines)
   - intro3.mp4 (Safety and privacy)

5. **Update the secret key** in `app.py`:
```python
app.config['SECRET_KEY'] = 'your-actual-secret-key-here-make-it-random-and-long'
```

### 5. Running the Application

1. **Initialize the database** (first time only):
```bash
python3 app.py
```
This will create the SQLite database file `elroiconnect.db`

2. **Run the development server**:
```bash
python3 app.py
```

3. **Access the website**:
Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage Guide

### For Users:

1. **Registration**:
   - Visit the homepage
   - Click "Get Started"
   - Watch at least 2 of the 3 introduction videos
   - Fill out the registration form
   - Create your account

2. **Profile Setup**:
   - Log in with your credentials
   - Navigate to "My Profile"
   - Click "Edit Profile"
   - Add your photo, bio, interests, and other details

3. **Finding Matches**:
   - Browse suggested matches on the dashboard
   - Use the search feature to find specific members
   - Filter by gender, location, or name

4. **Connecting**:
   - View profiles of members you're interested in
   - Click "Like" to show interest
   - When both users like each other, it's a match!
   - Send messages to matched users

5. **Messaging**:
   - Access "Messages" from the navigation
   - View all your conversations
   - Click on a conversation to chat

### For Administrators:

To add admin features, you can extend the User model with an `is_admin` field and create admin-only routes for:
- User management
- Content moderation
- Analytics dashboard

## Customization Options

### 1. Change Color Scheme
Edit the CSS in `templates/base.html`:
```css
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### 2. Add More Profile Fields
Modify the `User` model in `app.py` and update the forms in templates.

### 3. Email Verification
Install Flask-Mail and add email verification during registration.

### 4. Advanced Matching Algorithm
Implement compatibility scoring based on:
- Denomination preferences
- Shared interests
- Age range preferences
- Location proximity

## Security Considerations

⚠️ **Important for Production:**

1. **Change the secret key** to a strong, random value
2. **Use environment variables** for sensitive configuration
3. **Implement HTTPS** for secure connections
4. **Add email verification** to prevent fake accounts
5. **Implement rate limiting** to prevent abuse
6. **Use PostgreSQL** instead of SQLite for production
7. **Add CSRF protection** (Flask-WTF)
8. **Validate and sanitize** all user inputs
9. **Implement proper session management**
10. **Add profile photo moderation**

## Deployment

### For Production Deployment:

1. **Use a production WSGI server** (Gunicorn or uWSGI)
2. **Set up a reverse proxy** (Nginx or Apache)
3. **Use a production database** (PostgreSQL or MySQL)
4. **Configure proper logging**
5. **Set up automated backups**
6. **Use a CDN** for static files
7. **Implement monitoring** and error tracking

### Example Deployment with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Troubleshooting

### Database Issues
```bash
# Reset database
rm elroiconnect.db
python app.py  # This will recreate it
```

### Upload Issues
Ensure the upload folder exists and has proper permissions:
```bash
chmod 755 static/uploads
```

### Video Not Playing
- Ensure videos are in MP4 format
- Check video codec compatibility (H.264 recommended)
- Verify file paths in templates

## Future Enhancements

Consider adding:
- [ ] Video chat functionality
- [ ] Event creation and management
- [ ] Community forums
- [ ] Prayer request features
- [ ] Bible study groups
- [ ] Mobile app (React Native or Flutter)
- [ ] Push notifications
- [ ] Advanced search filters
- [ ] Profile verification badges
- [ ] Subscription/premium features

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review Flask documentation: https://flask.palletsprojects.com/
3. Check SQLAlchemy docs: https://docs.sqlalchemy.org/

## License

This project is created for personal use. Ensure you comply with all applicable laws and regulations when deploying a dating platform.

---

**Built with ❤️ for meaningful connections**# elroiconnect
