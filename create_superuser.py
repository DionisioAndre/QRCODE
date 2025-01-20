import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PROJECT.settings')
django.setup()

def create_superuser():
    """Cria o superusuário se ele não existir"""
    username = 'dionisio'
    email = 'dionisio@gmail.com'
    password = '12345'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created.")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == "__main__":
    create_superuser()
