#!/usr/bin/env python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

def activar_alta_demanda():
    settings.ALTA_DEMANDA_ACTIVADA = True
    print("Las horas de alta demanda han sido activadas.")

def desactivar_alta_demanda():
    settings.ALTA_DEMANDA_ACTIVADA = False
    print("Las horas de alta demanda han sido desactivadas.")

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        if 'activar_alta_demanda' in sys.argv:
            activar_alta_demanda()
        elif 'desactivar_alta_demanda' in sys.argv:
            desactivar_alta_demanda()
        else:
            raise e

if __name__ == '__main__':
    main()
