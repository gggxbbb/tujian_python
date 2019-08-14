from sys import stdout
import platform
import ctypes

def ifWindows():
    if(platform.system()=='Windows'):
        return True
    else:
        return False

def error(message):
    if ifWindows():
        print(message)
    else:
        print('\033[31m%s\033[0m' % message)

def success(message):
    if ifWindows():
        print(message)
    else:
        print('\033[32m%s\033[0m' % message)

def waring(message):
    if ifWindows():
        print(message)
    else:
        print('\033[33m%s\033[0m' % message)

class print2:
    @staticmethod
    def message(message):
        stdout.write(message)
        stdout.flush()
    @staticmethod
    def success(message):
        if ifWindows():
            stdout.write(message)
        else:
            stdout.write('\033[32m%s\033[0m' % message)
        stdout.flush()
    @staticmethod
    def error(message):
        if ifWindows():
            stdout.write(message)
        else:
            stdout.write('\033[31m%s\033[0m' % message)
        stdout.flush()
    @staticmethod
    def waring(message):
        if ifWindows():
            stdout.write(message)
        else:
            stdout.write('\033[33m%s\033[0m' % message)
        stdout.flush()
