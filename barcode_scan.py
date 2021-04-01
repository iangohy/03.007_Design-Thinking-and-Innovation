import sys

fp = open('/dev/hidraw0', 'rb')

while True:
    buffer = fp.readline()
    print(buffer)
