source venv/bin/activate
gunicorn -b :8000 routes:app
source deactivate