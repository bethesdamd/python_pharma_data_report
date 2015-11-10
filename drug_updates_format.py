# look for incoming csv files and extract and format relevant data into files
# Once it's done processing a csv file, it renames it with a '.DONE' extension

import pandas as pd
import numpy as np
import os as os
import io
import datetime
from os.path import isfile, join
import sys

cols = ['CompanyName','SpecificDrugProductName','SpecificDrugProductID', 'OnMarketDate','BrandGenericStatus','PackageSize','MarketClasses','WACBeginDate','WACPrice','WACUnitPrice']
inpath = '/Users/david/Dropbox/send-to-david/'
outpath = '/Users/david/Dropbox/FROM-david/'

today = datetime.date.today()
day_s = str(today.day)
day_s = '0' + day_s if len(day_s) == 1 else day_s 
today_yyyymmdd = str(today.year) + "-" + str(today.month) + "-" + day_s

onlyfiles = [ f for f in os.listdir(inpath) if isfile(join(inpath,f)) ]

csv = [k for k in onlyfiles if k.endswith(".csv")]
print(csv)

if len(csv) == 0:
	print("No files to process")
	sys.exit()

print("The following files were received: \n" + '\n'.join(csv) + "\n")
spacer = "\n-------------\n"

for filename in csv:
	df = pd.read_csv(inpath + filename)
	today = df[df.OnMarketDate.str.contains(today_yyyymmdd)]
	if len(today.index) > 0:
		fout = io.open(outpath + "report-" + today_yyyymmdd + "-from-file-" + filename + ".txt", 'w', newline='\r\n')
		for index, row in today.iterrows():
			print("inside index %s" % index)
			for col in cols:
				text = col + ": " + str(row[col]) 
				print(text)
				fout.write(text + "\n")
			print(spacer)
			fout.write(spacer)
		fout.close()
		os.rename(inpath + filename, inpath + filename + ".DONE")




