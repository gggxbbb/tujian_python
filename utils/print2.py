from sys import stdout

def error(message):
    print('\033[31m%s\033[0m' % message)

def success(message):
    print('\033[32m%s\033[0m' % message)

def waring(message):
    print('\033[33m%s\033[0m' % message)

class print2:
    @staticmethod
    def message(message):
        stdout.write(message)
        stdout.flush()
    @staticmethod
    def success(message):
        stdout.write('\033[32m%s\033[0m' % message)
        stdout.flush()
    @staticmethod
    def error(message):
        stdout.write('\033[31m%s\033[0m' % message)
        stdout.flush()
    @staticmethod
    def waring(message):
        stdout.write('\033[33m%s\033[0m' % message)
        stdout.flush()
