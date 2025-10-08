from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-for-local')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elroiconnect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    bio = db.Column(db.Text)
    profile_photo = db.Column(db.String(200))
    location = db.Column(db.String(100))
    denomination = db.Column(db.String(100))
    interests = db.Column(db.Text)
    looking_for = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    videos_watched = db.Column(db.Integer, default=0)
    
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    liked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/intro-videos')
def intro_videos():
    return render_template('intro_videos.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if user watched required videos
        videos_watched = int(request.form.get('videos_watched', 0))
        if videos_watched < 2:
            flash('You must watch at least 2 introduction videos before registering.', 'danger')
            return redirect(url_for('intro_videos'))
        
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=dob,
            videos_watched=videos_watched
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.first_name
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Get suggested matches (opposite gender, active users)
    if user.gender == 'Male':
        matches = User.query.filter_by(gender='Female', is_active=True).filter(User.id != user.id).limit(10).all()
    else:
        matches = User.query.filter_by(gender='Male', is_active=True).filter(User.id != user.id).limit(10).all()
    
    return render_template('dashboard.html', user=user, matches=matches)

@app.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    current_user = User.query.get(session['user_id'])
    
    # Check if already liked
    already_liked = Like.query.filter_by(user_id=current_user.id, liked_user_id=user_id).first()
    
    return render_template('profile.html', user=user, already_liked=already_liked)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        user.bio = request.form['bio']
        user.location = request.form['location']
        user.denomination = request.form['denomination']
        user.interests = request.form['interests']
        user.looking_for = request.form['looking_for']
        
        # Handle photo upload
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and file.filename:
                filename = secure_filename(f"user_{user.id}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_photo = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view_profile', user_id=user.id))
    
    return render_template('edit_profile.html', user=user)

@app.route('/like/<int:user_id>', methods=['POST'])
@login_required
def like_user(user_id):
    current_user_id = session['user_id']
    
    # Check if already liked
    existing_like = Like.query.filter_by(user_id=current_user_id, liked_user_id=user_id).first()
    if existing_like:
        return jsonify({'success': False, 'message': 'Already liked'})
    
    # Create like
    like = Like(user_id=current_user_id, liked_user_id=user_id)
    db.session.add(like)
    
    # Check for mutual like
    mutual_like = Like.query.filter_by(user_id=user_id, liked_user_id=current_user_id).first()
    if mutual_like:
        # Create match
        match = Match(user1_id=current_user_id, user2_id=user_id, status='accepted')
        db.session.add(match)
        db.session.commit()
        return jsonify({'success': True, 'match': True, 'message': "It's a match!"})
    
    db.session.commit()
    return jsonify({'success': True, 'match': False, 'message': 'Like sent!'})

@app.route('/messages')
@login_required
def messages():
    user = User.query.get(session['user_id'])
    
    # Get all conversations
    sent = db.session.query(Message.receiver_id).filter_by(sender_id=user.id).distinct()
    received = db.session.query(Message.sender_id).filter_by(receiver_id=user.id).distinct()
    
    conversation_ids = set([r[0] for r in sent] + [r[0] for r in received])
    conversations = User.query.filter(User.id.in_(conversation_ids)).all()
    
    return render_template('messages.html', conversations=conversations)

@app.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    current_user_id = session['user_id']
    other_user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        content = request.form['message']
        message = Message(sender_id=current_user_id, receiver_id=user_id, content=content)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('conversation', user_id=user_id))
    
    # Get all messages between users
    messages = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.timestamp.asc()).all()
    
    # Mark messages as read
    Message.query.filter_by(sender_id=user_id, receiver_id=current_user_id, is_read=False).update({'is_read': True})
    db.session.commit()
    
    return render_template('conversation.html', other_user=other_user, messages=messages)

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    gender = request.args.get('gender', '')
    location = request.args.get('location', '')
    
    users = User.query.filter(User.id != session['user_id'], User.is_active == True)
    
    if query:
        users = users.filter(
            (User.first_name.ilike(f'%{query}%')) |
            (User.last_name.ilike(f'%{query}%'))
        )
    
    if gender:
        users = users.filter_by(gender=gender)
    
    if location:
        users = users.filter(User.location.ilike(f'%{location}%'))
    
    users = users.all()
    
    return render_template('search.html', users=users, query=query)

# Initialize database
with app.app_context():
    db.create_all()
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)