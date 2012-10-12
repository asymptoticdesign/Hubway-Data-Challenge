"""
Title: Descriptives
Description: Computes descriptive statistics from a .csv dataset
Usage:
Date Started: 2012 Oct
Last Modified: 2012 Oct
http://www.asymptoticdesign.org/

Description of Usage:
scottnla@faraday-cage:~/$ python readSerial.py [filename]
Reads serial information from an arduino circuit, writes it to file.
"""

import sys
import csv
import scipy
import hubwaylib as hubway

#min/max/range
#median
#mean/std
#frequencies
def flattenToList(input):
	output = list(reduce(lambda p,q: p + q, input))
	return output

def agg_stats(fieldName):
	minQuery = "SELECT MIN(" + fieldName + ") FROM trips"
	min = hubway.MySQLquery(minQuery)[0][0]
	print "Duration Mininum:",min
	maxQuery = "SELECT MAX(" + fieldName + ") FROM trips"
	max = hubway.MySQLquery(maxQuery)[0][0]
	print "Duration Maximum:",max
	print "Duration Range:",max-min
	avgQuery = "SELECT AVG(" + fieldName + ") FROM trips"
	avg = hubway.MySQLquery(avgQuery)[0][0]
	print "Duration Mean:",avg
	stdQuery = "SELECT STDDEV_SAMP(" + fieldName + ") FROM trips"
	std = hubway.MySQLquery(stdQuery)[0][0]
	print "Duration Std:",std

	return [min,max,avg,std]

def modal_stats(fieldName):
	freqQuery = "SELECT " + fieldName + ", COUNT(" + fieldName + ") AS frequency FROM trips GROUP BY " + fieldName + " ORDER BY frequency DESC;"
	freqs = hubway.MySQLquery(freqQuery)
	print "Mode:",freqs[0]
	return freqs
	
def median(fieldName):
	count = hubway.MySQLquery("SELECT COUNT(" + fieldName + ") FROM trips;")[0][0]
	if count %2 == 0:
		medQuery = "SELECT " + fieldName + " FROM trips ORDER BY " + fieldName + " LIMIT " + str(count/2) + ",1;"
		median = hubway.MySQLquery(medQuery)
	else:
		medQuery = "SELECT " + fieldName + " FROM trips ORDER BY " + fieldName + " LIMIT " + str(int(scipy.floor(count/2))) + ",2;"
		median = hubway.MySQLquery(medQuery)
		return median



#ideas:
#track individual bikes through city
#distance to T stations
#distance to nearest item
