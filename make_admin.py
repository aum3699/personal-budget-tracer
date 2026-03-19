# make_admin.py - Script to make the first user an admin
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Get the first user (usually the one who registered first)
    first_user = User.query.first()
    
    if first_user:
        first_user.is_admin = True
        db.session.commit()
        print(f"✅ {first_user.username} is now an admin!")
        print(f"   Email: {first_user.email}")
        print(f"   User ID: {first_user.id}")
    else:
        print("❌ No users found in the database.")
        print("   Please register a user first, then run this script again.") 