from app import app, db, User
from werkzeug.security import generate_password_hash
from datetime import date

with app.app_context():
    users_to_create = [
        {'email': 'emily@test.com', 'first_name': 'Emily', 'last_name': 'Davis', 'gender': 'Female', 'dob': date(1993, 7, 15)},
        {'email': 'jessica@test.com', 'first_name': 'Jessica', 'last_name': 'Wilson', 'gender': 'Female', 'dob': date(1996, 11, 8)},
        {'email': 'michael@test.com', 'first_name': 'Michael', 'last_name': 'Brown', 'gender': 'Male', 'dob': date(1991, 4, 22)},
        {'email': 'david@test.com', 'first_name': 'David', 'last_name': 'Miller', 'gender': 'Male', 'dob': date(1994, 9, 30)},
    ]
    
    for user_data in users_to_create:
        user = User(
            email=user_data['email'],
            password_hash=generate_password_hash('password123'),
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            gender=user_data['gender'],
            date_of_birth=user_data['dob'],
            videos_watched=2
        )
        db.session.add(user)
        print(f"Created: {user.first_name} {user.last_name} ({user.gender})")
    
    db.session.commit()
    print("\nAll users created successfully!")
