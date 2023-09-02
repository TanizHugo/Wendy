import sys


def isRunServer():
    if len(sys.argv) >= 2:
        re = True
        if sys.argv[1] == 'makemigrations':
            re = False
        elif sys.argv[1] == 'migrate':
            re = False
        return re
    return True

