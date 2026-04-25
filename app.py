import os
from app import create_app, db

  # Create app with the correct config
app = create_app(os.environ.get('FLASK_ENV', 'development'))

  # Create tables
with app.app_context():
    db.create_all()
    print('Tables created!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)