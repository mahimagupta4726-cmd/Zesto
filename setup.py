"""
One-time setup for Zesto E-Commerce.
Run:  python setup.py
"""
import os, subprocess, sys

def run(cmd):
    print(f"\n  ▶ {cmd}")
    r = subprocess.run(cmd, shell=True)
    if r.returncode != 0:
        print(f"\n  ✗ Failed: {cmd}")
        sys.exit(1)

print("\n" + "="*55)
print("  ZESTO — E-Commerce Store  |  CodeAlpha Task 1")
print("="*55)

# Install deps (venv recommended; fallback for system Python)
ret = subprocess.run("pip install -r requirements.txt", shell=True)
if ret.returncode != 0:
    run("pip install -r requirements.txt --break-system-packages")

run("python manage.py makemigrations store")
run("python manage.py migrate")
run("python manage.py loaddata store/fixtures/sample_data.json")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zesto.settings')
import django; django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@zesto.com', 'admin123')
    print("\n  ✓ Admin created  →  admin / admin123")
else:
    print("\n  ℹ  Admin already exists.")

print("\n" + "="*55)
print("  ✅  Done! Run:  python manage.py runserver")
print("  Store:  http://127.0.0.1:8000/")
print("  Admin:  http://127.0.0.1:8000/admin/   admin / admin123")
print("="*55 + "\n")
