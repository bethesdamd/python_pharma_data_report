# As I recall, the purpose of this was to take a standard large dump of pharma data from Prospector,
# which often contains data for multiple dates, and a ton of columns,
# and retain just data for today, and just the columns specified in the 'cols' variable below.
# It then writes out a new report with just that data.
# So it makes it easier for him to extract a report of today's price moves, and this report can be sent in an email
# to prospects.
# The way this is run is it looks in a Dropbox folder and if it sees a new file (that doesn't have a .DONE extenstion),
# it processes that file(s) and puts the output in an output Dropbox folder, and then renames the original with .DONE.
# It runs on cron on my Mac.
# crontab looks like this:
#     */1 * * * * /Users/david/anaconda/bin/python  /Users/david/github_pharma_reports/drug_updates_format.py
# Incoming file format, example:
# CompanyName,ProductNameLong,PackageIdentifier,Description,OnMarketDate,BrandGenericStatus,PackageSize,MarketClasses,SpecificDrugProductName,SpecificDrugProductID,OffMarketDate,WACBeginDate,WACPrice,WACPriceChange,WACUnitPrice,DPBeginDate,DPPrice,DPPriceChange,DPUnitPrice
# "Accord Healthcare, Inc.",Montelukast Sodium 10mg Tablet,16729-0119-17,"bottle, 1,000 each Montelukast Sod 10mg, Oral tablet",9/11/2014 0:00,Generic,1000,"Antileukotriene Anti-asthmatics, Systemic (Oral)",Montelukast Sodium 10mg Oral tablet,7927,,11/6/2015,390,(-) 51.25,0.39,,,,
# "Accord Healthcare, Inc.",Topotecan Hydrochloride 4mg Powder for Injection,16729-0151-31,"vial, 1 each Topotecan HCl 4mg, Powder for solution for injection",7/23/2013 0:00,Generic,1,Camptothecin Analogs (Intravenous),Topotecan Hydrochloride 4mg Powder for solution for injection,9410,,11/6/2015,140,(-) 38.86,140,,,,


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




