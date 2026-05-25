#!/usr/bin/env python
"""Django command-line utility."""
import os, sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forensic_db.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()