import pandas as pd
import numpy as np
import datetime
from string_grouper import match_strings, match_most_similar, \
	group_similar_strings, compute_pairwise_similarities, \
	StringGrouper
from timeit import default_timer as timer

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)

import pandas as pd

sec_edgar_names = './tutorials/sec_edgar_company_info.csv'
sec_edgar_names = pd.read_csv(sec_edgar_names)#[0:50000]
print("companies with rows", len(sec_edgar_names))
import re
import unicodedata
def remove_stop_words(company_name: str):
#	p = re.compile('|'.join(map(re.escape, to_remove)))  # escape to handle metachars
#	return p.sub('', company_name.lower())
	company_name = company_name.encode('unicode-escape').decode('utf-8')
	#company_name = company_name.lower()
	company_name = unicodedata.normalize('NFKD', company_name).encode('ASCII', 'ignore').decode()
	company_name = re.sub(r'[^\w\s]', '', company_name)
	return company_name.lower()
#ln_sanction = './LN_Organization/new-clean-data.csv'
#ln_sanction = './tutorials/ln-sanction-list.csv'
#ln_sanction = './Individual_new2/Individual_new2.csv'
#ln_sanction = pd.read_csv(ln_sanction)
import csv
ln_file = "C://git//string_grouper//Organization_new//Organization_new.csv"
f = open(ln_file)
csv_f = csv.reader(f)
data = []
for row in csv_f:
    data.append(row)
f.close()
ln_sanction = pd.read_csv(ln_file, sep=',', encoding = "ISO-8859-1", engine='python')
print("ln_sanction with rows", len(ln_sanction))
ln_sanction['NAME'] = ln_sanction['NAME'].map(lambda x: str(remove_stop_words(x)))
ln_sanction.drop_duplicates("NAME", keep='first', inplace=True)
print("ln_sanction drop dulplicate with rows", len(ln_sanction))
ln_sanction.to_csv('./Organization_new/Organization_new-dup-name.csv', index=False)

'''
double_matches = match_strings(master= ln_sanction['Name'],
							   duplicates= sec_edgar_names['Company Name'],
							   master_id = ln_sanction['Ent_ID'],
							   duplicates_id =sec_edgar_names['Company CIK Key'],
							   ignore_index=True,
								#n_blocks = (1, 200)
							   min_similarity = 0.8)
'''