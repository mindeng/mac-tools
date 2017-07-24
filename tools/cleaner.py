#!/usr/bin/env python

'''
find . -type f | sed -E 's/.+[\./]([^/\.]+)/\1/' | sort -u
'''
EXTENSIONS = set([ '.'+e for e in 
'''
ARW
AVI
GIF
JPG
MOV
MP4
NEF
PNG
jpg
log
m4v
mov
mp4
png
'''.split()])

import zlib
import sys
import os
import platform
import sqlite3
import hashlib

_db = sqlite3.connect(':memory:')


BUF_SIZE = 65536

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def crc_file(path):
    crcvalue = 0
    with open(path, 'rb') as afile:
        buffr = afile.read(BUF_SIZE)
        while len(buffr) > 0:
            crcvalue = zlib.crc32(buffr, crcvalue)
            buffr = afile.read(BUF_SIZE)

    return crcvalue

def md5_file(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(BUF_SIZE), ""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def iter_media_files(path, cb):
    for root, dirs, files in os.walk(path):
        for name in files:
            p = os.path.join(root, name)
            if os.path.islink(p):
                # Ignore symbolic link
                continue
            elif is_hard_link(p):
                # Ignore hard link
                continue
            
            _, ext = os.path.splitext(name)
            ext = ext.lower()
            if ext in EXTENSIONS:
                size = os.path.getsize(p)
                created = creation_date(p)
                cb(p, size, created, ext)

def is_hard_link(path):
    inum = os.stat(path).st_ino
    _c = _db.cursor()
    _c.execute('select path from files where inum=?', (inum, ))
    return _c.fetchone() is not None

def file_handler(path, size, created, ext):
    crc = None
    md5 = None
    _c = _db.cursor()
    _c.execute('select path, crc32, md5 from files where size=? and extension=?', (size, ext))
    for row in _c.fetchall():
        if row[1]:
            matched_crc = row[1]
        else:
            matched_crc = crc_file(row[0])
            _c.execute('update files set crc32=? where path=?', (matched_crc, row[0]))
        crc = crc_file(path)
        _c.execute('update files set crc32=? where path=?', (crc, path.decode('utf-8')))
        if matched_crc == crc:
            if row[2]:
                matched_md5 = row[2]
            else:
                matched_md5 = md5_file(row[0])
                _c.execute('update files set md5=? where path=?', (matched_md5, row[0]))
            md5 = md5_file(path)
            _c.execute('update files set md5=? where path=?', (md5, path))
            if matched_md5 == md5:
                # repeated file
                print '%s\t%s' % (row[0], path)
                _db.commit()
                return
    
    inum = os.stat(path).st_ino
    _c.execute('insert into files values (?,?,?,?,?,?,?)', 
        (path.decode('utf-8'), inum, size, created, ext, crc, md5))
    # print 'add file %s' % path
    _db.commit()

def main():
    c = _db.cursor()

    # Create table
    c.execute('''CREATE TABLE files
             (path text unique, inum integer unique, size integer, created integer, extension text, crc32 integer, md5 text unique)''')
    sql = ("CREATE INDEX index_size ON files (size);")
    c.execute(sql)
    sql = ("CREATE INDEX index_crc ON files (crc32);")
    c.execute(sql)


    iter_media_files(sys.argv[1], file_handler)

if __name__ == '__main__':
    main()
