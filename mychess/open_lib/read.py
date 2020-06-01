import sys

fileName = 'BOOK.DAT'

f = open(fileName, 'rb')
line = f.readlines()
for i in line:
    print(i)

print(len(line))