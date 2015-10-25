#! /usr/bin/env python

from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import uuid
import getpass

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('-out', '--out-file', type=str, help='output file', dest='out')
    parser.add_argument('-d', '--decrypt', action='store_true')
    parser.add_argument('-k', '--key', metavar='key')
    args = parser.parse_args() 

    key = args.key if args.key else uuid.uuid4().hex
    #if len(key) not in (16, 32):
    #    if len(key) < 16:
    #        key = 'key%s' % ('.'*(16-len(key)),)
    #    else:
    #        key = key[:16]
    in_filename = args.input
    out_filename = args.out or in_filename + '.out'

    print '%s %s --> %s' % ('Decrypt' if args.decrypt else 'Encrypt', in_filename, out_filename)
    if args.key is None:
        #print 'key: ' + key
        key = getpass.getpass()

    password = key

    if args.decrypt:
        with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
            decrypt(in_file, out_file, password)
    else:
        with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
            encrypt(in_file, out_file, password)

