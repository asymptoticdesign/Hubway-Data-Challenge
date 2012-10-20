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
import hubwaylib as hubway

def flattenToList(input):
	output = list(reduce(lambda p,q: p + q, input))
	return output

def dateQuery(dateField,subField="month",filename="output"):
	queryString = "SELECT %s(%s), COUNT(*) AS frequency FROM trips GROUP BY %s(%s) ORDER BY %s;" %(subField.upper(), dateField, subField.upper(), dateField, dateField)
	freq = hubway.MySQLquery(queryString)
	#write to file here
	return freq[1:]

def modal_stats(fieldName,filename="output"):
	freqQuery = "SELECT %s, COUNT(%s) AS frequency FROM trips GROUP BY %s ORDER BY %s;" %(fieldName,fieldName,fieldName,fieldName)
	freqs = hubway.MySQLquery(freqQuery)
#	print "Mode:",freqs[0]
	print "Unique Items:",len(freqs)
	#write to file here
	return freqs[1:]
	

def plotData(frequencies,cutoff=-1,abscissa='Absicca [units]',ordinate='No. [counts]',title='Hubway DataViz'):
	bins = []
	counts = []
	for pair in frequencies:
		bins.append(pair[0])
		counts.append(pair[1])
	pylab.bar(bins[:cutoff],counts[:cutoff])
	pylab.xlabel(abscissa,{'fontsize':20})
	pylab.ylabel(ordinate,{'fontsize':20})
	pylab.title(title,{'fontsize':20})
	pylab.show()
