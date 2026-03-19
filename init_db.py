# init_db.py - Initialize database with correct schema
from app import create_app, db
from app.models import Transaction, User

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    
    print("Creating all tables...")
    db.create_all()
    
    print("Database initialized successfully!")
    print("You can now run the application with: python run.py") 