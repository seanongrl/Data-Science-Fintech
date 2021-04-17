from sys import argv

script, inputfile = argv


def printall(f):
    print(f.read())


def rewind(f):
    f.seek(0)


def printaline(linecount, f):
    print(linecount, f.readline())


currentfile = open(inputfile)

printall(currentfile)
rewind(currentfile)
currentline = 1
printaline(currentline, currentfile)
currentline = currentline + 1
printaline(currentline, currentfile)
currentline = currentline + 1
printaline(currentline, currentfile)
