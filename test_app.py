# test_app.py - Debug the Flask application
from app import create_app, db
from app.models import Transaction, User

app = create_app()

print("App created successfully!")
print(f"App name: {app.name}")
print(f"App config: {app.config}")

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created!")

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, host='127.0.0.1', port=5000) 