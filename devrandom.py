#!/usr/bin/env python

import binascii
import json
import os
import requests
import signal
import sys
import time

#Entropy source https://qrng.anu.edu.au
#API https://qrng.anu.edu.au/API/jsonI.php?length=[array length]&type=[data type]&size=[block size]
#example output
#https://qrng.anu.edu.au/API/jsonI.php?&length=3&type=hex16&size=1
#{"type":"string","length":3,"size":1,"data":["11","03","a8"],"success":true}

ENTROPY_URL = 'https://qrng.anu.edu.au/API/jsonI.php?'

def getEntropy(data_length=16, data_type='hex16', block_size='1'):
    entropy_source = ENTROPY_URL + ''.join((
        '&length=' + str(data_length),
        '&type=' + str(data_type),
        '&size=' + str(block_size)))

    try:
        entropy_data = requests.get(entropy_source).json()['data']
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    return entropy_data

def main():
    #set stdout to binary mode depending on platform
    if sys.platform == 'win32':
        import msvcrt
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    else:
        sys.stdout = os.fdopen(1, "wb")

    #Avoid traceback on ctrl-c
    signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

    #Create entropy list with initial entropy pool
    entropy_buffer = getEntropy()

    while True:
        if len(entropy_buffer) == 0:
            #print("Refill entropy buffer")
            entropy_buffer = getEntropy()

        #Convert hex from entropy buffer to binary
        binary_string = binascii.unhexlify(entropy_buffer.pop())

        #Print random binary
        sys.stdout.write(binary_string)
        sys.stdout.flush()

if __name__ == '__main__':
    main()
