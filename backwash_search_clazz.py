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
wc_sanction = pd.read_csv(wcfile, sep='\t', encoding = "ISO-8859-1", engine='python')
#print(*wc_sanction)
print("wc_sanction with rows", len(wc_sanction))
wc_sanction.FIRST_NAME = wc_sanction.FIRST_NAME.fillna('')
wc_sanction['WHOLE_NAME'] = wc_sanction['FIRST_NAME']+' '+wc_sanction['LAST_NAME']
wc_sanction = wc_sanction.drop('FURTHER_INFORMATION', 1)
wc_sanction = wc_sanction.drop('LOCATIONS', 1)
wc_sanction = wc_sanction.drop('PLACE_OF_BIRTH', 1)
wc_sanction = wc_sanction.drop('LOW_QUALITY_ALIASES', 1)
wc_sanction = wc_sanction.drop('PEP_ROLES', 1)
wc_sanction = wc_sanction.drop('TITLE', 1)
wc_sanction = wc_sanction.drop('POSITION', 1)
wc_sanction = wc_sanction.drop('COUNTRIES', 1)
wc_sanction = wc_sanction.drop('CITIZENSHIP', 1)
wc_sanction = wc_sanction.drop('AGE', 1)
wc_sanction = wc_sanction.drop('DOB', 1)
wc_sanction = wc_sanction.drop('DOBS', 1)
wc_sanction = wc_sanction.drop('EXTERNAL_SOURCES', 1)


company_names = './tutorials/sec_edgar_company_info.csv'
companies = pd.read_csv(company_names)#[0:50000]
print("companies with rows", len(companies))
start = timer()
print(datetime.datetime.now())
'''double_matches = match_strings(master= wc_sanction['WHOLE_NAME'],
							   duplicates= companies['Company Name'],
							   master_id = wc_sanction['UID'],
							   duplicates_id =companies['Company CIK Key'],
							   ignore_index=True, min_similarity = 0.6)
							   '''
string_grouper = StringGrouper(master= wc_sanction['WHOLE_NAME'],
							   duplicates= companies['Company Name'],
							   master_id = wc_sanction['UID'],
							   duplicates_id =companies['Company CIK Key'],
							   ignore_index=True, min_similarity = 0.6)
string_grouper.fit()
wc_sanction['deduplicated_name'] = string_grouper.get_groups()
print(datetime.datetime.now())
end = timer()
time_use_s = end - start
#print(double_matches)
wc_sanction.to_csv('double_matches_full_60_clazz.csv')
print("Total time usage for searching: {}s ({} rows search result)".format(int(time_use_s + 0.5), int(len(double_matches))))