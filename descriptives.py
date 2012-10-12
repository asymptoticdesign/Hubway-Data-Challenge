"""
Title: Descriptives
Description: Computes descriptive statistics from a .csv dataset
Usage:
Date Started: 2012 Oct
Last Modified:
http://asymptoticdesign.wordpress.com/
This work is licensed under a Creative Commons 3.0 License.
(Attribution - NonCommerical - ShareAlike)
http:#creativecommons.org/licenses/by-nc-sa/3.0/

In summary, you are free to copy, distribute, edit, and remix the work.
Under the conditions that you attribute the work to the author, it is for
noncommercial purposes, and if you build upon this work or otherwise alter
it, you may only distribute the resulting work under this license.

Of course, these permissions may be waived with permission from the author.

Description of Usage:
scottnla@faraday-cage:~/$ python readSerial.py [filename]
Reads serial information from an arduino circuit, writes it to file.
"""

import sys
import csv
import scipy
import hubwaylib as mysql

#min/max/range
#median
#mean/std
#frequencies
def aggregate_statistics(fieldName):
	minString = "SELECT MIN(" + fieldName + ") FROM trips"
	min = mysql.MySQLquery(minString)
	maxString = "SELECT MAX(" + fieldName + ") FROM trips"
	max = mysql.MySQLquery(maxString)
	avgString = "SELECT AVG(" + fieldName + ") FROM trips"
	avg = mysql.MySQLquery(avgString)
	stdString = "SELECT STD(" + fieldName + ") FROM trips"
	std = mysql.MySQLquery(stdString)
	return min,max,avg,std

#ideas:
#track individual bikes through city
#distance to T stations
#distance to nearest item
