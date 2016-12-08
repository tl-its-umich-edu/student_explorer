#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "student_explorer.local.settings_override")

    from django.core.management import execute_from_command_line

    if len(sys.argv) == 2 and sys.argv[1] == "runserver":
        sys.argv.append('0.0.0.0:8000')

    execute_from_command_line(sys.argv)
