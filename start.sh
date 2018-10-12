source venv/bin/activate
gunicorn routes:app
source deactivate