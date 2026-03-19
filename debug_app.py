# debug_app.py - Debug the Flask application routes
from app import create_app

app = create_app()

print("=== Flask App Debug Info ===")
print(f"App name: {app.name}")
print(f"App instance path: {app.instance_path}")
print(f"App root path: {app.root_path}")

print("\n=== Registered Routes ===")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")

print("\n=== App Config ===")
for key, value in app.config.items():
    if not key.startswith('_'):
        print(f"{key}: {value}")

if __name__ == "__main__":
    print("\n=== Starting Flask App ===")
    app.run(debug=True, host='127.0.0.1', port=5000) 