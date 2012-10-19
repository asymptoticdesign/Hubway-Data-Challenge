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
import pylab
import csv
import hubwaylib as hubway

def flattenToList(input):
	output = list(reduce(lambda p,q: p+q, input))
	return output

def writeToFile(list,filename):
	outputfile = open(filename+'.csv','w')
	for pair in list:
		outputfile.write(str(float(pair[0])) + "," + str(float(pair[1])) + "\n")
	outputfile.close()

def agg_stats(fieldName):
	minQuery = "SELECT MIN(" + fieldName + ") FROM trips"
	min = hubway.MySQLquery(minQuery)[0][0]
	print "Field Mininum:",min
	maxQuery = "SELECT MAX(" + fieldName + ") FROM trips"
	max = hubway.MySQLquery(maxQuery)[0][0]
	print "Field Maximum:",max
	avgQuery = "SELECT AVG(" + fieldName + ") FROM trips"
	avg = hubway.MySQLquery(avgQuery)[0][0]
	print "Field Mean:",avg
	stdQuery = "SELECT STDDEV_SAMP(" + fieldName + ") FROM trips"
	std = hubway.MySQLquery(stdQuery)[0][0]
	print "Field Std:",std
	return [min,max,avg,std]

def dateQuery(dateField,subField="month"):
	queryString = "SELECT %s(%s), COUNT(*) AS frequency FROM trips GROUP BY %s(%s) ORDER BY %s;" %(subField.upper(), dateField, subField.upper(), dateField, dateField)
	freq = hubway.MySQLquery(queryString)
	return freq[1:]

def modal_stats(fieldName):
	freqQuery = "SELECT %s, COUNT(%s) AS frequency FROM trips GROUP BY %s ORDER BY %s;" %(fieldName,fieldName,fieldName,fieldName)
	freqs = hubway.MySQLquery(freqQuery)
#	print "Mode:",freqs[0]
	print "Unique Items:",len(freqs)
	return freqs[1:]
	
def median(fieldName):
	count = hubway.MySQLquery("SELECT COUNT(" + fieldName + ") FROM trips;")[0][0]
	if count %2 == 0:
		medQuery = "SELECT " + fieldName + " FROM trips ORDER BY " + fieldName + " LIMIT " + str(count/2) + ",1;"
		median = hubway.MySQLquery(medQuery)
	else:
		medQuery = "SELECT " + fieldName + " FROM trips ORDER BY " + fieldName + " LIMIT " + str(int(scipy.floor(count/2))) + ",2;"
		median = hubway.MySQLquery(medQuery)
		return median

def plotData(frequencies,cutoff=-1,abscissa='Absicca [units]',ordinate='No. [counts]',title='Hubway DataViz'):
	bins = []
	counts = []
	for pair in frequencies:
		bins.append(pair[0])
		counts.append(pair[1])
		print pair[0],pair[1]
	pylab.bar(bins[:cutoff],counts[:cutoff])
	pylab.xlabel(abscissa,{'fontsize':20})
	pylab.ylabel(ordinate,{'fontsize':20})
	pylab.title(title,{'fontsize':20})
	pylab.show()

#ideas:
#track individual bikes through city
#distance to T stations
#distance to nearest item
