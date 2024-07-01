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
'''wcfile = "C://git//string_grouper//tutorials//Entities.txt"
f = open(wcfile, encoding='utf-8')
csv_f = csv.reader(f)
data = []
for row in csv_f:
    data.append(row)
f.close()
wc_sanction = pd.read_csv(wcfile, sep='|', encoding = "ISO-8859-1", engine='python')
'''
ln_file= './tutorials/ln-sanction-list.csv'
ln_sanction = pd.read_csv(ln_file, encoding='utf-8')
#print(*wc_sanction)
print("ln_sanction with rows", len(ln_sanction))
print(ln_sanction.shape)

company_names = './tutorials/sec_edgar_company_info.csv'
companies = pd.read_csv(company_names)#[0:50000]
print("companies with rows", len(companies))
start = timer()
print("start", datetime.datetime.now())
double_matches = match_strings(master= ln_sanction['Name'],
							   duplicates= companies['Company Name'],
							   master_id = ln_sanction['Ent_ID'],
							   duplicates_id =companies['Company CIK Key'],
							   ignore_index=True, min_similarity = 0.6)
print("end: ", datetime.datetime.now())
end = timer()
time_use_s = end - start
#print(double_matches)
double_matches.to_csv('LN_double_matches_full.csv')
print("Total time usage for searching: {}s ({}rows search result)".format(int(time_use_s + 0.5), int(len(double_matches))))
