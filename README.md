# python_pharma_data_report

Looks for new csv files in a dropbox folder, does some formatting and processing on these files,
then places the formatted output in another dropbox folder for pickup by the recipient.  In this manner, 
dropbox acts like an abstraction layer or service, allowing me to process files provided by a 
remote user.

This script is run as a cron job.

