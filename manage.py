#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

    from django.core.management import execute_from_command_line

    try:
        if sys.argv[1] == "runserver" and len(sys.argv) == 2:
            sys.argv.append('0.0.0.0:8000')
    except:
        pass

    execute_from_command_line(sys.argv)
