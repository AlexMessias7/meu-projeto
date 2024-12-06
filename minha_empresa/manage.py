#caminho para ativar o ambiente virtual e o codigo para ativar o site
#cd "C:\Users\gabri\OneDrive\photoshop\Estudo\Python\MEU SITE 2\minha_empresa"
#.\venv\Scripts\activate
#cd "C:\Users\gabri\OneDrive\photoshop\Estudo\Python\MEU SITE 2"
#python manage.py runserver



#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minha_empresa.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
