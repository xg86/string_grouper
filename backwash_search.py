import pandas as pd
import numpy as np
import datetime
from string_grouper import match_strings, match_most_similar, \
	group_similar_strings, compute_pairwise_similarities, \
	StringGrouper
from timeit import default_timer as timer

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)

import csv
import pandas as pd
wcfile = "C://git//New XLSX Worksheet1.txt"
f = open(wcfile)
csv_f = csv.reader(f)
data = []
for row in csv_f:
    data.append(row)
f.close()
wc_sanction = pd.read_csv(wcfile, sep='\t', encoding = "ISO-8859-1", engine='python')[0:1]
#print(*wc_sanction)
print("wc_sanction with rows", len(wc_sanction))
wc_sanction.FIRST_NAME = wc_sanction.FIRST_NAME.fillna('')
wc_sanction['WHOLE_NAME'] = wc_sanction['FIRST_NAME']+' '+wc_sanction['LAST_NAME']

company_names = './tutorials/sec_edgar_company_info.csv'
companies = pd.read_csv(company_names)[0:100000]
print("companies with rows", len(companies))
start = timer()
print("start", datetime.datetime.now())
#duplicates = pd.Series(['012 SMILE.COMMUNICATIONS'])
#for index, row in companies.iterrows():
#	master = pd.Series([row['Company Name']])

double_matches = match_strings( companies['Company Name'], #right
								wc_sanction['WHOLE_NAME'], #left
							   master_id = companies['Company CIK Key'],
							   duplicates_id = wc_sanction['UID'],
							   #n_blocks=(1, 50),
							   ignore_index=True,
							min_similarity = 0.8)



'''

#49s
double_matches = match_strings(wc_sanction['WHOLE_NAME'], #right
							   companies['Company Name'], #left
							   master_id = wc_sanction['UID'],
							   duplicates_id = companies['Company CIK Key'],
							   ignore_index=True,
							   min_similarity = 0.8
							   #n_blocks = 'auto'
							   )
  #38 sec
count = 0
while count < 5000000:
    #print("count: ", count)
    count = count + 1


#1 row 34
'''
print("end: ", datetime.datetime.now())
end = timer()
time_use_s = end - start
print("start: ", start)
print("end: ", end)
print("time_use_s: ", time_use_s)
#print(double_matches)
#double_matches.to_csv('double_matches_full_60_2.csv')
print("Total time usage for searching: {}s ({}rows search result)".format(int(time_use_s + 0.5), int(len(double_matches))))
#print("Total time usage for searching: {}s ({}rows search result)".format(int(time_use_s + 0.5), 0))
