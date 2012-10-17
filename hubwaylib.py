"""
Title: hubway lib
Author: nathan lachenmyer
Description: A python library to manipulate hubway data stored on a server.
Usage:
Date Started: 2012 Oct
Last Modified: 2012 Oct
"""
import MySQLdb as mdb
import sys
import urllib
import json
import time
import urlparse
import re

#store username/password in a .txt file (one line, user/pass seperated by a space)
passfile = open('/home/scottnla/hubwaypass','r')
contents = passfile.read()
username = contents.split()[0]
password = contents.split()[1]


def MySQLcommand(command,host='salmon-dance.cruftlabs.com',user=username,pw=password,database='hubway',port_no=3306):
    conn = None

    try:
        conn = mdb.connect(host,user,pw,database,port=port_no)
        cur = conn.cursor()
        cur.execute(command)
    
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()

def MySQLquery(command,host='salmon-dance.cruftlabs.com',user=username,pw=password,database='hubway',port_no=3306):
    conn = None

    try:
        conn = mdb.connect(host,user,pw,database,port=port_no)
        cur = conn.cursor()
        cur.execute(command)
        rows = cur.fetchall()
#        for row in rows:
#            print row
    
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        if conn:
            conn.commit()
            conn.close()

    return rows

def getCols():
	colNames = MySQLquery("SHOW COLUMNS FROM trips;")
	for row in colNames:
		print row
