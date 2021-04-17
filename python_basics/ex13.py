from sys import argv

script, filename = argv

print("we're gonna erase %r" % filename)
print("if you don't want that hit ctrl c")
print("if u do want that hit return")

input("?")

print("opening the file...")
target = open(filename, 'w')

print("truncating the file")
target.truncate()

print("pls input 3 lines")

line1 = input("line1: ")
line2 = input("line2: ")
line3 = input("line3: ")

print("ill write these to the file")

target.write(line1)
target.write("\n")
target.write(line2)
target.write("\n")
target.write(line3)
target.write("\n")

target.close()
