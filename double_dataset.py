import pandas as pd
import numpy as np
from string_grouper import match_strings, match_most_similar, \
	group_similar_strings, compute_pairwise_similarities, \
	StringGrouper
from timeit import default_timer as timer
import fuzzy
dmeta = fuzzy.DMetaphone(4)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

#company_names = './tutorials/sec_edgar_company_info.csv'
company_names = './tutorials/accounts.csv'
companies = pd.read_csv(company_names) #[0:50000]
companies['firstname'] = companies['name'].apply(lambda x: x.split(' ')[0])
companies['lastname'] = companies['name'].apply(lambda x: x.split(' ')[-1])
companies['firstname_phone'] = companies['firstname'].apply(lambda x: str(dmeta(x)))
companies['lastname_phone'] = companies['lastname'].apply(lambda x: str(dmeta(x)))
companies['name_phone'] = companies['name'].apply(lambda x: dmeta(x))
#print(companies)

request_names = './tutorials/test_queries.csv'
requests = pd.read_csv(request_names, delimiter=';') #[0:50000]
requests.firstname = requests.firstname.fillna('')
requests.lastname = requests.lastname.fillna('')
requests['whole_name'] = requests['firstname']+" "+ requests['lastname']
requests['firstname_phone'] = requests['firstname'].apply(lambda x: str(dmeta(x)))
requests['lastname_phone'] = requests['lastname'].apply(lambda x: str(dmeta(x)))
#matches = match_strings(companies['Company Name'])
# Look at only the non-exact matches:
#result = matches[matches['left_Company Name'] != matches['right_Company Name']].head()
#print(requests)

#duplicates = pd.Series(['S MEDIA GROUP', '012 SMILE.COMMUNICATIONS', 'foo bar', 'B4UTRADE COM CORP'])
#index=pd.Series([101,102,103,104])
#companies = companies.astype(str).apply(lambda x: x.str.lower())
#requests = requests.astype(str).apply(lambda x: x.str.lower())

start = timer()
#double_matches = match_strings(companies['Company Name'], duplicates)
# Create all matches:

#print("type is", type(requests['whole_name']))
double_matches  = match_strings(companies['name'], requests['whole_name'],
							   master_id = companies['id'] ,
							   duplicates_id = requests['list_reference'] ,
							   ignore_index=True, min_similarity = 0.25)

end = timer()
time_use_s = end - start
print("double_matches###")
print(double_matches)

matches_25_60 = double_matches.loc[double_matches["similarity"] < 0.60]
#matches_25_60 = matches_25_60.loc[double_matches["similarity"] > 0.25]
print("matches_25_60###")
print(matches_25_60)

companies_phone = companies[companies.id.isin(matches_25_60.left_id)]
print("companies_phone###")
print(companies_phone)
requests_phone = requests[requests.list_reference.isin(matches_25_60.right_list_reference)]
print("requests_phone###")
print(requests_phone)

first_phone_matches = match_strings(companies_phone['firstname_phone'], requests_phone['firstname_phone'],
							   master_id = companies_phone['id'] ,
							   duplicates_id = requests_phone['list_reference'] ,
							   ignore_index=True, min_similarity = 0.6)

lastname_phone_matches = match_strings(companies_phone['lastname_phone'], requests_phone['lastname_phone'],
							   master_id = companies_phone['id'] ,
							   duplicates_id = requests_phone['list_reference'] ,
							   ignore_index=True, min_similarity = 0.6)
phone_merged = pd.merge(first_phone_matches, lastname_phone_matches, how="outer", on=["right_list_reference"])
print("phone_merged###")
print(phone_merged)
phone_merged = phone_merged.drop('left_firstname_phone', 1)
phone_merged = phone_merged.drop('right_firstname_phone', 1)
phone_merged = phone_merged.drop('left_lastname_phone', 1)
phone_merged = phone_merged.drop('right_lastname_phone', 1)
phone_merged = phone_merged.drop('left_id_x', 1)
phone_merged = phone_merged.drop('left_id_y', 1)
matches_25_60 = pd.merge(matches_25_60, phone_merged, how="outer", on=["right_list_reference"])
matches_25_60 = matches_25_60.fillna(0)

matches_25_60['boost_similarity'] = matches_25_60.similarity + matches_25_60.similarity_x/10 + matches_25_60.similarity_y/10
print("phone_merged matches_25_60 ###")
print(matches_25_60)

matches_25_60 = matches_25_60.drop('similarity_x', 1)
matches_25_60 = matches_25_60.drop('similarity_y', 1)

matches_25_60_sec_step = matches_25_60.loc[matches_25_60["boost_similarity"] > 0.25]
matches_25_60_sec_step = matches_25_60_sec_step.loc[matches_25_60_sec_step["boost_similarity"] < 0.60]
print("matches_25_60_sec_round")
print(matches_25_60_sec_step)

companies_phone_2nd = companies[companies.id.isin(matches_25_60_sec_step.left_id)]
print("companies_phone_2nd###")
print(companies_phone_2nd)
requests_phone_2nd = requests[requests.list_reference.isin(matches_25_60_sec_step.right_list_reference)]
print("requests_phone_2nd###")
print(requests_phone_2nd)

first_last_phone_matches = match_strings(companies_phone_2nd['firstname_phone'], requests_phone_2nd['lastname_phone'],
							   master_id = companies_phone_2nd['id'] ,
							   duplicates_id = requests_phone_2nd['list_reference'] ,
							   ignore_index=True, min_similarity = 0.6)

last_first_phone_matches = match_strings(companies_phone_2nd['lastname_phone'], requests_phone_2nd['firstname_phone'],
							   master_id = companies_phone_2nd['id'] ,
							   duplicates_id = requests_phone_2nd['list_reference'] ,
							   ignore_index=True, min_similarity = 0.6)
phone_merged_2nd = pd.merge(first_last_phone_matches, last_first_phone_matches, how="outer", on=["right_list_reference"])
print("phone_merged_2nd###")
phone_merged_2nd = phone_merged_2nd.drop('left_firstname_phone', 1)
phone_merged_2nd = phone_merged_2nd.drop('right_firstname_phone', 1)
phone_merged_2nd = phone_merged_2nd.drop('left_lastname_phone', 1)
phone_merged_2nd = phone_merged_2nd.drop('right_lastname_phone', 1)
phone_merged_2nd = phone_merged_2nd.drop('left_id_x', 1)
phone_merged_2nd = phone_merged_2nd.drop('left_id_y', 1)
print("phone_merged_2nd")
print(phone_merged_2nd)
print(phone_merged_2nd.shape)
matches_25_60_sec_step = pd.merge(matches_25_60_sec_step, phone_merged_2nd, how="outer", on=["right_list_reference"])
matches_25_60_sec_step = matches_25_60_sec_step.fillna(0)

matches_25_60_sec_step['boost_similarity'] = matches_25_60_sec_step.similarity + matches_25_60_sec_step.similarity_x/10 + matches_25_60_sec_step.similarity_y/10
print("phone_merged matches_25_60_sec_step ###")
print(matches_25_60_sec_step)
print("Total time usage for searching: {}s ({}ns search result)".format(int(time_use_s + 0.5), int(len(double_matches))))

import re
to_remove = ['company', 'corporation', 'limited']
def remove_stop_words(company_name: str):
	p = re.compile('|'.join(map(re.escape, to_remove)))  # escape to handle metachars
	return p.sub('', company_name.lower())

print(remove_stop_words('DURAND PROPERTIES LIMITED'))
print(remove_stop_words('KOREA MINING DEVELOPMENT TRADING CORPORATION'))
print(remove_stop_words('MAMOUN DARKAZANLI IMPORT-EXPORT COMPANY'))